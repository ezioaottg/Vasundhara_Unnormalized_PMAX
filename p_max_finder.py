import glob
import utility
import pandas as pd
import os
import numpy as np
from openpyxl import load_workbook
import openpyxl


"""
This program loops over the PE Loop files to find the pmax values for each electrode measurement. The folders
must be organized and named in a very specific way:

Current Working Directory
    Sample (#)
        Sample A
            Files
        Sample B
        Sample C
        Sample D
    Sample (#)
        Sample A
        Sample B
        Sample C
        Sample D
    ...
    
The files must also be named very specifically in order for the program to read them:
    (Electrode Location)_(PE loop type)_(Voltage)_(Frequency)
    ex: A9_bipolar_20V_1kHz
    THE A IN A9 HAS TO BE CAPITALIZED

This file will output an excel sheet for each sub-sample with the different measurements with different 
frequencies in different sheets

"""



"""----------------------------------------------------------------------------------------------------------"""
#List the samples and frequencies of the files you want to find the pmax of
sample_numbers = ['2', '4', '5', '8']
sample_letters = ['A','B','C',"D"]
frequencies = ["5Hz", "1kHz", "100kHz"]

#Creates an ordered list [A1, A2, A3, ..., O15] to be used as reference ordering list
electrode_order= utility.cell_labels(letter_range= ['A', 'O'], num_range=[1, 16], inverse= True)

#The lines in the PE loop text files at which this program should skip
headerskip = 42
bottomskip = 18

#Change the directory to where the PE loops are stored
os.chdir("Old PE loops")

"""-------------------------------------------------------------------------------------------------------"""


#Loop over all samples
for number in sample_numbers:
    os.chdir("PE loop Sample " + number)

    # Loop over sample parts
    for letter in sample_letters:
        os.chdir("Sample " + letter)

        #Loops over the frequencies
        for frequency in frequencies:

            #Finds the electrode locations for each file with this frequency and stuffs them in a list
            file_names = glob.glob("*" + frequency + "*.txt")
            electrode_locs= utility.get_locs(file_names)
            p_max = {}

            #For each electrode measurement, find that file and grabs the pmax from it and saves it in a dictionary where the key is the electrode location index (i.e A9, O15, B7)
            for loc in electrode_locs:
                try:
                    filename = glob.glob(loc + "_" + "*" + frequency +".txt")[0]
                    df = pd.read_csv(filename, sep = '\t', header = headerskip, skipfooter = bottomskip ,encoding = 'latin1', engine = 'python')
                    df["Measured Polarization (uC/cm2)"] = pd.to_numeric(df["Measured Polarization (uC/cm2)"], errors= 'coerce')
                    polarization = np.asarray(df["Measured Polarization (uC/cm2)"])
                    p_max[loc] = np.nanmax(polarization)

                # Some files have different header lengths for some unknown reason. If the standard headerskip doesnt work, it tries again but with a different headerskip
                except:
                
                    filename = glob.glob(loc + "_" + "*" + frequency +".txt")[0]
                    df = pd.read_csv(filename, sep = '\t', header = headerskip - 2, skipfooter = bottomskip ,encoding = 'latin1', engine = 'python')
                    df["Measured Polarization (uC/cm2)"] = pd.to_numeric(df["Measured Polarization (uC/cm2)"], errors= 'coerce')
                    polarization = np.asarray(df["Measured Polarization (uC/cm2)"])
                    p_max[loc] = np.nanmax(polarization)


            #Turns that pmax library into a dataframe with one column being the location and another being the pmax value
            pmax_df = pd.DataFrame({
                                    "Loc" : p_max.keys(),
                                    "P_max": p_max.values()
                                    })
            

            #Changes the directory to where you wanna save the excel files
            os.chdir("..")
            os.chdir("..")
            os.chdir("..")
            os.chdir("Pmax")
            os.chdir("Old Pmax")


            #Saves the dataframe to an excel file, each desired frequency will get their own sheet in the excel file. Each Sample section (A,B,C,D) will get its own excel file
            filename = "Unnormalized_Pmax_"+ "Sample_" + number + letter + ".xlsx"
            #If the file doesn't exist, create it with the first sheet
            if not os.path.exists(filename):
                with pd.ExcelWriter(filename, engine = 'openpyxl') as writer:
                    pmax_df.to_excel(writer, sheet_name= frequency ,index = False)
            else:
                #If the file exists, load the workbook and create an excel writer in append mode
                with pd.ExcelWriter(filename,
                                    mode = 'a',
                                    engine = 'openpyxl',
                                    if_sheet_exists = 'replace'
                                    ) as writer:
                    pmax_df.to_excel(writer, sheet_name= frequency ,index = False)
                

            #Changes the directory back to where the PE loops are stored.
            os.chdir("..")
            os.chdir("..")
            os.chdir("Old PE loops")
            os.chdir("PE loop Sample " + number)
            os.chdir("Sample " + letter)
            
        os.chdir("..")
    os.chdir("..")



