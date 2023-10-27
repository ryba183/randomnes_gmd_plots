#PLOTS WITH COALESCENCE
from math import exp, log, sqrt, pi, erf, cos, pow, asin, atan, acos, factorial
import numpy as np
from sys import argv
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter, LogFormatter, LogLocator, LogFormatterSciNotation, AutoMinorLocator
import glob, os
plt.rcParams.update({'font.size': 22})

def multiplot_cases(name, paths, label, outfile, sd, cth, cc, cwp, rwp, prec):
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
        average =[0 for i in range(len(paths))]
        STD = [0 for i in range(len(paths))]
        variable = np.zeros((len(series_file[iter_value]),len(read_my_var(series_file[iter_value][0], str(parameter_name)))))
        for j in range(len(series_file[iter_value])):
            variable[j] = read_my_var(series_file[iter_value][j], str(parameter_name))
        average[iter_value] = variable.mean(0)
        STD[iter_value] = variable.std(0)
        return average[iter_value], STD[iter_value]

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
        average = do_average("cloud_top_height", p, paths)[0]
        STD = do_average("cloud_top_height", p, paths)[1]
        time = do_time(p)
        plt.plot(time, average,  color=colors[p], linewidth=3, label=(label[p]))
        plt.ylim((0, cth))
        plt.ylabel("CTH [m]")
        plt.text(100,cth*0.9,"(a)",fontsize = 22)
        # plt.legend(title=r"$N_\mathrm{SD}^\mathrm{(bin)}$ "+f"for {sd} scenario:", loc='upper center',
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.55), ncol=7,frameon=0 )
        plt.tick_params('x', labelbottom=False)
    axis2 = plt.subplot(512, sharex=axis1)
    for p in range(len(paths)):
        LWM = do_average("cloud_cover_rico", p, paths)[0]
        STD_LWM = do_average("cloud_cover_rico", p, paths)[1]
        time = do_time(p)
        plt.plot(time, LWM,  color=colors[p], linewidth=3, label=label[p])
        plt.ylabel("Cloud Cover [-]")
        plt.ylim((0, cc))
        plt.text(100,cc*0.9,"(b)",fontsize = 22)
        plt.tick_params('x', labelbottom=False)
    axis3 = plt.subplot(513, sharex=axis1)
    for p in range(len(paths)):
        average = do_average("cwp", p, paths)[0]
        STD = do_average("cwp", p, paths)[1]
        time = do_time(p)
        plt.plot(time, average,  color=colors[p], linewidth=3, label=(label[p]))
        plt.ylabel(r"CWP [g/m$^2$]")
        plt.ylim((0, cwp))
        plt.text(100,cwp*0.9,"(c)",fontsize = 22)
        plt.tick_params('x', labelbottom=False)
    axis4 = plt.subplot(514, sharex=axis1)
    for p in range(len(paths)):
        average = do_average("rwp", p, paths)[0]
        STD = do_average("rwp", p, paths)[1]
        time = do_time(p)
        plt.plot(time, average,  color=colors[p], linewidth=3, label=(label[p]))
        plt.ylabel(r"RWP [g/m$^2$]")
        plt.xlim((0, 10850))
        plt.ylim((0, rwp))
        plt.tick_params('x', labelbottom=False)
        plt.text(100,rwp*0.9,"(d)",fontsize = 22)
    axis5 = plt.subplot(515)
    for p in range(len(paths)):
        average = do_average("surf_precip", p, paths)[0]
        LWM = do_average("cloud_cover_rico", p, paths)[0]
        STD = do_average("surf_precip", p, paths)[1]
        time = do_time(p)
        plt.plot(time, average/LWM/24,  color=colors[p], linewidth=4, label=(label[p]))
        plt.xlabel("time [s]")
        plt.ylabel("Precipitation [mm/h] ")
        plt.xlim((0, 10850))
        plt.yscale('log')
        plt.ylim((10**-2, prec))
        plt.text(100,prec*0.5,"(e)",fontsize = 22)
    fig.tight_layout()
    fig.savefig(outfile + 'fig0'+name+'s.pdf')

#PLOTS WITHOUT COALESCENCE


