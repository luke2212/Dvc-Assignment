#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 16:47:46 2021

@author: luca
"""
import io
import sys
import re
import yaml
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans, vq

params = yaml.safe_load(open('params.yaml'))

i = params['prepare']['subject']
subject = pd.read_csv('data/prepared/subject{}.csv'.format(i))
action = params['kmeans']['activity']

os.makedirs(os.path.join('data','kmeans','Subject%s' %i), exist_ok=True)

data = np.matrix(subject.iloc[:,:-2])
centers, _ = kmeans(data, 6, iter=100)
cluster, _ = vq(data, centers)

df = pd.crosstab(cluster, subject['activity'])

fig = plt.figure()
idmax = np.argmax(np.array(df[action]))
plt.plot(centers[idmax,:10], 'ok')
plt.ylabel('Cluster Center');
fig.savefig(os.path.join('data','kmeans','Subject{}'.format(i),'Kmeans{}.png'.format(action)))


