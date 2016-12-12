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
from itertools import islice,combinations   
from subprocess import check_output 
from collections import Counter
import bltools as blt 

def getFilename(filedate):
    """Return filename in certain directory."""
    filename = check_output('find ./data_tag2count -type f -name "{}*_fword.*"'.format(filedate),shell=True)
    return filename

def count_lines(filepath):
    """Return number of lines in file given the full file path."""
    num_lines = int(check_output('less %s|wc -l'%filepath,shell=True))
    return num_lines

def nodes_connected(u, v):
    return u in Ghashtag.neighbors(v)

if __name__ == '__main__':
    start_time = time.time()

    # storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/hashtagStore/'
    storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/tagPerDay/'
    # storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/tagPerDayfilter/'

    filedates = ['2016-11-15']#,'2016-11-08','2016-11-09','2016-11-10','2016-11-11',
                # '2016-11-12','2016-11-13','2016-11-14','2016-11-15']
    for filedate in filedates:
        # filename = storePath + filedate + '_hashtag.json.gz'
        # filename = storePath + filedate+'_hashtagF.json.gz'
        filename = storePath + filedate + '_hashtag.json.gz' #filename to get all pairs of edges


        #### A. read top 1% hashtags
        tophashtags = set()
        countFile2open = getFilename(filedate).decode("utf-8").strip()
        # print(countFile2open)
        countfileLines = count_lines(countFile2open)
        cutoff = int(1*countfileLines) #only see the top 0.05% hashtags
        print(cutoff)
        with open(countFile2open,'rt') as fi:
            for line in islice(fi,cutoff):
                tag,count = line.strip().split()
                tophashtags.add(tag)

        tweetNum = re.search('(?<=\_)\d+(?=tweets)',countFile2open).group()

        print('START BUILDING NETWORK...')

        Ghashtag = nx.Graph()
        with gzip.open(filename,'rt') as fin:
            for linejson in fin:
                line = json.loads(linejson)
                if tophashtags&set(line['hashtags']):
                    edges = list(combinations(line['hashtags'],2))
                    if len(edges):
                        for edge in edges:
                            if edge[1] in Ghashtag.node and edge[0] in Ghashtag.node: 
                                if nodes_connected(edge[0],edge[1]):
                                    Ghashtag[edge[0]][edge[1]]["weight"] = Ghashtag[edge[0]][edge[1]]["weight"]+1
                            else:
                                Ghashtag.add_edge(edge[0],edge[1],weight=1)
        print('FINISH BUILDING NETWORK...')
        nx.write_graphml(Ghashtag, "./data_network/{}_fword_network.graphml".format(filedate))


    
    elp_time = (time.time() - start_time)
    print("FINISHED in {:.2f} seconds.".format(elp_time) )





