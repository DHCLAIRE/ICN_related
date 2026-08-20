#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# To Change the backend setting to PTB for millisecond-accurate audio timing
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

import os
import csv
import scipy
from scipy.io import wavfile
import numpy as np
from datetime import datetime, date
import json
import pandas as pd
import random

# Import PsychoPy modules (must come after setting prefs)
import psychtoolbox as ptb
from psychopy import sound, core, visual, event, gui, monitors, clock, parallel

print(f"[AUDIO BACKEND] Using sound library: {sound.Sound}")

# =============================================================================
# 1. CUSTOM EXCEPTION & DUMMY PORT
# =============================================================================

class ExitProcedureException(Exception):
    """Custom exception raised to cleanly exit the listening procedure."""
    pass

class DummyParallelPort:
    """
    A mock parallel port for testing without MEG hardware. 
    Prints TTL trigger codes to the console instead of sending hardware signals.
    """
    def __init__(self):
        print("[HARDWARE] Running in Test Mode: Using DummyParallelPort.")

    def setData(self, code):
        if code != 0:
            print(f"   >>> [MOCK MEG TRIGGER] TTL Code Sent: {code}")

# =============================================================================
# 2. HELPER FUNCTIONS
# =============================================================================

def display_ins(win, text_str, key_list=None):
    """Displays instructions on screen and waits for a specific keypress."""
    screens = text_str.split("\\\\")
    for t in screens:
        stim = visual.TextStim(win=win, text=t, height=0.08, wrapWidth=1.5)
        stim.draw()
        win.flip()
        event.waitKeys(keyList=key_list)
        win.flip()


def display_fix(win, duration=None):
    """Displays a central fixation cross."""
    fixation = visual.TextStim(win=win, text="+", height=0.15)
    fixation.draw()
    win.flip()
    if duration is not None:
        core.wait(duration)
        win.flip()


def play_audio_trial(file_name, port, writer=None, trial_info=None, 
                     onset_code=2, offset_code=4, data_path="", max_duration=None):
    """
    Universal audio player: Plays ANY .wav file, sends MEG TTL triggers via 
    parallel port, checks for ESC to abort, and logs trial details to CSV.
    """
    full_path = os.path.join(data_path, file_name)
    
    # --- SAFETY CHECK ---
    if not os.path.exists(full_path):
        raise FileNotFoundError(
            f"\n[ERROR] Could not find audio file at:\n   -> '{full_path}'\n"
            f"Please check your audio folder path and filename."
        )
    # --------------------
    
    # 1. Read exact audio duration
    sample_rate, data = wavfile.read(full_path)
    file_duration = len(data) / sample_rate
    
    # Determine actual playback duration
    if max_duration is not None and max_duration < file_duration:
        duration_sec = max_duration
        print(f"\n--- Playing: {file_name} (Custom Cutoff: {duration_sec:.2f}s / Total: {file_duration:.2f}s) ---")
    else:
        duration_sec = file_duration
        print(f"\n--- Playing: {file_name} (Full Duration: {duration_sec:.2f}s) ---")
    
    # Auto-convert mono to stereo to prevent PTB errors
    if data.ndim == 1:
        data = np.column_stack((data, data))
        
    # 2. Load sound stimulus
    script_sound = sound.Sound(full_path, stereo=True)  #value=data, sampleRate=sample_rate
    
    # 3. ONSET TRIGGER & PLAYBACK
    script_sound.play()
    port.setData(onset_code)
    core.wait(0.01)  # 10 ms pulse width for MEG acquisition system
    port.setData(0)
    
    # 4. Active listening loop (checks ESC key every 10 ms)
    timer = core.Clock()
    while timer.getTime() < duration_sec:
        keys = event.getKeys(keyList=['escape'])
        if 'escape' in keys:
            script_sound.stop()
            port.setData(99)  # Abort trigger code sent to MEG
            core.wait(0.01)
            port.setData(0)
            raise ExitProcedureException(f"Experiment aborted by user during {file_name}")
        
        core.wait(0.01)
        
    # Stop audio early if cut off by max_duration
    script_sound.stop()
    
    # 5. OFFSET TRIGGER
    port.setData(offset_code)
    core.wait(0.01)  # 10 ms pulse width
    port.setData(0)
    
    print(f"{file_name} DONE.")
    
    # 6. Log completion to CSV
    if writer and trial_info is not None:
        writer.writerow(trial_info + [file_name, round(duration_sec, 4), "DONE"])
    
    core.wait(0.5)  # Brief Inter-Trial Interval (ITI)


# =============================================================================
# 3. DIRECT EXPERIMENT EXECUTION (ONE TAPE = ONE BLOCK)
# =============================================================================

