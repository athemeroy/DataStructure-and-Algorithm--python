#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 23:37:58 2018

@author: zqun(athemeroy)
"""

def qsort(array):
    if len(array) < 2:
        return array
    mid = len(array) >> 1
    left = [i for i in array if i < array[mid]]
    right = [i for i in array if i > array[mid]]

    return qsort(left) + [array[mid]] + qsort(right)


def main():
    import random
    l = random.sample(range(0,10000), 500)
#    print(l)
    print(qsort(l))
    
if __name__ == "__main__":
    main()