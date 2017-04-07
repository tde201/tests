""" The sorting problem.

    Input:  Array of unsorted numbers.

    Output: Same set of numbers in increasing order.

"""

#-------------------------------------------------------------------------------
def simpleSort(anArray):
    """ A Simple sort.

        Repeatedly find the minimum of the anArray, and add to a sortedArray.

        Args:
          anArray: An array of numbers.

        Result:
          sortedArray: A sorted array of the input numbers, in increasing order.

        Raises:
          None.
    """

    n = len(anArray)
    sortedArray = []
    for i in range(n):
        # Find the smallest member of the array
        a = min(anArray)
        # Add this to the sorted array
        sortedArray.append(a)
        # Remove it from the input array
        anArray.remove(a)

    return sortedArray

#-------------------------------------------------------------------------------
def simpleSort2(anArray):
    """ Another Simple sort.

        Compare each member of the list with all other members. Build up an
        index of their sort order.
        
        Args:
          anArray: An array of numbers.

        Result:
          sortedArray: A sorted array of the input numbers, in increasing order.

        Raises:
          None.
    """

    n = len(anArray)
    indexArray  = range(n)
    sortedArray = [0] * n
    for i in range(n):
        k = 0
        for j in range(i, n):
            if anArray[i] > anArray[j]:
                k += 1

        l = indexArray[k]
        sortedArray[l] = anArray[i]
        indexArray.remove(l)

    return sortedArray

#-------------------------------------------------------------------------------
""" Merge sort.
    Recursively sort each half of the array.
    Merge each halves.
"""
# Initially ignoring n (length of input array) odd
# Split array into two halves A and B, output array is called C of length n
# Recursively sort these
# Merge two halves:
# i = 1, j = 1. i counts position in A, j in B
# for k = 1 to n
# if A(i) < B(j)
# C(k) = A(i)
# i += 1
# else
# C(k) = B(j)
# j += 1
# NB key point is that smallest element of the remainder of A or B is always
# we've got to in the lists.
# NB would need to check when you get to end of one of them
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
if __name__ == "__main__":
    print "Running simpleSort with an array [5, 4, 3, 2, 1]"

    simpleSort([5, 4, 3, 2, 1])
