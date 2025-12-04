#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
import eelbrain
from pathlib import Path
import os

# ==========================================
# 🟢 CONFIGURATION
# ==========================================
TRF_DIR = Path("/Path/To/Your/TRF_Folder")  # <--- UPDATE THIS
OUTPUT_FILE = "all_subjects_trf.npz"

# Define your subjects (1 to 57)
SUBJECTS = list(range(1, 58))

# Define your Groups (0 = Native, 1 = L2)
# UPDATE THIS LOGIC based on your real subject IDs
def get_label_for_subject(subj_id):
	if subj_id <= 20: 
		return 0 # Native
	else:             
		return 1 # L2

# ==========================================
# ⚙️ EXTRACTION LOGIC
# ==========================================
data_list = []
labels_list = []
valid_subjects = []

print(f"Processing {len(SUBJECTS)} subjects...")

for subj in SUBJECTS:
	# 1. Build the path: S003/S003 envelope+onset.pickle
	file_path = TRF_DIR / f'S{subj:03d}' / f'S{subj:03d} envelope+onset.pickle'

	if not file_path.exists():
		print(f"⚠️ Missing: {file_path}")
		continue

	try:
		# 2. Load the Eelbrain object
		res = eelbrain.load.unpickle(file_path)

		# 3. Extract the Numpy Array (The numbers)
		# res.h is the TRF. .x is the raw array.
		# Shape is typically (Features, Channels, Times) -> e.g. (7, 64, 128)
		trf_array = res.h.x

		data_list.append(trf_array)

		# 4. Create the Label
		label = get_label_for_subject(subj)
		labels_list.append(label)
		valid_subjects.append(subj)

		print(f"✅ Loaded S{subj:03d} | Label: {label} | Shape: {trf_array.shape}")

	except Exception as e:
		print(f"❌ Error loading S{subj}: {e}")

# ==========================================
# 💾 SAVE TO DISK
# ==========================================
if data_list:
	# Stack into one big array: (N_Subjects, 7, 64, 128)
	X = np.stack(data_list).astype(np.float32)
	y = np.array(labels_list).astype(np.longlong)

	print(f"\nSaving Data...")
	print(f"X shape: {X.shape}")
	print(f"y shape: {y.shape}")

	# Save as compressed numpy file
	np.savez_compressed(OUTPUT_FILE, X=X, y=y, subjects=valid_subjects)
	print(f"🎉 Done! Saved to '{OUTPUT_FILE}'")
else:
	print("No data was loaded. Check your paths.")