# To Change the backend setting to PTB
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB', 'pyo', 'pygame']

# Set other python packages
import psychtoolbox as ptb
from psychopy import sound, core, visual, event, gui, monitors, clock, parallel
print(sound.Sound)

import os
import csv
import scipy
from scipy.io import wavfile
import numpy as np
from datetime import datetime, date
import json
import pandas as pd
import random

# =============================================================================
# 1. CUSTOM EXCEPTION & DUMMY PORT FOR MACBOOK TESTING
# =============================================================================

class ExitProcedureException(Exception):
    """Custom exception raised to cleanly exit the listening procedure."""
    pass


class DummyParallelPort:
    """
    A mock parallel port for macOS testing. 
    Prints TTL trigger codes to the console instead of sending hardware signals.
    """
    def __init__(self):
        print("[HARDWARE] Running in macOS Test Mode: Using DummyParallelPort.")

    def setData(self, code):
        if code != 0:  # Avoid cluttering console with zero/reset pulses
            print(f"   >>> [MOCK MEG TRIGGER] TTL Code Sent: {code}")


# =============================================================================
# 2. HELPER FUNCTIONS
# =============================================================================

def display_ins(win, text_str, key_list=None):
    """Displays instructions and waits for a keypress."""
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
                     onset_code=2, offset_code=4, data_path=""):
    """
    Universal audio player: Plays ANY .wav file, sends MEG TTL triggers 
    (or prints to console), checks for ESC to abort, and logs data to CSV.
    """
    full_path = os.path.join(data_path, file_name)
    
    # --- SAFETY CHECK ---
    if not os.path.exists(full_path):
        raise FileNotFoundError(
            f"\n[ERROR] Could not find audio file at:\n   -> '{full_path}'\n"
            f"Please check that your external drive is plugged in and the folder name is correct."
        )
    # --------------------
    
    # 1. Read exact duration
    sample_rate, data = wavfile.read(full_path)
    duration_sec = len(data) / sample_rate
    print(f"\n--- Playing: {file_name} (Duration: {duration_sec:.2f}s) ---")
    
    # 2. Load sound
    script_sound = sound.Sound(full_path)
    
    # 3. Onset Trigger & Playback
    script_sound.play()
    port.setData(onset_code)
    core.wait(0.01)  # 10 ms TTL pulse
    port.setData(0)
    
    # 4. Active listening loop (checks ESC key every 10 ms)
    timer = core.Clock()
    while timer.getTime() < duration_sec:
        keys = event.getKeys(keyList=['escape'])
        if 'escape' in keys:
            script_sound.stop()
            port.setData(99)  # Abort trigger code
            core.wait(0.01)
            port.setData(0)
            raise ExitProcedureException(f"Experiment aborted by user during {file_name}")
        
        core.wait(0.01)
    
    # 5. Offset Trigger
    port.setData(offset_code)
    core.wait(0.01)
    port.setData(0)
    
    print(f"{file_name} DONE.")
    
    # 6. Log to CSV
    if writer and trial_info is not None:
        writer.writerow(trial_info + [file_name, round(duration_sec, 4), "DONE"])
    
    core.wait(0.5)  # Brief delay before next event


# =============================================================================
# 3. MASTER EXPERIMENT CONTROLLER
# =============================================================================

