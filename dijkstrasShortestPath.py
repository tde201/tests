""" Dijkstra's shortest path algorithm.

    Find the shortest path between a specified node and all other nodes in a
    graph. Implemented using two Heaps. The Heap class comes from the heap.py
    module.

    Improvement: Make heap implementation as a priority queue i.e. so each key
    has a value attached, and there is a method to update key values. Add an
    isEmpty method to the heap implementation as well.
"""
#===============================================================================
import numpy as np
import heap

#===============================================================================
class Variables():

    def __init__(self, gGraph, sNode):
        self.exploredNodes = [sNode]  # Region explored
        self.graphNodes    = gGraph.keys()  # Nodes in graph
        self.shortestPathLength = {}  # Shortest path lengths from sNode to key
        self.shortestRoute      = {}  # Shortest path routes from sNode to key
        self.shortestPathLength[sNode] = 0   # Path from sNode to sNode is zero
        self.shortestRoute[sNode]      = [sNode]  # Shortest route to sNode
        

    def addExploredNodeAndPath(self, vNode, wNode, pathLength):
        self.exploredNodes.append(wNode)
        self.shortestPathLength[wNode] = pathLength
        oldShortestRoute = self.shortestRoute[vNode]
        self.shortestRoute[wNode] = oldShortestRoute + [wNode]


#-------------------------------------------------------------------------------
class HeapVariables(heap.Heap):
    
    def __init__(self, gGraph, sNode):
        self.exploredNodes = [sNode]  # Region explored
        self.graphNodes    = gGraph.keys()  # Nodes in graph
        
        # Invariant 1, the heap has all vertices of the unexplored region.
        # Invariant 2, a heap with the smallest Dijkstra greed score of an edge
        # (u, v) where u in the explored set of nodes and v is in the
        # unexplored set of nodes. Set to +inf if no such edge exists.
        self.key = {}
        self.nodeToKey ={}  # Dictionary of nodes to keys. Only add in non-infs
        keyArray = [np.inf] * (len(self.graphNodes) - 1)  # for not sNode
        keyArray.append(0)  # for sNode
        
        for iNode in gGraph.keys():
            if iNode == sNode:
                self.key[iNode] = 0
                self.nodeToKey[0] = iNode
            else:
                self.key[iNode] = np.inf

        self.unexploredHeap = heap.Heap(keyArray)
        
        
#-------------------------------------------------------------------------------
def shortestPathNoHeap(gGraph, sNode):
    
    variables = Variables(gGraph, sNode)

    while set(variables.exploredNodes) != set(variables.graphNodes):

        greedyCriterion = np.inf

        # NB assumption that graph is connected
        for vNode in variables.exploredNodes:

            vEdges = gGraph[vNode]
            pathLengthToV = variables.shortestPathLength[vNode]

            for wNode, vwLength in vEdges.iteritems():
                if wNode not in variables.exploredNodes:
                    
                    pathLength = pathLengthToV + vwLength
                    
                    if pathLength < greedyCriterion:
                        greedyCriterion = pathLength
                        vStarNode = vNode
                        wStarNode = wNode

        variables.addExploredNodeAndPath(vStarNode, wStarNode, greedyCriterion)

    return variables

#-------------------------------------------------------------------------------
def shortestPath(gGraph, sNode):

    variables = HeapVariables(gGraph, sNode)
    
    while variables.unexploredHeap.heap != []:

        # Choose the key from the heap with the lowest value.
        wKey  = variables.unexploredHeap.extractMin()
        wNode = variables.nodeToKey[wKey]  # Find the node with this key

        # Update our list of explored nodes.
        variables.exploredNodes.append(wNode)
        
        for vNode, wvLength in gGraph[wNode].iteritems():
            if vNode not in variables.exploredNodes:

                vKey = variables.key[vNode]

                # Delete the vKey from the heap
                variables.unexploredHeap.delete(vKey)

                # Update the shortest path route using Dijkstra's greedy
                # criteria.
                variables.key[vNode] = min(vKey, wKey + wvLength)

                # Re-insert to the heap with a new key value.
                variables.unexploredHeap.insert(variables.key[vNode])

                # Update our dictionary of key-values to nodes.
                variables.nodeToKey[variables.key[vNode]] = vNode
                
    return variables

#===============================================================================
def main():
    gGraph = {}
    gGraph[0] = {1: 8, 3: 15}
    gGraph[1] = {2: 14, 3: 3}
    gGraph[2] = {4: 12}
    gGraph[3] = {2: 7, 4: 17}
    gGraph[4] = {4: 0}

    variables = shortestPathNoHeap(gGraph, 0)

    print variables.shortestPathLength
    print variables.shortestRoute

    heapVariables = shortestPath(gGraph, 0)

    print heapVariables.key

#===============================================================================
if __name__ == "__main__":
    main()
