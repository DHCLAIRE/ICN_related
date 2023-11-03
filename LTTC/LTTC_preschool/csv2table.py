#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""#!/usr/bin/python
# textgrid2csv.py
# D. Gibbon
# 2016-03-15
# 2016-03-15 (V02, includes filename in CSV records)
"""
#-------------------------------------------------
# Import modules

import sys, re

from pprint import pprint
import csv
import json
import random
from random import sample
import os
#from gtts import gTTS
import pandas as pd
import time
from pathlib import Path
#import nltk
#import re
#from nltk import sent_tokenize
#from nltk import tokenize
#-------------------------------------------------
# Text file input / output