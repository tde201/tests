""" Unit test functions in quickSort module. """

#===============================================================================
import unittest
import numpy as np
import quickSort as qS


#===============================================================================
class TestSwapArrayElements(unittest.TestCase):
    """ Unit test swapArrayElements. """

    def test_swap_element_2_and_5(self):
        """ Are elements 2 and 5 swapped correctly? """
        B      = [0, 1, 2, 3, 4, 5, 6, 7]
        i      = 2
        j      = 5
        BOut   = [0, 1, 5, 3, 4, 2, 6, 7]
        BPrime = qS.swapArrayElements(B, i, j)
        self.assertEqual(BOut, BPrime)

    def test_error_if_first_element_is_not_in_array(self):
        """ Is an error raised if the first swap element is not in array? """
        B      = [0, 1, 2, 3, 4, 5, 6, 7]
        i      = 9
        j      = 2
        self.assertRaises(IndexError, qS.swapArrayElements, B, i, j)
        
    def test_error_if_second_element_is_not_in_array(self):
        """ Is an error raised if the second swap element is not in array? """
        B      = [0, 1, 2, 3, 4, 5, 6, 7]
        i      = 2
        j      = 8
        self.assertRaises(IndexError, qS.swapArrayElements, B, i, j)

        
#-------------------------------------------------------------------------------
class TestPartition(unittest.TestCase):
    """ Unit test partition subroutine. """

    def test_partitioned_ascending_array(self):
        """ Ensure that the array B, an ascending sequence, is partitioned. """
        B         = [100, 1, 2, 3, 4, 5, 1000]  # Pivot element 1
        BPrime, k = qS.partition(B, 1, 5)
        self.assertEqual(B, BPrime)
        self.assertEqual(1, k)

    def test_partitioned_descending_array(self):
        """ Ensure that the array C, a descending sequence, is partitioned. """
        C          = [100, 5, 4, 3, 2, 1, 1000]  # Pivot element 5
        CPartition = [100, 1, 4, 3, 2, 5, 1000]
        CPrime, k  = qS.partition(C, 1, 5)
        self.assertEqual(CPartition, CPrime)
        self.assertEqual(5, k)
        

    def test_partitioned_mixed_array(self):
        """ Ensure that the array D, a mixed sequence, is partitioned. """
        D          = [3, 5, 4, 1, 2]  # Pivot element 3
        DPartition = [2, 1, 3, 5, 4]
        DPrime, k  = qS.partition(D, 0, 4)
        self.assertEqual(DPartition, DPrime)
        self.assertEqual(2, k)

    def test_error_raised_l_out_of_range(self):
        """ Ensure error is raised if l is out of range of A. """
        B = []
        # NB check type of error; syntax for below? Might be (B, 0, 0)
        self.assertRaises(IndexError, qS.partition, B, 0, 0)

    def test_error_raised_r_out_of_range(self):
        """ Ensure error is raised if r is out of range of A. """
        B = [100, 1, 2, 3, 4, 5, 1000]
        # Check type of error and syntax
        self.assertRaises(IndexError, qS.partition, B, 0, 7)

#-------------------------------------------------------------------------------
class TestSelectPivot(unittest.TestCase):
    """ Unit test selectPivot subroutine. """

    def test_given_pivot_selected(self):
        """ Check correct pivot is chosen.

            This utilises setting the random seed twice.
        """
        B = [100, 1, 2, 3, 4, 5, 1000]
        np.random.seed(936231120)
        l = 1
        r = 5
        
        i    = int(round(np.random.rand() * (r - l) + l))
        # Swap elements
        temp = B[i]
        B[i] = B[l]
        B[l] = temp

        np.random.seed(936231120)
        BPrime = qS.selectPivot(B, l, r)

        self.assertEquals(B, BPrime)
        
    def test_error_raised_l_out_of_range(self):
        """ Ensure error is raised if l is out of range of A. """
        B = [100, 1, 2, 3, 4, 5, 1000]
        l = 9
        r = 10
        # Check error type, syntax for below
        self.assertRaises(IndexError, qS.selectPivot, B, l, r)

    def test_error_raised_r_out_of_range(self):
        """ Ensure error is raised if r is out of range of A. """
        np.random.seed(19552314)
        B = [100, 1, 2, 3, 4, 5, 1000]
        l = 1
        r = 8
        # Check error type, syntax for below
        self.assertRaises(IndexError, qS.selectPivot, B, l, r)

        
#-------------------------------------------------------------------------------
class TestQuickSort(unittest.TestCase):
    """ Unit test quickSort subroutine. """

    def test_base_case(self):
        """ Does providing an input array of length 1 return the same array? """
        B = [1]
        self.assertEqual(B, qS.quickSort(B, 0, 0))

    def test_array_of_length_5(self):
        """ Does an array of length 5 get correctly sorted? """
        D      = [3, 5, 4, 1, 2]
        DPrime = [1, 2, 3, 4, 5]
        self.assertEqual(DPrime, qS.quickSort(D, 0, 4))
        
    def test_if_l_out_of_array_array_returned(self):
        """ Is the original array returned if l is outside of array? """
        D = [3, 5, 4, 1, 2]
        self.assertEqual(D, qS.quickSort(D, 8, 4))

    def test_error_if_r_in_array(self):
        """ Is an error raised if r outside of array? """
        D      = [3, 5, 4, 1, 2]
        self.assertRaises(IndexError, qS.quickSort, D, 0, 6)


#===============================================================================        
if __name__ == '__main__':
    unittest.main()
