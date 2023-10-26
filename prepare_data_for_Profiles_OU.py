import numpy as np
import os

def read_my_array(file_obj):
    arr_name = file_obj.readline()
    file_obj.readline()  # discarded line with size of the array
    line = file_obj.readline()
    line = line.split(" ")
    del line[0]
    del line[len(line) - 1]
    arr = list(map(float, line))
    return np.array(arr), arr_name

def read_my_var(file_obj, var_name):
    file_obj.seek(0)
    while True:
        arr, name = read_my_array(file_obj)
        if str(name).strip() == str(var_name).strip():
            break
    return arr

#Pick which case you want to run and comment out the rest
main_path = '/home/piotr-pc/response/to_share/odp_do_odp/Final/Dane/'
root_path = f'{main_path}/prof/distance_no_ta_no_rx'

folders = ['start_4800_outfreq_240_tmax_300_SD10','start_4800_outfreq_240_tmax_300_SD100','start_4800_outfreq_240_tmax_300_SD1000']
# folders = ['start_4800_outfreq_240_tmax_300', 'start_4800_outfreq_240_tmax_3600']

subfolders = ['9600']

# Initialize lists to store the values of mean_r, sigma_r, disp_r, actrw_rw_cl_conc, rliq, prflux, position
mean_r_list = []
sigma_r_list = []
disp_r_list = []
actrw_rw_cl_conc_list = []
rliq_list = []
prflux_list = []
position_list = []
rd_geq_08um_conc_list = []
rd_lt_08um_conc_list =[]
# Loop over the folders and subfolders and extract the values
for folder in folders:
    for subfolder in subfolders:
        path = os.path.join(root_path, folder, subfolder)
        for filename in os.listdir(path):
            if filename.endswith('.dat'):
               with open(os.path.join(path, filename)) as f:
                    print(f)
                    # Read the values from the file
                    mean_r = read_my_var(f, "mean_r")
                    mean_r[mean_r == 0] = np.nan
                    mean_r_list.append(mean_r)

                    sigma_r = read_my_var(f, "sigma_r")
                    sigma_r[sigma_r == 0] = np.nan
                    sigma_r_list.append(sigma_r)

                    disp_r = read_my_var(f, "disp_r")
                    disp_r[disp_r == 0] = np.nan
                    disp_r_list.append(disp_r)

                    actrw_rw_cl_conc = read_my_var(f, "actrw_rw_cl_conc")
                    actrw_rw_cl_conc[actrw_rw_cl_conc == 0] = np.nan
                    actrw_rw_cl_conc_list.append(actrw_rw_cl_conc)

                    rliq = read_my_var(f, "rliq")
                    rliq[rliq == 0] = np.nan
                    rliq_list.append(rliq)

                    rd_geq_08um_conc = read_my_var(f, "rd_geq_0.8um_conc")
                    rd_geq_08um_conc[rd_geq_08um_conc == 0] = np.nan
                    rd_geq_08um_conc_list.append(rd_geq_08um_conc)

                    rd_lt_08um_conc = read_my_var(f, "rd_lt_0.8um_conc")
                    rd_lt_08um_conc[rd_lt_08um_conc == 0] = np.nan
                    rd_lt_08um_conc_list.append(rd_lt_08um_conc)

                    prflux = read_my_var(f, "prflux")
                    prflux[prflux == 0] = np.nan
                    prflux_list.append(prflux)

                    position = read_my_var(f, "position")
                    position_list.append(position)

        # Calculate the average values for each position separately
        mean_r_avg = np.nanmean(mean_r_list, axis=0)
        sigma_r_avg = np.nanmean(sigma_r_list, axis=0)
        disp_r_avg = np.nanmean(disp_r_list, axis=0)
        actrw_rw_cl_conc_avg = np.nanmean(actrw_rw_cl_conc_list, axis=0)
        rliq_avg = np.nanmean(rliq_list, axis=0)
        prflux_avg = np.nanmean(prflux_list, axis=0)
        rd_geq_08um_conc_avg = np.nanmean(rd_geq_08um_conc_list, axis=0)
        rd_lt_08um_conc_avg = np.nanmean(rd_lt_08um_conc_list, axis=0)
        position_avg = np.nanmean(position_list, axis=0)

        # Change all nan values to 0 in *_avg arrays
        mean_r_avg = np.nan_to_num(mean_r_avg)
        sigma_r_avg = np.nan_to_num(sigma_r_avg)
        disp_r_avg = np.nan_to_num(disp_r_avg)
        actrw_rw_cl_conc_avg = np.nan_to_num(actrw_rw_cl_conc_avg)
        rliq_avg = np.nan_to_num(rliq_avg)
        prflux_avg = np.nan_to_num(prflux_avg)
        rd_geq_08um_conc_avg = np.nan_to_num(rd_geq_08um_conc_avg)
        rd_lt_08um_conc_avg = np.nan_to_num(rd_lt_08um_conc_avg)
        position_avg = np.nan_to_num(position_avg)

        # Save the average values to a csv file
        mean_values = np.column_stack((mean_r_avg, sigma_r_avg, disp_r_avg, actrw_rw_cl_conc_avg, rliq_avg, prflux_avg, rd_geq_08um_conc_avg, rd_lt_08um_conc_avg,position_avg))
        output_filename = f"{main_path}/CSV/{folder}_{subfolder}_relax.csv"
        np.savetxt(output_filename, mean_values, delimiter=",")

        # Reset the lists for the next subfolder
        mean_r_list = []
        sigma_r_list = []
        disp_r_list = []
        actrw_rw_cl_conc_list = []
        rliq_list = []
        prflux_list = []
        position_list = []
        rd_geq_08um_conc_list = []
        rd_lt_08um_conc_list =[]