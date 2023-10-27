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

#Please use this if for some reason your matplotlib won't work properly.
#pip install --upgrade matplotlib

#Loading data created with the aid of 'Fig_10_12_13_14_data_creation' necessary for making  plots.

path = ""#provide path to DATA folder
outfile_to_plot = ''#provide path to save the figure
########################## Fig 10

avg_time = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/coalescence/average_coalescence.npy',allow_pickle=True)
std_time = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/coalescence/STD_coalescence.npy',allow_pickle=True)
std_err_time = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/coalescence/std_error_coalescence.npy',allow_pickle=True)
mean_err_time = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/coalescence/mean_error_coalescence.npy',allow_pickle=True)
std_err_time_up = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/coalescence/std_error_up_coalescence.npy',allow_pickle=True)
std_err_time_down = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/coalescence/std_error_down_coalescence.npy',allow_pickle=True)

########################## Fig 11 & 13

avg_const_SD_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/average_constant_SD_init.npy',allow_pickle=True)
std_const_SD_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/STD_constant_SD_init.npy',allow_pickle=True)
std_err_const_SD_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/std_error_constant_SD_init.npy',allow_pickle=True)
mean_err_const_SD_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/mean_error_constant_SD_init.npy',allow_pickle=True)
std_err_const_SD_init_up = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/std_error_up_constant_SD_init.npy',allow_pickle=True)
std_err_const_SD_init_down = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/std_error_down_constant_SD_init.npy',allow_pickle=True)

########################## Fig 11 & 13

avg_const_SD_init_no10 = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/average_constant_SD_init_no10.npy',allow_pickle=True)
std_const_SD_init_no10 = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/STD_constant_SD_init_no10.npy',allow_pickle=True)
std_err_const_SD_init_no10 = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/std_error_constant_SD_init_no10.npy',allow_pickle=True)
mean_err_const_SD_init_no10 = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/mean_error_constant_SD_init_no10.npy',allow_pickle=True)
std_err_const_SD_init_up_no10 = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/std_error_up_constant_SD_init_no10.npy',allow_pickle=True)
std_err_const_SD_init_down_no10 = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/std_error_down_constant_SD_init_no10.npy',allow_pickle=True)

########################## Fig 14

avg_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/initialization/average_SD_initialization.npy',allow_pickle=True)
std_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/initialization/STD_SD_initialization.npy',allow_pickle=True)
std_err_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/initialization/std_error_SD_initialization.npy',allow_pickle=True)
mean_err_init = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/initialization/mean_error_SD_initialization.npy',allow_pickle=True)
std_err_init_up = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/initialization/std_error_up_SD_initialization.npy',allow_pickle=True)
std_err_init_down = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/initialization/std_error_down_SD_initialization.npy',allow_pickle=True)

########################## Fig 15

avg_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/old/average_OU.npy',allow_pickle=True)
std_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/old/STD_OU.npy',allow_pickle=True)
std_err_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/old/std_error_OU.npy',allow_pickle=True)
mean_err_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/old/mean_error_OU.npy',allow_pickle=True)
std_err_init_up_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/old/std_error_up_OU.npy',allow_pickle=True)
std_err_init_down_OU = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/mixing/old/std_error_down_OU.npy',allow_pickle=True)

avg_f15 = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/average_constant_SD_init.npy',allow_pickle=True)
std_f15 = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/STD_constant_SD_init.npy',allow_pickle=True)
std_err_f15 = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/std_error_constant_SD_init.npy',allow_pickle=True)
mean_err_f15 = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/mean_error_constant_SD_init.npy',allow_pickle=True)
std_err_f15_up = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/std_error_up_constant_SD_init.npy',allow_pickle=True)
std_err_f15_down = np.load(f'{path}/Data_for_Fig_10_11_13_14_15/init/Fig_15/std_error_down_constant_SD_init.npy',allow_pickle=True)

