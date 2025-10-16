import glob
import utility
import pandas as pd
import os
import numpy as np



Sample_number = "New PE loop Sample 2"
Sample_letter = "C"
frequency = "100kHz"
headerskip = 42
bottomskip = 18

os.chdir(Sample_number + "/" + Sample_letter)
electrode_order= utility.cell_labels(letter_range= ['A', 'O'], num_range=[1, 16], inverse= True)

text_files = glob.glob("*" + frequency + ".txt")
electrode_locs = []
for filename in text_files:
    electrode_locs.append(utility.get_loc(filename))
electrode_locs = utility.order_list_by_reference(electrode_locs, electrode_order)

p_max = {}
for loc in electrode_locs:
    try:
        filename = glob.glob(loc + "_" + "*" + frequency +".txt")[0]
        df = pd.read_csv(filename, sep = '\t', header = headerskip, skipfooter = bottomskip ,encoding = 'latin1', engine = 'python')
        df["Measured Polarization (uC/cm2)"] = pd.to_numeric(df["Measured Polarization (uC/cm2)"], errors= 'coerce')
        polarization = np.asarray(df["Measured Polarization (uC/cm2)"])
        p_max_unnorm = np.nanmax(polarization)

        with open(filename, 'r') as f:
            lines = f.readlines()
            offset = float(lines[-8][16:].strip())

        p_max_norm = p_max_unnorm + offset
        p_max[loc] = p_max_norm
    except:
        filename = glob.glob(loc + "_" + "*" + frequency +".txt")[0]
        df = pd.read_csv(filename, sep = '\t', header = headerskip - 2, skipfooter = bottomskip ,encoding = 'latin1', engine = 'python')
        df["Measured Polarization (uC/cm2)"] = pd.to_numeric(df["Measured Polarization (uC/cm2)"], errors= 'coerce')
        polarization = np.asarray(df["Measured Polarization (uC/cm2)"])
        p_max_unnorm = np.nanmax(polarization)

        with open(filename, 'r') as f:
            lines = f.readlines()
            offset = float(lines[-8][16:].strip())

        p_max_norm = p_max_unnorm + offset
        p_max[loc] = p_max_norm


pmax_df = pd.DataFrame({
    "Loc" : p_max.keys(),
    "P_max": p_max.values()
})



os.chdir("..")
os.chdir("..")
os.chdir("New Pmax")
os.chdir("with offsets")


pmax_df.to_excel(Sample_number + Sample_letter + " " + frequency + " (OFFSET INCLUDED)" + ".xlsx", index = False)
