#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors: Xipei Liu

Purpose: Count the appearence of different hashtags in the input file, 
store information in a dictionary.

Inputs: argv[1],stdin

Outputs: {%Y-%m-%d-%H-%M}_hashtag_dic.json.gz
"""

import warnings
warnings.filterwarnings("ignore")
from sys import stdin,stdout,exit,argv
import os,re
import gzip
import codecs
import ujson as json
import bltools as blt


if __name__ == '__main__':
    file_path = argv[1]
    timestamp = file_path[-19:-3]

    fout   = gzip.open('../hashtagStore/{}_hashtags.json.gz'.format(timestamp), 'wt')

    retweet = re.compile('(^|\s+)[rR][tT](\s+|$)') #match retweet

    tweetsource_str = 'Twitter for iPhone|Twitter Web Client|TweetDeck|Twitter for Android|Twitter for Website| \
                    Twitter for iPad|Twitter for BlackBerry|Twitter for Android Tablets|Mobile Web|iOS|twitterfeed \
                    IFTTT|TweetAdder|Hootsuite|SocialOomph|dlvr.it|Instagram|Facebook'
    tweetsource = re.compile(tweetsource_str)

    #---parsing & adding---
    for line in stdin:
        try:
            data = json.loads(line)
        except:
            pass

        ####### filtering retweets --1
        # block tweets has "retweeted_status" entity
        if 'retweeted_status' in data:
            continue

        ####### filtering deleted & filtering none English tweet --1
        # block tweets not written in English
        if 'lang' in data:
            if data['lang'] != 'en':
                continue

        ###### filtering retweets --2 & filtering none English ---2
        #block reTweets using a regex    
        try:
            txt  = data['text']
        except KeyError:
            continue
        txt  = txt.replace('\n','') 
        if retweet.search(txt):   
            continue
        if not blt.is_english(txt):
            continue


        ####### filtering tweets without hashtage
        if 'entities' in data:
            if len(data['entities']['hashtags']):
                lineInfo = {'hashtags':[]} 
                if tweetsource.serach(data['source']):
                    # appending hashtags into the dictionary
                    n_hashtag = len(data['entities']['hashtags'])
                    for i in range(n_hashtag):
                        tag_i = data['entities']['hashtags'][i]["text"]
                        lineInfo['hashtags'].append(tag_i)
                    lineInfo['text']    = data['text']
                    lineInfo['source']  = data['source']
                    lineInfo['user_lang'] = data['user']['lang']
                    lineInfo['created_at']  = data['created_at']
                    lineInfo['timestamp_ms'] = data['timestamp_ms'] 
                    lineInfo['retweet_count'] = data['retweet_count']
                    lineInfo['favorite_count'] = data['favorite_count']
                    json.dump(lineInfo, fout)
                    fout.write('\n')
    fout.close()
