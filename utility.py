import numpy as np
import pandas as pd
from scipy import signal


def cell_labels(letter_range: list = ['A', 'V'],
                num_range: list = [1, 41],
                inverse: bool = True) -> list:
    """
    Creates a list of inverse A1 reference style cell labels.

    It create create the list in two orders: 
    By setting inverse = True, where the numbers are ordered first  (i.e. A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C4)
    or by setting inverse = False, where the letters are ordered first (i.e. A1, B1, C1, A2, B2, C2, A3, B3, C3, A4, B4, C4)
    """

    if inverse == True:
        labels = [f"{letter}{num}"
            for letter in (chr(c) for c in range(ord(letter_range[0]), ord(letter_range[1]) + 1))
            for num in range(num_range[0], num_range[1])]
    else:
        labels = [f"{letter}{num}"
            for num in range(num_range[0], num_range[1])
            for letter in (chr(c) for c in range(ord(letter_range[0]), ord(letter_range[1]) + 1))]


    return labels


def order_list_by_reference(target_list: list,
                           reference_list: list):
    
    """
    Given a reference list of the order the things should be in, reorder the target_list to be in that order. 
    Similar to Excel's custom order.
    """

    order = {item: index for index, item in enumerate(reference_list)}
    sorted_list = sorted(target_list, key = lambda cell: order[cell])
    return sorted_list

def block_nonzero_average(matrix: np.ndarray,
              block_H: int = 2, 
              block_W: int = 2) -> np.ndarray:

    """
    Performs block average of non-zero values using a non-overlapping convolution method.
    The kernel is matrix of ones with size equalling the desired block-size.
    The resulting matrix is then downsampled with stride equal to the shape of the kernel to delete any overlapping sums.
    """
    kernel = np.ones((block_H, block_W))

    conv_output = signal.convolve2d(matrix, kernel, mode='valid')
    strided_output = conv_output[::block_H, ::block_W]

    #Converts all non-zeroes to one in the original matrix and does the same convolution
    count_ouput = signal.convolve2d((matrix !=0).astype(int), kernel, mode = 'valid')
    #Resulting output should be the number of nonzero values in each block
    strided_count = count_ouput[::block_H, ::block_H]

    #Divide the sum of each block by the number of nonzero values in each block to get the average
    strided_average = strided_output/strided_count

    return strided_average

def add_zeros(matrix: np.ndarray, columns: int = 1, rows: int = 1) -> np.ndarray:
    """
    Given a 2D matrix, add a specified number of columns or rows with just zero as values    
    """
    H, W = matrix.shape
    zeroes = np.zeros((H + rows,W + columns))
    zeroes[:H, :W] = matrix

    return zeroes

def get_loc(filename):
    if filename[2] == "_":
        loc = filename[0:2]
    else:
        loc = filename[0:3] 

    return loc


