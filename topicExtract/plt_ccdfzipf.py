#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors: Xipei Liu

Purpose: Code up rich-gets-richer problem.
         The Random Competitive Replication.        

Inputs: None

Outputs: None
"""

import warnings
warnings.filterwarnings("ignore")
import sys, os
import time
import gzip
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from collections import Counter
from bltools.plots import *


def fitfunc(x,a,b):
    """return a linear function"""
    # return a * x + b 
    return a * x + b 

def expfunc(x,a,b):
    """return a exponential function"""
    return b * np.power(x,a) 


def RCR(T,rho):
    """Perform the action of RCR
    population is a dictionary storing the item and """
    population = [1]
    t = 1
    while t<T:
        if random.random()<rho:
            population.append(population[-1]+1)
        else:
            # oldelem = np.floor(np.mean([random.sample(dpopulation, 1)[0] for i in range(10)]))
            oldelem = random.sample(population,1)
            population = oldelem + population
        t += 1
    freq = Counter(population)
    for item in freq:
        rank = list(freq.keys())
        size = list(freq.values())
        size.sort(reverse=True)
        rank.sort()
    # ki = []
    # Nk = []
    # ki_Nk = Counter(size)
    # for item in ki_Nk:
    #     ki.append(item)
    #     Nk.append(ki_Nk[item])
    # Pk = 1.0*np.array(ki)*np.array(Nk)/T
    # nk = Pk/np.array(ki)
    return rank,size



if __name__ == '__main__':
    start_time = time.time()
    # rhos  = [0.1,0.01,0.001]
    rhos  = [0.01]
    # Nruns = [10**5,10**7,10**8]
    # Nruns = [10**7]

    # fg,ax = plt.subplots(1,3)

    # for i,rho in enumerate(rhos):
    #     print('Strat...')
    #     rank = []
    #     with open('./rank3.txt','rt') as f:
    #         for line in f:
    #             rank.append(int(line.strip()))
    #     f.close()
    #     size = []
    #     with open('./size3.txt','rt') as f:
    #         for line in f:
    #             try:
    #                 size.append(int(line.strip())) 
    #             except ValueError:
    #                 pass
    #     f.close()
        # size.append(1734338)
        # size.append(98903117)
        # size.append(8864376)

    rho = 0.118
    size = []
    with open('./ulysses.txt','rt') as f:
        for line in f:
            w,c = line.strip().split(': ')
            size.append(int(c))
    size.sort(reverse=True)
    rank = np.arange(1,len(size)+1,1)
        # rank.sort() 
        # rank, size = RCR(Nruns[i],rho)
        # print('Sampled...')
        # popt, pcov = curve_fit(exp_fit, rank, size)
    log_rank = np.log10(rank)
    log_size = np.log10(size)

    popt, pcov = curve_fit(fitfunc, log_rank[1:], log_size[1:])
    # popt, pcov = curve_fit(expfunc, rank[1:], size[1:])
 
    print(pcov)

    # popt[0] = -0.99494575
    popt[0] = -0.98514575
    popt[1] = 4.92273101
    print(popt)
    fg,ax = plt.subplots()
    plt.sca(ax)
    plt.plot(rank[0],size[0],'r.',markersize=15)
    plt.plot(rank[1:],size[1:],'r.')
    plt.plot(rank[1:],expfunc(rank[1:],popt[0],10**popt[1]),'b-',
             label='$\\rho={}$\n$S_n \propto n^{{{:.4f}}}$'.format(rho,popt[0]))
    plt.legend(loc=3)
    ax.set_xlim([1,1.5*10**5])
    ax.set(xscale='log',yscale='log')
    label_axes("$log_{10}$ group rank $n$","$log_{10}$ group size $S_n$")
    plt.tight_layout()
    # fg.savefig ('./RCR{}.jpg'.format(i+3),dpi=300)
    fg.savefig ('./uly.jpg',dpi=300)

        


    
    print("FINISHED in {:.2f} seconds.".format((time.time() - start_time)) )
