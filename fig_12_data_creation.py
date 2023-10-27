import argparse
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

def plot_histograms(vars, time_start, time_end, level_start, level_end, dirs, labels, outfreq, normalize=False, mask_rico=False):
    nx = {}
    ny = {}
    nz = {}
    dx = {}
    dz = {}
    ref = {}
    mean_values = []
    final_result = []
    mean_values_mean = []
    mean_values_std = []
    for y in range(len(vars)):
        mean_values.append([])
        final_result.append([])
        mean_values_mean.append([])
        mean_values_std.append([])
    total_arr = OrderedDict()
    plot_labels = OrderedDict()

    # Directories loop
    for directory, lab in zip(dirs, labels):
        can_plot_refined_RH_derived = True
        for root, dirs, files in os.walk(directory):
            if root.endswith("out_lgrngn"):
                file_path = root

                # Init parameters from const.h5
                with h5py.File(file_path + "/const.h5", 'r') as consth5:
                    user_params = consth5.get("user_params")
                    if outfreq is None:
                        outfreq = int(user_params.attrs["outfreq"][0])
                    else:
                        outfreq = outfreq

                    advection = consth5.get("advection")
                    dx_adve = advection.attrs["di"]  # Its the resolved dx
                    dz_adve = advection.attrs["dj"]  # Its the resolved dx
                    dt = advection.attrs["dt"]
                    nx_adve = consth5["X"][:, :].shape[0] - 1
                    nz_adve = consth5["Y"][:, :].shape[1] - 1
                    X = dx_adve * (nx_adve - 1)
                    Y = dz_adve * (nz_adve - 1)
                    p_e = consth5["p_e"][:]
                    try:
                        refined_p_e = consth5["refined p_e"][:]
                    except:
                        can_plot_refined_RH_derived = False
                        print("'refined p_e' not found in const.h5. Won't be able to plot refined_RH_derived")
                i = 0
                # Variables loop
                for var in vars:
                    if not can_plot_refined_RH_derived and var == "refined RH_derived":
                        print("Skipping the refined_RH_derived plot")
                    time_start_idx = int(time_start / dt)
                    time_end_idx = int(time_end / dt)
                    # Init variable-specific array parameters based on the first timestep
                    filename = root + "/timestep" + str(time_start_idx).zfill(10) + ".h5"
                    if var == 'mean_radius':
                            w3d = h5py.File(filename, "r")['actrw_rw_mom0'][:, :]
                    elif var == 'disspersion':
                            w3d = h5py.File(filename, "r")['actrw_rw_mom0'][:, :]
                    else:
                        w3d = h5py.File(filename, "r")[var][:, :]
                    nx, nz = tuple(x for x in w3d.shape)
                    dx = X / (nx - 1)
                    ref = int(dx_adve / dx)
                    dz = Y / (nz - 1)
                    assert (float(level_start / dz).is_integer())
                    assert (float(level_end / dz).is_integer())
                    level_start_idx = int(level_start / dz)
                    level_end_idx = int(level_end / dz) + 1
                    lab_var = lab + '_' + str(var)
                    if mask_rico:
                        try:
                            mask = h5py.File(filename, "r")["cloud_rw_mom3"][:, :]
                            if mask.shape != w3d.shape:
                                print("Cloud mask shape is different than " + var + " shape. Skipping the plot.")
                        except:
                            print("Can't find cloud_rw_mom3 data, so can't use RICO cloud mask. Skipping the plot.")
                    total_arr = np.zeros(0)
                    # Time loop
                    for t in range(time_start_idx, time_end_idx + 1, outfreq):
                        filename = root + "/timestep" + str(t).zfill(10) + ".h5"
                        # Read the variable
                        if var == 'mean_radius':
                            w3d_0 = h5py.File(filename, "r")['actrw_rw_mom0'][0:nx - 1, level_start_idx:level_end_idx]
                            w3d_1 = h5py.File(filename, "r")['actrw_rw_mom1'][0:nx - 1, level_start_idx:level_end_idx]
                            w3d = w3d_1 / w3d_0
                        elif var == 'disspersion':
                            w3d_0 = h5py.File(filename, "r")['actrw_rw_mom0'][0:nx - 1, level_start_idx:level_end_idx]
                            w3d_1 = h5py.File(filename, "r")['actrw_rw_mom1'][0:nx - 1, level_start_idx:level_end_idx]
                            w3d_2 = h5py.File(filename, "r")['actrw_rw_mom2'][0:nx - 1, level_start_idx:level_end_idx]
                            w3d = np.sqrt(w3d_2 / w3d_0 - w3d_1 / w3d_0 * w3d_1 / w3d_0) / (w3d_1 / w3d_0)
                        elif 'mom3' in var:
                            w3d = h5py.File(filename, "r")[var][0:nx - 1, level_start_idx:level_end_idx] * 4. / 3. * 3.1416 * 1e3
                        else:
                            w3d = h5py.File(filename, "r")[var][0:nx - 1, level_start_idx:level_end_idx]
                        # Read and apply cloud mask
                        if mask_rico:
                            mask = h5py.File(filename, "r")["cloud_rw_mom3"][0:nx - 1, level_start_idx:level_end_idx] * 4. / 3. * 3.1416 * 1e3
                            mask = np.where(mask > 1.e-5, 1., 0.)
                            w3d = w3d[(mask == 1)]
                        total_arr = np.append(total_arr, w3d)

                    plt.figure(1)
                    number_of_bins = 50
                    if 'rain_rw_mom0' in var:
                        biny = (np.logspace(np.log10(0.00001),np.log10(5e8),num=number_of_bins)).tolist()#mom0
                    elif 'mom0' in var:
                        biny = (np.logspace(np.log10(1e6),np.log10(2e9),num=number_of_bins)).tolist()#mom0
                    elif 'mean_radius' in var:
                        biny = (np.logspace(np.log10(1e-6),np.log10(1e-4),num=number_of_bins)).tolist()#mom1
                    elif 'disspersion' in var:
                        biny = (np.logspace(np.log10(0.001),np.log10(10),num=number_of_bins)).tolist()#mom2
                    elif 'rain_rw_mom3' in var:
                        biny = (np.logspace(np.log10(1e-15),np.log10(0.1),num=number_of_bins)).tolist()#mom3
                    else:
                        biny = (np.logspace(np.log10(1e-6),np.log10(0.1),num=number_of_bins)).tolist()#mom3
                    #creat a histogram of total_arr based on the bins given by biny
                    n, bins, patches = plt.hist(total_arr, bins=biny, density=normalize, histtype='step') 
                    mean_values[i].append(n)
                    i += 1

        for y in range(len(vars)):
            final_result[y] = np.array(mean_values[y])
            mean_values_mean[y] = np.mean(final_result[y], axis=0)
            mean_values_std[y] = np.std(final_result[y], axis=0)

    return mean_values_mean, mean_values_std

