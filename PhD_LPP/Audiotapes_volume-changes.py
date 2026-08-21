#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np
from scipy.io import wavfile
from pathlib import Path
import noisereduce as nr
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
        
import numpy as np
from scipy.io import wavfile

def soft_clip_amplify(input_path, output_path, target_rms_dbfs):
    sample_rate, data = wavfile.read(input_path)
    
    # Convert to 32-bit float scale (-1.0 to 1.0) for easier math
    if data.dtype == np.int16:
        data = data.astype(np.float64) / 32768.0
        
    # Calculate RMS and amplify
    current_rms = np.sqrt(np.mean(data**2))
    target_rms = 10 ** (target_rms_dbfs / 20.0)
    amplified_data = data * (target_rms / current_rms)
    
    # Apply Soft Clipping (Hyperbolic Tangent curve)
    # This gently squashes peaks as they approach 1.0, rather than chopping them
    soft_clipped_data = np.tanh(amplified_data)
    
    # Convert back to 16-bit integer
    final_data = np.int16(soft_clipped_data * 32767.0)
    
    wavfile.write(output_path, sample_rate, final_data)
    
import numpy as np
from scipy.io import wavfile
import noisereduce as nr
def smart_dynamic_prepare_stimuli(input_path, output_path, target_rms_dbfs):
    # 1. Load the wav file
    sample_rate, data = wavfile.read(input_path)
    original_dtype = data.dtype
    
    # 2. Detect Bit Depth and normalize to a unified float range [-1.0, 1.0]
    if original_dtype == np.int16:
        print(f"[{input_path}] Detected 16-bit PCM format.")
        # Convert int16 integers to decimals scaled between -1.0 and 1.0
        work_data = data.astype(np.float64) / 32768.0
        
    elif original_dtype in [np.float32, np.float64]:
        print(f"[{input_path}] Detected 32-bit/64-bit Float format.")
        # Already in float range, just ensure 64-bit precision for calculations
        work_data = data.astype(np.float64)
        
    else:
        raise ValueError(f"Unsupported audio format: {original_dtype}")
        
    # 3. Apply Spectral Noise Reduction (background hiss/hum removal)
    clean_data = nr.reduce_noise(y=work_data, sr=sample_rate)
    
    # 4. Calculate RMS and amplify to target dBFS
    # On a normalized [-1.0, 1.0] scale, the absolute ceiling limit is 1.0
    current_rms = np.sqrt(np.mean(clean_data**2))
    
    if current_rms == 0:
        raise ValueError(f"[{input_path}] Error: Audio file is completely silent (RMS is 0).")
        
    target_rms = 10 ** (target_rms_dbfs / 20.0)
    scale_multiplier = target_rms / current_rms
    amplified_data = clean_data * scale_multiplier
    
    # 5. Conditional Check: Will this cause digital clipping/static?
    highest_peak = np.max(np.abs(amplified_data))
    
    if highest_peak > 1.0:
        print(f"-> Peak detected at {highest_peak:.2f} (> 1.0). Applying Soft-Clipping (tanh).")
        # Soft-clip to round off the peaks smoothly within the [-1.0, 1.0] ceiling
        final_data = np.tanh(amplified_data)
    else:
        print(f"-> Peak at {highest_peak:.2f} (<= 1.0). Passing through normally.")
        # No clipping needed, leave the waveform intact
        final_data = amplified_data
        
    # 6. Convert back to the exact original bit depth and format for export
    if original_dtype == np.int16:
        # Scale back up to 16-bit integer range, apply hard safety clip, and cast to int16
        scaled_int_data = final_data * 32768.0
        safe_clipped_data = np.clip(scaled_int_data, -32768.0, 32767.0)
        final_output = safe_clipped_data.astype(np.int16)
    else:
        # For float formats, ensure absolute bounds are respected and cast back
        safe_float_data = np.clip(final_data, -1.0, 1.0)
        final_output = safe_float_data.astype(original_dtype)
        
    # 7. Write the processed file to disk
    wavfile.write(output_path, sample_rate, final_output)
    print(f"Successfully exported: {output_path}\n")

# Example usage for a batch or single file:
# smart_dynamic_prepare_stimuli("raw_voice_tape.wav", "processed_stimulus.wav", -15)


import numpy as np
from scipy.io import wavfile
import noisereduce as nr

