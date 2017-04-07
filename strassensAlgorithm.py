""" Implement Strassen's Algorithm. """

import numpy as np


#===============================================================================
def decomposeXYAndMultiply(X, Y):
    """ Decompose the n by n matrices X and Y into 8 blocs, then find product.

        Recursively call decomposeXYAndMultiply to gain seven products. Then
        combine these to give back Z.
        
        Args:
          X: n by n matrix.
          Y: n by n matrix.

        Returns:
          Z: n by n matrix.

        Raises:
          sys.exit(1): If X or Y are not square or if the dimensions of X and Y
                       disagree.
    """

    ### Assume n is even - but how can this work for n odd? ###
    ### Suspect you trim original matrix by one row and one column do this
    ### then finish by computing thw row/column.
    
    [m, n] = X.shape
    [p, q] = Y.shape

    # Error checks
    if n != m:
        print 'X is not square.'
        print 'Rows: ' + str(m)
        print 'Columns: ' + str(n)
        sys.exit(1)

    if p != q:
        print 'Y is not square.'
        print 'Rows: ' + str(p)
        print 'Columns: ' + str(q)
        sys.exit(1)
    
    if (m != q):  # NB only one test needed as X, Y are square
        print 'X and y have different dimensions.'
        print 'Size X: ' + str(m) + ', ' + str(n)
        print 'Size Y: ' + str(Y.shape)
        sys.exit(1)


    if n == 1:
        
        # Base case
        el = X[0, 0] * Y[0, 0]
        Z  = np.matrix([[el]])

        return Z

    else:
        n1 = n / 2

        # Split X into four blocks
        A = X[0:n1, 0:n1]
        B = X[0:n1, n1:]
        C = X[n1:, 0:n1]
        D = X[n1:, n1:]

        # Split Y into four blocks
        E = Y[0:n1, 0:n1]
        F = Y[0:n1, n1:]
        G = Y[n1:, 0:n1]
        H = Y[n1:, n1:]

        # Determine 7 clever products
        P1 = decomposeXYAndMultiply(A, F - H)
        P2 = decomposeXYAndMultiply(A + B, H)
        P3 = decomposeXYAndMultiply(C + D, E)
        P4 = decomposeXYAndMultiply(D, G - E)
        P5 = decomposeXYAndMultiply(A + D, E + H)
        P6 = decomposeXYAndMultiply(B - D, G + H)
        P7 = decomposeXYAndMultiply(A - C, E + F)

        Aprime = P5 + P4 - P2 + P6
        Bprime = P1 + P2
        Cprime = P3 + P4
        Dprime = P1 + P5 - P3 - P7

        Z = np.bmat([[Aprime, Bprime],
                     [Cprime, Dprime]])
        return Z

#-------------------------------------------------------------------------------
def main():
    """ Run main code. Find product of matrices specified below. """

    # Define Matrices
    X = np.random.rand(16, 16)
    Y = np.random.rand(16, 16)
    Z = np.dot(X, Y)

    # Run algorithm
    Zprime = decomposeXYAndMultiply(X, Y)

    # Print number of inversions
    print np.linalg.norm(Z - Zprime)
           
#-------------------------------------------------------------------------------
if __name__ == "__main__":

    main()
