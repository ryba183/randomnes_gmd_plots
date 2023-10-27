from math import exp, log, sqrt, pi, erf, cos, pow, asin, atan, acos, factorial
import numpy as np
from scipy.stats import moment
from scipy.stats.distributions import chi2
from sys import argv
import glob, os


def prepare_data(path, save_name):

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

    def do_average(parameter_name, iter_value, path):
        dl = len(series_file[iter_value])
        average_list =[0 for i in range(len(path))]
        STD = [0 for i in range(len(path))]
        std_error = [0 for i in range(len(path))]
        std_error_up = [0 for i in range(len(path))]
        std_error_down = [0 for i in range(len(path))]
        mean_error = [0 for i in range(len(path))]
        Zmienna = np.zeros((len(series_file[iter_value])))
        for j in range(len(series_file[iter_value])):
            Zmienna[j] = read_my_var(series_file[iter_value][j], str(parameter_name))[-1]
        average_list[iter_value] = Zmienna.mean(0)
        STD[iter_value] = Zmienna.std(0)
        mean_error[iter_value] = Zmienna.std(0)/sqrt(dl)
        std_error[iter_value] = np.power(1/dl * (moment(Zmienna,4) - (dl-3)/(dl-1)*np.power(STD[iter_value],4)),1/2)/(2*STD[iter_value])#nowa wersja powiina być dobra!
        std_error[iter_value] = np.nan_to_num(std_error[iter_value])
        std_error_down[iter_value] = STD[iter_value] *np.power((dl-1)/chi2.ppf(1-(0.05/2), df=dl-1) ,1/2)
        std_error_up[iter_value] = STD[iter_value] * np.power((dl-1)/chi2.ppf(0.05/2, df=dl-1) ,1/2)
        #Error from this https://stats.stackexchange.com/questions/156518/what-is-the-standard-error-of-the-sample-standard-deviation
        return average_list[iter_value], STD[iter_value], std_error[iter_value], mean_error[iter_value], std_error_up[iter_value], std_error_down[iter_value]

    files = [0 for i in range(len(path))]
    series_file = [0 for i in range(len(path))]

    for p in range(len(path)):
        os.chdir(path[p])
        series_file[p] = [open(file_names, "r") for file_names in glob.glob("*.dat")]
        files[p] = glob.glob("*.dat")

    average_list, STD, std_error, mean_error, std_error_upp, std_error_downn = [[0 for i in range(len(paths))] for i in range(6)]
    for n in range(len(paths)):
        average_list[n], STD[n], std_error[n], mean_error[n], std_error_upp[n], std_error_downn[n]  = do_average("acc_precip", n, path)

    np.save(outfile+'average_'+save_name, average_list)
    np.save(outfile+'STD_'+save_name, STD)
    np.save(outfile+'std_error_'+save_name, std_error)
    np.save(outfile+'mean_error_'+save_name, mean_error)
    np.save(outfile+'paths_'+save_name, paths)
    np.save(outfile+'std_error_up_'+save_name, std_error_upp)
    np.save(outfile+'std_error_down_'+save_name, std_error_downn)

path = ""#provide path to DATA folder
outfile_to_plot = ''#provide path to save the figure
######### DATA FOR FIG 10
paths = [f'{path}/D/constant_SD_init/coalescence_substep/005/',
         f'{path}/D/constant_SD_init/coalescence_substep/01/',
         f'{path}/D/constant_SD_init/coalescence_substep/05/',
         f'{path}/LR/constant_SD_init/coalescence_substep/005/',
         f'{path}/LR/constant_SD_init/coalescence_substep/01/',
         f'{path}/LR/constant_SD_init/coalescence_substep/05/',
         f'{path}/MR/constant_SD_init/coalescence_substep/005/',
         f'{path}/MR/constant_SD_init/coalescence_substep/01/',
         f'{path}/MR/constant_SD_init/coalescence_substep/05/',
         f'{path}/HR/constant_SD_init/coalescence_substep/005/',
         f'{path}/HR/constant_SD_init/coalescence_substep/01/',
         f'{path}/HR/constant_SD_init/coalescence_substep/05/']

outfile = f'{outfile_to_plot}/coalescence/'
outfile_name = 'coalescence'
prepare_data(paths, outfile_name)

