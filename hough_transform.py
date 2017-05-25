# -*- coding: utf-8 -*-
"""
Hough transform for straight lines implementation.

A Hough transform is a voting technique, this allows features that fit a parametric model to be recognized by the high
number of votes that are observed. To use a hough tranform to identify lines we:
    1) Use an edge detector (e.g. Canny edge detector) to identify pixels that form edges.
    2) For each point on an edge vote for parameters of straight lines that run through the point.
    3) Identify the lines which get the highest number of votes.
    4) Reconstruct the lines from the points which voted for them.
"""

import cv2
import numpy as np

class Hough_transform:
    """ Perform a Hough transform on an image to determine where the straight lines lie.
    
    TODO: Extra find the lines extend (need to keep account of which edge points voted for which lines to do this)
    
    Args:
      img: A greyscale image.
      d_bin_size: The size of the bin for the distance of the line from the origin. Default value 10 pixels.
      theta_bin_size: The size of the angular bin for the angle of the line with the x-axis. Default 1 degree.
      hough_threshold: Number of votes required to be considered a fit.
    """
    
    def __init__(self, img, d_bin_size=10, theta_bin_size=1, hough_threshold=10000):
        self.img = img
        self.img_lines = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        self.img_width = int(img.shape[1])
        self.img_height = int(img.shape[0])
        self.theta_vals = 360
        self.theta_bin_size = theta_bin_size
        self.theta_num_bins = int(self.theta_vals / float(self.theta_bin_size))
        self.theta_range = [(t + 0.5) * self.theta_bin_size for t in xrange(self.theta_num_bins)]
        self.d_vals = int(np.ceil(np.sqrt(self.img_width**2 + self.img_height**2)))
        self.d_bin_size = d_bin_size
        self.d_num_bins = int(self.d_vals / float(self.d_bin_size))
        self.d_range = [(d + 0.5) * self.d_bin_size for d in xrange(self.d_num_bins)]
        self.hough_treshold = hough_threshold
        
        # Find edges using Canny edge detection and create a set of points that lie on these edges.
        self.img_canny = cv2.Canny(img, 150, 200)
        self.set_edge_points()
        
        # Perform the Hough transform and reconstruct the image showing where the identified straight lines lie.
        self.init_hough_space()
        self.hough_transform()
        self.reconstruct_lines()
    
    def set_edge_points(self):
        """ Identify the set of edge points in the image from the Canny edge detected pixels. """
        # Create the set of all (x, y) coordinates of points on the edges
        # Must be a quicker way to do this!?!
        self.edge_set = set()
        for x in xrange(self.img_width):
            for y in xrange(self.img_height):
                if self.img_canny[y, x] > 0:
                    self.edge_set.add((x, y))
        
    def init_hough_space(self):
        """ Initialise the Hough space <H> with variables set in the class initialisation. """
        self.H = np.zeros((self.d_num_bins, self.theta_num_bins))
    
    def line_distance(self, x, y, theta):
        """ Determine the perpendicular to the line distance from the origin. """
        return x * np.cos(theta / 180.0 * np.pi) + y * np.sin(theta / 180.0 * np.pi)
    
    def d_bin(self, d):
        """ Find the bin in the Hough space that an line distance lies in. """
        return int(d / float(self.d_vals) * self.d_num_bins)
    
    def theta_bin(self, theta):
        """ Find the theta bin in the Hough space that a line distance lies in. """
        return int(theta / float(self.theta_vals) * self.theta_num_bins)
        
    def hough_transform(self):
        """ Perform the Hough transform. """
        # Hough algorithm
        self.init_hough_space()
        
        for (x, y) in self.edge_set:
            for theta in self.theta_range:
                d = self.line_distance(x, y, theta)
                d_bin_val = self.d_bin(d)
                theta_bin_val = self.theta_bin(theta)
                self.H[d_bin_val, theta_bin_val] += 1
    
    def line_points(self, d, theta):
        """ Find the points where the proposed line crosses the edges of the image. The line crosses exactly two image
        edges (within the height and width of the image). Use these to provide points to plot on the image.
        """
        # Each infinite straight line must intersect two edges.
        point_1 = None
        point_2 = None
        
        # Left edge
        x_0 = 0
        y_0 = d / np.sin(theta / 180.0 * np.pi) 
        
        # Right edge
        x_1 = self.img_width
        y_1 = (d - self.img_width * np.cos(theta / 180.0 * np.pi)) / np.sin(theta / 180.0 * np.pi) 
        
        # Top edge
        y_2 = 0
        x_2 = d / np.cos(theta / 180.0 * np.pi)
        
        # Bottom edge
        y_3 = self.img_height
        x_3 = (d - self.img_height * np.sin(theta / 180.0 * np.pi)) / np.cos(theta / 180.0 * np.pi)
        
        # NB Extending range by one pixel to guard against numerical errors.
        
        # The left i.e. x = 0 with y in range -1 to self.img_height + 1
        if (-1 <= y_0) and (y_0 <= self.img_height + 1):
                point_1 = (int(x_0), int(y_0))
        
        # The right i.e. x = self.img_width with y in range -1 to self.img_height + 1
        if (-1 <= y_1) and (y_1 <= self.img_height + 1):
            coord = (int(x_1), int(y_1))
            if not point_1:
                point_1 = coord
            else:
                point_2 = coord
        
        # The top i.e. y = 0 with x in range -1 to self.img_width + 1
        if (-1 <= x_2) and (x_2 <= self.img_width + 1):
            coord = (int(x_2), int(y_2))
            if not point_1:
                point_1 = coord
            else:
                point_2 = coord
        
        # The bottom i.e. y = self.img_height with x in range -1 to self.img_width + 1
        if (-1 <= x_3) and (x_3 <= self.img_width + 1):
            coord = (int(x_3), int(y_3))
            if not point_1:
                point_1 = coord
            else:
                point_2 = coord
        
        return (point_1, point_2)
    
    def reconstruct_lines(self):
        """ From the peaks identified in the Hough space, plot the corresponding lines on the original image for
        visualisation purposes.
        """
        # Find peaks in hough space
        output_line_values = ((d, theta) for d in self.d_range for theta in self.theta_range if 
                              self.H[self.d_bin(d), self.theta_bin(theta)] > self.hough_treshold)
        
        # Plot them on the image
        for d, theta in output_line_values:
            point_1, point_2 = self.line_points(d, theta)
            print d, theta, point_1, point_2
            cv2.line(self.img_lines, point_1, point_2, color=(255, 0, 0), thickness=3)
    
    def show_original_image(self, show_standalone=False):
        """ Show the originial image. """
        cv2.imshow('Original image', self.img)
        if not show_standalone:
            cv2.waitKey(0) 
    
    def show_canny_edge_image(self, show_standalone=False):
        """ Show the Canny edges depicted in the image. """
        cv2.imshow('Canny Edge lines', self.img_canny)
        if not show_standalone:
            cv2.waitKey(0)      
        
    def show_hough_space(self, show_standalone=False):
        """ Show the Hough space as an image. """
        min_val = np.min(self.H)
        max_val = np.max(self.H)
        print 'Maximum bin count in Hough space is:', max_val
        H_img = np.uint8((self.H - min_val) / float(max_val) * 255)
        cv2.imshow('Hough image', H_img)
        if not show_standalone:
            cv2.waitKey(0)
        
    def show_image_with_lines(self, show_standalone=False):
        cv2.imshow('Image with lines identified', self.img_lines)
        if not show_standalone:
            cv2.waitKey(0)
        
    def show_results(self):
        """ Show all the images generated: original, canny edge image, hough space and image with lines identified. """
        self.show_original_image(True)
        self.show_canny_edge_image(True)
        self.show_hough_space(True)
        self.show_image_with_lines(True)
        cv2.waitKey(0)

if __name__ == "__main__":
    img_file = 'football_pitch.jpg'
    
    img = cv2.imread(img_file)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Create an image with one vertical stripe and one horizontal stripe
    black_stripe = np.zeros((50, 150), dtype='uint8')
    white_stripe = np.ones((50, 150), dtype='uint8') * 255
    horz_stripe = np.vstack([white_stripe, black_stripe, white_stripe])
    vert_stripe = np.hstack([white_stripe.transpose(), black_stripe.transpose(), white_stripe.transpose()])
    diagonal_line = np.ones((100, 300), dtype='uint8') * 255
    cv2.line(diagonal_line,(200, 0), (300, 100), (0, 0, 0), 5)
    
#    hough_line_img = Hough_transform(horz_stripe, d_bin_size=1, theta_bin_size=0.5, hough_threshold=148)
#    hough_line_img = Hough_transform(vert_stripe, d_bin_size=1, theta_bin_size=0.5, hough_threshold=148)
#    hough_line_img = Hough_transform(diagonal_line, d_bin_size=1, theta_bin_size=1, hough_threshold=115)
    hough_line_img = Hough_transform(img_grey, d_bin_size=1, theta_bin_size=1, hough_threshold=100)
    hough_line_img.show_results()
    