if __name__ == "__main__":
    
    # --- 1. EXPERIMENT SETTINGS ---
    sub_id = "999"
    order_type = "Type A"                 # 'Type A' through 'Type F'
    languages = ["CHT", "ENG", "FRN"]     # Index 0 = L1, Index 1 = L2, Index 2 = L3
    
    # Use 'r' before the string to safely handle Windows backslashes!
    results_data_path = r"F:\LPP_Materials" 
    
    # --- 2. HARDWARE INITIALIZATION ---
    win = visual.Window(size=[500, 500], units="norm", fullscr=False)
    
    # Standard parallel port hardware address (e.g., 0x0378, 0x4FF8)
    # If testing without the MEG connected, use DummyParallelPort() instead.
    meg_port = parallel.ParallelPort(address=0x4FF8)  
    
    # --- 3. MAP COUNTERBALANCED LANGUAGE ORDER & CREATE PLAYLIST ---
    order_map = {
        "Type A": [languages[0], languages[1], languages[2]],  # L1-L2-L3
        "Type B": [languages[0], languages[2], languages[1]],  # L1-L3-L2
        "Type C": [languages[1], languages[0], languages[2]],  # L2-L1-L3
        "Type D": [languages[1], languages[2], languages[0]],  # L2-L3-L1
        "Type E": [languages[2], languages[0], languages[1]],  # L3-L1-L2
        "Type F": [languages[2], languages[1], languages[0]]   # L3-L2-L1
    }
    
    if order_type not in order_map:
        raise ValueError(f"Invalid order_type '{order_type}'. Must be: {list(order_map.keys())}")
        
    selected_langs = order_map[order_type]
    
    # Build a linear playlist of 9 tapes (One tape per block)
    playlist = []
    for tape_num in range(1, 4):  # Tapes 1, 2, 3 -> L1
        playlist.append((selected_langs[0], tape_num))
    for tape_num in range(4, 7):  # Tapes 4, 5, 6 -> L2
        playlist.append((selected_langs[1], tape_num))
    for tape_num in range(7, 10): # Tapes 7, 8, 9 -> L3
        playlist.append((selected_langs[2], tape_num))
        
    # --- 4. PREPARE CSV LOG FILE ---
    clean_type = order_type.replace(" ", "")
    csv_name = f"LPP_S{sub_id}{clean_type}_{selected_langs[0]}_{selected_langs[1]}_{selected_langs[2]}.csv"
    log_filename = os.path.join(results_data_path, csv_name)
    
    if not os.path.exists(results_data_path):
        os.makedirs(results_data_path, exist_ok=True)
        
    # --- 5. MAIN EXPERIMENT LOOP ---
    try:
        with open(log_filename, mode='w', newline='', encoding='utf-8') as log_file:
            writer = csv.writer(log_file)
            writer.writerow(["sub_id", "order_type", "language", "stim_type", "item_num", 
                             "filename", "duration_sec", "status"])
            
            # Initial Experiment Welcome Screen
            display_ins(win, "Welcome to the Listening Experiment.\\\\Press SPACE to begin.", ['space'])
            
            # Iterate through the playlist (9 blocks total)
            for block_idx, (lang, tape_num) in enumerate(playlist, start=1):
                
                # Instruction screen for each individual tape
                display_ins(
                    win, 
                    f"Block {block_idx} of 9 ({lang}).\\\\Listen carefully to the story.\\\\Press SPACE when ready.", 
                    ['space']
                )
                
                # Show Fixation cross before story starts (1 second)
                display_fix(win, duration=1.0)
                
                # ---------------------------------------------------------
                # A. PLAY STORY TAPE
                # ---------------------------------------------------------
                tape_file = f"LPP_{lang}_tape_{tape_num}.wav"
                play_audio_trial(
                    file_name=tape_file,
                    port=meg_port,
                    writer=writer,
                    trial_info=[sub_id, order_type, lang, "StoryTape", tape_num],
                    onset_code=10 + tape_num,
                    offset_code=50 + tape_num,
                    data_path=results_data_path,
                    max_duration=20.0  # Cut off at 60 seconds
                )
                
                # ---------------------------------------------------------
                # B. PLAY COMPREHENSION QUESTION (Optional/Commented Out)
                # ---------------------------------------------------------
                """
                question_file = f"LPP_{lang}_question_{tape_num}.wav"
                play_audio_trial(
                    file_name=question_file,
                    port=meg_port,
                    writer=writer,
                    trial_info=[sub_id, order_type, lang, "ComprehensionQ", tape_num],
                    onset_code=100 + tape_num,
                    offset_code=150 + tape_num,
                    data_path=results_data_path,
                    max_duration=30.0
                )
                """
                
                # Short pause before moving to the next block
                core.wait(5.0)
                
            # Completion Screen
            display_ins(win, "You have completed the experiment!\\\\Thank you for your participation.", ['space'])
            print(f"\nAll 9 tapes completed successfully! Log saved to: {log_filename}")
            
    except ExitProcedureException as e:
        print(f"\n[ABORTED]: {e}")
        print(f"Data saved up to abort point in: {log_filename}")
        display_ins(win, "Experiment aborted by user.", ['space'])
        
    finally:
        win.close()
        core.quit()