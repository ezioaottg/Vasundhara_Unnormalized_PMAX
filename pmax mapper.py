import numpy as np
import plotly.express as px
from matplotlib import colors
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pandas as pd
import utility

"""
values = np.random.randn(40,20)


norm = colors.Normalize(vmin = np.nanmin(values), vmax= np.nanmax(values))
cmap = mpl.colormaps.get_cmap("viridis")
rgba = cmap(norm(values))
img = (rgba * 255).astype(np.uint8)

fig = px.imshow(img)
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)
fig.show()
"""

os.chdir("Pmax/Old Pmax/Sample 4")
filename = "Unnormalized_Pmax_Sample_4D_1kHz.xlsx"
electrode_loc_column_name = "Electrode Locations"
Pmax_column_name = "Unnormalized P_max"


cell_order = utility.cell_labels(letter_range= ["A", "O"], num_range=[1,16])
df = pd.read_excel(filename)


measured_loc = list(df[electrode_loc_column_name])
df = df.set_index(electrode_loc_column_name)



scalar_list = []
for loc in cell_order:
    if loc in measured_loc:
        scalar_list.append(df.loc[loc, Pmax_column_name])
    else:
        scalar_list.append(float('nan'))

scalar_map = [scalar_list[i:i + 15] for i in range(0, len(scalar_list), 15)]


#norm = colors.Normalize(vmin = np.nanmin(scalar_map), vmax= np.nanmax(scalar_map))
#cmap = mpl.colormaps.get_cmap("RdBu")
#rgba = cmap(norm(scalar_map))
#img = (rgba * 255).astype(np.uint8)

fig = px.imshow(scalar_map, color_continuous_scale='RdBu_r', title = "Old Sample 4D 1kHz")
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)
fig.show()



