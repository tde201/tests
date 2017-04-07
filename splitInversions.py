""" Count number of inversions in an array. """


#===============================================================================
def sortAndCount(inArray, numInv = 0):
    """ Sort an array and count the number of Inversions.

        Inversions are pairs (i, j) where for an array A, A[i] > A[j] for i < j.
        This routine counts them by splitting the array into two pieces, and
        recursing. When a pair of sorted arrays ar returned, then a merge sort
        is performed. In the merge sort, each time an element is taken from the
        second array there are as many inversions as there are elements in the
        first array remaining. These are counted. Running the recursions
        takes O(log_{2}(n) operations, while running the merge and count takes
        O(n) operations. The overall running time is thus O(nlog_{2}(n)).
        
        Args:
          inArray: unsorted input array of numbers.

        Returns:
          sorteArray: Sorted version of inArray.
          numInv:     Number of inversions counted (so far)

        Raises:
          None.
    """

    n = len(inArray)
    #numInv = 0

    if n == 1:    
        return inArray, 0

    else:
        array1 = inArray[0:n / 2]
        array2 = inArray[n / 2:]
        
        array1, numInv1     = sortAndCount(array1, numInv)
        array2, numInv2     = sortAndCount(array2, numInv)
        sortedArray, numSplitInv = mergeAndCountSplitInv(array1, array2)

        numInv += numInv1 + numInv2 + numSplitInv

        return sortedArray, numInv

#-------------------------------------------------------------------------------
def mergeAndCountSplitInv(array1, array2):
    """ Merge two sorted lists together.

        Running time O(length input array)

        Args:
          array1: Sorted array 1.
          array2: Sorted array 2.

        Returns:
          sortedArray: Sorted mix of List1 and List2.

        Raises:
          None.
    """

    len1        = len(array1)
    len2        = len(array2)
    sLen        = len1 + len2
    i           = 0
    j           = 0
    numSplitInv = 0
    sortedArray = [0] * sLen

    for k in range(sLen):      
        if i == len1:
            sortedArray[k:] = array2[j:]
            break

        if j == len2:
            sortedArray[k:] = array1[i:]
            break
        
        if array1[i] < array2[j]:
            sortedArray[k] = array1[i]
            i             += 1
        else:
            sortedArray[k] = array2[j]
            j             += 1
            numSplitInv   += len1 - i

    return sortedArray, numSplitInv

#-------------------------------------------------------------------------------
def main():
    """ Run main code. Find number inversions in specified array. """

    # Define array
    inArray = [6, 5, 4, 3, 2, 1, 0]

    # Run algorithm
    sortedArray, numInv = sortAndCount(inArray)

    # Print number of inversions
    print numInv

            
#-------------------------------------------------------------------------------
if __name__ == "__main__":

    main()

    

