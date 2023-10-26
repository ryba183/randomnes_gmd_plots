from math import sqrt
from sys import argv, path, maxsize
import cProfile, pstats
import h5py
import functools
import numpy as np
from itertools import product
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob, os
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import multiprocessing
import concurrent.futures
import threading
import concurrent.futures
from matplotlib.ticker import ScalarFormatter
import timeit
import pandas as pd
from matplotlib.gridspec import SubplotSpec
plt.rcParams.update({'font.size': 20})

########################## Fig 11 & 13

path_to_old = '/home/piotr-pc/response/to_share/odp_do_odp/Final/Dane/time_series/precip_data/ALL_old'
# DATA/Data_for_Fig_10_11_13_14_15/init
avg_const_SD_init = np.load(f'{path_to_old}/average_constant_SD_init.npy',allow_pickle=True)
std_const_SD_init = np.load(f'{path_to_old}/STD_constant_SD_init.npy',allow_pickle=True)
std_err_const_SD_init = np.load(f'{path_to_old}/std_error_constant_SD_init.npy',allow_pickle=True)
mean_err_const_SD_init = np.load(f'{path_to_old}/mean_error_constant_SD_init.npy',allow_pickle=True)
std_err_const_SD_init_up = np.load(f'{path_to_old}/std_error_up_constant_SD_init.npy',allow_pickle=True)
std_err_const_SD_init_down = np.load(f'{path_to_old}/std_error_down_constant_SD_init.npy',allow_pickle=True)

########################## Fig 15
path_to_old = '/home/piotr-pc/response/to_share/odp_do_odp/Final/Dane/time_series/precip_data/GA17_old'
# DATA/Data_for_Fig_10_11_13_14_15/mixing
avg_GA17 = np.load(f'{path_to_old}/average_GA17.npy',allow_pickle=True)
std_GA17 = np.load(f'{path_to_old}/STD_GA17.npy',allow_pickle=True)
std_err_GA17 = np.load(f'{path_to_old}/std_error_GA17.npy',allow_pickle=True)
mean_err_GA17 = np.load(f'{path_to_old}/mean_error_GA17.npy',allow_pickle=True)
std_err_init_up_GA17 = np.load(f'{path_to_old}/std_error_up_GA17.npy',allow_pickle=True)
std_err_init_down_GA17 = np.load(f'{path_to_old}/std_error_down_GA17.npy',allow_pickle=True)

########################## UPDATE

main_path = '/home/piotr-pc/response/to_share/odp_do_odp/Final/Dane/time_series'
avg_distance = np.load(f'{main_path}/All/average_distance.npy',allow_pickle=True)
std_distance = np.load(f'{main_path}/All/STD_distance.npy',allow_pickle=True)
std_err_distance = np.load(f'{main_path}/All/std_error_distance.npy',allow_pickle=True)
mean_err_distance = np.load(f'{main_path}/All/mean_error_distance.npy',allow_pickle=True)
std_err_init_up_distance = np.load(f'{main_path}/All/std_error_up_distance.npy',allow_pickle=True)
std_err_init_down_distance = np.load(f'{main_path}/All/std_error_down_distance.npy',allow_pickle=True)

def create_subtitle(fig: plt.Figure, grid: SubplotSpec, title: str):
    "Sign sets of subplots with title"
    row = fig.add_subplot(grid)
    # the '\n' is important
    row.set_title(f'{title}\n', fontweight='semibold')
    # hide subplot
    row.set_frame_on(False)
    row.axis('off')

#Comparision between mixing and no mixing simulations  - Fig_15

SD_to_plot_c_compare = [10, 50, 100, 1000, 10000, 40000, 100000]
SD_to_plot_c_compare_HR = [10, 50, 100, 1000, 5000, 10000, 40000, 100000]
text_for_legend = ['D', 'LR', 'MR','HR']
subplots_marks = {0:'(a)', 1:'(b)', 2:'(c)', 3:'(d)', 4:'(e)', 5:'(f)', 6:'(g)', 7:'(h)'}
def major_formatter(x, pos):
    return f'{x:.1f}'
plt.rcParams.update({'font.size': 21})
N = int(len(text_for_legend))
fig, ax = plt.subplots(2, N, sharex=True)
fig.set_size_inches(19.5, 15.0)

