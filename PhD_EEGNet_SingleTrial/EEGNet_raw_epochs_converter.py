#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
import mne
import os
from pathlib import Path


import numpy as np
import mne
import os
from pathlib import Path


# VERSION 8: add sub-num into the labeling. 
# ==========================================
# 🟢 CONFIGURATION
# ==========================================
DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")

wOnset_DIR_Natives = DATA_ROOT / 'EEG_Natives' / 'Alice_Natives_wOnset_raw_epochs'
wOnset_DIR_ESLs = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESLs_wOnset_raw_epochs'

OUTPUT_FILE = "all_subjects_epochs.npz"

# Updated Labels: Native=0, ESL=1 (Standard 0-based index)
DIRS_TO_PROCESS = [
        (wOnset_DIR_Natives, 0, "Native"), 
    (wOnset_DIR_ESLs, 1, "ESL")
]

# ==========================================
# ⚙️ PROCESSING
# ==========================================
all_epochs_data = []
all_labels = []
all_subject_ids = [] # New: Track Subject ID

print(f"Starting processing...")

# --- STEP 1: Establish Master Channel Names from ESL ---
print("🔍 Step 1: Extracting standard channel names from an ESL file...")
master_channel_names = None

esl_files = [f for f in os.listdir(wOnset_DIR_ESLs) if f.endswith('epochs_allTapes_raw.fif')]
if not esl_files:
	print("❌ No ESL files found.")
	exit()

template_path = wOnset_DIR_ESLs / esl_files[0]
temp_info = mne.io.read_info(template_path, verbose=False)
master_channel_names = [ch.strip() for ch in temp_info['ch_names']] 
print(f"✅ Template: {len(master_channel_names)} channels")


# --- STEP 2: Load and Harmonize ---
print(f"\n🚀 Step 2: Harmonizing and Loading...")

# Generate a unique integer ID for every file/subject processed
subject_counter = 0

for folder_path, label, group_name in DIRS_TO_PROCESS:
	if not folder_path.exists():
		continue

	files = [f for f in os.listdir(folder_path) if f.endswith('epochs_allTapes_raw.fif')]
	files.sort()

	for fname in files:
		file_path = folder_path / fname

		try:
			epochs = mne.read_epochs(file_path, verbose=False, preload=True)

			# --- CHANNEL FIX LOGIC ---
			if group_name == "ESL":
				epochs.rename_channels({ch: ch.strip() for ch in epochs.info['ch_names']})
			elif group_name == "Native":
				if len(epochs.ch_names) > len(master_channel_names):
					keep_indices = np.arange(len(master_channel_names)) 
					keep_names = [epochs.ch_names[i] for i in keep_indices]
					epochs.pick_channels(keep_names, ordered=True)

				if len(epochs.ch_names) == len(master_channel_names):
					rename_map = dict(zip(epochs.ch_names, master_channel_names))
					epochs.rename_channels(rename_map)
				else:
					print(f"⚠️ Skipping {fname}: Channel count mismatch.")
					continue

			epochs.pick_channels(master_channel_names, ordered=True)

			# Extract
			data = epochs.get_data(copy=False)
			n_epochs = data.shape[0]

			# Create Labels (0 or 1)
			labels = np.full(n_epochs, label, dtype=np.longlong)

			# Create Subject IDs (Every epoch gets the current subject_counter)
			sub_ids = np.full(n_epochs, subject_counter, dtype=np.longlong)

			all_epochs_data.append(data)
			all_labels.append(labels)
			all_subject_ids.append(sub_ids) # Store IDs

			print(f"   ✅ {fname} | SubjectID {subject_counter} | Shape {data.shape}")

			# Increment counter for next file
			subject_counter += 1

		except Exception as e:
			print(f"   ❌ Error {fname}: {e}")

# --- STEP 3: Time Harmonization & Save ---
if all_epochs_data:
	time_dims = [d.shape[2] for d in all_epochs_data]
	min_time = min(time_dims)

	all_epochs_data = [d[:, :, :min_time] for d in all_epochs_data]

	# Concatenate
	X = np.concatenate(all_epochs_data, axis=0).astype(np.float32)
	y = np.concatenate(all_labels, axis=0).astype(np.longlong)
	z = np.concatenate(all_subject_ids, axis=0).astype(np.longlong) # The Subject IDs

	print(f"\n✨ DONE. Final Shape: {X.shape}")
	print(f"Subjects Tracked: {len(np.unique(z))}")

	# Save 'z' (subjects) along with X and y
	np.savez_compressed(OUTPUT_FILE, X=X, y=y, subjects=z)
	print(f"Saved to {OUTPUT_FILE}")
