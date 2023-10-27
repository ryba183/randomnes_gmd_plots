from math import exp, log, sqrt, pi, erf, cos, pow, asin, atan, acos, factorial
import numpy as np
from scipy.stats import moment
from sys import argv
import matplotlib as plt
import matplotlib.pyplot as plt
import glob, os
import random
import string
plt.rcParams.update({'font.size': 26})

def read_my_array(file_obj):
    arr_name = file_obj.readline()
    file_obj.readline() # discarded line with size of the array
    line = file_obj.readline()
    line = line.split(" ")
    del line[0]
    del line[len(line)-1]
    arr = list(map(float,line))
    return np.array(arr), arr_name

def read_my_var(file_obj, var_name):
    file_obj.seek(0)
    while True:
        arr, name = read_my_array(file_obj)
        if(str(name).strip() == str(var_name).strip()):
            break
    return arr[-1]

path = ""#provide path to DATA folder
outfile_to_plot = ''#provide path to save the figure
path_to_data_folder = f'{path}/Frequency_histogram_data/'
mydict = {}
dir_list = os.listdir(path_to_data_folder)
files_list = [(file.split("_out")[0]).split("_")[-1] for file in dir_list]

for i in range(len(dir_list)):
    mydict[files_list[i]] = read_my_var(open(path_to_data_folder+dir_list[i], "r"), "acc_precip")

myList = mydict.items()
myList = sorted(myList) 
Y = np.zeros(len(dir_list)+1)
for i in range(len(dir_list)+1):
    Y[i] = mydict.get(str(i))
bin_hist = np.arange(0, 0.15, step=3/400)
fig, ax = plt.subplots(1,1)
fig.set_size_inches(19.5, 16.0)

N, bins, patches = ax.hist(Y,bins=bin_hist,log=1,range=(0, 0.15), width=3/400*0.9, align = 'mid')
bin_centers = 0.5 * (bins[:-1] + bins[1:])
ax.set_xlim((-0.001, 0.151))
ax.set_ylim(0,1e3)
bin_manual = np.array([0,0.0075, 0.015,0.0225, 0.03,0.0375,0.045,0.0525,0.06,0.0675,0.075,0.0825,0.09,0.0975,0.105,0.1125,0.12,0.1275,0.135,0.1425])
xticks_bins = np.around((bin_manual + 3/400/2)*100, decimals=4)
patches[16].set_facecolor("#6F183D")
patches[0].set_facecolor("#6F183D")
patches[4].set_facecolor("#6F183D")
plt.xticks(bin_manual+3/400*0.9/2,xticks_bins, ha = 'center', fontsize=25, rotation='vertical')
ax.set_xlabel(r'$P / 10^{2}$ [mm]', fontsize=25)
ax.set_ylabel('number of simulations', fontsize=25)
plt.tight_layout()
plt.savefig(f'{outfile_to_plot}Fig_6.pdf')
