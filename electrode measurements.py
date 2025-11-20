import numpy as np
import os
import pandas as pd
import utility
from glob import glob

list_order = utility.cell_labels(['A', 'O'], [1,16])
 

os.chdir("Pmax/Old Pmax")
os.chdir("Sample 2")
text_files = glob("U*Sample_2D*.xlsx")
print(text_files)

loc_list = []   
for file in text_files:
    df =pd.read_excel(file)
    loc_list.append(list(df["Loc"]))

loc_intersection = set(loc_list[0]) & set(loc_list[1]) & set(loc_list[2])
intersection_list = list(loc_intersection)
ordered_intersection_list = utility.order_list_by_reference(intersection_list, list_order)
print(ordered_intersection_list)