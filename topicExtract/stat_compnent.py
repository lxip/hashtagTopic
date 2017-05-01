#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors: Xipei Liu

Purpose: Count the appearence of different hashtags in the input file, 
store information in a dictionary.

Inputs: $BL_DATASTORE_DIR/csys300/hashtagStore/{%Y-%m-%d-%H-%M}_hashtag_dic.json.gz 

Outputs: 
"""

import warnings
warnings.filterwarnings("ignore")
import sys,os,re
import gzip
import time
import datetime as dt
import ujson as json
import networkx as nx
import numpy as np 
import operator
import community 
from itertools import islice,combinations  
from scipy.optimize import curve_fit 
from subprocess import check_output 
from collections import Counter
import matplotlib.pyplot as plt
import bltools as blt 
from bltools.plots import *

def getFilename(filedate):
    """Return filename in certain directory."""
    filename = check_output('find ./data_tag2count -type f -name "{}*fword.*"'.format(filedate),shell=True)
    return filename

def getNetwork(filedate):
    """Return filename in certain directory."""
    filename = check_output('find ./data_network -type f -name "{}_fw*"'.format(filedate),shell=True)
    return filename



if __name__ == '__main__':
    start_time = time.time()

    with open('./data_tag2count/3daysTop20hashtags.json') as fo:
        top20hashtags = json.load(fo)
    fo.close()

    filedates = ['2016-11-08','2016-11-09','2016-11-15']
    
    for filedate in filedates:
        networkfile = getNetwork(filedate).decode("utf-8").strip()
        print(filedate)
        G = nx.read_graphml(networkfile)
        tagstudy = {}
        for tc in np.arange(len(top20hashtags[filedate])):
            tag,count = top20hashtags[filedate][tc]
            tagstudy[tag] = {'freq':int(count)}
            tagstudy[tag]['degree'] = G.degree(tag)
            neighbors = sorted(G[tag].items(), key=lambda edge: edge[1]['weight'],reverse=True)
            neighbors_list = [('a', node) for node, _metadata in neighbors]
            tag_list,neighbor_list = zip(*neighbors_list)
            tagstudy[tag]['top10neighbors'] = neighbor_list[:10]
            tagstudy[tag]['Wneighbors'] = [neighbors[i][1]['weight'] for i in range(len(neighbors))] #weight
            tagstudy[tag]['Wmean'] = np.median(tagstudy[tag]['Wneighbors'])

        with open('./data_network/{}_tagStudy.json'.format(filedate),'wt') as f:
            json.dump(tagstudy,f)
        f.close()


    
    elp_time = (time.time() - start_time)
    print("FINISHED in {:.2f} seconds.".format(elp_time) )



####### OUTPUT ########