######### DATA FOR FIG 11 (a-d) & FIG 13
paths = [f'{path}/D/constant_SD_init/SD10/',
         f'{path}/D/constant_SD_init/SD50/',
         f'{path}/D/constant_SD_init/SD100/',
         f'{path}/D/constant_SD_init/SD1000/',
         f'{path}/D/constant_SD_init/SD10000/',
         f'{path}/D/constant_SD_init/SD40000/',
         f'{path}/D/constant_SD_init/SD100000/',
         f'{path}/LR/constant_SD_init/SD10/',
         f'{path}/LR/constant_SD_init/SD50/',
         f'{path}/LR/constant_SD_init/SD100/',
         f'{path}/LR/constant_SD_init/SD1000/',
         f'{path}/LR/constant_SD_init/SD10000/',
         f'{path}/LR/constant_SD_init/SD40000/',
         f'{path}/LR/constant_SD_init/SD100000/',
         f'{path}/MR/constant_SD_init/SD10/',
         f'{path}/MR/constant_SD_init/SD50/',
         f'{path}/MR/constant_SD_init/SD100/',
         f'{path}/MR/constant_SD_init/SD1000/',
         f'{path}/MR/constant_SD_init/SD10000/',
         f'{path}/MR/constant_SD_init/SD40000/',
         f'{path}/MR/constant_SD_init/SD100000/',
         f'{path}/HR/constant_SD_init/SD10/',
         f'{path}/HR/constant_SD_init/SD50/',
         f'{path}/HR/constant_SD_init/SD100/',
         f'{path}/HR/constant_SD_init/SD1000/',
         f'{path}/HR/constant_SD_init/SD10000/',
         f'{path}/HR/constant_SD_init/SD40000/',
         f'{path}/HR/constant_SD_init/SD100000/']

outfile = f'{outfile_to_plot}/init/'
outfile_name = 'constant_SD_init'
prepare_data(paths, outfile_name)

######### DATA FOR FIG 11 (e-h)
paths = [f'{path}/D/constant_SD_init/SD50/',
         f'{path}/D/constant_SD_init/SD100/',
         f'{path}/D/constant_SD_init/SD1000/',
         f'{path}/D/constant_SD_init/SD10000/',
         f'{path}/D/constant_SD_init/SD40000/',
         f'{path}/D/constant_SD_init/SD100000/',
         f'{path}/LR/constant_SD_init/SD50/',
         f'{path}/LR/constant_SD_init/SD100/',
         f'{path}/LR/constant_SD_init/SD1000/',
         f'{path}/LR/constant_SD_init/SD10000/',
         f'{path}/LR/constant_SD_init/SD40000/',
         f'{path}/LR/constant_SD_init/SD100000/',
         f'{path}/MR/constant_SD_init/SD50/',
         f'{path}/MR/constant_SD_init/SD100/',
         f'{path}/MR/constant_SD_init/SD1000/',
         f'{path}/MR/constant_SD_init/SD10000/',
         f'{path}/MR/constant_SD_init/SD40000/',
         f'{path}/MR/constant_SD_init/SD100000/',
         f'{path}/HR/constant_SD_init/SD50/',
         f'{path}/HR/constant_SD_init/SD100/',
         f'{path}/HR/constant_SD_init/SD1000/',
         f'{path}/HR/constant_SD_init/SD10000/',
         f'{path}/HR/constant_SD_init/SD40000/',
         f'{path}/HR/constant_SD_init/SD100000/']


outfile = f'{outfile_to_plot}/init/'
outfile_name = 'constant_SD_init_no10'
prepare_data(paths, outfile_name)

######### DATA FOR FIG 14 
paths = [f'{path}/HR/constant_SD_init/SD10/',
         f'{path}/HR/constant_SD_init/SD100/',
         f'{path}/HR/constant_SD_init/SD1000/',
         f'{path}/HR/constant_SD_init/SD5000/',
         f'{path}/HR/constant_SD_init/SD10000/',
         f'{path}/HR/const_multiplicity_init/SD10/',
         f'{path}/HR/const_multiplicity_init/SD100/',
         f'{path}/HR/const_multiplicity_init/SD1000/',
         f'{path}/HR/const_multiplicity_init/SD5000/',
         f'{path}/HR/const_multiplicity_init/SD10000/',
         f'{path}/HR/constant_SD_fixed_init/SD10/',
         f'{path}/HR/constant_SD_fixed_init/SD100/',
         f'{path}/HR/constant_SD_fixed_init/SD1000/',
         f'{path}/HR/constant_SD_fixed_init/SD5000/',
         f'{path}/HR/constant_SD_fixed_init/SD10000/']
       

