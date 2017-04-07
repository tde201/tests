# -*- coding: utf-8 -*-
"""
OpenCV tests
"""

import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt

def display_image_and_attributes(img):
    """ Display the input image, and its attributes. """
    cv2.imshow('Ship', img)
    cv2.waitKey(0)
    
    # Display image size
    print 'image size: {:,}'.format(np.size(img))
    print 'with dimension:', img.shape  # Equivalent to np.shape(img)
    
    # Display image type
    print 'image type:', type(img)
    print 'with data values:', img.dtype
    
    # Display a value of a pixel at a particular point
    print 'Value of pixel at 100, 150:', img[100, 150]

def plot_slice_show_slice_crop(img):
    """ Plot the value of one channel in a horizontal slice across the image. Show the slice on the image and crop the
    image above this slice.
    """    
    # Plot the values in a vertical slice down column 100, for the B channel [0->B, 1-> G, 2-> R]; note in Matplotlib
    # it is RGB.
    plt.plot(img[:, 100, 0])
    plt.show()
    
    # Next plot a blue horizontal line in an image
    img_line = img.copy()
    cv2.line(img_line, (0, 100), (img_line.shape[1], 100), (255, 0, 0), 5)
    cv2.imshow('Ship with line', img_line)
    
    # Crop the image and display by dislaying everything above the line.
    img_crop = img[:100, :]  # so note that we have img[rows, cols, color] but referring to a pixel is (x, y, color)!!!
    cv2.imshow('Ship cropped', img_crop)
    cv2.waitKey(0)

def alpha_blend(img_A, img_B, alpha):
    """ Blend <alpha> of <img_A> with (1 - <alpha>) of <img_B>, show the blended image.
    
    Args:
      img_A: Image.
      img_B: Image.
      alpha: Float between 0 and 1.
    
    Returns:
      blend: Alpha-blend of img_A and img_B.
    """
#    blend = alpha * img_A + (1 - alpha) * img_B  # This is wrong as it converts uint8 to float!
    blend = np.uint8(alpha * img_A + (1 - alpha) * img_B)
    return blend

def scale_2_images(img_A, img_B):
    """ Scale two images to be the same size, choosing the minimum of the widths and heights.
    
    Args:
      img_A: Image.
      img_B: Image.
    
    Returns:
      scaled_img_A: Scaled image.
      scaled_img_B: Scaled image.
    """
    # Add two images (first converting to greyscale and scaling to be the same size.)
    h1, w1, c1 = img_A.shape
    h2, w2, c2 = img_B.shape
    
    # Choose width and height to be the minimum value between the two images.
    width = min(w1, w2)
    height = min(h1, h2)
    scaled_img_A = cv2.resize(img_A, (width, height))
    scaled_img_B = cv2.resize(img_B, (width, height))
    return scaled_img_A, scaled_img_B

def adding_images_tests(img_A, img_B):
    """ Add two images (first converting to greyscale and scaling to be the same size.) Plot the results of different
    ways of adding the images.
    """
    # Scale images to be the same size.
    img_A_std_size, img_B_std_size = scale_2_images(img_A, img_B)
    
    # Convert to greyscale
    img_A_std_size = cv2.cvtColor(img_A_std_size, cv2.COLOR_BGR2GRAY)
    img_B_std_size = cv2.cvtColor(img_B_std_size, cv2.COLOR_BGR2GRAY)
    
    
    mix = img_A_std_size + img_B_std_size  # Note values will be truncated at 255, meaning the image is oversaturated
    avg1 = img_A_std_size / 2 + img_B_std_size / 2  # Gives a true average image
    avg2 = (img_A_std_size + img_B_std_size) / 2  # Note that this is not the same as the above; the sum is performed
                                                # first meaning values are truncated at 255, then divided by 2, giving
                                                # an overall lighter image.
    blend = alpha_blend(img_A_std_size, img_B_std_size, 0.25)
    
    cv2.imshow('mix', mix)
    cv2.imshow('avg1', avg1)
    cv2.imshow('avg2', avg2)
    cv2.imshow('blend', blend)
    cv2.waitKey(0)

def add_gaussian_noise(img, mu=0, sigma=2):
    """ Add Guassian noise with mean <mu> and sd <sigma> to image <img>.
    
    Args:
      img: Image.
      mu: Mean of noise. Default value 0.
      sigma: SD of noise. Default value 2.
    
    Returns:
      noisy_img: The img with noise added.
    """
    img_dimension = img.shape
    noise = np.uint8(np.random.normal(mu, sigma, img_dimension))
    print img.size, noise.size
    noisy_img = img + noise
    return noisy_img

def make_noisy_img(img):
    """ Show an image with Gaussian noise added. """
    noisy_img = add_gaussian_noise(img, 10, 10)
    cv2.imshow('Image with noise', noisy_img)
    cv2.waitKey(0)

def subtract_images_test(img_A, img_B):
    """ Subtract the images from each other (in both possible ways), and determine the absolute difference of the
    images. Display the results.
    """
    # Subtract two images from each other. NB ordering matters.Lighter=> more differences. Actually interested in the
    # absolute difference between images. Consider what happens with uint8 - note that if the difference in pixel
    # values for images A and B at i is negative this gets rounded to zero. Hence must use (A-B) + (A+B). This is 
    # True in Matlab is it True in openCV as well? Is there a built in value?
    img_A_std_size, img_B_std_size = scale_2_images(img_A, img_B)
    
    # Convert to greyscale for ease of viewing
    img_A_std_size = cv2.cvtColor(img_A_std_size, cv2.COLOR_BGR2GRAY)
    img_B_std_size = cv2.cvtColor(img_B_std_size, cv2.COLOR_BGR2GRAY)
    
    # Note that these are sort of the reverse of each other, order matters. However if the difference is less than
    # zero or greater than 255 the values will be scaled up/down. e.g. uint8(5) - uint8(10) = 251 = 256 - 5
    diff_img_1 = img_A_std_size - img_B_std_size 
    diff_img_2 = img_B_std_size - img_A_std_size
    
    # It is better to determine the absolute difference. In Matlab if x and y are uint8 variables, then if x - y < 0,
    # the value is scaled to zero, so the absolute difference can be determined by (a - b) + (b - a).
    diff_abs = np.uint8(np.abs(np.int16(img_A_std_size) - np.int16(img_B_std_size)))
    diff_abs_cv = cv2.absdiff(img_A_std_size, img_B_std_size)
    
    print sum(sum(diff_abs - diff_abs_cv))  # Should print zero if my abs siff image is the same as the cv2 version.
    
    cv2.imshow('Diff 1', diff_img_1)
    cv2.imshow('Diff 2', diff_img_2)
    cv2.imshow('ABS diff', diff_abs)
    cv2.imshow('ABS diff CV func', diff_abs_cv)
    cv2.waitKey(0)
    

if __name__ == "__main__":
    img_file_A = 'ship.jpg'
    img_file_B = 'testA.jpg'
    
    img_A = cv2.imread(img_file_A)
    img_B = cv2.imread(img_file_B)
    
#    display_image_and_attributes(img_A)
    
#    plot_slice_show_slice_crop(img_A)
        
#    adding_images_tests(img_A, img_B)
    
#    make_noisy_img(img_B)
    
    subtract_images_test(img_A, img_B)
    
    
    