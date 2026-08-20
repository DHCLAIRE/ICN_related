#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
from scipy.io import wavfile
from pathlib import Path
"""
def generate_incremental_stimuli(input_path, base_name, max_dbfs):
    # 1. Load the stereo wav file (Shape: [samples, 2])
    sample_rate, data = wavfile.read(input_path)
    data = data.astype(np.float64) 
    max_val = 32768.0 
    
    # 2. Calculate the current global RMS across BOTH channels combined
    current_rms = np.sqrt(np.mean(data**2))
    
    # 3. Calculate multiplier to scale exactly to -15 dBFS
    target_rms_15 = max_val * (10 ** (-15.0 / 20.0))
    scale_to_15 = target_rms_15 / current_rms
    
    # Shift the raw data to exactly -15 dBFS
    data_base = data * scale_to_15
    
    # 4. Loop to generate the +1 dBFS incremental files
    # E.g., range(-15, -9) will generate -15, -14, -13, -12, -11, -10
    for target_db in range(-15, max_dbfs + 1):
        # Calculate how much to add on top of the -15 dBFS baseline
        db_difference = target_db - (-15.0)
        step_multiplier = 10 ** (db_difference / 20.0)
        
        # Apply the step multiplier
        step_data = data_base * step_multiplier
        
        # Clip to prevent digital distortion (overflow)
        step_data = np.clip(step_data, -max_val, max_val - 1)
        
        # Export the file
        output_name = f"{base_name}_{target_db}dBFS.wav"
        wavfile.write(output_name, sample_rate, step_data.astype(np.int16))
        print(f"Generated: {output_name}")
"""
if __name__ == "__main__":
    
    # Set Data path (Make sure trailing slashes are present!)
    data_root_path = "/Volumes/DH_4GB/" #"F:\LPP_Materials"
    results_data_path = "/Volumes/DH_4GB/LPP_Materials/" #"F:\LPP_Materials" #"/Volumes/DH_4GB/LPP_Materials/"
    
    for tape_numSTR in range(1, 10):
        target_wavfileSTR = f"LPP_ENG_tape_{tape_numSTR}.wav" #"LPP_FRN_tape_1.wav"
        audio_wavfile = results_data_path / Path(target_wavfileSTR)
        
        # Set the ceiling of the dBFS baseline ()
        max_dbfs = -10 
        
        # 1. Load the stereo wav file (Shape: [samples, 2])
        sample_rate, data = wavfile.read(audio_wavfile)
        print(data.dtype)
        # 2. Detect Bit Depth and set Maximum Value dynamically
        original_dtype = data.dtype
        
        if original_dtype == np.int16:
            # Configuration for 16-bit PCM
            max_val = 32768.0
            clip_min = -32768.0
            clip_max = 32767.0
            print("Detected 16-bit PCM format.")
            
        elif original_dtype in [np.float32, np.float64]:
            # Configuration for 32-bit Float
            max_val = 1.0
            clip_min = -1.0
            clip_max = 1.0
            print("Detected 32-bit Float format.")
            
        else:
            raise ValueError(f"Unsupported audio format: {original_dtype}")
        
        data = data.astype(np.float64) 
        max_val = 32768.0 
        
        # 2. Calculate the current global RMS across BOTH channels combined
        current_rms = np.sqrt(np.mean(data**2))
        #print(current_rms)
        # 3. Calculate multiplier to scale exactly to -15 dBFS
        target_rms_15 = max_val * (10 ** (-15.0 / 20.0))
        #print(target_rms_15)
        scale_to_15 = target_rms_15 / current_rms
        
        # Shift the raw data to exactly -15 dBFS
        data_base = data * scale_to_15
        
        # 4. Loop to generate the +1 dBFS incremental files
        # E.g., range(-15, -9) will generate -15, -14, -13, -12, -11, -10
        for target_db in range(-15, max_dbfs + 1):
            # Calculate how much to add on top of the -15 dBFS baseline
            db_difference = target_db - (-15.0)
            step_multiplier = 10 ** (db_difference / 20.0)
            
            # Apply the step multiplier
            step_data = data_base * step_multiplier
            
            # Clip to prevent digital distortion (overflow)
            step_data = np.clip(step_data, -max_val, max_val - 1)
            
            # Export the file
            output_name = f"{target_wavfileSTR}_{target_db}dBFS.wav"
            wavfile.write(results_data_path / Path(output_name), sample_rate, step_data.astype(np.int16))
            print(f"Generated: {output_name}")
        
        
        # Example usage: Will create files from -15 dBFS up to -10 dBFS
        #generate_incremental_stimuli(results_data_path / Path("LPP_FRN_tape_1.wav"), "LPP_FRN_tape_1.wav", -10)