def multiplot_cases_no_coal_no_rwp(name, paths, label, outfile, sd, cth, cc, cwp):
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
        average =[0 for i in range(len(paths))]
        STD = [0 for i in range(len(paths))]
        variable = np.zeros((len(series_file[iter_value]),len(read_my_var(series_file[iter_value][0], str(parameter_name)))))
        for j in range(len(series_file[iter_value])):
            variable[j] = read_my_var(series_file[iter_value][j], str(parameter_name))
        average[iter_value] = variable.mean(0)
        STD[iter_value] = variable.std(0)
        return average[iter_value], STD[iter_value]

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
    num_colors = 8 # You can change this to your desired number
    # Create a list of colors from the "gnuplot" colormap
    colors = [plt.cm.cool(i / num_colors) for i in range(num_colors)]

    fig.set_size_inches(14.5, 20.5)
    axis1 = plt.subplot(311)
    for p in range(len(paths)):
        average = do_average("cloud_top_height", p, paths)[0]
        STD = do_average("cloud_top_height", p, paths)[1]
        time = do_time(p)
        plt.plot(time, average,  color=colors[p], linewidth=4, label=(label[p]))
        plt.ylim((0, cth))
        plt.ylabel("CTH [m]")
        plt.xlim((0, 10850))
        plt.text(100,cth*0.9,"(a)",fontsize = 22)
        # plt.legend(title=r"$N_\mathrm{SD}^\mathrm{(bin)}$ "+f"for {sd} scenario:", loc='upper center',
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=7,frameon=0 )
        plt.tick_params('x', labelbottom=False)
    axis2 = plt.subplot(312, sharex=axis1)
    for p in range(len(paths)):
        LWM = do_average("cloud_cover_rico", p, paths)[0]
        STD_LWM = do_average("cloud_cover_rico", p, paths)[1]
        time = do_time(p)
        plt.plot(time, LWM,  color=colors[p], linewidth=4, label=label[p])
        plt.ylabel("Cloud Cover [-]")
        plt.xlim((0, 10850))
        plt.ylim((0, cc))
        plt.text(100,cc*0.9,"(b)",fontsize = 22)
        plt.tick_params('x', labelbottom=False)
    axis3 = plt.subplot(313, sharex=axis1)
    for p in range(len(paths)):
        average = do_average("cwp", p, paths)[0]
        STD = do_average("cwp", p, paths)[1]
        time = do_time(p)
        plt.plot(time, average,  color=colors[p], linewidth=4, label=(label[p]))
        plt.ylabel(r"CWP [g/m$^2$]")
        plt.xlim((0, 10850))
        plt.ylim((0, cwp))
        plt.text(100,cwp*0.9,"(c)",fontsize = 22)
        plt.xlabel("time [s]")
    fig.tight_layout()
    fig.savefig(outfile + 'fig0'+name+'s.pdf')

######################TIME SERIES WITH COALESCENCE
Case = ['D', 'LR', 'MR', 'HR']
Cth = [4000,4000, 4000,5000 ]
Cc = [0.25, 0.3, 0.3, 0.3]
Cwp = [80, 100, 150, 200]
Rwp = [40, 40, 100, 225]
Prec = [1, 1, 10, 50]
Fig_number = [8,2,4,6]


path = ""#provide path to DATA folder
outfile_to_plot = ''#provide path to save the figure

for ca, cth, cc, cwp, rwp, prec, f_num in zip(Case, Cth,Cc, Cwp, Rwp,Prec,Fig_number):
    name_to_plot = f'{f_num}'
    paths_to_plot = [
                     f'{path}/{ca}/constant_SD_init/SD10',
                     f'{path}/{ca}/constant_SD_init/SD50',
                     f'{path}/{ca}/constant_SD_init/SD100',
                     f'{path}/{ca}/constant_SD_init/SD1000',
                     f'{path}/{ca}/constant_SD_init/SD10000',
                     f'{path}/{ca}/constant_SD_init/SD40000',
                     f'{path}/{ca}/constant_SD_init/SD100000']
    label_to_plot = [ 10, 50, 100, 1000, 10000, 40000, 100000]
    outfile_to_plot = f'{outfile_to_plot}'

    multiplot_cases(name_to_plot, paths_to_plot, label_to_plot, outfile_to_plot, ca, cth, cc, cwp, rwp, prec)

######################TIME SERIES WITHOUT COALESCENCE
Case = ['D', 'LR', 'MR', 'HR']
Cth = [4000,4000, 4000,5000 ]
Cc = [0.25, 0.3, 0.3, 0.3]
Cwp = [100, 100, 150, 225]
Rwp = [20, 20, 50, 80]
Fig_number = [9,3,5,7]

for ca, cth, cc, cwp, rwp, f_num in zip(Case, Cth,Cc, Cwp, Rwp, Fig_number):
    name_to_plot = f'{f_num}'
    paths_to_plot = [
                     f'{path}/{ca}/constant_SD_init_no_coalescence/SD10',
                     f'{path}/{ca}/constant_SD_init_no_coalescence/SD50',
                     f'{path}/{ca}/constant_SD_init_no_coalescence/SD100',
                     f'{path}/{ca}/constant_SD_init_no_coalescence/SD1000',
                     f'{path}/{ca}/constant_SD_init_no_coalescence/SD10000',
                     f'{path}/{ca}/constant_SD_init_no_coalescence/SD40000']
    label_to_plot = [ 10, 50, 100, 1000, 10000, 40000]
    outfile_to_plot = f'{outfile_to_plot}'

    multiplot_cases_no_coal_no_rwp(name_to_plot, paths_to_plot, label_to_plot, outfile_to_plot, ca, cth, cc, cwp)
    
