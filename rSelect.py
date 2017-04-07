""" Implements randomised selection.

    Given an array A with n distinct numbers and a number i within the set
    {0, n}, return the ith order statistic. This is the ith smallest element
    of the input array.

    Runs in linear time O(n).
"""
#===============================================================================
import sys
import numpy as np

#===============================================================================
def swapArrayElements(A, i, j):
    """ Swap elements A[i] and A[j].

        Args:
          A: Input array.
          i: First element to swap.
          j: Second element to swap.

        Results:
          A: Array A with ith and jth elements swapped.

        Raises:
          None.
    """
    temp = A[i]
    A[i] = A[j]
    A[j] = temp
    
    return A

#-------------------------------------------------------------------------------
def rSelect(A, n, i):
    """ Randomised selection algorithm.

        Args:
          A: Array of n distinct numbers.
          n: Length of array A.
          i: Order of the statistic we want to return.

        Returns:
          p: The pivot value.

        Raises:
          None.
    """

    # Pseudocode
    # 0) if n = 1 return A[0]
    # 1) choose pivot p from A uniformly at random
    # 2) Partition A around pivot p. Let j = new index of p
    # 3) If j = i return p
    # 4) If j > i return rSelect(1st part of A, j - 1, i)
    # 5) Else return rSelect(2nd part of A, n - j, i - j)

    if n == 1:
        return A[0]
    
    A = selectPivot(A, n)

    A, j = partition(A, n)

    p = A[j]
    
    if j == i - 1:
        return p
    elif j > i - 1:
        Aprime = A[0:j]
        return rSelect(Aprime, j, i)
    else:
        Aprime = A[j+1:]
        return rSelect(Aprime, n - j - 1, i - j - 1)
    
#-------------------------------------------------------------------------------
def selectPivot(A, n):
    """ Randomly select pivot element; set as first element of subarray.

        Args:
          A: Input array.
          n: Length of input array.
          
        Returns:
          A: Input array with pivot p swapped into position A[0].

        Raises:
          None.
    """
    i = int(round(np.random.rand() * (n - 1)))
        
    # Swap A[0] and p = A[i]; 0 <= i <= n
    A = swapArrayElements(A, i, 0)
    
    return A

#-------------------------------------------------------------------------------
def partition(A, n):
    """ Partition A around a pivot. The pivot is assumed to be A[0].

        Args:
          A: Array of length n.
          n: Length of A.

        Returns:
          A: Partitioned array.
          j: Final position of pivot.

        Raises:
          None.
    """

    # Pseudocode
    # p = A[l]  # This is the pivot element
    # i = l + 1
    # for j = l + 1 to r
    #     if A[j] < p:
    #         swap A[j] and A[i]
    #         i++
    # swap A[l] and A[i - 1]
    # NB if A[j] > p, do nothing.

    p = A[0]
    i = 1
    for k in range(i, n):
        if A[k] < p:
            A  = swapArrayElements(A, i, k)
            i += 1

    j = i - 1
    A = swapArrayElements(A, 0, j)

    return A, j

#-------------------------------------------------------------------------------
def main(args):
    """ Run main code.

        Call rSelect
        Print output

        Args:
          args: Command line arguments.

        Results:
          print out of ith order statistic of input Array.

        Raises:
          None
    """
    
    if len(args) != 1:
        print 'Syntax: $python rSelect.py'
        sys.exit(1)
        
    A = [10, 8, 2, 4, 1, 5, 7, 11]
    n = len(A)
    i = 8
    p = rSelect(A, n, i)

    print str(i) + 'th order statistic of A: ' + str(p)
    
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)
