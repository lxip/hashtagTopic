#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Authors: Xipei Liu

Purpose: Automatically sending job to VACC. 
         Collect tweet hashtag counts per 15min.

Inputs: ../file2run_2014-11-01_2016-11-11.txt

Outputs: None
"""

import sys
from time import sleep
import subprocess as sp


def qs():
    """ Count how many jobs currently running
    """
    try:
        return int(sp.check_output('qstat -u xliu15 | grep -c "shortq"',shell=True))
    except:
        return 0

def send(f):
    """ Send file path to job_hashtagDic.sh
    """
    sp.check_call('qsub -v FILE="%s" job_hashtag.sh' % f,shell=True)

if __name__ == '__main__':
    jobs = []
    for line in open('../file2run_2015-11-11_2016-11-15.txt','rt'):
        jobs.append(line.strip())
    pop = jobs.pop

    while jobs:
        q = qs()
        if q > 180:
            sleep(1)
            continue
        else:
            send(pop())
            sleep(0.1)
    print("Finished sending jobs.")
