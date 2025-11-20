import glob
import utility
import pandas as pd
import os
import numpy as np


os.chdir("Old PE loops")
Sample_number = "PE loop Sample 2"
Sample_letter = "A"
frequency = "5Hz"
headerskip = 42
bottomskip = 18

os.chdir(Sample_number + "/" + "Sample " +  Sample_letter)
electrode_order= utility.cell_labels(letter_range= ['A', 'O'], num_range=[1, 16], inverse= True)

text_files = glob.glob("*" + frequency + "*.txt")
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
        p_max[loc] = np.nanmax(polarization)
        
    except:
        filename = glob.glob(loc + "_" + "*" + frequency +".txt")[0]
        df = pd.read_csv(filename, sep = '\t', header = headerskip - 2, skipfooter = bottomskip ,encoding = 'latin1', engine = 'python')
        df["Measured Polarization (uC/cm2)"] = pd.to_numeric(df["Measured Polarization (uC/cm2)"], errors= 'coerce')
        polarization = np.asarray(df["Measured Polarization (uC/cm2)"])
        p_max[loc] = np.nanmax(polarization)

pmax_df = pd.DataFrame({
    "Loc" : p_max.keys(),
    "P_max": p_max.values()
})


os.chdir("..")
os.chdir("..")
os.chdir("..")
os.chdir("Pmax")
os.chdir("Old Pmax")
#os.chdir("Sample " + Sample_letter)
print("\n\n\n\n")
print(os.getcwd())
pmax_df.to_excel("Unnormalized_Pmax_"+ "Sample_" + Sample_number[-1] + Sample_letter + "_" + frequency + ".xlsx", index = False)
    



