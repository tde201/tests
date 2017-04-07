""" Given a set of points of n points P in the plane, output the closest pair.

    Assume: No points have same x and y coordinate.
    d(p, q) = sqrt(|p_x - q_x|^2 + |p_y - q_y|^2) i.e. Euclidean distance.
    NB Brute force takes O(n^2) (compare all points).
    This approach takes O(nlogn).
    1) Preprocessing step: takes copies of P sorted by the x-coordinate (P_x)
       and by the y-coordinate (P_y). Takes O(nlogn) using merge sort.
    2) Use divide and conquer:
       i)  Let Q by the left half of P (split by x-coord), and R the right half.
       ii) (p_1, q_1) = closestPair(Q_x, Q_y).
       iii)(p_2, q_2) = closestPair(R_x, R_y).
       iv) Let delta = min(d(p_1, q_1), d(p_2, q_2)).
       v)  (p_3, q_3) = closestSplitPair(P_x, P_y, delta)
       vi) Return best from (ii), (iii), or (v).
    3) closestSplitPair runs in O(n) as the pseudocode is:
       Set S_y to be the subset of P_y s.t. xbar - delta <= p_x <= xbar + delta
       where xbar is the largest x-value in the left set of P_x i.e xbar =
       P_x[n / 2][0].
       best = delta, bestPair = Null
       for i in range(|S_y| - 1):
           for j = 1 in range(min(7, |S_y| - i)):
               let p be ith member of and q be (i + j)th member of S_y.
               if d(p, q) < best:
                   bestPair = (p, q)
                   best     = d(p, q)

       See notes to see why you only need to check 7 closest points.
"""

import numpy as np

#===============================================================================
def euclideanMetric(p, q):
    """ Determine Euclidean distance between two points in the plane.

        Args:
          p: array of two points, real valued.
          q: array of two points, real valued.

        Returns:
          d: Eucleadian distance between p and q.

        Raises:
          None.
    """

    d = np.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

    return d

#-------------------------------------------------------------------------------
def bruteForceNearestNeighbours(P):
    """ Using brute force approach find two closest points in set P.

        Args:
          P: Set of points in plane R^2.

        Returns:
          bestPair: Closest pair of points, as tuple.

        Raises:
          None.
    """
    n    = len(P)
    best = float('Inf')
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclideanMetric(P[i], P[j])
            if dist < best:
                best = dist
                bestPair = (P[i], P[j])
            
    return bestPair
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
def preprocessSort(P):
    """ Sort the set P by the x-coordinate and the y-coordinate.

        Args:
          P: Set of 2D arrays of real numbers giving the points in a plane.

        Returns:
          Px: P sorted by the x-coordinate.
          Py: P sorted by the y-coordinate.

        Raises:
          None.
    """

    n = len(P)
    dictPx = {}
    dictPy = {}
    Qx = []
    Qy = []
    Px = np.empty([n, 2])
    Py = np.empty([n, 2])

    for i in range(n):
        # Dictionary with key x and value y
        dictPx[P[i, 0]] = P[i, 1]
        # Dictionary with key y and value x
        dictPy[P[i, 1]] = P[i, 0]

        Qx.append(P[i, 0])  # List of x-coordinate
        Qy.append(P[i, 1])  # List of y-coordinate

    Qx = mergeSort(Qx)  # Sort list of x-coordinate
    Qy = mergeSort(Qy)  # Sort list of y-coordinate

    # Merge y and x coordinates back into list Qx, Qy respectively
    for i in range(n):
        Px[i, 0] = Qx[i]
        Px[i, 1] = dictPx[Qx[i]]
        Py[i, 0] = dictPy[Qy[i]]
        Py[i, 1] = Qy[i]

    return Px, Py
    