outfile = f'{outfile_to_plot}/initialization/'
outfile_name = 'SD_initialization'
prepare_data(paths, outfile_name)

######### DATA FOR FIG 15 
paths = [f'{path}/D/mixing/SD10/',
        f'{path}/D/mixing/SD50/',
        f'{path}/D/mixing/SD100/',
        f'{path}/D/mixing/SD1000/',
        f'{path}/D/mixing/SD10000/',
        f'{path}/D/mixing/SD40000/',
        f'{path}/D/mixing/SD100000/',
        f'{path}/LR/mixing/SD10/',
        f'{path}/LR/mixing/SD50/',
        f'{path}/LR/mixing/SD100/',
        f'{path}/LR/mixing/SD1000/',
        f'{path}/LR/mixing/SD10000/',
        f'{path}/LR/mixing/SD40000/',
        f'{path}/LR/mixing/SD100000/',
        f'{path}/MR/mixing/SD10/',
        f'{path}/MR/mixing/SD50/',
        f'{path}/MR/mixing/SD100/',
        f'{path}/MR/mixing/SD1000/',
        f'{path}/MR/mixing/SD10000/',
        f'{path}/MR/mixing/SD40000/',
        f'{path}/MR/mixing/SD100000/',
        f'{path}/HR/mixing/SD10/',
        f'{path}/HR/mixing/SD50/',
        f'{path}/HR/mixing/SD100/',
        f'{path}/HR/mixing/SD1000/',
        f'{path}/HR/mixing/SD5000/',
        f'{path}/HR/mixing/SD10000/',
        f'{path}/HR/mixing/SD40000/',
        f'{path}/HR/mixing/SD100000/']
        
outfile = f'{outfile_to_plot}/mixing/old/'
outfile_name = 'OU'
prepare_data(paths, outfile_name)

paths = [f'{path}/D/constant_SD_init/SD10/',
         f'{path}/D/constant_SD_init/SD50/',
         f'{path}/D/constant_SD_init/SD100/',
         f'{path}/D/constant_SD_init/SD1000/',
         f'{path}/D/constant_SD_init/SD10000/',
         f'{path}/D/constant_SD_init/SD40000/',
         f'{path}/D/constant_SD_init/SD100000/',
         f'{path}/LR/constant_SD_init/SD10/',
         f'{path}/LR/constant_SD_init/SD50/',
         f'{path}/LR/constant_SD_init/SD100/',
         f'{path}/LR/constant_SD_init/SD1000/',
         f'{path}/LR/constant_SD_init/SD10000/',
         f'{path}/LR/constant_SD_init/SD40000/',
         f'{path}/LR/constant_SD_init/SD100000/',
         f'{path}/MR/constant_SD_init/SD10/',
         f'{path}/MR/constant_SD_init/SD50/',
         f'{path}/MR/constant_SD_init/SD100/',
         f'{path}/MR/constant_SD_init/SD1000/',
         f'{path}/MR/constant_SD_init/SD10000/',
         f'{path}/MR/constant_SD_init/SD40000/',
         f'{path}/MR/constant_SD_init/SD100000/',
         f'{path}/HR/constant_SD_init/SD10/',
         f'{path}/HR/constant_SD_init/SD50/',
         f'{path}/HR/constant_SD_init/SD100/',
         f'{path}/HR/constant_SD_init/SD1000/',
         f'{path}/HR/constant_SD_init/SD5000/',
         f'{path}/HR/constant_SD_init/SD10000/',
         f'{path}/HR/constant_SD_init/SD40000/',
         f'{path}/HR/constant_SD_init/SD100000/']

outfile = f'{outfile_to_plot}/init/Fig_15/'
outfile_name = 'constant_SD_init'
prepare_data(paths, outfile_name)

paths = [f'{path}/D/distance_D/start_4800_outfreq_240_tmax_300_SD10',
         f'{path}/D/distance_D/start_4800_outfreq_240_tmax_300_SD100',
         f'{path}/D/distance_D/start_4800_outfreq_240_tmax_300_SD1000',
         f'{path}/HR/distance/start_4800_outfreq_240_tmax_300_SD10',
         f'{path}/HR/distance/start_4800_outfreq_240_tmax_300_SD100',
         f'{path}/HR/distance/start_4800_outfreq_240_tmax_300_SD1000']
outfile = f'{outfile_to_plot}/mixing/'
outfile_name = 'OU'
prepare_data(paths, outfile_name)