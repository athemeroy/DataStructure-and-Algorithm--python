#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 23:42:28 2018

@author: zqun(athemeroy)
"""
from memo import memo


@memo
def fib1(n):
    """
    递归方式 很容易出现栈溢出
    同时用cache来存储已经计算过的内容
    空间消耗非常大
    1000000 loops, best of 3: 260 ns per loop
    """
    if n == 0 or n == 1:
        return 1
    else:
        return fib1(n-1) + fib1(n-2)
    
def fib2(n):
    """
    100000 loops, best of 3: 13.9 µs per loop
    动态规划(这是用C++的版本改写的)
    自下而上解决这个问题
    和人类算菲波那切数列是同样的手段
    """
    f = 0
    g = 1
    while (n > 0):
        n -= 1
        g += f
        f = g - f
    return g

def fib3(n):
    """
    100000 loops, best of 3: 7.37 µs per loop
    动态规划（自己尝试使用Python的手段重写）
    自下而上解决这个问题
    和人类算菲波那切数列是同样的手段
    """
    x1 = 0
    x2 = 1
    for i in range(n):
        now = x1 + x2
        x1, x2 = x2, now
    return now

    
    
if __name__ == "__main__":
#    print(f'fib1({1000}):{fib1(1000)}')
#    print(f'fib2({1000}):{fib2(1000)}')
    pass
    