def generate_smart_incremental_stimuli(input_path, base_name, baseline_dbfs=-15, max_dbfs=-10):
    # 1. Load the original audio and detect format
    sample_rate, data = wavfile.read(input_path)
    original_dtype = data.dtype
    
    print(f"--- Processing: {input_path} ---")
    
    # 2. Normalize into a unified float scale [-1.0, 1.0] for math
    if original_dtype == np.int16:
        print("Format: 16-bit PCM")
        work_data = data.astype(np.float64) / 32768.0
    elif original_dtype in [np.float32, np.float64]:
        print("Format: 32/64-bit Float")
        work_data = data.astype(np.float64)
    else:
        raise ValueError(f"Unsupported audio format: {original_dtype}")
        
    # 3. Clean background noise (Hiss/Hum) universally
    print("Applying Spectral Noise Reduction...")
    clean_data = nr.reduce_noise(y=work_data, sr=sample_rate)
    
    # 4. Calculate RMS and establish the Baseline (e.g., -15 dBFS)
    current_rms = np.sqrt(np.mean(clean_data**2))
    if current_rms == 0:
        raise ValueError("Error: Audio file is completely silent.")
        
    baseline_rms = 10 ** (baseline_dbfs / 20.0)
    baseline_data = clean_data * (baseline_rms / current_rms)
    
    print(f"Starting increment generation from {baseline_dbfs} dBFS to {max_dbfs} dBFS...\n")
    
    # 5. THE LOOP: Generate each increment step-by-step
    for target_db in range(baseline_dbfs, max_dbfs + 1):
        
        # Calculate multiplier relative to the baseline
        db_difference = target_db - baseline_dbfs
        step_multiplier = 10 ** (db_difference / 20.0)
        
        # Apply volume increase for this specific loop iteration
        step_data = baseline_data * step_multiplier
        
        # 6. Conditional Check: Will THIS specific volume level cause static?
        highest_peak = np.max(np.abs(step_data))
        
        if highest_peak > 1.0:
            print(f"[{target_db} dBFS] Warning: Peak at {highest_peak:.2f}. Applying Soft-Clipping.")
            # Apply mathematical curve to smooth the peaks
            final_data = np.tanh(step_data)
        else:
            print(f"[{target_db} dBFS] Safe: Peak at {highest_peak:.2f}. Passing cleanly.")
            # Leave the soundwave completely intact
            final_data = step_data
            
        # 7. Convert back to original format and Export
        if original_dtype == np.int16:
            # Scale back to 16-bit limits and apply hard safety clip
            safe_clipped = np.clip(final_data * 32768.0, -32768.0, 32767.0)
            final_output = safe_clipped.astype(np.int16)
        else:
            safe_clipped = np.clip(final_data, -1.0, 1.0)
            final_output = safe_clipped.astype(original_dtype)
            
        output_name = f"{base_name}_{target_db}dBFS.wav"
        wavfile.write(output_name, sample_rate, final_output)
        
    print("\n--- Processing Complete ---")

# Example Usage:
# generate_smart_incremental_stimuli("raw_voice_tape.wav", "stimulus_block", baseline_dbfs=-15, max_dbfs=-10)
"""
if __name__ == "__main__":
    
    # Set Data path (Make sure trailing slashes are present!)
    data_root_path = "/Volumes/DH_4GB/" #"F:\LPP_Materials"
    results_data_path = "/Volumes/DH_4GB/LPP_Materials/" #"F:\LPP_Materials" #"/Volumes/DH_4GB/LPP_Materials/"
    
    # Start the loop if audiotapes processing in batch
    #for tape_numSTR in range(1, 10):
    target_wavfileSTR =  "LPP_CHT_tape_1_5min.wav" #f"LPP_CHT_tape_{tape_numSTR}.wav" #"LPP_FRN_tape_1.wav"
    audio_wavfile = results_data_path / Path(target_wavfileSTR)
    
    # 1. Load the stereo wav file (Shape: [samples, 2]), and set the target_rms_dbfs
    sample_rate, data = wavfile.read(audio_wavfile)
    #print(data.dtype)
    original_dtype = data.dtype
    target_rms_dbfs = -15.0
    
    print(f"--- Processing: {input_path} ---")
        
    # 2. Normalize into a unified float scale [-1.0, 1.0] for math
    if original_dtype == np.int16:
        print("Format: 16-bit PCM")
        work_data = data.astype(np.float64) / 32768.0
    elif original_dtype in [np.float32, np.float64]:
        print("Format: 32/64-bit Float")
        work_data = data.astype(np.float64)
    else:
        raise ValueError(f"Unsupported audio format: {original_dtype}")
    
    # 3. Clean background noise (Hiss/Hum) universally
    print("Applying Spectral Noise Reduction...")
    clean_data = nr.reduce_noise(y=work_data, sr=sample_rate)
    
    # 4. Calculate RMS and establish the Baseline (e.g., -15 dBFS)
    current_rms = np.sqrt(np.mean(clean_data**2))
    if current_rms == 0:
        raise ValueError("Error: Audio file is completely silent.")
        
    baseline_rms = 10 ** (baseline_dbfs / 20.0)
    baseline_data = clean_data * (baseline_rms / current_rms)
    
    print(f"Starting increment generation from {baseline_dbfs} dBFS to {max_dbfs} dBFS...\n")
        
    # 5. THE LOOP: Generate each increment step-by-step
    for target_db in range(baseline_dbfs, max_dbfs + 1):
        
        # Calculate multiplier relative to the baseline
        db_difference = target_db - baseline_dbfs
        step_multiplier = 10 ** (db_difference / 20.0)
        
        # Apply volume increase for this specific loop iteration
        step_data = baseline_data * step_multiplier
        
        # 6. Conditional Check: Will THIS specific volume level cause static?
        highest_peak = np.max(np.abs(step_data))
        
        if highest_peak > 1.0:
            print(f"[{target_db} dBFS] Warning: Peak at {highest_peak:.2f}. Applying Soft-Clipping.")
            # Apply mathematical curve to smooth the peaks
            final_data = np.tanh(step_data)
        else:
            print(f"[{target_db} dBFS] Safe: Peak at {highest_peak:.2f}. Passing cleanly.")
            # Leave the soundwave completely intact
            final_data = step_data
            
        # 7. Convert back to original format and Export
        if original_dtype == np.int16:
            # Scale back to 16-bit limits and apply hard safety clip
            safe_clipped = np.clip(final_data * 32768.0, -32768.0, 32767.0)
            final_output = safe_clipped.astype(np.int16)
        else:
            safe_clipped = np.clip(final_data, -1.0, 1.0)
            final_output = safe_clipped.astype(original_dtype)
            
        # Export the file
        output_name = f"{target_wavfileSTR[0:-4]}_{target_db}dBFS.wav"  #target_wavfileSTR[0:-4]= exclude the .wav string in btw
        wavfile.write(results_data_path / Path(output_name), sample_rate, step_data.astype(np.int16))
        
    print("\n--- Processing Complete ---")
    