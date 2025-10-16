import numpy as np
import pandas as pd


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

    order = {item: index for index, item in enumerate(reference_list)}
    sorted_list = sorted(target_list, key = lambda cell: order[cell])
    return sorted_list

def get_loc(filename):
    if filename[2] == "_":
        loc = filename[0:2]
    else:
        loc = filename[0:3] 

    return loc



