#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:10:45 2021

@author: luca
"""

import io
import sys
import re
import os
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

params = yaml.safe_load(open('params.yaml'))


features = params['analyze']['features']
f0 = features[0]
f1 = features[1]
i = params['prepare']['subject']

subject = pd.read_csv('data/prepared/subject{}.csv'.format(i))

numericActivity = subject.groupby('activity')
os.makedirs(os.path.join('data', 'analysis', 'Subject{}'.format(i)), exist_ok=True)

cols = {'laying' : 'b',
        'sitting' : 'g',
        'standing' : 'r',
        'walk' : 'c',
        'walkdown' : 'm',
        'walkup' : 'y'}

f, (ax1, ax2) = plt.subplots(ncols=2)
f.set_size_inches(10, 5)

for act, df in numericActivity:
    ax1.scatter(df.index, df.iloc[:,f0], c=cols[act], label=act)
    ax2.scatter(df.index, df.iloc[:,f1], c=cols[act], label=act)

ax1.set_ylabel(subject.columns[features[0]])
ax2.set_ylabel(subject.columns[features[1]])
ax2.legend(loc='lower right')

f.tight_layout();
f.savefig(os.path.join('data','analysis','Subject{}'.format(i),'Feature{}-{}.png'.format(f0,f1)))

