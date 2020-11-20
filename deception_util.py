#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 19:54:38 2020

@author: kevinbarker
"""

import math
import numpy as np
from itertools import tee, chain
from datetime import datetime


def previous_and_curr(some_iterable):
    prevs, items = tee(some_iterable, 2)
    prevs = chain([None], prevs)
    return zip(prevs, items)

def create_count(row):
    if row['balls'] == 0:
        if row['strikes'] == 0:
            return '0-0'
        elif row['strikes'] == 1:
            return '0-1'
        elif row['strikes'] == 2:
            return '0-2'
    elif row['balls'] == 1:
        if row['strikes'] == 0:
            return '1-0'
        elif row['strikes'] == 1:
            return '1-1'
        elif row['strikes'] == 2:
            return '1-2'
    elif row['balls'] == 2:
        if row['strikes'] == 0:
            return '2-0'
        elif row['strikes'] == 1:
            return '2-1'
        elif row['strikes'] == 2:
            return '2-2'
    elif row['balls'] == 3:
        if row['strikes'] == 0:
            return '3-0'
        elif row['strikes'] == 1:
            return '3-1'
        elif row['strikes'] == 2:
            return '3-2'
    elif row['balls'] == 4:
        #Handling DeGrom v Hernandez on 8/24/15, umps forgot count
        if row['strikes'] == 0:
            return '4-0'
        elif row['strikes'] == 1:
            return '4-1'
        elif row['strikes'] == 2:
            return '4-2'

def merge(list1, list2): 
      
    merged_list = tuple(zip(list1, list2))  
    return merged_list 

def isnan(value):
    try:
        return math.isnan(float(value))
    except:
        return False
    
def retrieve_percentile_of_set(a, p):
    prob_set = []
    for b in a:
        for c in list(a[b].values()):
            prob_set.append(c)
    return np.percentile(prob_set, p)

def check_for_completed_at_bats(e, ab):
    if not isnan(e):
        if e.startswith('pickoff') or e.startswith('caught_stealing') or e.startswith('interf_def'):
            #print('AB ended via', e, 'for', ab)
            return False
        else:
            return True
    else:
        return False

def get_current_time(x):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(x, 'time:', current_time)
        