""" Implements Depth First Search (DFS) and finds the shortest path using
    DFS.
"""
#===============================================================================
import sys
import numpy as np
import Queue


#===============================================================================
def readFile(inputFile):
    """ Read an adjacency list from an input file.

        Args:
          inputFile: The input file name and location.

        Returns:
          G: An adjacency list representation of a graph.

        Raises:
          IOError: If the file cannot be opened.
    """

    try:
        inF = open(inputFile, 'r')
    except:
        print 'Cannot open', inputFile
        return 1

    adjList = {}
    for line in inF:
        linedata = line.rstrip('\n').split()
        key      = int(linedata[0])
        value    = []
        for i in range(1, len(linedata)):
            value.append(int(linedata[i]))
        adjList[key] = value
        
    inF.close()
    
    return adjList

#-------------------------------------------------------------------------------
def DFS(G, s):
    """ Depth First Search (DFS) of a graph G, starting from node s.

        Args:
          G: adjacency list representation of a graph.
          s: start node.

        Returns:
          exploredList: A dictionary giving a boolean value for whether a node
                        has been explored or not.

        Raises:
          None.
    """
    
    exploredList = dict.fromkeys(G.keys(), 0)  # Initialise as zero (False)

    # Define a stack (last in first out, lifo, queue) with s as the only entry
    # (so far)
    S = Queue.LifoQueue()
    S.put(s)

    while not S.empty():
        v = S.get()  # remove last entry of the stack
        
        if not exploredList[v]:  # If it has been explored go back 1 step
            exploredList[v] = 1  # Mark as explored
            
            for w in G[v]:  # Look at each node w connected to v
                S.put(w)    # add to stack

    return exploredList

#-------------------------------------------------------------------------------
def DFSRecursive(G, s, exploredList):
    """ Depth First Search (DFS) of a graph G, starting from node s recursively.

        Args:
          G:            adjacency list representation of a graph.
          s:            start node.
          exploredList: Dictionary giving a boolean value for whehter a node has
                        been explored or not.

        Returns:
          exploredList: Dictionary giving a boolean value for whether a node has
                        been explored or not.

        Raises:
          None.
    """

    exploredList[s] = 1  # Mark s as explored

    for v in G[s]:
        if not exploredList[v]:
            exploredList = DFSRecursive(G, v, exploredList)

    return exploredList

#-------------------------------------------------------------------------------
def DFSRecursive2(G, s, exploredList, nodeOrder, currentLabel):
    """ Depth First Search (DFS) of a graph G, starting from node s recursively.

        Args:
          G:            adjacency list representation of a graph.
          s:            start node.
          exploredList: Dictionary giving a boolean value for whehter a node has
                        been explored or not.
          nodeOrder:    Dictionary listing order of each node.
          currentLabel: Current node label.

        Returns:
          exploredList: Dictionary giving a boolean value for whether a node has
                        been explored or not.
          nodeOrder:    Dictionary listing order of each node.
          currentLabel: Current node label.

        Raises:
          None.
    """

    exploredList[s] = 1  # Mark s as explored

    for v in G[s]:
        if not exploredList[v]:
            exploredList, nodeOrder, currentLabel = DFSRecursive2(G, v,
                                                        exploredList, nodeOrder,
                                                        currentLabel)
    
    nodeOrder[s]  = currentLabel
    
    currentLabel -= 1

    return exploredList, nodeOrder, currentLabel

#-------------------------------------------------------------------------------
def topologicalOrder(G):
    """ Topologically order nodes a graph using DFS.

        Args:
          G: Adjacency list of a graph.

        Returns:
          nodeOrder: Order of nodes.

        Raises:
          None.
    """
    
    exploredList = dict.fromkeys(G.keys(), 0)  # Initialise as zero
    nodeOrder    = dict.fromkeys(G.keys())

    currentLabel = len(G.keys())

    for v in G:
        if not exploredList[v]:
            exploredList, nodeOrder, currentLabel = DFSRecursive2(G, v,
                                                       exploredList, nodeOrder,
                                                       currentLabel)

    return nodeOrder
            
#-------------------------------------------------------------------------------
def main(args):
    """ Run main code.

        Read input file in the form of an adjancency list.
        Call BFS
        print exploredList

        Args:
          args: Command line arguments.

        Results:
          prints exploredList

        Raises:
          sys.exit: if there are not 2 arguments in call from command line.
    """

    # Adjacency List of graph G
    G    = {}
    G[0] = [1, 2]
    G[1] = [0, 2, 3]
    G[2] = [0, 1, 4]
    G[3] = [1, 4, 5]
    G[4] = [2, 3, 5]
    G[5] = [3, 4]

    # Start node
    s = 0
    exploredList = DFS(G, s)
    recursiveExp = dict.fromkeys(G.keys(), 0)  # Initialise as zero
    recursiveExp = DFSRecursive(G, s, recursiveExp)
    nodeOrder = topologicalOrder(G)
    print exploredList
    print recursiveExp
    print nodeOrder
    

#===============================================================================
if __name__ == "__main__":
    main(sys.argv)
