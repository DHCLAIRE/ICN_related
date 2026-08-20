#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
from scipy.io import wavfile

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

# Example usage: Will create files from -15 dBFS up to -10 dBFS
generate_incremental_stimuli("raw_voice_tape.wav", "stimulus", -10)