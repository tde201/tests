# -*- coding: utf-8 -*-
"""
Script to solve programming task 5 for Algorithms 2.

Task: Find the minimum cost of a travelling salesman tour of a graph.

Input: Text file noting the number of nodes and the (x, y) coordinates of the nodes. The distance between them is
       given by the Euclidean distance.
"""
import numpy as np
import math
import itertools
import matplotlib.pyplot as plt
from copy import deepcopy

def euclidean_distance((x_1, y_1), (x_2, y_2)):
    """ Find the Euclidean distance between two points. """
    return np.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

def read_file(file_name):
    """ Read the <file_name> file.
    
    Fomat: Number of nodes (line 0), (x, y) coordinates of each node on subsequent lines.
    
    Input:
      file_name: Name of file.
      
    Returns:
      distance_mat: A distance matrix between nodes.
    """
    nodes = list()
#    distance_mat = dict()
    with open(file_name, 'r') as fn:
        for num, line in enumerate(fn):
            data = line.split(' ')
            if num == 0:
                num_nodes = int(data[0])
                
            else:
                nodes.append((float(data[0]), float(data[1])))
    
    plot_cities(nodes)
    
    distance_mat =[[0] * num_nodes for _ in range(num_nodes)] #np.empty([num_nodes, num_nodes])
    for n in range(num_nodes):
        for m in range(num_nodes):
            distance_mat[n][m] = euclidean_distance(nodes[n], nodes[m])
#            distance_mat[n, m] = euclidean_distance(nodes[n], nodes[m])
            
    return distance_mat, num_nodes

def plot_cities(nodes):
    """ Plot the tour cities. """
    xy_list = zip(*nodes)
    plt.scatter(xy_list[0], xy_list[1])
    for n in range(len(nodes)):
        plt.annotate(n, (xy_list[0][n], xy_list[1][n]))
    

def tsp(distance_mat, n, s=0):
    """ Use a dynamic program to find the shortest tour through the set of nodes.
    
    Input:
      distance_mat: Matrix of distances between nodes.
      n: Integer. Number of vertices on tour.
      s: Integer. Start vertex. Default = 0.
      
    Returns:
      shortest_tour_len: The length of the shortest tour.
    """
    # Initialisation
    nodes = range(1, n)
    A_last = dict(((X, [distance_mat[0][X[0]]]) for X in itertools.combinations(nodes, 1)))
    for m in range(2, n):
        A = dict(((X, [0] * m) for X in itertools.combinations(nodes, m)))
        for X in A.keys():
            for p, j in enumerate(X):
                X_prime = tuple(k for k in X if k != j)
                A[X][p] = min(A_last[X_prime][q] + distance_mat[k][j] for q, k in enumerate(X_prime))
        A_last = A
        print 'm:', m, len(A)
     
    complete_set = tuple(nodes)
    candidate_mins = (A[complete_set][p] + distance_mat[k][s] for p, k in enumerate(complete_set))
    min_path = min(candidate_mins)
    
    return min_path

def nCr(n, r):
    f = math.factorial
    return f(n) / f(r) / f(n - r)

def tsp_table(distance_mat, n, s=0):
    nodes = range(1, n)  # assuming s = 0
    B = distance_mat[s, 1:]
    B_subsets = tuple(itertools.combinations(nodes, 1))
    for m in range(2, n):
        A_subsets = tuple(itertools.combinations(nodes, m))
        A_keys = ((X, j) for X in A_subsets for j in X)
        A = np.empty(nCr(n - 1, m) * m)
        for p, (X, j) in enumerate(A_keys):
            X_prime = tuple(k for k in X if k != j)
            start = B_subsets.index(X_prime) * (m - 1)
            end = start + m - 1
#            distances = np.array([distance_mat[k, j] for k in X_prime])
            distances = distance_mat[X_prime, j]
            A[p] = min(B[start:end] + distances)
                
        B = deepcopy(A)
        B_subsets = deepcopy(A_subsets)
        print m
    
    min_path = np.inf
    all_subsets = itertools.combinations(nodes, n - 1)
    B_keys = ((X, j) for X in all_subsets for j in X)
    for p, (X, j) in enumerate(B_keys):
        min_path = min(B + distance_mat[0, 1:])
                
    return min_path
        
if __name__ == "__main__":
    file_name = 'tsp.txt'
    distance_mat, num_nodes = read_file(file_name)
    min_path = tsp(distance_mat, num_nodes)
    print min_path
    
    # Test
    file_name = 'tsp_test.txt'
    distance_mat1, num_nodes = read_file(file_name)
    print distance_mat1
    min_path = tsp(distance_mat1, num_nodes)
#    min_table_path = tsp_table(distance_mat1, num_nodes)
    print min_path  #, min_table_path
    
#    distance_mat = {(0, 0):0, (0, 1):1, (0, 2):3, (0, 3):6,
#                    (1, 0):1, (1, 1):0, (1, 2):2, (1, 3):4,
#                    (2, 0):3, (2, 1):2, (2, 2):0, (2, 3):5,
#                    (3, 0):6, (3, 1):4, (3, 2):5, (3, 3):0}
    distance_mat = np.array([[0, 1, 3, 6],
                    [1, 0, 2, 4],
                    [3, 2, 0, 5],
                    [6, 4, 5, 0]])
    min_path = tsp(distance_mat, 4)
#    min_table_path = tsp_table(distance_mat, 4)
    print min_path  #, min_table_path
    print min_path == 13