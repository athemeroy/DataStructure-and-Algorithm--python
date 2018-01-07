#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 00:31:01 2018

@author: zqun(athemeroy)
"""

def merge_sort(array):
    """
    归并排序
    :return: 排序好的列表
    """
    def merge(left, right):
        """
        归并排序的合并部分
        :param left: 左侧列表
        :param right: 右侧列表
        :return: 按照大小合并之后的列表
        """
        if right is None:
            return left
        merged_result = []
        i = 0
        j = 0
        for k in range(len(left) + len(right)):
            if i == len(left):
                merged_result.append(right[j])
                j += 1
            elif j == len(right):
                merged_result.append(left[i])
                i += 1
            elif left[i] < right[j]:
                merged_result.append(left[i])
                i += 1
            else:
                merged_result.append(right[j])
                j += 1
        return merged_result
    # 用来分割列表， 生成一个包含仅由一个一个元素组成的列表的
    divided = [[i] for i in array]

    while len(divided) > 1:
        if len(divided) % 2:
            divided.append(None)
        
        # 就用一个新的列表组成两两合并之后的列表
        merged = [merge(divided[i], divided[i+1]) for i in range(len(divided))[::2]]
        # 用一个新的列表组成两两合并之后的列表
        divided = merged
        print(divided)
    # 因为上面是最后append了merge之后的结果，所以最后得到的列表一定是Vector[Vector, None]的形式
    # 所以最后取列表的第一个就可以了
    return divided[0]

if __name__ == "__main__":
    import random
    ll = []
    for i in range(1501):
        ll.append(random.randint(0,400))
    print(merge_sort(ll))