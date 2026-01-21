#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
import mne
import os
import re
from pathlib import Path

# ==========================================
# 🟢 CONFIGURATION
# ==========================================
# Path where your 59 segmented epoch files are located
#EPOCH_DIR = Path("/Path/To/Your/Segmented_Epochs_Folder") 
STIMULI = [str(i) for i in range(1, 13)]
DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")
wOnset_DIR_Natives = DATA_ROOT / 'EEG_Natives' / 'Alice_Natives_wOnset_raw_epochs'
wOnset_DIR_ESLs = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESLs_wOnset_raw_epochs'

# Output filename
OUTPUT_FILE = DATA_ROOT / "Alice_all_subjects_raw_epochs.npz"


# Configuration List: (Directory Path, Label ID, Group Name)
# Label 0 = Native
# Label 1 = ESL
DIRS_TO_PROCESS = [
    (wOnset_DIR_Natives, 0, "Native"),
    (wOnset_DIR_ESLs, 1, "ESL")
]

# ==========================================
# ⚙️ PROCESSING
# ==========================================
all_epochs_data = []
all_labels = []
all_file_paths = []

print(f"Starting processing...")

# 1. Collect all valid file paths first
print(f"🔍 Pass 1: Indexing files and determining common channels...")
for folder_path, label, group_name in DIRS_TO_PROCESS:
	if not folder_path.exists():
		print(f"⚠️ Directory not found: {folder_path}")
		continue

	files = [f for f in os.listdir(folder_path) if f.endswith('epochs_allTapes_raw.fif')]
	files.sort()

	for fname in files:
		all_file_paths.append({
	        'path': folder_path / fname,
	    'label': label,
	    'group': group_name,
	    'fname': fname
	})

if not all_file_paths:
	print("❌ No files found in any directory.")
	exit()

# 2. Determine Common Channels (Intersection of all subjects)
# This prevents the ValueError by ensuring everyone has the same dimension
common_channels = None

for item in all_file_paths:
	try:
		# Read info only (fast) to get channel names
		info = mne.io.read_info(item['path'], verbose=False)
		ch_names = set(info['ch_names'])

		if common_channels is None:
			common_channels = ch_names
		else:
			common_channels = common_channels.intersection(ch_names)
	except Exception as e:
		print(f"⚠️ Warning reading info from {item['fname']}: {e}")

if common_channels is None or len(common_channels) == 0:
	print("❌ No common channels found across files. Cannot combine.")
	exit()

# Convert set to sorted list to ensure consistent order
target_channels = sorted(list(common_channels))
print(f"✅ Found {len(target_channels)} common channels across {len(all_file_paths)} files.")
print(f"   Channels to be used: {target_channels}")

# 3. Pass 2: Load Data and Harmonize Channels
print(f"\n🚀 Pass 2: Loading data and matching channels...")

for item in all_file_paths:
	fname = item['fname']
	file_path = item['path']
	label = item['label']

	try:
		# Load Epochs
		epochs = mne.read_epochs(file_path, verbose=False, preload=True)

		# CRITICAL: Pick only the common channels in the specific order
		# This handles the 59 vs 57 channel mismatch
		epochs.pick_channels(target_channels, ordered=True)

		# Extract Data (N_Epochs, N_Channels, N_TimePoints)
		data = epochs.get_data(copy=False)

		# Check integrity
		if data.shape[1] != len(target_channels):
			print(f"⚠️ Skipping {fname}: Channel count mismatch after pick ({data.shape[1]} vs {len(target_channels)})")
			continue

		# Create Labels
		n_epochs = data.shape[0]
		labels = np.full(n_epochs, label, dtype=np.longlong)

		all_epochs_data.append(data)
		all_labels.append(labels)

		print(f"   ✅ Loaded {fname} | Epochs: {n_epochs} | Chans: {data.shape[1]}")

	except Exception as e:
		print(f"   ❌ Error loading {fname}: {e}")

# ==========================================
# 💾 COMBINE & SAVE
# ==========================================
if all_epochs_data:
	# Concatenate all subjects into one massive array
	# Result Shape: (Total_Epochs_All_Subjects, Channels, Time)
	X = np.concatenate(all_epochs_data, axis=0)
	y = np.concatenate(all_labels, axis=0)

	# Ensure float32 for PyTorch
	X = X.astype(np.float32)

	print(f"\n✨ COMPLETED ✨")
	print(f"Total Epochs: {X.shape[0]}")
	print(f"Channels:     {X.shape[1]}")
	print(f"Time Points:  {X.shape[2]}")
	print(f"Labels:       {np.unique(y)} (0=Native, 1=ESL)")

	np.savez_compressed(OUTPUT_FILE, X=X, y=y)
	print(f"Saved to '{OUTPUT_FILE}'")

