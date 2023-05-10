#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""This script estimates TRFs for IF & F0 models from emd and saves them"""
from pathlib import Path
import re

import eelbrain
import mne
import trftools
import emd

import numpy as np

if __name__ == "__main__":
    