else:
	print("❌ No data loaded.")


"""
# VERSION seven: considering different epoch length
# ==========================================
# 🟢 CONFIGURATION
# ==========================================
DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")

wOnset_DIR_Natives = DATA_ROOT / 'EEG_Natives' / 'Alice_Natives_wOnset_raw_epochs'
wOnset_DIR_ESLs = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESLs_wOnset_raw_epochs'

OUTPUT_FILE = DATA_ROOT / "all_subjects_epochs.npz"

# Updated Labels: Native=1, ESL=2
DIRS_TO_PROCESS = [
        (wOnset_DIR_Natives, 1, "Native"), 
    (wOnset_DIR_ESLs, 2, "ESL")
]

# ==========================================
# ⚙️ PROCESSING
# ==========================================
all_epochs_data = []
all_labels = []

print(f"Starting processing...")

# --- STEP 1: Establish Master Channel Names from ESL ---
# ESLs have the correct 57 channel names (10-20 system)
print("🔍 Step 1: Extracting standard channel names from an ESL file...")
master_channel_names = None

esl_files = [f for f in os.listdir(wOnset_DIR_ESLs) if f.endswith('epochs_allTapes_raw.fif')]
if not esl_files:
	print("❌ No ESL files found.")
	exit()

template_path = wOnset_DIR_ESLs / esl_files[0]
temp_info = mne.io.read_info(template_path, verbose=False)
master_channel_names = [ch.strip() for ch in temp_info['ch_names']] # Clean names
print(f"✅ Template: {len(master_channel_names)} channels (e.g., {master_channel_names[:3]}...)")


# --- STEP 2: Load and Harmonize ---
print(f"\n🚀 Step 2: Harmonizing and Loading...")

for folder_path, label, group_name in DIRS_TO_PROCESS:
	if not folder_path.exists():
		continue

	files = [f for f in os.listdir(folder_path) if f.endswith('epochs_allTapes_raw.fif')]
	files.sort()

	for fname in files:
		file_path = folder_path / fname

		try:
			epochs = mne.read_epochs(file_path, verbose=False, preload=True)

			# --- CHANNEL FIX LOGIC ---

			# Case A: ESL (Standard)
			if group_name == "ESL":
				# Sanitize current names
				epochs.rename_channels({ch: ch.strip() for ch in epochs.info['ch_names']})

			# Case B: Native (Numeric 1-59 -> Needs to map to ESL names)
			elif group_name == "Native":
				# 1. Drop the extra channels (58, 59)
				if len(epochs.ch_names) > len(master_channel_names):
					# Keep only the first 57
					keep_indices = np.arange(len(master_channel_names)) 
					keep_names = [epochs.ch_names[i] for i in keep_indices]
					epochs.pick_channels(keep_names, ordered=True)

				# 2. Rename the remaining 57 numbers to the 57 ESL names
				# Assumes consistent electrode order
				if len(epochs.ch_names) == len(master_channel_names):
					rename_map = dict(zip(epochs.ch_names, master_channel_names))
					epochs.rename_channels(rename_map)
				else:
					print(f"⚠️ Skipping {fname}: Channel count mismatch.")
					continue

			# Ensure exact order matches Master
			epochs.pick_channels(master_channel_names, ordered=True)

			# Extract
			data = epochs.get_data(copy=False)
			n_epochs = data.shape[0]
			n_times = data.shape[2]

			# Create Labels (1 or 2)
			labels = np.full(n_epochs, label, dtype=np.longlong)

			all_epochs_data.append(data)
			all_labels.append(labels)
			print(f"   ✅ {fname} ({group_name}) | Label {label} | Shape {data.shape}")

		except Exception as e:
			print(f"   ❌ Error {fname}: {e}")

# --- STEP 3: Time Harmonization & Save ---
if all_epochs_data:
	# Check for time dimension mismatches
	time_dims = [d.shape[2] for d in all_epochs_data]
	min_time = min(time_dims)
	max_time = max(time_dims)

	if min_time != max_time:
		print(f"\n⚠️ TIME MISMATCH DETECTED: Lengths vary from {min_time} to {max_time} samples.")
		print(f"✂️ Cropping all subjects to the shortest length: {min_time} samples...")

		# Crop all arrays to the minimum length to allow concatenation
		all_epochs_data = [d[:, :, :min_time] for d in all_epochs_data]

	# Concatenate
	X = np.concatenate(all_epochs_data, axis=0).astype(np.float32)
	y = np.concatenate(all_labels, axis=0).astype(np.longlong)

	print(f"\n✨ DONE. Final Shape: {X.shape}, Labels: {np.unique(y)}")
	np.savez_compressed(OUTPUT_FILE, X=X, y=y)
	print(f"Saved to {OUTPUT_FILE}")
else:
	print("❌ No data loaded.")
"""

