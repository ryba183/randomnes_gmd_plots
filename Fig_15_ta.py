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

########################## Fig 15

path = ''#provide path to DATA folder
avg_const_SD_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/average_constant_SD_init.npy',allow_pickle=True)
std_const_SD_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/STD_constant_SD_init.npy',allow_pickle=True)
std_err_const_SD_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/std_error_constant_SD_init.npy',allow_pickle=True)
mean_err_const_SD_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/mean_error_constant_SD_init.npy',allow_pickle=True)
std_err_const_SD_init_up = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/std_error_up_constant_SD_init.npy',allow_pickle=True)
std_err_const_SD_init_down = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/std_error_down_constant_SD_init.npy',allow_pickle=True)

########################## Fig 15 OU

path = ''#provide path to DATA folder
avg_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/average_OU.npy',allow_pickle=True)
std_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/STD_OU.npy',allow_pickle=True)
std_err_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/std_error_OU.npy',allow_pickle=True)
mean_err_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/mean_error_OU.npy',allow_pickle=True)
std_err_init_up_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/std_error_up_OU.npy',allow_pickle=True)
std_err_init_down_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/std_error_down_OU.npy',allow_pickle=True)

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
SD_to_plot_OU = [10, 100, 1000]
SD_to_plot_c_compare_HR = [10, 50, 100, 1000, 5000, 10000, 40000, 100000]
text_for_legend = ['D','HR']
subplots_marks = {0:'(a)', 1:'(b)', 2:'(c)', 3:'(d)', 4:'(e)', 5:'(f)', 6:'(g)', 7:'(h)'}
def major_formatter(x, pos):
    return f'{x:.1f}'
plt.rcParams.update({'font.size': 21})
N = int(len(text_for_legend))
fig, ax = plt.subplots(2, N, sharex=True)
fig.set_size_inches(19.5, 15.0)

for j in range(len(text_for_legend)):
    if j == 1:
      ax[0,j].errorbar(SD_to_plot_c_compare_HR, avg_const_SD_init[3*7:4*7+1]*100,  color='k',
                     yerr=((mean_err_const_SD_init[3*7:4*7+1])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      ax[0,j].errorbar(SD_to_plot_OU, avg_OU[3:]*100,  color='r',
                     yerr=((mean_err_OU[3:])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      ax[0,j].text(0.03, 0.05, subplots_marks[j], fontsize=20,transform=ax[0,j].transAxes)
      ax[1,j].text(0.03, 0.05, subplots_marks[j+N], fontsize=20,transform=ax[1,j].transAxes)

      CV = (std_const_SD_init[3*7:4*7+1]/avg_const_SD_init[3*7:4*7+1])
      CV_error_1 =np.power(mean_err_const_SD_init[3*7:4*7+1]/avg_const_SD_init[3*7:4*7+1],2)
      CV_error_2 = np.power(std_err_const_SD_init[3*7:4*7+1]/std_const_SD_init[3*7:4*7+1],2)
      CV_error = np.sqrt(CV_error_1 + CV_error_2)

      ax[1,j].errorbar(SD_to_plot_c_compare_HR, CV,  color='k',  yerr=CV_error*CV, fmt=".",
                    alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)

      CV_OU = (std_OU[3:]/avg_OU[3:])
      CV_error_1_OU =np.power(mean_err_OU[3:]/avg_OU[3:],2)
      CV_error_2_OU = np.power(std_err_OU[3:]/std_OU[3:],2)
      CV_error_OU = np.sqrt(CV_error_1_OU + CV_error_2_OU)

      ax[1,j].errorbar(SD_to_plot_OU, CV_OU,  color='r',  yerr=CV_error_OU*CV_OU, fmt=".",
                    alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)
      ax[0,j].set_title(text_for_legend[j])

    else:
      print(avg_OU[:3])
      ax[0,j].errorbar(SD_to_plot_c_compare, avg_const_SD_init[0+j*7:7+j*7]*100,  color='k',
                     yerr=((mean_err_const_SD_init[0+j*7:7+j*7])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      ax[0,j].errorbar(SD_to_plot_OU, avg_OU[:3]*100,  color='r',
                     yerr=((mean_err_OU[:3])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)      

      CV = (std_const_SD_init[0+j*7:7+j*7]/avg_const_SD_init[0+j*7:7+j*7])
      CV_error_1 =np.power(mean_err_const_SD_init[0+j*7:7+j*7]/avg_const_SD_init[0+j*7:7+j*7],2)
      CV_error_2 = np.power(std_err_const_SD_init[0+j*7:7+j*7]/std_const_SD_init[0+j*7:7+j*7],2)
      CV_error = np.sqrt(CV_error_1 + CV_error_2)

      ax[1,j].errorbar(SD_to_plot_c_compare, CV,  color='k',  yerr=CV_error*CV, fmt=".",
                      alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)

      CV_OU = (std_OU[:3]/avg_OU[:3])
      CV_error_1_OU =np.power(mean_err_OU[:3]/avg_OU[:3],2)
      CV_error_2_OU = np.power(std_err_OU[:3]/std_OU[:3],2)
      CV_error_OU = np.sqrt(CV_error_1_OU + CV_error_2_OU)

      ax[1,j].errorbar(SD_to_plot_OU, CV_OU,  color='r',  yerr=CV_error_OU*CV_OU, fmt=".",
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
ax[1,1].set_xticks([10, 50, 100, 1000, 5000, 10000, 40000, 100000])

plt.subplots_adjust(left=0.06,
                bottom=0.06,
                right=0.99,
                top=0.95,
                wspace=0.1,
                hspace=0.05)

grid = plt.GridSpec(2, 4)
outfile_to_plot = ''#provide path to save the figure
plt.savefig(f'{outfile_to_plot}Fig_15_updated.pdf')
