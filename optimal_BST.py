# -*- coding: utf-8 -*-
"""
Optimal binary search trees. Find the best binary search tree for a given set of keys with a known set of frequencies
to be serached for.
"""
import numpy as np
import pandas as pd

def optimal_binary_search_tree(keys, freq):
    """ Determine the average search time for a binary tree with known key frequencies.
    
    Args:
      keys: List of key values.
      freq: List of frequency values for each <key>.
      
    Returns:
      A[0, n - 1]: The optimal average search time for the binary tree.
    """
    n = len(keys)
    A = pd.DataFrame(index = range(n), columns = range(n))
    for s in range(n):
        for i in range(n):
            if i + s < n:
                minS = np.inf
                const = 0
                endVal = min(n, i + s + 1)
                for r in range(i, endVal):
                    const += freq[r]
                    if i > r - 1:
                        t1Sum = 0
                    else:
                        t1Sum = A.loc[i, r - 1]
                    if ((r + 1 > i + s) or
                        (r + 1 >= n)):
                        t2Sum = 0
                    else:
                        t2Sum = A.loc[r + 1, i + s]
    
                    candidate = t1Sum + t2Sum
                    if candidate < minS:
                        minS = candidate
                minS += const
                A.loc[i, i + s] = minS
    print A
    return A.loc[0, n - 1]

if __name__ == "__main__":
#    keys = [1, 2, 3, 4]
#    freq = [0.02, 0.23, 0.73, 0.01]
    keys = [1, 2, 3, 4, 5, 6, 7]
    freq = [0.05, 0.4, 0.08, 0.04, 0.1, 0.1, 0.23]
    result = optimal_binary_search_tree(keys, freq)
    print result