"""
# Version SIX: Retry everything
# ==========================================
# 🟢 CONFIGURATION
# ==========================================
DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")

wOnset_DIR_Natives = DATA_ROOT / 'EEG_Natives' / 'Alice_Natives_wOnset_raw_epochs'
wOnset_DIR_ESLs = DATA_ROOT / 'EEG_ESLs' / 'Alice_ESLs_wOnset_raw_epochs'

OUTPUT_FILE = "Alice_all_subjects_epochs.npz"

# Updated Labels: Native=1, ESL=2
DIRS_TO_PROCESS = [
        (wOnset_DIR_Natives, 1, "Native"), 
    (wOnset_DIR_ESLs, 2, "ESL")
]

# ==========================================
# ⚙️ PROCESSING
# ==========================================
all_epochs_data = []
all_labels = []

print(f"Starting processing...")

# --- STEP 1: Establish Master Channel Names from ESL ---
# ESLs have the correct 57 channel names (10-20 system)
print("🔍 Step 1: Extracting standard channel names from an ESL file...")
master_channel_names = None

esl_files = [f for f in os.listdir(wOnset_DIR_ESLs) if f.endswith('epochs_allTapes_raw.fif')]
if not esl_files:
	print("❌ No ESL files found.")
	exit()

template_path = wOnset_DIR_ESLs / esl_files[0]
temp_info = mne.io.read_info(template_path, verbose=False)
master_channel_names = [ch.strip() for ch in temp_info['ch_names']] # Clean names
print(f"✅ Template: {len(master_channel_names)} channels (e.g., {master_channel_names[:3]}...)")


# --- STEP 2: Load and Harmonize ---
print(f"\n🚀 Step 2: Harmonizing and Loading...")

for folder_path, label, group_name in DIRS_TO_PROCESS:
	if not folder_path.exists():
		continue

	files = [f for f in os.listdir(folder_path) if f.endswith('epochs_allTapes_raw.fif')]
	files.sort()

	for fname in files:
		file_path = folder_path / fname

		try:
			epochs = mne.read_epochs(file_path, verbose=False, preload=True)

			# --- CHANNEL FIX LOGIC ---

			# Case A: ESL (Standard)
			if group_name == "ESL":
				# Sanitize current names
				epochs.rename_channels({ch: ch.strip() for ch in epochs.info['ch_names']})

			# Case B: Native (Numeric 1-59 -> Needs to map to ESL names)
			elif group_name == "Native":
				# 1. Drop the extra channels (58, 59)
				if len(epochs.ch_names) > len(master_channel_names):
					# Keep only the first 57
					keep_indices = np.arange(len(master_channel_names)) 
					keep_names = [epochs.ch_names[i] for i in keep_indices]
					epochs.pick_channels(keep_names, ordered=True)

				# 2. Rename the remaining 57 numbers to the 57 ESL names
				# Assumes consistent electrode order
				if len(epochs.ch_names) == len(master_channel_names):
					rename_map = dict(zip(epochs.ch_names, master_channel_names))
					epochs.rename_channels(rename_map)
				else:
					print(f"⚠️ Skipping {fname}: Channel count mismatch.")
					continue

			# Ensure exact order matches Master
			epochs.pick_channels(master_channel_names, ordered=True)

			# Extract
			data = epochs.get_data(copy=False)
			n_epochs = data.shape[0]

			# Create Labels (1 or 2)
			labels = np.full(n_epochs, label, dtype=np.longlong)

			all_epochs_data.append(data)
			all_labels.append(labels)
			print(f"   ✅ {fname} ({group_name}) | Label {label} | Shape {data.shape}")

		except Exception as e:
			print(f"   ❌ Error {fname}: {e}")

# --- STEP 3: Save ---
if all_epochs_data:
	X = np.concatenate(all_epochs_data, axis=0).astype(np.float32)
	y = np.concatenate(all_labels, axis=0).astype(np.longlong)

	print(f"\n✨ DONE. Final Shape: {X.shape}, Labels: {np.unique(y)}")
	np.savez_compressed(OUTPUT_FILE, X=X, y=y)
	print(f"Saved to {OUTPUT_FILE}")
else:
	print("❌ No data loaded.")
"""
    