def create_subtitle(fig: plt.Figure, grid: SubplotSpec, title: str):
    "Sign sets of subplots with title"
    row = fig.add_subplot(grid)
    # the '\n' is important
    row.set_title(f'{title}\n', fontweight='semibold')
    # hide subplot
    row.set_frame_on(False)
    row.axis('off')

#Coalescence substep value compare - Fig_10

timesteps = [0.05, 0.1, 0.5]
text_for_legend_time = ['D','LR','MR','HR']
subplots_marks = {0:'(a)', 1:'(b)', 2:'(c)', 3:'(d)', 4:'(e)', 5:'(f)', 6:'(g)', 7:'(h)'}

def major_formatter(x, pos):
    return f'{x:.1f}'
P = int(len(text_for_legend_time))
fig4, ax4 = plt.subplots(2, P, sharex=True)
fig4.set_size_inches(20.5, 16.0)
xlabels = [0.05, 0.1, 0.5]

for j in range(len(text_for_legend_time)):        

    ax4[0,j].errorbar(timesteps, np.array_split(avg_time, P)[j]*100,  color='k',  yerr=np.array_split(mean_err_time, P)[j]*1.96*100,
                     fmt=".", ms=20,elinewidth=3,alpha=0.5, linestyle=':', capsize=6)
    
    ax4[0,0].set_ylabel(r"$\langle {P} \rangle\cdot 10^{2}$ [mm]")
    ax4[0,j].set_title(text_for_legend_time[j])
    ax4[0,j].set_xscale('log')
    locator = matplotlib.ticker.MaxNLocator(nbins=6)
    ax4[0,j].yaxis.set_major_locator(locator)
    ax4[0,j].get_yaxis().set_major_formatter(major_formatter)  
    ax4[0,j].set_ylim(bottom=0)
    ax4[0,j].text(0.03, 0.05, subplots_marks[j], fontsize=20,transform=ax4[0,j].transAxes)


    ax4[1,j].errorbar(timesteps, np.array_split(std_time, P)[j]*100,  color='k',
                      yerr=(np.array_split(std_time, P)[j]*100 - np.array_split(std_err_time_down, P)[j]*100,
                            np.array_split(std_err_time_up, P)[j]*100 - np.array_split(std_time, P)[j]*100 ),
                      fmt=".",alpha=0.5,elinewidth=3, ms=20, linestyle=':', capsize=6)
    
    ax4[1,0].set_ylabel(r"$\sigma (P)\cdot 10^{2}$ [mm]")
    ax4[1,j].set_ylim(bottom=0)
    ax4[1,j].set_xscale('log')
    ax4[1,j].set_xticks(ticks=timesteps, rotation=45, fontsize=10)
    ax4[1,j].set_xticklabels(timesteps, rotation=45)
    locator = matplotlib.ticker.MaxNLocator(nbins=10)
    ax4[1,j].yaxis.set_major_locator(locator)
    ax4[1,j].get_yaxis().set_major_formatter(major_formatter)
    ax4[1,j].set(xlabel='$\Delta t_\mathrm{coal}$ [s]')
    ax4[1,j].text(0.03, 0.05, subplots_marks[j+P], fontsize=20,transform=ax4[1,j].transAxes)

ax4[0,0].set_ylim((0,3))
ax4[0,2].set_ylim((0,3))
ax4[0,1].set_ylim((0,1))
ax4[0,3].set_ylim((0,12))
ax4[1,0].set_ylim((0,3))
ax4[1,2].set_ylim((0,3))
ax4[1,1].set_ylim((0,1))
ax4[1,3].set_ylim((0,4))

plt.subplots_adjust(left=0.065,
                bottom=0.08, 
                right=0.99, 
                top=0.95, 
                wspace=0.3, 
                hspace=0.1)

grid = plt.GridSpec(2, 4)
plt.savefig(f'{outfile_to_plot}Fig_10.pdf')

#Case compare average - Fig_11

