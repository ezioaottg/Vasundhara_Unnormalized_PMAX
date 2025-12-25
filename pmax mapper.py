import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import colors
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pandas as pd
import utility
from glob import glob
import math


#-------------------------------------------------------------------------------------------------------
#For the excel files we're loop over, the names for the electrode location and pmax should be consistent
electrode_loc_column_name = "Loc"
Pmax_column_name = "P_max"

#Creates an ordered list [A1, A2, A3, ..., O15] to be used as reference ordering list
cell_order = utility.cell_labels(letter_range= ["A", "O"], num_range=[1,16])

#Change directory to where the electrode pmax values are stored
os.chdir("Pmax/Old Pmax")
#-------------------------------------------------------------------------------------------------------


# Grabs all the excel files with pmax values and electrode locations we want to map and loops over them
filenames = glob("*.xlsx")
for filename in filenames:


    #For each excel file, grabs the pmax values and orders them by our ordered list.
    df = pd.read_excel(filename)
    measured_loc = list(df[electrode_loc_column_name])
    df = df.set_index(electrode_loc_column_name)
    scalar_list = []
    for loc in cell_order:
        if loc in measured_loc:
            scalar_list.append(df.loc[loc, Pmax_column_name])
        else:
            scalar_list.append(float(0))



    # Turns our list of scalar values into a 15x15 array. This is an accurate representation of the location of each electrode measurement.
    scalar_map = np.array([scalar_list[i:i + 15] for i in range(0, len(scalar_list), 15)])

    # We reduce the size of the 2d array since not all electrode locations have a measurement
    # Done by using a convolution method with a kernel of 1s.
    # kernel size must be a factor of the 2D array dimensions. Can add rows or columns of zeroes to force this.
    reduced_map = utility.block_nonzero_average(scalar_map, block_H=2, block_W=2)

    # Turns 0 values to nan values so our plotting gradient is not messed up.
    reduced_map = np.where(reduced_map ==0, math.nan, reduced_map)




    fig = px.imshow(reduced_map, color_continuous_scale='RdBu_r', title = "Old Sample 4`D 1kHz", origin='upper',)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    os.chdir("..")
    os.chdir("..")
    os.chdir("Pmax Maps")
    fig.write_html(filename[18:27] + ".html")
    os.chdir("..")
    os.chdir("Pmax/Old Pmax")