for j in range(len(text_for_legend)):
    if j == 3:
      print(SD_to_plot_c_compare_HR, avg_const_SD_init[3*7:4*7+1])
      ax[0,j].errorbar(SD_to_plot_c_compare_HR, avg_const_SD_init[3*7:4*7+1]*100,  color='k',
                     yerr=((mean_err_const_SD_init[3*7:4*7+1])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      ax[0,j].errorbar(SD_to_plot_c_compare_HR, avg_GA17[3*7:4*7+1]*100,  color='r',
                     yerr=((mean_err_GA17[3*7:4*7+1])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
    #   ax[0,j].set_title(podpisy_c_compare[j])
      ax[0,j].text(0.03, 0.05, subplots_marks[j], fontsize=20,transform=ax[0,j].transAxes)
      ax[1,j].text(0.03, 0.05, subplots_marks[j+N], fontsize=20,transform=ax[1,j].transAxes)

      CV = (std_const_SD_init[3*7:4*7+1]/avg_const_SD_init[3*7:4*7+1])
      CV_error_1 =np.power(mean_err_const_SD_init[3*7:4*7+1]/avg_const_SD_init[3*7:4*7+1],2)
      CV_error_2 = np.power(std_err_const_SD_init[3*7:4*7+1]/std_const_SD_init[3*7:4*7+1],2)
      CV_error = np.sqrt(CV_error_1 + CV_error_2)

      ax[1,j].errorbar(SD_to_plot_c_compare_HR, CV,  color='k',  yerr=CV_error*CV, fmt=".",
                    alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)

      CV_GA17 = (std_const_SD_init[3*7:4*7+1]/avg_GA17[3*7:4*7+1])
      CV_error_1_GA17 =np.power(mean_err_GA17[3*7:4*7+1]/avg_GA17[3*7:4*7+1],2)
      CV_error_2_GA17 = np.power(std_err_const_SD_init[3*7:4*7+1]/std_GA17[3*7:4*7+1],2)
      CV_error_GA17 = np.sqrt(CV_error_1_GA17 + CV_error_2_GA17)

      ax[1,j].errorbar(SD_to_plot_c_compare_HR, CV_GA17,  color='r',  yerr=CV_error_GA17*CV_GA17, fmt=".",
                    alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)
      ax[0,j].set_title(text_for_legend[j])

    else:
      ax[0,j].errorbar(SD_to_plot_c_compare, avg_const_SD_init[0+j*7:7+j*7]*100,  color='k',
                     yerr=((mean_err_const_SD_init[0+j*7:7+j*7])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      ax[0,j].errorbar(SD_to_plot_c_compare, avg_GA17[0+j*7:7+j*7]*100,  color='r',
                     yerr=((mean_err_GA17[0+j*7:7+j*7])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)      

      CV = (std_const_SD_init[0+j*7:7+j*7]/avg_const_SD_init[0+j*7:7+j*7])
      CV_error_1 =np.power(mean_err_const_SD_init[0+j*7:7+j*7]/avg_const_SD_init[0+j*7:7+j*7],2)
      CV_error_2 = np.power(std_err_const_SD_init[0+j*7:7+j*7]/std_const_SD_init[0+j*7:7+j*7],2)
      CV_error = np.sqrt(CV_error_1 + CV_error_2)

      ax[1,j].errorbar(SD_to_plot_c_compare, CV,  color='k',  yerr=CV_error*CV, fmt=".",
                      alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)

      CV_GA17 = (std_const_SD_init[0+j*7:7+j*7]/avg_GA17[0+j*7:7+j*7])
      CV_error_1_GA17 =np.power(mean_err_GA17[0+j*7:7+j*7]/avg_GA17[0+j*7:7+j*7],2)
      CV_error_2_GA17 = np.power(std_err_GA17[0+j*7:7+j*7]/std_GA17[0+j*7:7+j*7],2)
      CV_error_GA17 = np.sqrt(CV_error_1_GA17 + CV_error_2_GA17)

      ax[1,j].errorbar(SD_to_plot_c_compare, CV_GA17,  color='r',  yerr=CV_error_GA17*CV_GA17, fmt=".",
                      alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)

      ax[0,j].text(0.03, 0.05, subplots_marks[j], fontsize=20,transform=ax[0,j].transAxes)
      ax[1,j].text(0.03, 0.05, subplots_marks[j+N], fontsize=20,transform=ax[1,j].transAxes)


    ax[0,0].set_ylabel(r"$\langle {P} \rangle \cdot 10^{2}$ [mm]")
    ax[0,j].set_xscale('log')
    ax[1,0].set_ylabel(r"$\sigma (P) /\langle {P}\rangle$ [-]")
    ax[1,j].set_xscale('log')

    ax[0,j].set_title(text_for_legend[j])
    ax[0,j].text(0.03, 0.05, subplots_marks[j], fontsize=20,transform=ax[0,j].transAxes)
    ax[1,j].text(0.03, 0.05, subplots_marks[j+N], fontsize=20,transform=ax[1,j].transAxes)
    ax[1,j].set_xticks([10, 50, 100, 1000, 10000, 40000, 100000])
    ax[1,j].set_xlabel(r'$N_\mathrm{SD}^\mathrm{(bin)}$')
ax[1,3].set_xticks([10, 50, 100, 1000, 5000, 10000, 40000, 100000])


plt.subplots_adjust(left=0.06,
                bottom=0.06,
                right=0.99,
                top=0.95,
                wspace=0.3,
                hspace=0.1)

grid = plt.GridSpec(2, 4)
outfile_to_plot = '/home/piotr-pc/response/to_share/odp_do_odp/Final/Wykresy/'
plt.savefig(f'{outfile_to_plot}Fig_15_update_befor.pdf')