import os
import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
from pathlib import Path
#----------- user entered information -----------------------------
saved_filename = 'SAMPLE_D_DATA.csv' #the name of the csv file that will be saved
electrode_measurements = False
electrode_x_y_filename = 'AC1065B1.csv'
top_skip = 42 #the number of rows to skip from the top to when the data starts
bottom_skip = 18 #the number of rows to skip from the bottom to when the data endss
start_threshold = -999 #if the starting point is greater than this number, it will also find the max
columns = dict(Polarization = "Measured Polarization", Voltage = "Drive Voltage")
cwd = "PE loop Sample 5/Sample A"
glob_stuff = "*5Hz.txt"
excel_name = "Unnormalized_Pmax_Sample_5A_5Hz.xlsx"

# txt_files[count] shows the file that is producing the error
#------------------------------------------------------------------


#Creates default electrode data and saves to csv (use until electrode data measurements are done)
def get_electrode_data(): 
    nums = np.arange(200)
    ones1 = np.ones(200) * 2 * np.sqrt(1e4/3.14159) 
    ones2 = np.ones(200) * 2 * np.sqrt(1e4/3.14159)
    miss = np.zeros(200)
    electrode_data = pd.DataFrame(data=np.transpose([nums,ones1,ones2,miss]),
                                  columns=['loc','x','y','miss'])
        
    return electrode_data

# Checks if a data file has multiple sets of saved data runs inside it

def is_multi_file(filepath) -> bool:

    end_line_number_list = []         #the line numbers that correspond to the end of a dataset

    with open(filepath, "r", encoding = 'latin1') as f:
        all_lines_list = f.readlines()
        for i, line in enumerate(all_lines_list):
            if line.strip() == ("Hysteresis Version: 5.48.1 - Radiant Technologies, Inc., 1999 - 9/12/24"):
                end_line_number_list.append(i)
    
        if(len(end_line_number_list) > 1):
            return True
        else: 
            return False

# Splits a file that has multiple sets of saved data into multiple ones
def split_file(filepath: str, cwd: str, end_line: str = "Hysteresis Version: 5.48.1 - Radiant Technologies, Inc., 1999 - 9/12/24") -> None:
    
    end_line_number_list = []         #the line numbers that correspond to the end of a dataset
    new_files = []
    new_file_paths = []

    with open(filepath, "r", encoding = 'latin1') as f:
        all_lines_list = f.readlines()
        for i, line in enumerate(all_lines_list):
            if line.strip() == (end_line):
                end_line_number_list.append(i)

        begin_line = 0
        end_line = end_line_number_list[0] + 2
        for i, elm in enumerate(end_line_number_list):

            new_file = all_lines_list[begin_line: elm + 2]
            new_files.append(new_file)

            new_path = cwd + "/"+ Path(filepath).stem + "_Run" + str(i+1) + ".txt"
            new_file_paths.append(new_path)
            begin_line = (elm + 2)

    for i, filepath in enumerate(new_file_paths):
        with open(filepath, "w", encoding = 'latin1') as f:
            file_lines = new_files[i]
            for line in file_lines:
                f.write(line)

def fix_files(cwd, text_file_paths) -> list[str]:
    mult_file_list = []
    for file in txt_files:
        if is_multi_file(file) == True:
            mult_file_list.append(file)
            split_file(file, path)

    return mult_file_list
   
def get_coersive(polarize,voltage):
    global electrode_data, i
    
    half_p = int(len(polarize)/2) # to find the halfway point
    quart_p = int(half_p + half_p/2)  #to find the three quarters through point
    third_quarter = polarize[half_p:quart_p] # taking third quarter of list
    fourth_quarter = polarize[quart_p:] # taking fourth quarter of list
    
    Ec_minus = np.nanmin(np.abs(third_quarter)) #minimum value in 3rd quarter
    Ec_plus = np.nanmin(np.abs(fourth_quarter)) #minimum value in 4th quarter
    #Ec_avg = (np.abs(Ec_minus) + np.abs(Ec_plus)) / 2 #avg
    
    # both of the below values contain the index location of Ec_minus
    # and Ec_plus in the polarize vector
    #print('where',np.where(np.abs(third_quarter) == Ec_minus)[0])
    H_minus_loc = int(half_p + np.where(np.abs(third_quarter) == Ec_minus)[0][0])
    H_plus_loc = int(quart_p + np.where(np.abs(fourth_quarter) == Ec_plus)[0][0])
    
    # the below values then index the voltage vector at the same location
    # to find the corresponding x-values
    H_minus = voltage[H_minus_loc]
    H_plus = voltage[H_plus_loc]
    # average is calculated using the absolute values of both
    H_avg = (np.abs(H_minus) + np.abs(H_plus)) / 2
    H_avg_normalized = H_avg * 1e4 / electrode_data['area corrected'][area_loc[filename][0]]
    
    return(H_minus,H_plus,H_avg,H_avg_normalized)

def errorprop_area(electrode_data,iteration):

    
    #finding the uncertainty in the area measurement
    a = electrode_data['x'][iteration] / 2
    b = electrode_data['y'][iteration] / 2
    miss = electrode_data['miss'][iteration]
    if miss != 0: #if eyeballing missing portion, assume 20% uncertainty in the measurement
        uncertA, uncertB = 0.05*a, 0.05*b
    else: #if whole electrode intact, assume 4% uncertainty in the measurement
        uncertA, uncertB = 0.02*a, 0.02*b
    deriv_a = 3.14159 * b
    deriv_b = 3.14159 * a
    a_part = (uncertA * deriv_a)**2
    b_part = (uncertB * deriv_b)**2
    uncertainty = np.sqrt((a_part + b_part))
    return(uncertainty)

