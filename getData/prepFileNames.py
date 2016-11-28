#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors: Xipei Liu

Purpose: Prepare full file paths for VACC job. 
         From 2013-07-01 to 2016-06-30, 18:00 to 23:00.
         ** This script needs to run inside VACC 
         in terms of filtering out defective file.

Inputs: None      

Outputs: ../data/file2run_2014-11-11_2016-11-11.txt

"""

import warnings
warnings.filterwarnings("ignore")
import sys, os
import time
import random
import datetime as dt

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
    num4files = ((end_dt - start_dt).days+1)*96
    return num4files

def get_full_path(timestamp):
    """Return full file path on VACC."""
    p = '/users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/'
    return p+timestamp[:10]+'/'+timestamp+'.gz'

def chosen_timeperiod(start,end):
    """Return a list of possible time from 18:00 ~23:00.
    Formatted in %H-%M."""
    time_list = [start]
    start_t = dt.datetime.strptime(start,'%H-%M')
    end_t   = dt.datetime.strptime(end,  '%H-%M')
    while start_t!=end_t:
        start_t = start_t + dt.timedelta(minutes=15)
        time_list.append(dt.datetime.strftime(start_t,'%H-%M'))
    return time_list

if __name__ == '__main__':
    start_time = time.time()
    
    t_start   = '2014-11-11-00-00'
    p_start   = get_full_path(t_start)
    num4files = get_num4files('2014-11-11-00-00','2016-11-11-23-45')
    time_list = chosen_timeperiod('00-00','23-45')
    print(len(time_list))
    print(num4files)
    
    fout = open('../file2run_2014-11-01_2016-11-11.txt','wt')
    fout.write(p_start+'\n')

    for i in range(num4files-1):
        t_next = get_timestamp(t_start)
        p_next = get_full_path(t_next)    
        if t_next[-5:] in time_list:
            try:
                file_size = os.path.getsize(p_next)
                if file_size>50:
                    fout.write(p_next+'\n')
            except FileNotFoundError:
                pass
        t_start = t_next
    fout.close()

    print("FINISHED in {:.2f} seconds.".format((time.time() - start_time)) )