def run_meg_experiment(sub_id, order_type, win, port, 
                       languages=["CHT", "ENG", "FRN"], data_path=""):
    """
    Executes the full MEG experiment: displays instructions, plays tapes 
    followed by comprehension questions, and logs all events to one CSV file.
    """
    # Map counterbalanced orders (L1, L2, L3)
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
    
    # Assign Language Blocks -> (Language, Tape_Range)
    blocks = [
        (selected_langs[0], range(1, 4)),   # Block 1: Tapes 1 to 3
        (selected_langs[1], range(4, 7)),   # Block 2: Tapes 4 to 6
        (selected_langs[2], range(7, 10))   # Block 3: Tapes 7 to 9
    ]
    
    # Prepare single CSV log file inside your results folder
    clean_type = order_type.replace(" ", "")
    csv_name = f"LPP_S{sub_id}{clean_type}_{selected_langs[0]}_{selected_langs[1]}_{selected_langs[2]}.csv"
    log_filename = os.path.join(data_path, csv_name)
    
    try:
        with open(log_filename, mode='w', newline='', encoding='utf-8') as log_file:
            writer = csv.writer(log_file)
            # Unified CSV Headers for both Story Tapes & Comprehension Qs
            writer.writerow(["sub_id", "order_type", "language", "stim_type", "item_num", 
                             "filename", "duration_sec", "status"])
            
            # Initial Experiment Welcome Screen
            display_ins(win, "Welcome to the Listening Experiment.\\\\Press SPACE to begin.", ['space'])
            
            # --- MAIN EXPERIMENT LOOP ---
            for block_idx, (lang, tape_range) in enumerate(blocks, start=1):
                
                # Display block instructions before switching languages
                display_ins(
                    win, 
                    f"Block {block_idx} of 3 ({lang}).\\\\Listen carefully to the story.\\\\Press SPACE when ready.", 
                    ['space']
                )
                
                for tape_num in tape_range:
                    # Show Fixation cross before story starts (1 second)
                    display_fix(win, duration=1.0)
                    
                    # ---------------------------------------------------------
                    # A. PLAY STORY TAPE
                    # ---------------------------------------------------------
                    tape_file = f"LPP_{lang}_tape_{tape_num}.wav"
                    play_audio_trial(
                        file_name=tape_file,
                        port=port,
                        writer=writer,
                        trial_info=[sub_id, order_type, lang, "StoryTape", tape_num],
                        onset_code=10 + tape_num,   # Unique trigger per tape
                        offset_code=50 + tape_num,
                        data_path=data_path
                    )
                    
                    # ---------------------------------------------------------
                    # B. PLAY COMPREHENSION QUESTION
                    # ---------------------------------------------------------
                    question_file = f"LPP_{lang}_question_{tape_num}.wav"
                    play_audio_trial(
                        file_name=question_file,
                        port=port,
                        writer=writer,
                        trial_info=[sub_id, order_type, lang, "ComprehensionQ", tape_num],
                        onset_code=100 + tape_num,  # Unique trigger per question
                        offset_code=150 + tape_num,
                        data_path=data_path
                    )
                    
                    # Short pause between trials
                    core.wait(1.0)
                    
            # Completion Screen
            display_ins(win, "You have completed the experiment!\\\\Thank you for your participation.", ['space'])
            print(f"\nAll 9 tapes completed successfully! Log saved to: {log_filename}")
            
    except ExitProcedureException as e:
        print(f"\n[ABORTED]: {e}")
        print(f"Data saved up to abort point in: {log_filename}")
        display_ins(win, "Experiment aborted by user.", ['space'])


# =============================================================================
# 4. RUNNER EXECUTION (MACBOOK TEST MODE)
# =============================================================================

if __name__ == "__main__":
    
    # Set Data path (Make sure trailing slashes are present!)
    data_root_path = "/Volumes/DH_4GB/"
    results_data_path = "/Volumes/DH_4GB/LPP_Materials/"
    
    # Initialize PsychoPy Window
    win = visual.Window(size=[500, 500], units="norm", fullscr=False)
    
    # Use DummyParallelPort instead of real parallel hardware
    meg_port = DummyParallelPort()
    
    # Run Experiment (e.g., Sub '01', Type A order: CHT 1-3 -> ENG 4-6 -> FRN 7-9)
    run_meg_experiment(
        sub_id="01",
        order_type="Type A",
        win=win,
        port=meg_port,
        languages=["CHT", "ENG", "FRN"],
        data_path=results_data_path
    )
    
    win.close()
    core.quit()