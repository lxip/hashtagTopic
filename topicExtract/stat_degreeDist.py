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
from itertools import islice,combinations  
from scipy.optimize import curve_fit 
from subprocess import check_output 
from collections import Counter
import matplotlib.pyplot as plt
import bltools as blt 
from bltools.plots import *

def getFilename(filedate):
    """Return filename in certain directory."""
    filename = check_output('find ./data_network -type f -name "{}_fw*"'.format(filedate),shell=True)
    return filename

def fitfunc(x,a,b):
    """return a linear function"""
    # return a * x + b 
    return a * x + b

def ccdf(data):
    """compute the cumulative distribution for plotting, P(X>=x)"""
    ccdf  = 1-1.0*np.arange(len(data))/len(data)
    return ccdf

def ccdf_p(Nx):
    """Return P(X>=x)"""
    N = len(Nx)
    S = 1.0*np.sum(Nx)
    Y = [ np.sum(Nx[i+1:]/S) for i in range(N) ]
    return Y

def powerlaw(Nx):
    Sn = np.sum(Nx)
    Px = [ 1.0*Nx[i]/Sn for i in range(len(Nx))]
    return Px


def expfunc(x,a,b):
    """return a exponential function"""
    return b * np.power(x,a) 

if __name__ == '__main__':
    start_time = time.time()

    storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/tagPerDay/'

    filedates = ['2016-11-08','2016-11-09','2016-11-15']
    degreeC4pl = {}
    degree4pl  = {}
    # degreeC4ccdf = {}
    # degree4ccdf  = {}
    for filedate in filedates:
        # filename = storePath + filedate + '_hashtag.json.gz' #filename to get all pairs of edges
        networkfile = getFilename(filedate).decode("utf-8").strip()
        print(filedate)
        G = nx.read_graphml(networkfile)
        print('Network density: {:.8f}.'.format(nx.density(G)))
        degree_sequence = sorted(G.degree().values(),reverse=True)
        print('Max degree in this network is {}.'.format(max(degree_sequence)) )

        degree_count = Counter(degree_sequence)
        degree,count = zip(*degree_count.most_common())

        degreeC4pl[filedate] = count
        degree4pl [filedate] = degree

        # sorted_degree_count = sorted(degree_count.items(), key=operator.itemgetter(0),reverse=True)
        # degree,count = zip(*sorted_degree_count)

        # degreeC4ccdf[filedate] = count
        # degree4ccdf [filedate] = degree

    popt = []
    pcov = []
    for i in range(len(filedates)):
        # rank = np.arange(1,len(degreeC4pl[filedates[i]])+1,1)
        # log_rank  = np.log10(rank)
        log_degree = np.log10(degree4pl[filedates[i]])
        log_count = np.log10(degreeC4pl[filedates[i]])
        # pt, pv = curve_fit(fitfunc, log_rank[1:], log_count[1:])
        pt, pv = curve_fit(fitfunc, log_degree, log_count)
        popt.append(pt)
        pcov.append(pv)

    ppt = []
    pov = []
    for i in range(len(filedates)):
        rank = np.arange(1,len(degreeC4pl[filedates[i]])+1,1)
        log_rank  = np.log10(rank)
        log_count = np.log10(degreeC4pl[filedates[i]])
        pt, pv = curve_fit(fitfunc, log_rank[1:], log_count[1:])
        ppt.append(pt)
        pov.append(pv)


    # degree distribution plot
    fg,ax = subplots_1x3()
    letter_subplots(ax)

    plt.sca(ax[0])
    for i in range(len(filedates)):
        plt.plot(degree4pl[filedates[i]],ccdf_p(degreeC4pl[filedates[i]]),'.',label=filedates[i])
    label_axes("degree",r'$P_{\geq}$')
    # ax[0].set(xscale='log',yscale='log')
    plt.legend(loc=3)
    plt.tight_layout()

    plt.sca(ax[1])
    for i in range(len(filedates)):
        Pdegree = powerlaw(degreeC4pl[filedates[i]])
        plt.plot(degree4pl[filedates[i]],Pdegree,'.',markersize=8,label=filedates[i])
        # rank = np.arange(1,len(degreeC4pl[filedates[i]])+1,1)
        # plt.plot(rank,degreeC4pl[filedates[i]],'.',markersize=8,label=filedates[i])
    plt.plot(degree4pl[filedates[i]],expfunc(degree4pl[filedates[i]],popt[2][0]-.4,popt[2][1]/8),'k-',
             label='$P(n_k) \propto k^{{{:.4f}}}$'.format(popt[2][0]-.4))
    label_axes(r'node degree $k$',r'$P(n_k)$')
    ax[1].set(xscale='log',yscale='log')
    plt.legend()
    plt.tight_layout()
    

    plt.sca(ax[2])
    for i in range(len(filedates)):
        # Pdegree = powerlaw(degreeC4pl[filedates[i]])
        # plt.plot(degree4pl[filedates[i]],Pdegree,'.',markersize=8,label=filedates[i])
        rank = np.arange(1,len(degreeC4pl[filedates[i]])+1,1)
        plt.plot(rank,degreeC4pl[filedates[i]],'.',markersize=8,label=filedates[i])
    plt.plot(degree4pl[filedates[i]],expfunc(degree4pl[filedates[i]],ppt[2][0]-.4,ppt[2][1]/8),'k-',
             label='$ S_n_k \propto r^{{{:.4f}}}$'.format(ppt[2][0]-.4))
    label_axes(r'rank $r_n_k$',r'Size of degree$S_n_k$')
    ax[2].set(xscale='log',yscale='log')
    plt.legend()
    plt.tight_layout()
    plt.show()

    fg.savefig('./fig/degreeDist_add.pdf')


    
    elp_time = (time.time() - start_time)
    print("FINISHED in {:.2f} seconds.".format(elp_time) )



####### OUTPUT ########
##### WITH WORD FILTER
# 2016-11-08
# Network density: 0.00001026.
# Max degree in this network is 3630.
# 2016-11-09
# Network density: 0.00001092.
# Max degree in this network is 3964.
# 2016-11-15
# Network density: 0.00001134.
# Max degree in this network is 492.

##### WITHOUT FILTER
# 2016-11-08
# Network density: 0.00000836.
# Max degree in this network is 3583.
# 2016-11-09
# Network density: 0.00000881.
# Max degree in this network is 3952.
# 2016-11-15
# Network density: 0.00000904.
# Max degree in this network is 488.