""" VERSION FIVE: Turn Natives 59 ch-names into ESL's 57 channels (exclude the 2 extra one) >> which I think is wrong doing. 
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

print(f"Starting processing...")

# --- STEP 1: Establish the "Master" Channel Names from ESL Group ---
# We use ESL as the 'Standard' because they have 10-20 names (Fz, Cz, etc.)
# Natives have numbers (1, 2, 3...), so we will rename Natives to match ESL.
print("🔍 Step 1: extracting standard channel names from an ESL file...")
master_channel_names = None

# Find an ESL file to serve as the template
esl_files = [f for f in os.listdir(wOnset_DIR_ESLs) if f.endswith('epochs_allTapes_raw.fif')]
if not esl_files:
	print("❌ No ESL files found to establish channel names.")
	exit()

template_path = wOnset_DIR_ESLs / esl_files[0]
temp_info = mne.io.read_info(template_path, verbose=False)
# Strip spaces just in case
master_channel_names = [ch.strip() for ch in temp_info['ch_names']]
print(f"✅ Template established from {esl_files[0]}")
print(f"   Count: {len(master_channel_names)} channels")
print(f"   Names: {master_channel_names[:5]} ...")


# --- STEP 2: Load and Harmonize All Files ---
print(f"\n🚀 Step 2: Loading, Renaming, and Stacking...")

for folder_path, label, group_name in DIRS_TO_PROCESS:
	if not folder_path.exists():
		print(f"⚠️ Directory not found: {folder_path}")
		continue

	files = [f for f in os.listdir(folder_path) if f.endswith('epochs_allTapes_raw.fif')]
	files.sort()

	for fname in files:
		file_path = folder_path / fname

		try:
			epochs = mne.read_epochs(file_path, verbose=False, preload=True)

			# --- CHANNEL HARMONIZATION LOGIC ---

			# Case A: ESL Files (Already have correct names, check count)
			if group_name == "ESL":
				# Just ensure names are clean
				current_map = {ch: ch.strip() for ch in epochs.info['ch_names']}
				epochs.rename_channels(current_map)

				# Check if it matches master list exactly
				if len(epochs.ch_names) != len(master_channel_names):
					print(f"⚠️ Skipping {fname}: ESL file has {len(epochs.ch_names)} channels, expected {len(master_channel_names)}.")
					continue

			# Case B: Native Files (Numbers 1-59 -> Needs to become Names)
			elif group_name == "Native":
				# 1. Handle the Count Mismatch (59 vs 57)
				# Assumption: The first 57 channels correspond to the 57 ESL channels.
				# The extra 2 (58, 59) are likely EOG/AUX and are dropped.
				if len(epochs.ch_names) > len(master_channel_names):
					# Pick only the first N channels
					keep_indices = np.arange(len(master_channel_names))
					# Map indices to current numeric names
					keep_names = [epochs.ch_names[i] for i in keep_indices]
					epochs.pick_channels(keep_names, ordered=True)

				# 2. Rename to match Master List
				# This assumes the ORDER of electrodes is the same (e.g., Ch1=Fp1 in both caps)
				if len(epochs.ch_names) == len(master_channel_names):
					rename_map = dict(zip(epochs.ch_names, master_channel_names))
					epochs.rename_channels(rename_map)
				else:
					print(f"⚠️ Skipping {fname}: Native file has {len(epochs.ch_names)} chans, cannot map to {len(master_channel_names)}.")
					continue

			# --- END HARMONIZATION ---

			# Double check alignment before extracting data
			# Ensure strictly ordered selection to match the master list
			epochs.pick_channels(master_channel_names, ordered=True)

			data = epochs.get_data(copy=False)
			n_epochs = data.shape[0]
			labels = np.full(n_epochs, label, dtype=np.longlong)

			all_epochs_data.append(data)
			all_labels.append(labels)

			print(f"   ✅ Loaded {fname} ({group_name}) | Renamed & Stacked | Epochs: {n_epochs}")

		except Exception as e:
			print(f"   ❌ Error loading {fname}: {e}")

# --- STEP 3: Save ---
if all_epochs_data:
	X = np.concatenate(all_epochs_data, axis=0)
	y = np.concatenate(all_labels, axis=0)
	X = X.astype(np.float32)

	print(f"\n✨ COMPLETED ✨")
	print(f"Total Epochs: {X.shape[0]}")
	print(f"Channels:     {X.shape[1]}")
	print(f"Time Points:  {X.shape[2]}")
	print(f"Labels:       {np.unique(y)} (0=Native, 1=ESL)")

	np.savez_compressed(OUTPUT_FILE, X=X, y=y)
	print(f"Saved to '{OUTPUT_FILE}'")
else:
	print("\n❌ No data loaded.")
"""