else:
	print("\n❌ No data loaded. Please check your paths.")
	

""" VERSION TWO
# ==========================================
# ⚙️ PROCESSING
# ==========================================
all_epochs_data = []
all_labels = []

print(f"Starting processing...")

for folder_path, label, group_name in DIRS_TO_PROCESS:
	print(f"\n📂 Scanning {group_name} folder: {folder_path}")

	if not folder_path.exists():
		print(f"⚠️ Directory not found: {folder_path}")
		continue

	# List all files matching the specific pattern provided
	# Pattern example: S010_ESLs_wOnset_epochs_allTapes_raw.fif
	files = [f for f in os.listdir(folder_path) if f.endswith('epochs_allTapes_raw.fif')]
	files.sort()

	if len(files) == 0:
		print(f"⚠️ No 'epochs_allTapes_raw.fif' files found in {group_name} folder.")
		continue

	for fname in files:
		file_path = folder_path / fname

		try:
			# 1. Load Epochs (Using MNE)
			epochs = mne.read_epochs(file_path, verbose=False, preload=True)

			# 2. Extract Data
			# Shape: (N_Epochs, N_Channels, N_TimePoints)
			data = epochs.get_data(copy=False)

			# 3. Create Labels
			# Assign the specific label (0 or 1) based on the folder we are in
			n_epochs = data.shape[0]
			labels = np.full(n_epochs, label, dtype=np.longlong)

			# 4. Collect
			all_epochs_data.append(data)
			all_labels.append(labels)

			print(f"   ✅ Loaded {fname} | Epochs: {n_epochs}")

		except Exception as e:
			print(f"   ❌ Error loading {fname}: {e}")

# ==========================================
# 💾 COMBINE & SAVE
# ==========================================
if all_epochs_data:
	# Concatenate all subjects into one massive array
	# Result Shape: (Total_Epochs_All_Subjects, Channels, Time)
	X = np.concatenate(all_epochs_data, axis=0)
	y = np.concatenate(all_labels, axis=0)

	# Ensure float32 for PyTorch
	X = X.astype(np.float32)

	print(f"\n✨ COMPLETED ✨")
	print(f"Total Epochs: {X.shape[0]}")
	print(f"Channels:     {X.shape[1]}")
	print(f"Time Points:  {X.shape[2]}")
	print(f"Labels:       {np.unique(y)} (0=Native, 1=ESL)")

	np.savez_compressed(OUTPUT_FILE, X=X, y=y)
	print(f"Saved to '{OUTPUT_FILE}'")

else:
	print("\n❌ No data loaded. Please check your paths.")
"""

""" VERSION one (filename errors)
for folder_path, label, group_name in DIRS_TO_PROCESS:
	print(f"\n📂 Scanning {group_name} folder: {folder_path}")

	if not folder_path.exists():
		print(f"⚠️ Directory not found: {folder_path}")
		continue

	# List all .fif files in this specific folder
	files = [f for f in os.listdir(folder_path) if f.endswith('.fif')]
	files.sort()

	if len(files) == 0:
		print(f"⚠️ No .fif files found in {group_name} folder.")
		continue

	for fname in files:
		file_path = folder_path / fname

		try:
			# 1. Load Epochs (Using MNE)
			epochs = mne.read_epochs(file_path, verbose=False, preload=True)

			# 2. Extract Data
			# Shape: (N_Epochs, N_Channels, N_TimePoints)
			data = epochs.get_data(copy=False)

			# 3. Create Labels
			# Assign the specific label (0 or 1) based on the folder we are in
			n_epochs = data.shape[0]
			labels = np.full(n_epochs, label, dtype=np.longlong)

			# 4. Collect
			all_epochs_data.append(data)
			all_labels.append(labels)

			print(f"   ✅ Loaded {fname} | Epochs: {n_epochs}")

		except Exception as e:
			print(f"   ❌ Error loading {fname}: {e}")

# ==========================================
# 💾 COMBINE & SAVE
# ==========================================
if all_epochs_data:
	# Concatenate all subjects into one massive array
	# Result Shape: (Total_Epochs_All_Subjects, Channels, Time)
	X = np.concatenate(all_epochs_data, axis=0)
	y = np.concatenate(all_labels, axis=0)

	# Ensure float32 for PyTorch
	X = X.astype(np.float32)

	print(f"\n✨ COMPLETED ✨")
	print(f"Total Epochs: {X.shape[0]}")
	print(f"Channels:     {X.shape[1]}")
	print(f"Time Points:  {X.shape[2]}")
	print(f"Labels:       {np.unique(y)} (0=Native, 1=ESL)")

	np.savez_compressed(OUTPUT_FILE, X=X, y=y)
	print(f"Saved to '{OUTPUT_FILE}'")

else:
	print("\n❌ No data loaded. Please check your paths.")
"""