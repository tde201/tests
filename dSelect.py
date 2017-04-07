""" Implements deterministic selection.

    Given an array A with n distinct numbers and a number i within the set
    {0, n}, return the ith order statistic. This is the ith smallest element
    of the input array.

    Runs in linear time O(n). It does not operate in place however, and has
    larger constants. In practice rSelect is the better choice.
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
def dSelect(A, n, i):
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
    # 1) choose pivot p from A
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
        return dSelect(Aprime, j, i)
    else:
        Aprime = A[j+1:]
        return dSelect(Aprime, n - j - 1, i - j - 1)
    
#-------------------------------------------------------------------------------
def selectPivot(A, n):
    """ Select pivot element; set as first element of array.

        Args:
          A: Input array.
          n: Length of input array.

        Returns:
          A: Input array with pivot p swapped into position A[0].

        Raises:
          sys.Exit: If the pivotChoice is not 1, 2, 3, or 4.
    """
    
    # Pseudocode
    # 1) Break A into n / 5 groups of size 5 each
    # 2) sort each group (e.g. using merge sort)
    # 3) copy n/5 medians into new array C
    # 4) Recursively compute median of C i.e. p = dSelect(C, n/5, n/10)
    #    return this as the pivot, p.
    
    C = []
    for i in range(0, n, 5):
        # i gives start of subarrays of length 5

        if n < i + 4:
            r = n  # last subarray may have length < 5
        else:
            r = i + 4  # end of subarrays of length 5

        j = (r - i) / 2  # index of median

        A[i:r] = mergeSort(A[i:r])

        C.append(A[j])

    # Find length of C. If n is divisible by 5 then it is n / 2, else it is
    # n / 2 + 1
    if n % 5 == 0:
        m = n / 5
    else:
        m = n / 5 + 1
    
    p = dSelect(C, m, m / 2)
        
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
def mergeSort(inArray):
    """ Merge sort algorithm.

        Split (unsorted) input array into two halves, list1 and list2. If the
        length of the input array is odd these will differ in length by 1. If
        either list1 or list2 has length greater than 1 then call mergeSort
        (recursively). The base case is gained when both lists have at most one
        entry. If the input array is of length m, the time complexity scales as
        at most 6m*(log_{2}(m) + 1). As the depth of recursion is at most
        log_{2}(m) + 1, and the merge subroutine takes 6m operations.

        Args:
          inArray: Unsorted input array (of numbers).

        Returns:
          sortedList: A sorted version of the inArray (in ascending order).

        Raises:
          None.
    """

    m = len(inArray)
    list1 = inArray[0:m/2]
    list2 = inArray[m/2:]

    if (len(list1) > 1 or
        len(list2) > 1):
        sorted1 = mergeSort(list1)
        sorted2 = mergeSort(list2)
        sortedList = merge(sorted1, sorted2)
        return sortedList

    else:
        sortedList = merge(list1, list2)
        return sortedList

#-------------------------------------------------------------------------------
def merge(list1, list2):
    """ Merge two sorted lists together.

        Args:
          List1: Sorted list 1.
          List2: Sorted list 2.

        Returns:
          sortedList: Sorted mix of List1 and List2.

        Raises:
          None.
    """

    m          = len(list1)
    n          = len(list2)
    sLen       = m + n
    i          = 0
    j          = 0
    sortedList = [0] * sLen

    for k in range(sLen):
        if i == m:
            sortedList[k:] = list2[j:]
            break

        if j == n:
            sortedList[k:] = list1[i:]
            break
        
        if list1[i] < list2[j]:
            sortedList[k] = list1[i]
            i            += 1
        else:
            sortedList[k] = list2[j]
            j            += 1

    return sortedList

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
          sys.exit: if there are not 2 arguments in call from command line.
    """
    
    if len(args) != 1:
        print 'Syntax: $python dSelect.py'
        sys.exit(1)
        
    A = [10, 8, 2, 4, 1, 5, 7]
    n = len(A)
    i = 7
    p = dSelect(A, n, i)

    print str(i) + 'th order statistic of A: ' + str(p)
    
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)
