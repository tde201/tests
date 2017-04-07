""" Unit test functions in BFS module. """

#===============================================================================
import unittest
import numpy as np
import DFS


#===============================================================================
class TestDFS(unittest.TestCase):
    """ Unit test DFS. """

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

        exploredList    = DFS.DFS(G, s)
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
        
        exploredList    = DFS.DFS(G, s)
        expExploredList = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:0, 7:0}  # i.e. 6 & 7
                                                                    # unexplored

        self.assertEqual(expExploredList, exploredList)
        
        
#-------------------------------------------------------------------------------
class TestDFSRecursive(unittest.TestCase):
    """ Unit test DFSRecursive. """

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
        recursiveExp    = dict.fromkeys(G.keys(), 0)
        exploredList    = DFS.DFSRecursive(G, s, recursiveExp)
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
        recursiveExp    = dict.fromkeys(G.keys(), 0)
        exploredList    = DFS.DFSRecursive(G, s, recursiveExp)
        expExploredList = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:0, 7:0}  # i.e. 6 & 7
                                                                    # unexplored

        self.assertEqual(expExploredList, exploredList)
        

#-------------------------------------------------------------------------------
class TestDFSRecursive2(unittest.TestCase):
    """ Unit test DFSRecursive2. """

    def test_find_connected_elements(self):
        """ Is a connected node explored? """
        
        # Adjacency List of graph G
        G    = {}
        G[0] = [1, 2]
        G[1] = [3]
        G[2] = [4]
        G[3] = [4, 5]
        G[4] = [5]
        G[5] = []

        # Start node
        s = 0
        currentLabel = len(G.keys())
        recursiveExp = dict.fromkeys(G.keys(), 0)
        nodeOrder    = dict.fromkeys(G.keys())
        exploredList, nodeOrder, currentLabel = DFS.DFSRecursive2(G, s,
                                                    recursiveExp, nodeOrder,
                                                    currentLabel)
        expExploredList = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1}  # i.e. all explored
        nodeOrderExp    = {0:1, 1:3, 2:2, 3:4, 4:5, 5:6}
        self.assertEqual(expExploredList, exploredList)
        self.assertEqual(nodeOrderExp, nodeOrder)


    def test_do_not_find_unconnected_element(self):
        """ Does an unconnected node remain unexplored? """
        
        # Adjacency List of graph G
        G    = {}
        G[0] = [1, 2]
        G[1] = [3]
        G[2] = [4]
        G[3] = [4, 5]
        G[4] = [5]
        G[5] = []
        G[6] = [7]
        G[7] = []

        # Start node
        s = 0
        currentLabel = len(G.keys())
        recursiveExp = dict.fromkeys(G.keys(), 0)
        nodeOrder    = dict.fromkeys(G.keys())
        exploredList, nodeOrder, currentLabel = DFS.DFSRecursive2(G, s,
                                                    recursiveExp, nodeOrder,
                                                    currentLabel)
        expExploredList = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:0, 7:0}  # i.e. 6 & 7
                                                                    # unexplored
        nodeOrderExp    = {0:3, 1:5, 2:4, 3:6, 4:7, 5:8, 6:None, 7:None}
        self.assertEqual(expExploredList, exploredList)
        self.assertEqual(nodeOrderExp, nodeOrder)

        
#===============================================================================        
if __name__ == '__main__':
    unittest.main()
