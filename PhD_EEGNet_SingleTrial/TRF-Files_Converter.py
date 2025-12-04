#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
import eelbrain
from pathlib import Path
import os
import re

# ==========================================
# 🟢 CONFIGURATION & PROCESSING
# ==========================================
DATA_ROOT = Path("/Users/neuroling/Downloads/DINGHSIN_Results/Alice_Experiments_Results")#Path("/Volumes/Neurolang_1/Master Program/New_Thesis_topic/Experiments_Results")
OUTPUT_FILE = "all_subjects_trf.npz"

TRF_Group_typesLIST = ["Natives", "ESLs"]

data_list = []
labels_list = []
valid_subjects = []

print(f"Starting data extraction from: {DATA_ROOT}")

for G_typesSTR in TRF_Group_typesLIST:
    # 1. Determine Label and Settings based on Group
    if G_typesSTR.lower() == "natives":
        label = 0
        regex_pattern = r'S\d*' # Regex for Natives
        print(f"\n🔵 Processing NATIVE group (Label {label})...")
    else:
        label = 1
        regex_pattern = r'n_2_S\d*' # Regex for ESLs
        print(f"\n🟠 Processing ESL group (Label {label})...")

    # 2. Setup Paths dynamically
    # Constructing paths based on your logic:
    # EEG_DIR: .../EEG_Natives/Alice_Natives_ICAed_fif
    # TRF_DIR: .../TRFs_Natives
    EEG_DIR = DATA_ROOT / f'EEG_{G_typesSTR}' / f'Alice_{G_typesSTR}_ICAed_fif'
    TRF_DIR = DATA_ROOT / f'TRFs_{G_typesSTR}'
    
    if not EEG_DIR.exists():
        print(f"⚠️ EEG Directory not found: {EEG_DIR}")
        continue
    
    if not TRF_DIR.exists():
        print(f"⚠️ TRF Directory not found: {TRF_DIR}")
        continue

    # 3. Find Subjects in EEG Directory using Regex
    # We iterate over the EEG directory to get the valid subject names
    try:
        subject_names = [path.name for path in EEG_DIR.iterdir() if re.match(regex_pattern, path.name)]
        subject_names.sort()
    except FileNotFoundError:
        print(f"❌ Could not iterate EEG_DIR: {EEG_DIR}")
        continue
    
    print(f"Found {len(subject_names)} subjects in {G_typesSTR}")

    # 4. Load TRFs for these subjects
    for subj_name in subject_names:
        # Construct path: TRF_DIR / SubjectName / SubjectName envelope+onset.pickle
        # Example: .../TRFs_Natives/S01/S01 envelope+onset.pickle
        file_path = TRF_DIR / subj_name / f'{subj_name} envelope+onset.pickle'
        
        if not file_path.exists():
            print(f"  ⚠️ Missing pickle: {file_path}")
            continue
            
        try:
            # Load Eelbrain object
            res = eelbrain.load.unpickle(file_path)
            
            # Extract Numpy Array (Features, Channels, Times)
            # res.h is the TRF. .x is the raw array.
            trf_array = res.h.x
            
            data_list.append(trf_array)
            labels_list.append(label)
            valid_subjects.append(subj_name)
            
            print(f"  ✅ Loaded {subj_name} | Shape: {trf_array.shape}")

        except Exception as e:
            print(f"  ❌ Error loading {subj_name}: {e}")

# ==========================================
# 💾 SAVE TO DISK
# ==========================================
if data_list:
    # Stack into one big array: (Total_Subjects, Features, Channels, Time)
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