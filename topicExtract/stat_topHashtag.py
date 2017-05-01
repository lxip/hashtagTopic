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
import numpy as np 
import operator
from itertools import islice,combinations  
from subprocess import check_output 

def getFilename(filedate):
    """Return filename in certain directory."""
    filename = check_output('find ./data_tag2count -type f -name "{}*fword.*"'.format(filedate),shell=True)
    return filename


if __name__ == '__main__':
    start_time = time.time()

    filedates = ['2016-11-08','2016-11-09','2016-11-15']
    top20tags = {}
    for filedate in filedates:
        networkfile = getFilename(filedate).decode("utf-8").strip()
        print(filedate)
       
        tagfile = getFilename(filedate).decode("utf-8").strip()
        print('Top 20 hashtags on {}'.format(filedate))
        tag2count = {}
        with open(tagfile,'rt') as f:
            for line in f:
                tag,count = line.strip().split()
                tag2count[tag] = int(count)
        f.close()
        sorted_tag2count = sorted(tag2count.items(), key=operator.itemgetter(1),reverse=True)
        for i in range(20):
            hashtag, c = sorted_tag2count[i]
            print(hashtag,(25-len(hashtag))*' ',c)
        top20tags[filedate] = sorted_tag2count[:20]

    with open('./data_tag2count/3daysTop20hashtags.json','wt') as fo:
        json.dump(top20tags,fo)
    fo.close()


    
    elp_time = (time.time() - start_time)
    print("FINISHED in {:.2f} seconds.".format(elp_time) )



####### OUTPUT ########
# Top 20 hashtags on 2016-11-08
# ElectionNight              27084
# ElectionDay                17361
# Election2016               9198
# BIGOLIVE                   8737
# DolanTwinsNewVideo         6349
# ImWithHer                  4848
# AMAs                       3324
# Trump                      2992
# electionday                2961
# MAGA                       2756
# Elections2016              2663
# vote                       2222
# election2016               2104
# imwithher                  1929
# SincerelyVee               1859
# ALDUBfromHoneymoon         1763
# USElection2016             1740
# TrumpPence16               1457
# MakeAmericaGreatAgain      1376
# BlackMoney                 1251
#####################
# Top 20 hashtags on 2016-11-09
# ElectionNight              19368
# BIGOLIVE                   8921
# Trump                      6315
# Election2016               6309
# USElection2016             4355
# ElectionDay                4070
# NotMyPresident             3369
# AMAs                       3032
# PresidentTrump             2819
# Elections2016              2812
# MAGA                       2542
# ThankObamaIn4Words         2439
# trump                      1751
# TrumpPresident             1654
# DonaldTrump                1562
# trumpwins                  1471
# ElectionResults            1401
# DjMensahAllWhiteParty      1394
# MakeAmericaGreatAgain      1373
# ALDUBLambingan             1340
#####################
# Top 20 hashtags on 2016-11-15
# BIGOLIVE                   9962
# AMAs                       4720
# DolanTwinsNewVideo         4309
# TVPersonality2016          3631
# ShaktiAstitvaKeEhsaasKi    2199
# VivianDsena                2032
# ShadowhuntersandBeyond     1534
# ALDUBMomAndDad             1459
# SDLive900                  1441
# ARIASONEDIRECTION          1420
# NewYorkNewYork             1319
# TeenWolf                   1293
# DenverColorado             1179
# TooMuchSauce               1099
# ARIASJUSTINBIEBER          1054
# ShadowhuntersAndBeyond     987
# ALDUB16thMonthsary         926
# TeenWolfSeason6            816
# ThankYouObama              806
# Trump                      771





