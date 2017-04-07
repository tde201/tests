# -*- coding: utf-8 -*-
"""
Script to answer question 3 of Algorithms II week 1 programming challenge. It is an 
implementation of Prim's MST algorithm (without using a heap).
"""

import numpy as np

def read_graph(fileName):
    """ Read a text file describing a graph.
    
    Format is: # vertices, # edges on row 1, followed by (u, v, w) on succeeding rows where
    u is the start vertex, v the end vertex and w the weight of an edge.
    
    Args:
      fileName: The name of the text file.
      
    Returns:
      g: The graph as a adjacency list.
      numEdges: Integer. Number of edges in the graph.
      numVertices: Integer. Number of vertices in the graph.
   """
   
    g = list()
    
    with open(fileName, 'r') as graphFile:
        for lineNum, line in enumerate(graphFile):
            row = line.strip('\n')
            data = row.split(' ')
            if lineNum == 0:
                numVertices = int(data[0])
                numEdges = int(data[1])
            else:
                g.append(tuple(map(int, data)))
                
    return g, numEdges, numVertices

def prims_MST_algorithm(g, numVertices):
    # Initialise set X containing one arbitrary vertex s
    V = set(range(1, numVertices + 1))
    VNotX = set(range(2, numVertices + 1))
    X = set([1])
    
    # Initialise set T as empty. This is the spanning tree.
    T = set()
    costMST = 0
    
    while X != V:
        # let e = [u, v] be the cheapest edge of G with u in X and v not in X
        eWeight = np.inf
        for u, v, w in g:
            if ((u in X and v in VNotX) and
                (w < eWeight)):
                eWeight = w
                edge = (u, v, w) 
            elif((v in X and u in VNotX) and
                 (w < eWeight)):
                eWeight = w
                edge = (v, u, w)
                    
        # add e to T
        T.add(edge)
        
        # add v to X
        X.add(edge[1])
        VNotX.remove(edge[1])
        
        # cost_MST add cost of edge to this.
        costMST += eWeight
        
    return X, T, costMST
        
if __name__ == "__main__":
    fileName = 'edges.txt'
    g, numEdges, numVertices = read_graph(fileName)
    X, T, costMST = prims_MST_algorithm(g, numVertices)
    print costMST