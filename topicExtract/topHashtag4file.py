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

def isascii(s): 
    return len(s) == len(s.encode())

if __name__ == '__main__':
    start_time = time.time()

    # storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/hashtagStore/'
    storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/tagPerDay/'
    # storePath = os.environ['BL_DATASTORE_DIR']+'/csys300/tagPerDayfilter/'

# ########### process a certain time period
#     startT   = '2016-11-08-00-00'
#     endT     = '2016-11-08-03-00'
#     num4files = get_num4files(startT,endT)
#     filenames = [get_filename(startT,storePath)]
#     for i in range(num4files-1):
#         nextT = get_timestamp(startT)
#         filenames.append( get_filename(nextT,storePath) )
#         startT = nextT
#     print('%s FILES TO PROCESS.'%len(filenames)) 


# ########### read files and get information
#     badWords = set()
#     with open('badLang.txt','rt') as f:
#         for line in f:
#             badWords.update(line.strip().split())
#     f.close()

#### test 1: top hashtags within one day
    hashtag2count_dic = {}
    hashtag2count_list = []
    hashtag2neighbor = {'hashtag':{},'tweet':[]}
    tophashtagtweet = []

    filedate = '2016-11-08'
    # filedates = ['2016-11-07','2016-11-08','2016-11-09','2016-11-10','2016-11-11',
                # '2016-11-12','2016-11-13','2016-11-14','2016-11-15']
    # for filedate in filedates:
        # filename = storePath + filedate + '_hashtag.json.gz'
        # filename = storePath + filedate+'_hashtagF.json.gz'
    filename = storePath + filedate+'_hashtag.json.gz'

    # for ind,file in enumerate(filenames):
        # print(ind,file[-33:])
    tweetNum = count_lines(filename)
        # tweetNum = count_lines(filename)
    print(tweetNum)
        # dateTime = file[:16]

        # try:
    with gzip.open(filename,'rt') as fin:
    # with gzip.open(filename,'rt') as fin:
        for linejson in fin:
            line = json.loads(linejson)


            ########1. count hashtag frequency without filter ########
            for tag in line['hashtags']:
                if isascii(tag):
                hashtag2count_list.append(tag)
                try:
                    hashtag2count_dic[tag] += 1 
                except KeyError:
                    hashtag2count_dic[tag] = 1

                # ########2. count hashtag frequency with word filter ########
                # if not set(line['hashtags'])&badWords:
                #     tweetwords = set(line['text'].strip().split())
                #     if not tweetwords&badWords:
                #     if set(line['hashtags'])&set(tophashtag): 




    hashtag2count = Counter(hashtag2count_list)
    with open('./data_tag2count/{}_{}tweets_hashtag2count.txt'.format(filedate,tweetNum),'wt') as f:
        for hashtag, count in hashtag2count.most_common():
            f.write('{} {}\n'.format(hashtag,count))
    f.close()



                    

                    # for h in tophashtag:
                    #     if h in line['hashtags']:
                    #         try:
                    #             hashtag2neighbor['hashtag'][h].extend(line['hashtags'].remove(h)) 
                    #         except KeyError:
                    #             hashtag2neighbor['hashtag'][h] = []
                    #         # try:
                    #         hashtag2neighbor['tweet'].append(line['text'])
                                    # except KeyError:
                                    #     hashtag2neighbor['tweet'] = [line['text']]
        # except FileNotFoundError:
        #     continue


    
    elp_time = (time.time() - start_time)
    print("FINISHED in {:.2f} seconds.".format(elp_time) )





