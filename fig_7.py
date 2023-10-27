from math import exp, log, sqrt, pi, erf, cos, pow, asin, atan, acos, factorial
import numpy as np
from sys import argv
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter, LogFormatter, LogLocator, LogFormatterSciNotation, AutoMinorLocator
import glob, os
plt.rcParams.update({'font.size': 18})

def multiplot(paths, label, outfile, sd):

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
        return arr

    def do_average(parameter_name, iter_value, paths):
        dl = len(parameter_name)
        average_list =[0 for i in range(len(paths))]
        STD = [0 for i in range(len(paths))]
        data_list = np.zeros((len(series_file[iter_value]),len(read_my_var(series_file[iter_value][0], str(parameter_name)))))
        for j in range(len(series_file[iter_value])):
            data_list[j] = read_my_var(series_file[iter_value][j], str(parameter_name))
        average_list[iter_value] = data_list.mean(0)
        STD[iter_value] = data_list.std(0)
        return average_list[iter_value], STD[iter_value]

    def do_time(iter_value):
        for j in range(len(series_file[iter_value])):
            time = read_my_var(series_file[iter_value][j], "position")
        return time

    files = [0 for i in range(len(paths))]
    series_file = [0 for i in range(len(paths))]

    for p in range(len(paths)):
        os.chdir(paths[p])
        series_file[p] = [open(file_names, "r") for file_names in glob.glob("*.dat")]
        files[p] = glob.glob("*.dat")

    fig = plt.figure()
    fig.set_size_inches(18.5, 10.5)
    # Number of colors you need
    num_colors = 8 # You can change this to your desired number
    # Create a list of colors from the "gnuplot" colormap
    colors = [plt.cm.cool(i / num_colors) for i in range(num_colors)]

    fig.set_size_inches(14.5, 20.5)
    axis1 = plt.subplot(511)
    for p in range(len(paths)):
        CTH = do_average("cloud_top_height", p, paths)[0]
        time = do_time(p)
        plt.plot(time, CTH,  color=colors[p], linewidth=3, label=(label[p]))
        plt.ylim((0, 5000))
        plt.ylabel("CTH [m]")
        plt.text(100,5000*0.9,"(a)",fontsize = 22)
        plt.legend(title=r"$N_\mathrm{SD}^\mathrm{(bin)}$ = "+f"{sd} for tested scenarios:", loc='upper center',
                bbox_to_anchor=(0.5, 1.35), ncol=7,frameon=0 )
        plt.tick_params('x', labelbottom=False)
    axis2 = plt.subplot(512, sharex=axis1)
    for p in range(len(paths)):
        CC = do_average("cloud_cover_rico", p, paths)[0]
        time = do_time(p)
        plt.plot(time, CC,  color=colors[p], linewidth=3, label=label[p])
        plt.ylabel("Cloud Cover [-]")
        plt.ylim((0, 0.3))
        plt.text(100,0.3*0.9,"(b)",fontsize = 22)
        plt.tick_params('x', labelbottom=False)
    axis3 = plt.subplot(513, sharex=axis1)
    for p in range(len(paths)):
        CWP = do_average("cwp", p, paths)[0]
        time = do_time(p)
        plt.plot(time, CWP,  color=colors[p], linewidth=3, label=(label[p]))
        plt.ylabel(r"CWP [g/m$^2$]")
        plt.ylim((0, 200))
        plt.text(100,200*0.9,"(c)",fontsize = 22)
        plt.tick_params('x', labelbottom=False)
    axis4 = plt.subplot(514, sharex=axis1)
    for p in range(len(paths)):
        RWP = do_average("rwp", p, paths)[0]
        time = do_time(p)
        plt.plot(time, RWP,  color=colors[p], linewidth=3, label=(label[p]))
        plt.ylabel(r"RWP [g/m$^2$]")
        plt.xlim((0, 10850))
        plt.ylim((0, 220))
        plt.tick_params('x', labelbottom=False)
        plt.text(100,220*0.9,"(d)",fontsize = 22)
    axis5 = plt.subplot(515)
    for p in range(len(paths)):
        Sur_precip = do_average("surf_precip", p, paths)[0]
        CC = do_average("cloud_cover_rico", p, paths)[0]
        time = do_time(p)
        plt.plot(time, Sur_precip/CC/24,  color=colors[p], linewidth=4, label=(label[p]))
        plt.xlabel("time [s]")
        plt.ylabel("Precipitation [mm/h] ")
        plt.xlim((0, 10850))
        plt.yscale('log')
        plt.ylim((10**-2, 2*10))
        plt.text(100,2*10*0.5,"(e)",fontsize = 22)
    fig.tight_layout()
    fig.savefig(outfile + 'Fig_7.pdf')


sd = 100
path = ""#provide path to DATA folder
outfile_to_plot = ''#provide path to save the figure
paths_to_plot = [f'{path}/D/constant_SD_init/SD{sd}',
        f'{path}/LR/constant_SD_init/SD{sd}',
        f'{path}/MR/constant_SD_init/SD{sd}',
        f'{path}/HR/constant_SD_init/SD{sd}']
label_to_plot = [ 'D','LR', 'MR', 'HR']

multiplot(paths_to_plot, label_to_plot, outfile_to_plot,sd)