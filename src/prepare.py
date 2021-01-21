#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 12:21:02 2021

@author: luca
"""

import io
import sys
import re
import os
import yaml
import pandas as pd
import numpy as np

params = yaml.safe_load(open('params.yaml'))['prepare']
os.makedirs(os.path.join('data', 'prepared'), exist_ok=True)

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython prepare.py data-file\n")
    sys.exit(1)
    
samsungData = pd.read_csv(sys.argv[1])
samsungData = samsungData.drop(['Unnamed: 0'], axis=1)

i = params['subject'] # number of the subject
subject = samsungData[samsungData['subject'] == i]

path = os.path.join('data','prepared','subject{}.csv'.format(i))
subject.to_csv(path, index=False)
