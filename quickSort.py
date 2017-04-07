""" Quick sort using a pivot approach. """

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
def quickSort(A, l = 0, r = None):
    """ Pivot sort the input array.

        The input array of length n is sorted using a pivot method, the sorted
        array (in ascending order is returned. On average the running time is of
        O(nlogn). NB This algorithm sorts in place; it requires minimal extra
        memory.

        Args:
          A: Array of numbers of length n.
          l: Start of subarray of A to consider. Default is zero.
          r: End of subarray of A to consider. Default is None; if default is
             supplied set as len(A) - 1.

        Output:
          A: A in sorted order.

        Raises:
          None.
    """

    # Pseudocode
    # base case: if n = 1 return A
    # selectPivot(A, l, r), randomly choose pivot p in subarray. Set p as first
    # element of array.
    # Partition A around pivot p: call partition(A, l, r), A[l] is pivot element
    # recursively sort 1st part
    # recursively sort second part

    if r == None:
        r = len(A) - 1

    if (r - l == 0 or
        r - l < 0):
        # Base Case
        return A
    else:
        # Randomly choose pivot p in subarray. Set as first element of subarray
        # A[l, r].
        A = selectPivot(A, l, r)

        # Partition subarray A[l, r] around pivot A[l]
        A, k = partition(A, l, r)

        # Recurvise calls
        A = quickSort(A, l, k)      # First half of pivoted array
        A = quickSort(A, k + 1, r)  # Second half of pivoted array
        
        return A
        
#-------------------------------------------------------------------------------
def selectPivot(A, l, r):
    """ Randomly select pivot element; set as first element of subarray.

        Args:
          A: Input array.
          l: Start of subarray.
          r: End of subarray.

        Returns:
          A: Input array with pivot p swapped into position A[l].

        Raises:
          None.
    """

    # Randomly choose pivot from subarray A[l, r]
    i = int(round(np.random.rand() * (r - l) + l))
    
    # Swap A[l] and p = A[i]; l <= i <= r
    A = swapArrayElements(A, i, l)
    
    return A

#-------------------------------------------------------------------------------
def partition(A, l, r):
    """ Partition A[l, r] around a pivot. The pivot is assumed to be A[l].

        Args:
          A: Array of length n.
          l: Start od subarray.
          r: End of subarray.

        Returns:
          A: Array with partitioned subarray A[l, r].
          k: Final position of pivot.

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

    p = A[l]
    i = l + 1
    for j in range(i, r + 1):
        if A[j] < p:
            A  = swapArrayElements(A, i, j)
            i += 1

    k = i - 1
    A = swapArrayElements(A, l, k)

    return A, k

#-------------------------------------------------------------------------------
def main(args):
    # read input file
    # call quickSort
    # print output
    A = [5, 6, 3, 2, 4, 1, 8, 7]
    
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv)
