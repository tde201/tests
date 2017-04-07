""" Implements Breadth First Search (BFS) and finds the shortest path using
    BFS.
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
def BFS(G, s):
    """ Breadth First Search (BFS) of a graph G, starting from node s.

        Args:
          G: adjacency list representation of a graph.
          s: start node.

        Returns:
          exploredList: A dictionary giving a boolean value for whether a node
                        has been explored or not.

        Raises:
          None.
    """
    
    exploredList = dict.fromkeys(G.keys(), 0)  # Initialise as zero

    # Mark s as explored
    exploredList[s] = 1

    # Define a queue with s as the only entry (so far)
    Q = Queue.Queue()
    Q.put(s)

    while not Q.empty():
        v = Q.get()  # remove first entry of the queue
        
        for w in G[v]:  # Look at each node w connected to v
            if not exploredList[w]:  # if w has not been explored
                exploredList[w] = 1  # mark as explored
                Q.put(w)             # add to queue

    return exploredList

#-------------------------------------------------------------------------------
def BFSShortestPath(G, s):
    """ Find shortest paths using Breadth First Search (BFS).

        Args:
          G: adjacency list representation of a graph.
          s: start node.

        Returns:
          dist: dictionary giving distance (in # edges) of node from s.

        Raises:
          None.
    """

    exploredList = dict.fromkeys(G.keys(), 0)  # Initialise as zero
    dist = dict.fromkeys(G.keys(), np.inf)

    # Mark s as explored and set dist[s] = 0
    exploredList[s] = 1
    dist[s] = 0

    # Define a queue with s as the only entry (so far)
    Q = Queue.Queue()
    Q.put(s)

    while not Q.empty():
        v = Q.get()  # remove first entry of the queue
        
        for w in G[v]:  # Look at each node w connected to v
            if not exploredList[w]:  # if w has not been explored
                exploredList[w] = 1  # mark as explored
                Q.put(w)             # add to queue
                dist[w] = dist[v] + 1

    return dist

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
    G[1] = [0, 3]
    G[2] = [0, 3, 4]
    G[3] = [1, 2, 4, 5]
    G[4] = [2, 3, 5]
    G[5] = [4, 5]
    G[6] = []

    # Start node
    s = 0
    exploredList = BFS(G, s)
    dist         = BFSShortestPath(G, s)
    print exploredList
    print dist
    

#===============================================================================
if __name__ == "__main__":
    main(sys.argv)
