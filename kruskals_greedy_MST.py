# -*- coding: utf-8 -*-
"""
Kruksal's algorithm, Dasgupta p.138. A greedy algorithm to find a MST of a graph.

Requires |V| makeset operations, 2|E| find operations, |V| - 1 union operations.

procedure kruskal(G,w)
Input: A connected undirected graph G = (V, E) with edge weights w
Output: A minimum spanning tree defined by the edges X

for all u in V :
    makeset(u)
    
X = {}
Sort the edges E by weight
for all edges {u, v} in E, in increasing order of weight:
    if find(u) != find(v):
        add edge {u, v} to X
        union(u, v)

TODO: Store sets as unions by rank, p.138 onward.

Created on Wed Aug 31 16:42:51 2016

@author: Torran
"""
import operator

class Kruskal():
    
    def __init__(self, G):
        self.X = {}
        self.sets = []
        self.V = G['V']  # Vertices
        self.E = G['E']  # Edges
        self.E_sorted = sorted(self.E.items(), key=operator.itemgetter(1))  # Sorted edges
        print self.E_sorted
        for u in self.V:
            self.makeset(u)
        print self.sets
        
    def makeset(self, u):
        """ Create a singleton set containing just u. """
        self.sets.append({u})
        
    def find(self, u):
        """ Find which set u belongs to. """
        for iCounter, setMembers in enumerate(self.sets):
            if u in setMembers:
                return iCounter
    
    def union(self, x, y):
        """ Merge sets containing x and y. """
        xCounter = self.find(x)
        xSet = self.sets.pop(xCounter)
        yCounter = self.find(y)        
        ySet = self.sets.pop(yCounter)
        xSet.update(ySet)
        print xCounter, yCounter, xSet
        self.sets.append(xSet)
        
    def procedureKruskal(self):
        """ Run Kruskal's greedy algorithm. """
        for ((u, v), weight) in self.E_sorted:
            print u, self.find(u), v, self.find(v), weight
            if self.find(u) != self.find(v):
                print u, v, weight
                self.X[(u, v)] = weight
                self.union(u, v)

if __name__ == "__main__":
    # Create graph, as shown on p.137 of Disgupta.
    G = {'V':{'A', 'B', 'C', 'D', 'E', 'F'}, 
         'E':{('A', 'B'): 2,
            ('A', 'C'): 1,
            ('B', 'C'): 2,
            ('B', 'D'): 1,
            ('C', 'D'): 2,
            ('C', 'E'): 3,
            ('D', 'E'): 3,
            ('D', 'F'): 4,
            ('E', 'F'): 1}}
    
    kruskalObj = Kruskal(G)
    kruskalObj.procedureKruskal()
    print kruskalObj.X
    