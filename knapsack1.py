# -*- coding: utf-8 -*-
"""
Script to solve knapsack problem for Algorithms II week 3 course.
"""
import numpy as np
from copy import deepcopy
#import pandas as pd
from collections import namedtuple

Item = namedtuple('Item', 'value size')

def read_file(fileName):
    """ Read file describing knapsack instance.
    
    Format:
    [knapsack_size] [number_of_items]
    [value_1] [weight_1]
    [value_2] [weight_2]
    
    Args:
      fileName: String. File name.
      
    Returns:
      kSize: The size of the knapsack.
      numItems: The number of items in the knapsack.
      kData: Dict of named tuples, key = item number, value = tuple with <value> and <size> properties.
    """
    kData = dict()
    with open(fileName, 'r') as fn:
        for lineNum, line in enumerate(fn):
            row = line.strip('\n')
            row = row.strip()
            data = row.split(' ')
            if lineNum == 0:
                kSize = int(data[0])
                numItems = int(data[1])
            else:
                kData[lineNum] = (Item(int(data[0]), int(data[1])))
    
    return kSize, numItems, kData


def knapsack(numItems, kSize, kData):
    """ Determine the maximal value given the total available size.
    
    Args:
      kSize: The size of the knapsack.
      numItems: The number of items in the knapsack.
      kData: Dict of named tuples, key = item number, value = tuple with <value> and <size> properties.
      
    Returns:
      A: Dict, key = (i, x) where i is the number of the item and x is the size of that item.
    """
    # Save minimal amount of data?
    A = dict()  # pd.DataFrame(index = range(numItems + 1), columns = range(kSize + 1))
    for i in range(numItems + 1):
        for x in range(kSize + 1):
            if i == 0:
                A[0, x] = 0
            else:
                try:
                    A[i, x] = max(A[i - 1, x], A[i - 1, x - kData[i].size] + kData[i].value)
                except:
                    A[i, x] = A[i - 1, x]
    return A


def big_knapsack(numItems, kSize, kData):
    """ Determine the maximal value given the total available size.
    
    Args:
      kSize: The size of the knapsack.
      numItems: The number of items in the knapsack.
      kData: Dict of named tuples, key = item number, value = tuple with <value> and <size> properties.
      
    Returns:
      A: Dict, key = (i, x) where i is the number of the item and x is the size of that item.
    """
    # Save minimal amount of data?
    A = np.zeros(kSize + 1)
    
    for i in range(1, numItems + 1):
        B = deepcopy(A)
        size = kData[i].size
        value = kData[i].value
        C = np.append(np.zeros(size), B[:-size]) + np.append(np.zeros(size), [value] * (kSize + 1 - size))
        A = np.maximum(A, C)
    
    return A[-1]
    

def reconstruct(numItems, kSize, A):
    """ Reconstruct the set of values. 
    
    Args:
      kSize: The size of the knapsack.
      numItems: The number of items in the knapsack.
      A: Dict, key = (i, x) where i is the number of the item and x is the size of that item.
      
    Returns:
      S: List of items in order they were added to the knapsack.
    """
    i = numItems
    x = kSize
    S = list()
    while i > 0:
        try:
            case2 = A[i - 1, x - kData[i].size] + kData[i].value
        except:
            case2 = 0
        if A[i - 1, x] >= case2:
            i -= 1
        else:
            S.append(i)
            x -= kData[i].size
            i -= 1
    S.reverse()
    return S

if __name__ == "__main__":
    fileName = 'knapsack_big.txt'
    kSize, numItems, kData = read_file(fileName)
#    A = knapsack(numItems, kSize, kData)
#    print A[numItems, kSize]
#    S = reconstruct(numItems, kSize, A)
#    print S
    
    B = big_knapsack(numItems, kSize, kData)
    print B

    