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


paths = ['/home/piotr-pc/response/TEST_PIOTRA/Dane/D_ta/time_series/SD10/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/D_ta/time_series/SD50/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/D_ta/time_series/SD100/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/D_ta/time_series/SD1000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/D_ta/time_series/SD10000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/D_ta/time_series/SD40000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/D_ta/time_series/SD100000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/LR_ta/time_series/SD10/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/LR_ta/time_series/SD50/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/LR_ta/time_series/SD100/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/LR_ta/time_series/SD1000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/LR_ta/time_series/SD10000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/LR_ta/time_series/SD40000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/LR_ta/time_series/SD100000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/MR_ta/time_series/SD10/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/MR_ta/time_series/SD50/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/MR_ta/time_series/SD100/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/MR_ta/time_series/SD1000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/MR_ta/time_series/SD10000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/MR_ta/time_series/SD40000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/MR_ta/time_series/SD100000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/HR_ta/time_series/SD10/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/HR_ta/time_series/SD50/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/HR_ta/time_series/SD100/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/HR_ta/time_series/SD1000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/HR_ta/time_series/SD5000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/HR_ta/time_series/SD10000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/HR_ta/time_series/SD40000/',
        '/home/piotr-pc/response/TEST_PIOTRA/Dane/HR_ta/time_series/SD100000/']
outfile = '/home/piotr-pc/response/to_share/odp_do_odp/Final/Dane/time_series/precip_data/GA17_old/'
outfile_name = 'GA17'
# prepare_data(paths, outfile_name)

path_to_old = '/home/piotr-pc/response/to_share/Cumulus_Congestus'
paths = [f'{path_to_old}/DATA/D/constant_SD_init/SD10/',
         f'{path_to_old}/DATA/D/constant_SD_init/SD50/',
         f'{path_to_old}/DATA/D/constant_SD_init/SD100/',
         f'{path_to_old}/DATA/D/constant_SD_init/SD1000/',
         f'{path_to_old}/DATA/D/constant_SD_init/SD10000/',
         f'{path_to_old}/DATA/D/constant_SD_init/SD40000/',
         f'{path_to_old}/DATA/D/constant_SD_init/SD100000/',
         f'{path_to_old}/DATA/LR/constant_SD_init/SD10/',
         f'{path_to_old}/DATA/LR/constant_SD_init/SD50/',
         f'{path_to_old}/DATA/LR/constant_SD_init/SD100/',
         f'{path_to_old}/DATA/LR/constant_SD_init/SD1000/',
         f'{path_to_old}/DATA/LR/constant_SD_init/SD10000/',
         f'{path_to_old}/DATA/LR/constant_SD_init/SD40000/',
         f'{path_to_old}/DATA/LR/constant_SD_init/SD100000/',
         f'{path_to_old}/DATA/MR/constant_SD_init/SD10/',
         f'{path_to_old}/DATA/MR/constant_SD_init/SD50/',
         f'{path_to_old}/DATA/MR/constant_SD_init/SD100/',
         f'{path_to_old}/DATA/MR/constant_SD_init/SD1000/',
         f'{path_to_old}/DATA/MR/constant_SD_init/SD10000/',
         f'{path_to_old}/DATA/MR/constant_SD_init/SD40000/',
         f'{path_to_old}/DATA/MR/constant_SD_init/SD100000/',
         f'{path_to_old}/DATA/HR/constant_SD_init/SD10/',
         f'{path_to_old}/DATA/HR/constant_SD_init/SD50/',
         f'{path_to_old}/DATA/HR/constant_SD_init/SD100/',
         f'{path_to_old}/DATA/HR/constant_SD_init/SD1000/',
         f'{path_to_old}/DATA/HR/constant_SD_init/SD5000/',
         f'{path_to_old}/DATA/HR/constant_SD_init/SD10000/',
         f'{path_to_old}/DATA/HR/constant_SD_init/SD40000/',
         f'{path_to_old}/DATA/HR/constant_SD_init/SD100000/']

outfile = '/home/piotr-pc/response/to_share/odp_do_odp/Final/Dane/time_series/precip_data/ALL_old/'
outfile_name = 'constant_SD_init'
prepare_data(paths, outfile_name)