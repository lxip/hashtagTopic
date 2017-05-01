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
    filename = check_output('find ./data_network -type f -name "{}_tag*"'.format(filedate),shell=True)
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
    
    fg,ax = subplots_1x2()
    letter_subplots(ax)

    for filedate in filedates:
        filename = getFilename(filedate).decode("utf-8").strip()
        # networkfile = getNetwork(filedate).decode("utf-8").strip()
        print(filedate)
        top20tagFreq = top20hashtags[filedate]
        top20tag = [i[0] for i in top20tagFreq]
        top20tagfreq = [i[1] for i in top20tagFreq]
        print(top20tagfreq)
        # G = nx.read_graphml(networkfile)
        with open(filename,'rt') as f:
            tagstudy = json.load(f)
        f.close()
        plt.sca(ax[0])
        plt.plot(top20tagfreq,[tagstudy[tag]['Wmean'] for tag in top20tag],'*-',label=filedate)
        plt.sca(ax[1])
        plt.plot(top20tagfreq,[tagstudy[tag]['degree'] for tag in top20tag],'o--',label=filedate)

    plt.sca(ax[0])
    label_axes('top 20 hashtag frequency','mean weight for neighbors')
    plt.legend()
    # ax[0].set_xticks(np.arange(1,21,1))
    ax[0].set_xlim([10**2.7,10**4.6])
    ax[0].set_ylim([.5,4000])
    ax[0].set(xscale='log',yscale='log')
    # plt.setp(ax[0].get_xticklabels(), rotation=45)
    plt.legend(loc=1)
    plt.tight_layout()

    plt.sca(ax[1])
    label_axes('top 20 hashtag frequency','degree')
    plt.legend()
    # ax[1].set_xticks(np.arange(1,21,1))
    ax[1].set(xscale='log',yscale='log')
    ax[1].set_xlim([10**2.7,10**4.6])
    # plt.setp(ax[1].get_xticklabels(), rotation=45)
    plt.legend(loc=4)
    plt.tight_layout()

    fg.savefig('./fig/neighborDist.pdf')
    
    elp_time = (time.time() - start_time)
    print("FINISHED in {:.2f} seconds.".format(elp_time) )



####### OUTPUT ########






