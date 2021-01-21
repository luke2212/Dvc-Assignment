#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 16:15:32 2021

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

i = params['prepare']['subject']
features = params['analyze']['dendogram']
f0 = features[0]
f1 = features[1]
    
subject = pd.read_csv('data/prepared/subject{}.csv'.format(i))
actlabels = pd.Categorical(subject['activity'])

os.makedirs(os.path.join('data', 'SVD', 'Subject{}'.format(i)), exist_ok=True)

def scale(matrix):
    return (matrix - np.mean(matrix, axis=0)) / np.std(matrix, axis=0)


U, D, Vt = np.linalg.svd(subject.iloc[:,:-2].apply(scale), full_matrices=False)

f, (ax1, ax2) = plt.subplots(ncols=2)
f.set_size_inches(10, 5)

for lb, cl in zip(list(actlabels.categories), 'b g r c m y k'.split()):
    idx = subject['activity'] == lb
    ax1.scatter(subject.index[idx], U[idx,0], c=cl, label=lb)
    ax2.scatter(subject.index[idx], U[idx,1], c=cl, label=lb)
    
ax1.set_ylabel('U[:,0]')
ax2.set_ylabel('U[:,1]')
ax2.legend(loc='lower right')

f.tight_layout();
f.savefig(os.path.join('data','SVD','Subject{}'.format(i),'SVD.png'))

fig = plt.figure()
maxContrib = np.argmax(Vt[1,:])

distanceMatrix = pdist(subject.take(list(range(f0,f1)) + [maxContrib], axis=1))
dendrogram(linkage(distanceMatrix, method='complete'), 
           color_threshold=0.3, 
           leaf_label_func=lambda x: 'O' * (actlabels.codes[x] + 1),
           leaf_font_size=6)
fig.set_size_inches(8, 4);
fig.savefig(os.path.join('data','SVD','Subject{}'.format(i),'Dendogram{}-{}.png'.format(f0,f1)))