path = ""#provide path to DATA folder
args = argparse.ArgumentParser()
args.add_argument("--vars", nargs='+', default=['actrw_rw_mom0','rain_rw_mom0','mean_radius','disspersion','actrw_rw_mom3','rain_rw_mom3'])
args.add_argument("--time_start", type=int, default=1800)
args.add_argument("--time_end", type=int, default=9600)
args.add_argument("--level_start", type=int, default=500)
args.add_argument("--level_end", type=int, default=5000)
args.add_argument("--dirs", nargs='+', default=[f'{path}/HR/Profiles/prflux_prof_HR_SD10/'])
args.add_argument("--labels", nargs='+', default=["0"])
args.add_argument("--outfreq", type=int, default=240)
args.add_argument("--normalize", type=bool, default=True)
args.add_argument("--mask_rico", type=bool, default=True)
args.add_argument("--SD_label", nargs='+', default=['1000'])
args.add_argument("--Outdir", nargs='+', default=[f'{path}/HR/Fig_12_data/'])
args = args.parse_args()

#use args to run for loop over Dirs, Outdir, SD_label

vars = args.vars
time_start = args.time_start
time_end = args.time_end
level_start = args.level_start
level_end = args.level_end
Dirs = [args.dirs]
labels = args.labels
outfreq = args.outfreq
normalize = args.normalize
mask_rico = args.mask_rico
SD_label = args.SD_label
Outdir = args.Outdir

for dirs, outdir,sd in zip(Dirs, Outdir, SD_label):
    result = plot_histograms(vars, time_start, time_end, level_start, level_end, dirs, labels, outfreq, normalize ,mask_rico)

    for y in range(len(vars)):
        np.save(outdir+vars[y]+f'_mean_SD{sd}_{time_start}_{time_end}.npy', result[0][y])
        np.save(outdir+vars[y]+f'_std_SD{sd}_{time_start}_{time_end}.npy', result[1][y])
