""" Unit test functions in BFS module. """

#===============================================================================
import unittest
import numpy as np
import BFS


#===============================================================================
class TestBFS(unittest.TestCase):
    """ Unit test BFS. """

    def test_find_connected_elements(self):
        """ Is a connected node explored? """

        # Adjacency List of graph G
        G    = {}
        G[0] = [1, 2]
        G[1] = [0, 3]
        G[2] = [0, 3, 4]
        G[3] = [1, 2, 4, 5]
        G[4] = [2, 3, 5]
        G[5] = [4, 5]

        # Start node
        s = 0

        exploredList    = BFS.BFS(G, s)
        expExploredList = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1}  # i.e. all explored

        self.assertEqual(expExploredList, exploredList)


    def test_do_not_find_unconnected_element(self):
        """ Does an unconnected node remain unexplored? """
        
        # Adjacency List of graph G
        G    = {}
        G[0] = [1, 2]
        G[1] = [0, 3]
        G[2] = [0, 3, 4]
        G[3] = [1, 2, 4, 5]
        G[4] = [2, 3, 5]
        G[5] = [4, 5]
        G[6] = [7]
        G[7] = [6]

        # Start node
        s = 0
        
        exploredList    = BFS.BFS(G, s)
        expExploredList = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:0, 7:0}  # i.e. 6 & 7
                                                                    # unexplored

        self.assertEqual(expExploredList, exploredList)
        
        
#-------------------------------------------------------------------------------
class TestBFSShortestPath(unittest.TestCase):
    """ Unit test BFS. """

    def test_correctly_identify_shortest_path(self):
        """ Is the shortest path correctly identified? """

        # Adjacency List of graph G
        G    = {}
        G[0] = [1, 2]
        G[1] = [0, 3]
        G[2] = [0, 3, 4]
        G[3] = [1, 2, 4, 5]
        G[4] = [2, 3, 5]
        G[5] = [4, 5]

        # Start node
        s = 0
        
        dist    = BFS.BFSShortestPath(G, s)
        expDist = {0:0, 1:1, 2:1, 3:2, 4:2, 5:3}
        
        self.assertEqual(expDist, dist)
        

#===============================================================================        
if __name__ == '__main__':
    unittest.main()