SD_to_plot_c_compare = [10, 50, 100, 1000, 10000, 40000, 100000]
SD_to_plot_c_compare_no10 = SD_to_plot_c_compare[1::]
SD_to_plot_c_compare_HR = [10, 50, 100, 1000, 5000, 10000, 40000, 100000]
SD_to_plot_c_compare_no10_HR = SD_to_plot_c_compare_HR[1::]
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
      mean_c_comp = np.array_split(avg_const_SD_init, N)[j]
      mean_c_comp = np.insert(mean_c_comp, 4, avg_init[3])
      mean_error = np.array_split(mean_err_const_SD_init, N)[j]
      mean_error = np.insert(mean_error, 4, mean_err_init[3])
      ax[0,j].errorbar(SD_to_plot_c_compare_HR, mean_c_comp*100,  color='k', 
                     yerr=mean_error*1.96*100,
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      mean_c_comp_no10 = np.array_split(avg_const_SD_init_no10, N)[j]
      mean_c_comp_no10 = np.insert(mean_c_comp_no10, 3, avg_init[3])
      mean_error_no10 = np.array_split(mean_err_const_SD_init_no10, N)[j]
      mean_error_no10 = np.insert(mean_error_no10, 3, mean_err_init[3])
      ax[1,j].errorbar(SD_to_plot_c_compare_no10_HR, mean_c_comp_no10*100,  color='k', 
                     yerr=mean_error_no10*1.96*100,
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      ax[0,j].set_title(text_for_legend[j])
      ax[0,j].text(0.03, 0.05, subplots_marks[j], fontsize=20,transform=ax[0,j].transAxes)
      ax[1,j].text(0.03, 0.05, subplots_marks[j+N], fontsize=20,transform=ax[1,j].transAxes)
      
    else:
      ax[0,j].errorbar(SD_to_plot_c_compare, np.array_split(avg_const_SD_init, N)[j]*100,  color='k', 
                     yerr=np.array_split(mean_err_const_SD_init, N)[j]*1.96*100,
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      ax[1,j].errorbar(SD_to_plot_c_compare_no10, np.array_split(avg_const_SD_init_no10, N)[j]*100,  color='k', 
                     yerr=np.array_split(mean_err_const_SD_init_no10, N)[j]*1.96*100,
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
    
    ax[0,0].set_ylabel(r"$\langle {P} \rangle \cdot 10^{2}$ [mm]")
    ax[0,j].set_xscale('log')
    ax[1,0].set_ylabel(r"$\langle {P} \rangle \cdot 10^{2}$ [mm]")
    ax[1,j].set_xscale('log')

    ax[0,j].set_title(text_for_legend[j])
    ax[0,j].text(0.03, 0.05, subplots_marks[j], fontsize=20,transform=ax[0,j].transAxes)
    ax[1,j].text(0.03, 0.05, subplots_marks[j+N], fontsize=20,transform=ax[1,j].transAxes)
    ax[1,j].set_xticks([10, 50, 100, 1000, 10000, 40000, 100000])
    ax[1,j].set_xlabel(r'$N_\mathrm{SD}^\mathrm{(bin)}$')
ax[1,3].set_xticks([10, 50, 100, 1000, 5000, 10000, 40000, 100000])
    

ax[0,0].set_ylim((0,4))
ax[0,1].set_ylim((0,2))
ax[0,2].set_ylim((1,5))
ax[0,3].set_ylim((10,19))
ax[1,0].set_ylim((0.75,2.25))
ax[1,1].set_ylim((0,0.25))
ax[1,2].set_ylim((1.9,3.2))
ax[1,3].set_ylim((10,13.75))


plt.subplots_adjust(left=0.06,
                bottom=0.06, 
                right=0.99, 
                top=0.95, 
                wspace=0.3, 
                hspace=0.1)

grid = plt.GridSpec(2, 4)
plt.savefig(f'{outfile_to_plot}Fig_12.pdf')

#Case compare std and cv - Fig_13

SD_to_plot_c_compare = [10, 50, 100, 1000, 10000, 40000, 100000]
SD_to_plot_c_compare_no10 = SD_to_plot_c_compare[1::]
SD_to_plot_c_compare_HR = [10, 50, 100, 1000, 5000, 10000, 40000, 100000]
SD_to_plot_c_compare_no10_HR = SD_to_plot_c_compare_HR[1::]
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
      STD_c_comp = np.array_split(std_const_SD_init, N)[j]
      STD_c_comp = np.insert(STD_c_comp, 4, std_init[3])
      error_down = np.array_split(std_err_const_SD_init_down, N)[j]
      error_down = np.insert(error_down, 4, std_err_init_down[3])
      error_up = np.array_split(std_err_const_SD_init_up, N)[j]
      error_up = np.insert(error_up, 4, std_err_init_up[3])  
      error_comp = np.array_split(std_err_const_SD_init, N)[j]
      error_comp = np.insert(error_comp, 4, std_err_init[3])

      ax[0,j].errorbar(SD_to_plot_c_compare_HR, STD_c_comp*100,  color='k',
                     yerr=(STD_c_comp*100 - error_down*100, error_up*100 - STD_c_comp*100 ), fmt=".",
                     alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)
    
      CV = (STD_c_comp/mean_c_comp)
      CV_error_1 =np.power(mean_error/mean_c_comp,2)
      CV_error_2 = np.power(error_comp/STD_c_comp,2)
      CV_error = np.sqrt(CV_error_1 + CV_error_2)

      ax[1,j].errorbar(SD_to_plot_c_compare_HR, CV,  color='k',  yerr=CV_error*CV, fmt=".",
                     alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)
      ax[0,j].set_title(text_for_legend[j])
      ax[1,j].set_xlabel(r'$N_\mathrm{SD}^\mathrm{(bin)}$')
      ax[0,j].get_xaxis().set_minor_formatter(matplotlib.ticker.LogFormatter())
      ax[0,j].text(0.03, 0.05, subplots_marks[j], fontsize=20,transform=ax[0,j].transAxes)
      ax[1,j].text(0.03, 0.05, subplots_marks[j+N], fontsize=20,transform=ax[1,j].transAxes)

    else:
      ax[0,j].errorbar(SD_to_plot_c_compare, np.array_split(std_const_SD_init, N)[j]*100,  color='k',
                     yerr=(np.array_split(std_const_SD_init, N)[j]*100 - np.array_split(std_err_const_SD_init_down, N)[j]*100,np.array_split(std_err_const_SD_init_up, N)[j]*100 - np.array_split(std_const_SD_init, N)[j]*100 ), fmt=".",
                     alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)
    
      CV = (np.array_split(std_const_SD_init, N)[j]/np.array_split(avg_const_SD_init, N)[j])
      CV_error_1 =np.power(np.array_split(mean_err_const_SD_init, N)[j]/np.array_split(avg_const_SD_init, N)[j],2)
      CV_error_2 = np.power(np.array_split(std_err_const_SD_init, N)[j]/np.array_split(std_const_SD_init, N)[j],2)
      CV_error = np.sqrt(CV_error_1 + CV_error_2)

      ax[1,j].errorbar(SD_to_plot_c_compare, CV,  color='k',  yerr=CV_error*CV, fmt=".",
                      alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)
      ax[0,j].set_title(text_for_legend[j])
      ax[0,0].set_ylabel(r"$\sigma (P) \cdot 10^{2}$ [mm]")
      ax[1,0].set_ylabel(r"$\sigma (P) /\langle {P}\rangle$ [-]")
      ax[0,j].set_xscale('log')
      ax[1,j].set_xlabel(r'$N_\mathrm{SD}^\mathrm{(bin)}$')
      ax[0,j].get_xaxis().set_minor_formatter(matplotlib.ticker.LogFormatter())
      ax[0,j].text(0.03, 0.05, subplots_marks[j], fontsize=20,transform=ax[0,j].transAxes)
      ax[1,j].text(0.03, 0.05, subplots_marks[j+N], fontsize=20,transform=ax[1,j].transAxes)
      ax[1,j].set_xticks([10, 50, 100, 1000, 10000, 40000, 100000])

ax[1,3].set_xticks([10, 50, 100, 1000, 5000, 10000, 40000, 100000])
ax[0,0].set_ylim((1.9,3.75))
ax[0,1].set_ylim((0,0.8))
ax[0,2].set_ylim((0,1.2))
ax[0,3].set_ylim((0,3.5))
ax[1,0].set_ylim((0,2.3))
ax[1,1].set_ylim((0,2.75))
ax[1,2].set_ylim((0,0.5))
ax[1,3].set_ylim((0,0.3))

plt.subplots_adjust(left=0.06,
                bottom=0.06, 
                right=0.99, 
                top=0.95, 
                wspace=0.3, 
                hspace=0.1)

grid = plt.GridSpec(2, 4)
plt.savefig(f'{outfile_to_plot}Fig_13.pdf')

#Initialization method comparison  - Fig_14

SD_to_plot_init = [10, 100, 1000, 5000, 10000]
text_for_legend_init = ['"constant SD" - init', r'$\xi_\mathrm{const}$-init', '"constant SD" fixed - init']
subplots_marks = {0:'(a)', 1:'(b)'}

def major_formatter(x, pos):
    return f'{x:.1f}'
plt.rcParams.update({'font.size': 22})
subplots_marks = {0:'(a)', 1:'(b)'}
L = int(len(text_for_legend_init))
fig3, ax3 = plt.subplots(2, 1, sharex=True)
fig3.set_size_inches(18.5, 15.5)
colors = ['k', 'r', 'g']
form = [".",".", "." ]

for j in range(len(text_for_legend_init)):  

    ax3[0].errorbar(SD_to_plot_init, np.array_split(avg_init, L)[j]*100,  color=colors[j],  yerr=np.array_split(mean_err_init, L)[j]*1.96*100,
                     fmt=form[j], ms=20,elinewidth=3,alpha=0.6, linestyle='--', label=text_for_legend_init[j], capsize=6, linewidth=3)
    
    ax3[0].set_ylabel(r"$\langle {P} \rangle\cdot 10^{2}$ [mm]")
    ax3[0].set_xscale('log')
    ax3[0].text(0.03, 0.05, subplots_marks[0], fontsize=20,transform=ax3[0].transAxes)
    
    ax3[1].errorbar(SD_to_plot_init, np.array_split(std_init, L)[j]*100,  color=colors[j],
                    yerr=(np.array_split(std_init, L)[j]*100 - np.array_split(std_err_init_down, L)[j]*100,np.array_split(std_err_init_up, L)[j]*100 - np.array_split(std_init, L)[j]*100 ),
                    fmt=form[j],alpha=0.6,elinewidth=3, ms=20, linestyle='--', capsize=6, linewidth=3)
    
    ax3[1].set_ylabel(r"$\sigma (P)\cdot 10^{2}$ [mm]")
    ax3[1].set_xscale('log')
    ax3[1].set_xlim(1, 40000)
    ax3[1].set_xlabel('$N_\mathrm{SD}^\mathrm{(bin)}$;$N_\mathrm{SD}^\mathrm{(init)}$')
    ax3[1].get_xaxis().set_minor_formatter(matplotlib.ticker.LogFormatter())
    ax3[1].set_ylim((-0.1,4))
    ax3[0].set_ylim((-1,20))
    ax3[1].text(0.03, 0.05, subplots_marks[1], fontsize=20,transform=ax3[1].transAxes)
    ax3[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, frameon=False)


plt.subplots_adjust(left=0.07,
                bottom=0.06, 
                right=0.98, 
                top=0.95, 
                wspace=0.3, 
                hspace=0.05)

grid = plt.GridSpec(2, 4)
plt.savefig('Fig_14.pdf')

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
      ax[0,j].errorbar(SD_to_plot_c_compare_HR, avg_f15[3*7:4*7+1]*100,  color='k',
                     yerr=((mean_err_f15[3*7:4*7+1])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      ax[0,j].errorbar(SD_to_plot_c_compare_HR, avg_OU[3*7:4*7+1]*100,  color='r',
                     yerr=((mean_err_OU[3*7:4*7+1])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      ax[0,j].text(0.03, 0.05, subplots_marks[j], fontsize=20,transform=ax[0,j].transAxes)
      ax[1,j].text(0.03, 0.05, subplots_marks[j+N], fontsize=20,transform=ax[1,j].transAxes)

      CV = (std_f15[3*7:4*7+1]/avg_f15[3*7:4*7+1])
      CV_error_1 =np.power(mean_err_f15[3*7:4*7+1]/avg_f15[3*7:4*7+1],2)
      CV_error_2 = np.power(std_err_f15[3*7:4*7+1]/std_f15[3*7:4*7+1],2)
      CV_error = np.sqrt(CV_error_1 + CV_error_2)

      ax[1,j].errorbar(SD_to_plot_c_compare_HR, CV,  color='k',  yerr=CV_error*CV, fmt=".",
                    alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)

      CV_OU = (std_OU[3*7:4*7+1]/avg_OU[3*7:4*7+1])
      CV_error_1_OU =np.power(mean_err_OU[3*7:4*7+1]/avg_OU[3*7:4*7+1],2)
      CV_error_2_OU = np.power(std_err_OU[3*7:4*7+1]/std_OU[3*7:4*7+1],2)
      CV_error_OU = np.sqrt(CV_error_1_OU + CV_error_2_OU)

      ax[1,j].errorbar(SD_to_plot_c_compare_HR, CV_OU,  color='r',  yerr=CV_error_OU*CV_OU, fmt=".",
                    alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)
      ax[0,j].set_title(text_for_legend[j])

    else:
      ax[0,j].errorbar(SD_to_plot_c_compare, avg_f15[0+j*7:7+j*7]*100,  color='k',
                     yerr=((mean_err_f15[0+j*7:7+j*7])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)
      ax[0,j].errorbar(SD_to_plot_c_compare, avg_OU[0+j*7:7+j*7]*100,  color='r',
                     yerr=((mean_err_OU[0+j*7:7+j*7])*1.96*100),
                     fmt=".", ms=20,elinewidth=3,alpha=0.6, linestyle=':', capsize=6)      

      CV = (std_f15[0+j*7:7+j*7]/avg_f15[0+j*7:7+j*7])
      CV_error_1 =np.power(mean_err_f15[0+j*7:7+j*7]/avg_f15[0+j*7:7+j*7],2)
      CV_error_2 = np.power(std_err_f15[0+j*7:7+j*7]/std_f15[0+j*7:7+j*7],2)
      CV_error = np.sqrt(CV_error_1 + CV_error_2)

      ax[1,j].errorbar(SD_to_plot_c_compare, CV,  color='k',  yerr=CV_error*CV, fmt=".",
                      alpha=0.6,elinewidth=3, ms=20, linestyle=':', capsize=6)

      CV_OU = (std_OU[0+j*7:7+j*7]/avg_OU[0+j*7:7+j*7])
      CV_error_1_OU =np.power(mean_err_OU[0+j*7:7+j*7]/avg_OU[0+j*7:7+j*7],2)
      CV_error_2_OU = np.power(std_err_OU[0+j*7:7+j*7]/std_OU[0+j*7:7+j*7],2)
      CV_error_OU = np.sqrt(CV_error_1_OU + CV_error_2_OU)

      ax[1,j].errorbar(SD_to_plot_c_compare, CV_OU,  color='r',  yerr=CV_error_OU*CV_OU, fmt=".",
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
plt.savefig(f'{outfile_to_plot}Fig_15_old.pdf')