#-------------------------------------------------------------------------------
def closestPair(Px, Py):
    """ Find closest pair in input set.

        i)  Let Q by the left half of P (split by x-coord), and R the right
            half.
        ii) Recursive call:(p_1, q_1) = closestPair(Q_x, Q_y).
        iii)Recursive call:(p_2, q_2) = closestPair(R_x, R_y).
        iv) Let  delta = min(d(p_1, q_1), d(p_2, q_2)).
        v)  (p_3, q_3) = closestSplitPair(P_x, P_y, delta)
        vi) Return best from (ii), (iii), or (v).

        Args:
          Px: Input array sorted by x-coordinate.
          Py: Input array sorted by y-coordinate.

        Returns:
          p, q: Closest two points in the set.

        Raises:
          sys.exit(1): If the sorted input arrays are of different length.
    """

    n = len(Px)
    # Error check Px and Py are same length
    if n != len(Py):
        print 'Error: Px and Py are different lengths'
        sys.exit(1)
        
    if n < 3:
        # Base case, just use brute force; we know this is O(2^2)
        p, q = bruteForceNearestNeighbours(Px)
        return p, q
        
    else:
        # Split P into left and right half based on x-value
        Qx = Px[0:n / 2]
        Rx = Px[n / 2:]

        # Find y-sorted companion sets
        # Allocate to sets based on value of x-coordinate. This runs in O(n).
        midX = Px[n/2, 0]  # Dividing value of x sorted set Px
        Qy   = np.empty([n / 2, 2])
        Ry   = np.empty([n - n / 2, 2])
        j    = 0
        k    = 0
        for i in range(n):
            if Py[i, 0] < midX:
                Qy[j] = Py[i]
                j += 1
            else:
                Ry[k] = Py[i]
                k += 1
        
        # Recursive calls
        p1, q1 = closestPair(Qx, Qy)
        p2, q2 = closestPair(Rx, Ry)

        # Determine delta
        pq1Sep = euclideanMetric(p1, q1)
        pq2Sep = euclideanMetric(p2, q2)
        delta = min(pq1Sep, pq2Sep)

        # Find if split pairs are closer
        p3, q3 = closestSplitPair(Px, Py, delta)

        # nan returned from closestSplitPair implies no shorter split pairs
        if np.isnan(p3[0]):
            pq3Sep = np.Inf
        else:
            pq3Sep = euclideanMetric(p3, q3)

        bestSep = min(pq1Sep, pq2Sep, pq3Sep)

        # Retrun the lowest separation
        if bestSep == pq1Sep:
            return p1, q1
        elif bestSep == pq2Sep:
            return p2, q2
        elif bestSep == pq3Sep:
            return p3, q3
    
#-------------------------------------------------------------------------------
def closestSplitPair(Px, Py, delta):
    """ Find split pairs that have smaller separation that non-split pairs.

        Runs in O(n).
        Set S_y to be the subset of P_y s.t. midX - delta <= p_x <= midX + delta
        where xbar is the largest x-value in the left set of P_x i.e midX =
        P_x[n / 2, 0].
        best = delta, bestPair = Null
        for i in range(|S_y| - 1):
            for j = 1 in range(min(7, |S_y| - i)):
                let p be ith member of and q be (i + j)th member of S_y.
                if d(p, q) < best:
                    bestPair = (p, q)
                    best     = d(p, q)

        Args:
          Px:    Set P sorted by x-coordinate.
          Py:    Set P sorted by y-coordinate.
          delta: Smallest separation found from right and left halves of P.

        Returns:
          p, q: Pair of points with smallest separation. If no points are
                separated by less than delta these are returned as nan.

        Raises:
          None.
    """

    n     = len(Px)
    midX  = Px[n / 2, 0]
    best  = delta
    Sy    = np.empty([n, 2])  # Initialise Sy to have length n
    k     = 0
    bestP = np.empty([1])
    bestQ = np.empty([1])
    bestP.fill(np.nan)  # Fill empty array with nans
    bestQ.fill(np.nan)
    
    
    # Create set Sy
    for i in range(n):
        if (Py[i, 0] >= midX - delta and
            Py[i, 0] <= midX + delta):
            Sy[k] = Py[i]
            k    += 1

    Sy = Sy[:k]  # Remove empty entries of Sy

    # Consider 7 next points in Sy, a smaller split pair must be within 7
    # entries
    for i in range(k - 1):
        for j in range(min(7, k - 1 - i)):
            p     = Sy[i]
            q     = Sy[i + j + 1]
            pqSep = euclideanMetric(p, q)
            if pqSep < best:
                best  = pqSep
                bestP = p
                bestQ = q

    return bestP, bestQ

#-------------------------------------------------------------------------------
def main():
    """ Find closest pair of set P using brute force and a faster algorithm """

    # Define set of points on the plane. This is to be used for testing.
    P = np.array([[0.0, 0.0], [1.0, 1.0], [0.25, 0.25], [4.0, 2.0], [2.0, 7.0],
         [6.0, 4.0], [5.0, 3.0], [3.0, 5.0]])

    # Determine bestPair using brut force O(n^2) for testing.
    pBrute, qBrute = bruteForceNearestNeighbours(P)
    
    print pBrute, qBrute

    # Preprocess set P into lists sorted by x and y coordinates respectively.
    Px, Py = preprocessSort(P)

    # Find closest pair in time O(nlog_{2}(n)).
    p, q = closestPair(Px, Py)

    print p, q
    
#-------------------------------------------------------------------------------
if __name__ == "__main__":

    main()
