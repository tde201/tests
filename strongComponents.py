""" Compute the strong components of a directed graph using Kosaraju's two-pass
    algorithm.
"""
#===============================================================================
import sys
import numpy as np
import Queue
import operator


#===============================================================================
def readInput(inputFile):

    try:
        inF = open(inputFile, 'r')
    except:
        print 'Cannot open', inputFile
        return 1
    
    keyRange = range(1, 10)

    G    = dict.fromkeys(keyRange)
    Grev = dict.fromkeys(keyRange)

    for line in inF:
        linedata = line.split()
        node1 = int(linedata[0])
        node2 = int(linedata[1])

        if G[node1] == None:
            G[node1] = [node2]
        else:
            G[node1].append(node2)
            
        if Grev[node2] == None:
            Grev[node2] = [node1]
        else:
            Grev[node2].append(node1)
    
    inF.close()
    
    return G, Grev

#-------------------------------------------------------------------------------
def DFSLoop(G, nodeOrder):
    """ Run DFS to find the strongly connected components of the graph G.

        Args:
          G: Adjacency list of graph G.

        Returns:
          leader:     List of what the leading node is for each node.
          finishTime: List of finish time for each node.

        Raises:
          None.
    """

    t = 0
    s = None
    n = len(G.keys())
    explored   = dict.fromkeys(G.keys(), 0)
    finishTime = dict.fromkeys(G.keys(), None)
    leader     = dict.fromkeys(G.keys(), None)

    for fTime in range(n, 0, -1):
        iNode = nodeOrder[fTime]  # Find the node with finishing time given
        if not explored[iNode]:
            s = fTime
            explored, finishTime, leader, s, t = (
                DFS(G, iNode, explored, finishTime, leader, s, t))

    return finishTime, leader

#-------------------------------------------------------------------------------
def DFS(G, iNode, explored, finishTime, leader, s, t):

    explored[iNode] = 1
    leader[iNode]   = s

    for jNode in G[iNode]:
        if explored[jNode] == 0:
            explored, finishTime, leader, s, t = (
                DFS(G, jNode, explored, finishTime, leader, s, t))

    t += 1
    finishTime[iNode] = t

    return explored, finishTime, leader, s, t
            
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

    inputFile = 'sCTest.txt'
    
    # Read Input File
    G, Grev = readInput(inputFile)
    
##    # Adjacency List of graph G
##    G    = {}
##    G[1] = [4]
##    G[2] = [8]
##    G[3] = [6]
##    G[4] = [7]
##    G[5] = [2]
##    G[6] = [9]
##    G[7] = [1]
##    G[8] = [5, 6]
##    G[9] = [3, 7]
##
##    Grev    = {}
##    Grev[1] = [7]
##    Grev[2] = [5]
##    Grev[3] = [9]
##    Grev[4] = [1]
##    Grev[5] = [8]
##    Grev[6] = [3, 8]
##    Grev[7] = [4, 9]
##    Grev[8] = [2]
##    Grev[9] = [6]
    
    nodeOrder = dict.fromkeys(G.keys(), 0)
    for iNode in range(1, len(G.keys()) + 1):
        nodeOrder[iNode] = iNode

    # First Pass on reverse graph    
    finishTime, leader = DFSLoop(Grev, nodeOrder)

    # Set nodeOrder by entries in finishTime
    for iNode, fTime in finishTime.iteritems():
        nodeOrder[fTime] = iNode
    
    # Second pass on forward graph
    finishTime, leader = DFSLoop(G, nodeOrder)

    print leader
    summary = {}
    for key, value in leader.iteritems():
        if value not in summary.keys():
            summary[value] = 1
        else:
            summary[value] += 1
    sortedSummary = sorted(summary.items(), key = operator.itemgetter(1))
    print sortedSummary

#===============================================================================
if __name__ == "__main__":
    main(sys.argv)
