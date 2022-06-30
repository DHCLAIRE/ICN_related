#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# for stimuli
from pprint import pprint
import csv
import json
import random
from random import sample
import numpy as np
from datetime import datetime,date
import pandas as pd
from collections import Counter
import statistics



import tkinter as tk




if __name__ == "__main__":
    window = tk.Tk()
    window.title('TESTING')  # The title for the windows
    window.geometry('700x600')   # the size of the windows
    window.resizable(True, True)   # whether the window could be zoom in or zoom out through x and y axis >> False, False means no in x and y axis 
    window.iconbitmap('icon.ico')
    window.mainloop()