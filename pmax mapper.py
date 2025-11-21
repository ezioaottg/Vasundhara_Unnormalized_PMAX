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


electrode_loc_column_name = "Loc"
Pmax_column_name = "P_max"
cell_order = utility.cell_labels(letter_range= ["A", "O"], num_range=[1,16])



os.chdir("Pmax/Old Pmax")
filenames = glob("*.xlsx")
for filename in filenames:
    df = pd.read_excel(filename)
    measured_loc = list(df[electrode_loc_column_name])
    df = df.set_index(electrode_loc_column_name)
    scalar_list = []
    for loc in cell_order:
        if loc in measured_loc:
            scalar_list.append(df.loc[loc, Pmax_column_name])
        else:
            scalar_list.append(float(0))

    scalar_map = np.array([scalar_list[i:i + 15] for i in range(0, len(scalar_list), 15)])
    reduced_map = utility.block_nonzero_average(scalar_map, block_H=3, block_W=3)
    reduced_map = np.where(reduced_map ==0, math.nan, reduced_map)



    fig = px.imshow(reduced_map, color_continuous_scale='RdBu_r', title = "Old Sample 4D 1kHz", origin='upper',)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    os.chdir("..")
    os.chdir("..")
    os.chdir("Pmax Maps")
    fig.write_html(filename[18:27] + ".html")
    os.chdir("..")
    os.chdir("Pmax/Old Pmax")