def errorprop_norm(electrode_data,polarize,iteration,filename):
    #finding the uncertainty in each normalized data measurement
    global area_loc
    global electrode_loc
    area_corr = electrode_data['area corrected'][area_loc[filename][0]]
    area_uncert = electrode_data['area uncertainty'][area_loc[filename][0]]
    deriv_area = -((polarize*10**4)/(area_corr**2))
    area_part = (deriv_area*area_uncert)**2
    uncertainty = np.sqrt((area_part))
    return(uncertainty)

def errorprop_mean(uncert_min1,uncert_min2):
    #finding the uncertainty in the mean 
    deriv_min1 = 0.5
    deriv_min2 = 0.5
    min1_part = (deriv_min1 * uncert_min1)**2
    min2_part = (deriv_min2 * uncert_min2)**2
    uncertainty = np.sqrt(min1_part + min2_part)
    return(float(uncertainty))

os.chdir(cwd)
path = os.getcwd()
print(path)
txt_files = glob.glob(os.path.join(path,glob_stuff))
mult_file_list = fix_files(path, txt_files)
electrode_data = get_electrode_data()


#Doing somehting with the electrode data
areas = []
area_corrected = []
a_uncert = []
for elec in range(len(electrode_data['loc'])):
    x = electrode_data['x'][elec]
    y = electrode_data['y'][elec]
    areas.append(3.14159 * (x/2) * (y/2)) #in um^2
    if electrode_measurements:
        just_loc = int(electrode_data['loc'][elec][1:])
        electrode_data['loc'][elec] = just_loc
    missing = electrode_data['miss'][elec]
    area_corrected.append( areas[elec] - areas[elec]*(missing/100))
    a_uncert.append(errorprop_area(electrode_data,elec))
electrode_data['areas'] = areas
electrode_data['area corrected'] = area_corrected
electrode_data['area uncertainty'] = a_uncert


#Getting filenames in datasets into a list to be manipulated
filenames = []
data_list = []
area_loc = {}
electrode_locs = []
for count, file in enumerate(txt_files):
    if file not in mult_file_list:
        filename = os.path.basename(file)
        filenames.append(filename)
        data_list.append(pd.read_csv(file, sep = '\t', header = 42, skipfooter = bottom_skip,encoding = 'latin1', engine = 'python'))

        find = filename[:3]
        
        if find[-1].isdigit():
            electrode_loc = int(find[1:])
        else:
            electrode_loc = int(find[1:2])

        electrode_locs.append(electrode_loc)
        area_loc[filename] = np.where(electrode_data['loc']==electrode_loc)[0]


polarization_list = []
P_maxes = []
max_difference = []
min_list = []
avs = []
stds = []
polarize0 = []
norm_data_uncert = []
norm_mean_uncert = []
Ec_minus = []
Ec_plus = []
Ec_average = []
max_sp_diff = []
max_sp_uncert = []
Ec_average_normalized=[]
unnorm_p_max = []

for i in range(len(data_list)):
    if file not in mult_file_list:
            filename = filenames[i]
            polarization = np.array(data_list[i]["Measured Polarization (uC/cm2)"])
            unnorm_p_max.append(np.nanmax(polarization))
            voltage = np.array(data_list[i]["Drive Voltage"])
            polarization = polarization.astype(float) * 1e4 / electrode_data['area corrected'][area_loc[filename][0]]
            polarization_list.append(polarization)
            P_maxes.append(np.nanmax(polarization))


            half = int(len(voltage)/2)
            min1 = min(polarization[:half])
            loc1 = np.where(polarization[:half] == min1)[0][0]
            min2 = min(polarization[half:])
            loc2 = np.where(polarization[half:] == min2)[0][0]
            max_difference.append(max(polarization)-min(polarization))
            min_list.append([min1,min2])
            avs.append(np.abs(np.mean(min_list[i])))
            stds.append(np.std(min_list[i]))
            polarize0.append(polarization[0])

            norm_data_uncert.append(errorprop_norm(electrode_data,polarization,i,filename))
            uncert_min1, uncert_min2 = norm_data_uncert[i][[0]], norm_data_uncert[i][loc2]
            norm_mean_uncert.append(errorprop_mean(uncert_min1,uncert_min2))

            Ec_minus.append(get_coersive(polarization,voltage)[0])
            Ec_plus.append(get_coersive(polarization,voltage)[1])
            Ec_average.append(get_coersive(polarization,voltage)[2])
            Ec_average_normalized.append(get_coersive(polarization,voltage)[3])

            if polarization[0] >= start_threshold:
                max_whole = np.nanmax(polarization)
                max_minus_start = max_whole - polarization[0]
                max_sp_diff.append(max_minus_start)
                max_sp_uncert.append(np.sqrt(2*norm_data_uncert[i][loc1]**2)) #error propagation equation for: Polarization = Data_pt1 - Data_pt2
            else:
                max_sp_diff.append('na')
                max_sp_uncert.append('na')





data = {"File Name" : filenames,
        "Normalized Minimums": min_list,
        "Normalized Means": avs,
        "Normalized Mean Uncertainty": norm_mean_uncert,
        "std": stds,
        "Initial Polarization": polarize0,
        "Max Starting Point": max_sp_diff,
        "Max Starting Point Uncertainty": max_sp_uncert,
        "Maximum Difference": max_difference,
        "Hc Plus": Ec_plus,
        "Hc Minus": Ec_minus,
        "Hc Average": Ec_average,
        "Hc Average Normalized": Ec_average_normalized,
        "Unnormalized P_max": unnorm_p_max

}



df = pd.DataFrame(data)

print(df)

df2 = df[['File Name', "Unnormalized P_max"]]
df2.to_excel(excel_name, index = False)









