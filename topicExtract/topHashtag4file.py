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
from collections import Counter, OrderedDict
from subprocess import check_output
from collections import Counter
from scipy.misc import comb
import bltools as blt 


def count_lines(filepath):
    """Return number of lines in file given the full file path."""
    num_lines = int(check_output('gzip -cd %s|wc -l'%filepath,shell=True))
    return num_lines

def isascii(s): 
    return len(s) == len(s.encode())

if __name__ == '__main__':
    start_time = time.time()

    storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/tagPerDay/'
    # storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/tagPerDayfilter/'



#### test I: top hashtags within one day
    hashtag2count_list = []

    filedates = ['2016-11-07','2016-11-08','2016-11-09','2016-11-10','2016-11-11',
                 '2016-11-12','2016-11-13','2016-11-14','2016-11-15']
    for filedate in filedates:
        filename = storePath + filedate + '_hashtag.json.gz'
        # filename = storePath + filedate+'_hashtagF.json.gz'
        tweetNum = count_lines(filename)
        print(tweetNum)

        with gzip.open(filename,'rt') as fin:
            for linejson in fin:
                line = json.loads(linejson)


                ######## 1. count hashtag frequency without filter ########
                for tag in line['hashtags']:
                    if isascii(tag): # filter non-English hashtags
                        hashtag2count_list.append(tag)

                # ######## 2. count hashtag frequency with word filter ########
                # if not set(line['hashtags'])&badWords:
                #     tweetwords = set(line['text'].strip().split())
                #     if not tweetwords&badWords:
                #     if set(line['hashtags'])&set(tophashtag): 

        hashtag2count = Counter(hashtag2count_list)
        with open('./data_tag2count/{}_{}tweets_h2cEn.txt'.format(filedate,tweetNum),'wt') as f:
            for hashtag, count in hashtag2count.most_common():
                f.write('{} {}\n'.format(hashtag,count))
        f.close()


    elp_time = (time.time() - start_time)
    print("FINISHED in {:.2f} seconds.".format(elp_time) )





