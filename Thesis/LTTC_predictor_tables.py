#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pprint import pprint
import csv
import json
import random
from random import sample
import os
from gtts import gTTS
import pandas as pd
import time
from pathlib import Path

"""
# for audio file alternation
from scipy.io import wavfile
import scipy.signal
from pydub import AudioSegment
"""

if __name__ == "__main__":
    stim_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_material_2nd/2nd_Stim-Materials/"
    result_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_audio_behavioral/"
    text_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_material_2nd/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/"
    textSets_data_path = "/Volumes/Neurolang_1/Project_Assistant/2021_Ongoing/2020_LTTC/Experiment_materials/LTTC_material_2nd/2nd_Stim-Materials/USE_Output/LTTC_modifiedTexts_output/LTTC_TextSets/"

