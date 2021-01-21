#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 15:53:33 2021

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
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram

params = yaml.safe_load(open('params.yaml'))
    
features = params['analyze']['dendogram']
f0 = features[0]
f1 = features[1]
i = params['prepare']['subject']
subject = pd.read_csv('data/prepared/subject{}.csv'.format(i))

os.makedirs(os.path.join('data', 'dendograms', 'Subject{}'.format(i)), exist_ok=True)

def makeDendogram(subject, f0, f1):
    fig = plt.figure()
    actlabels = pd.Categorical(subject['activity'])
    distanceMatrix = pdist(subject.iloc[:,f0:f1])
    dendrogram(linkage(distanceMatrix, method='complete'), 
               color_threshold=0.3, 
               leaf_label_func=lambda x: 'O' * (actlabels.codes[x] + 1),
               leaf_font_size=6)
    
    fig.set_size_inches(8, 4);
    fig.savefig(os.path.join('data','dendograms','Subject{}'.format(i),'Dendogram{}-{}.png'.format(f0,f1)))

makeDendogram(subject, f0, f1)