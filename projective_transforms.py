# -*- coding: utf-8 -*-
"""
Projective geometry tests.
"""

import numpy as np

def p_img(p, f):
    """ Project the point p into a 2D image plane via a pinhole camera model with focal length f.
    
    Args:
      p: Numpy array, (x, y, z) coordinates of point in space.
      f: Focal length of pinhole camera model.
      
    Returns:
      p_prime: Numpy array, (u, v) coordinates of the point in the projection plane.
    """
    # Transform p into homogeneous coordinates
    p = np.concatenate((p, [1]))
    
    proj_matrix = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1/f, 0]])
    
    projected_p = np.dot(proj_matrix, p)
    
    # Convert to non-homogeneous coordinates in the projected plane.
    p_prime = np.array([projected_p[0] / projected_p[2], projected_p[1] / projected_p[2]])
    
    return p_prime

if __name__ == "__main__":
    p = np.array([200, 100, 100])
    f = 50.0
    
    p_prime = p_img(p, f)
    
    print p_prime
    
    