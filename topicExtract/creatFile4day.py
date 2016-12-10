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
import sys,os
import gzip
import time
import datetime as dt
import ujson as json
import networkx as nx
from subprocess import check_output
from collections import Counter
import bltools as blt 

def get_timestamp(start):
    """Return timestamp from start point to after 15min,
    format in %Y-%m-%d-%H-%M"""
    start_dt = dt.datetime.strptime(start,'%Y-%m-%d-%H-%M')
    end_dt   = start_dt + dt.timedelta(minutes=15)
    end      = dt.datetime.strftime(end_dt,'%Y-%m-%d-%H-%M')
    return end

def get_num4files(start,end):
    """Return number of files from start time to end time in 15min interval."""
    start_dt = dt.datetime.strptime(start,'%Y-%m-%d-%H-%M')
    end_dt   = dt.datetime.strptime(end,  '%Y-%m-%d-%H-%M')
    num4files = ((end_dt - start_dt).total_seconds())/60/15
    return int(num4files)

def get_filename(timestamp,p):
    """Return file name in format."""
    return p+timestamp+'_hashtags.json.gz'

def count_lines(filepath):
    """Return number of lines in file given the full file path."""
    num_lines = int(check_output('gzip -cd %s|wc -l'%filepath,shell=True))
    return num_lines

if __name__ == '__main__':
    start_time = time.time()

    storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/hashtagStorefilter/'
    savePath  = os.environ['BL_DATASTORE_DIR']+'/csys300/tagPerDayfilter/' 
    # storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/hashtagStore/'
    # savePath  = os.environ['BL_DATASTORE_DIR']+'/csys300/tagPerDay/' 

########### process a certain time period

    # dateS = ['2016-11-12-00-00','2016-11-13-00-00','2016-11-14-00-00','2016-11-15-00-00']
    # dateE = ['2016-11-13-00-00','2016-11-14-00-00','2016-11-15-00-00','2016-11-16-00-00']
    # for i in range(len(dateS)):
    #     startT = dateS[i]
    #     endT = dateE[i]
    startT   = '2016-11-07-00-00'
    endT     = '2016-11-07-03-00'
    num4files = get_num4files(startT,endT)
    filenames = [get_filename(startT,storePath)]
    for i in range(num4files-1):
        nextT = get_timestamp(startT)
        filenames.append( get_filename(nextT,storePath) )
        startT = nextT
    print('%s FILES TO PROCESS.'%len(filenames)) 

    saveT = startT[:10]
    fout = gzip.open(savePath+saveT+'_test.json.gz','wt')
    for ind,file in enumerate(filenames):
        # print(ind,file[-33:])
        tweetNum = count_lines(file)
        dateTime = file[:16]

        try:
            with gzip.open(file,'rt') as fin:
                for linejson in fin:
                    line = json.loads(linejson)
                    json.dump(line, fout)
                    fout.write('\n')
        except FileNotFoundError:
            continue
    fout.close() 

    elp_time = (time.time() - start_time)
    print("FINISHED in {:.2f} seconds.".format(elp_time) )