""" VERSION FOUR: Channels name not aligned
# ==========================================
# ⚙️ PROCESSING
# ==========================================
all_epochs_data = []
all_labels = []
all_file_paths = []

print(f"Starting processing...")

# --- 1. Collect Valid Files ---
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

# --- 2. Determine Common Channels (With Sanitation) ---
common_channels = None
debug_sample_prev = None

for item in all_file_paths:
	try:
		info = mne.io.read_info(item['path'], verbose=False)
		# SANITIZE: Strip whitespace from channel names (e.g., "Cz " -> "Cz")
		current_ch = set([c.strip() for c in info['ch_names']])

		if common_channels is None:
			common_channels = current_ch
			debug_sample_prev = list(current_ch)[:5]
			print(f"   Reference file ({item['fname']}) has {len(common_channels)} channels.")
		else:
			prev_len = len(common_channels)
			common_channels = common_channels.intersection(current_ch)
			new_len = len(common_channels)

			# DEBUGGING: If intersection drops to 0, show why
			if new_len == 0 and prev_len > 0:
				print(f"\n❌ CRITICAL MISMATCH at file: {item['fname']}")
				print(f"   Channels remaining before this file: {len(common_channels)}")
				print(f"   Sample of Expected: {debug_sample_prev}")
				print(f"   Sample of Current:  {list(current_ch)[:5]}")
				print("   The intersection is empty. Check if naming conventions (e.g., 'Cz' vs '1') differ.")
				exit()

	except Exception as e:
		print(f"⚠️ Warning reading info from {item['fname']}: {e}")

if common_channels is None or len(common_channels) == 0:
	print("❌ No common channels found. Cannot combine.")
	exit()

target_channels = sorted(list(common_channels))
print(f"✅ Found {len(target_channels)} common channels across {len(all_file_paths)} files.")

# --- 3. Pass 2: Load and Stack ---
print(f"\n🚀 Pass 2: Loading data...")

for item in all_file_paths:
	fname = item['fname']
	file_path = item['path']
	label = item['label']

	try:
		epochs = mne.read_epochs(file_path, verbose=False, preload=True)

		# SANITIZE: Rename channels in the loaded object to match the stripped versions
		# This ensures 'Cz ' becomes 'Cz' so pick_channels works
		rename_map = {ch: ch.strip() for ch in epochs.info['ch_names']}
		epochs.rename_channels(rename_map)

		# Select common channels
		epochs.pick_channels(target_channels, ordered=True)

		data = epochs.get_data(copy=False)

		if data.shape[1] != len(target_channels):
			print(f"⚠️ Skipping {fname}: Channel mismatch.")
			continue

		n_epochs = data.shape[0]
		labels = np.full(n_epochs, label, dtype=np.longlong)

		all_epochs_data.append(data)
		all_labels.append(labels)

		print(f"   ✅ Loaded {fname} | Epochs: {n_epochs} | Chans: {data.shape[1]}")

	except Exception as e:
		print(f"   ❌ Error loading {fname}: {e}")

# --- 4. Save ---
if all_epochs_data:
	X = np.concatenate(all_epochs_data, axis=0)
	y = np.concatenate(all_labels, axis=0)
	X = X.astype(np.float32)

	print(f"\n✨ COMPLETED ✨")
	print(f"Total Epochs: {X.shape[0]}")
	print(f"Channels:     {X.shape[1]}")
	print(f"Time Points:  {X.shape[2]}")

	np.savez_compressed(OUTPUT_FILE, X=X, y=y)
	print(f"Saved to '{OUTPUT_FILE}'")
else:
	print("\n❌ No data loaded.")
"""

"""VERSION THREE: Channel length not aligned
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
	
"""

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