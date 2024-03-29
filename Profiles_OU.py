import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})

def multiplot_data(parent_directories, subfolders, subfolders2,time_moments, names, outfile):
    """
    Plot the data in a multiplot format.

    Args:
        parent_directories (list): List of parent directories.
        subfolders (list): List of subfolders.
        time_moments (list): List of time moments.
        names (list): List of names.

    Returns:
        None
    """
    num_rows = 2
    num_cols = 4
    f_size = 20
    l_width = 3
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(25, 20), sharey=True)
    fig.tight_layout(pad=3.0)
    text_letters = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)', '(k)', '(l)']
    # colors = ['black', 'purple', 'blue', 'green', 'yellow', 'orange', 'red', 'magenta']
    colors = ['blue', 'blue', 'red', 'red', 'black', 'black', 'magenta', 'yellow']
    colors2 = ['blue', 'red', 'black']
    linestyles = ['-', '--', '-', '--', '-', '--']

    for p_dir in parent_directories:
        for i, time in enumerate(time_moments):
            for j, (subfolder, subfolder2) in enumerate(zip(subfolders,subfolders2)):
                sd = subfolder.split('SD')[-1]
                filename = os.path.join(p_dir +'/'+ subfolder, f"start_4800_outfreq_240_tmax_300_SD{sd}_9600_relax.csv")
                filename2 = os.path.join(p_dir +'/'+ subfolder2, f"start_4800_outfreq_240_tmax_300_SD{sd}_9600_relax.csv")
                # print(names[j],filename)
                disp_r_data = []
                pos_avg_data = []
                actrw_rw_cl_conc_avg_data = []
                actrw_rw_cl_avg_data = []
                rd_geq_08um_conc_avg_data = []
                rd_lt_08um_conc_avg_data =[]
                
                disp_r_data2 = []
                pos_avg_data2 = []
                actrw_rw_cl_conc_avg_data2 = []
                actrw_rw_cl_avg_data2 = []
                rd_geq_08um_conc_avg_data2 = []
                rd_lt_08um_conc_avg_data2 =[]

                try:
                    data = np.loadtxt(filename, delimiter=",")
                    actrw_rw_cl_avg_data=data[:, 0]
                    disp_r_data=data[:, 2]
                    actrw_rw_cl_conc_avg_data=data[:, 3]
                    rd_geq_08um_conc_avg_data=data[:, -3]
                    rd_lt_08um_conc_avg_data=data[:, -2]
                    pos_avg_data=data[:, -1]
                    
                    data2 = np.loadtxt(filename2, delimiter=",")
                    actrw_rw_cl_avg_data2=data2[:, 0]
                    disp_r_data2=data2[:, 2]
                    actrw_rw_cl_conc_avg_data2=data2[:, 3]
                    rd_geq_08um_conc_avg_data2=data2[:, -3]
                    rd_lt_08um_conc_avg_data2=data2[:, -2]
                    pos_avg_data2=data2[:, -1]

                except OSError:
                    print(f"Error loading file: {filename}")
                    print(f"Error loading file: {filename2}")

                axs[0,0].plot(actrw_rw_cl_conc_avg_data, pos_avg_data,  linestyle=linestyles[j], linewidth=l_width,color=colors[j])
                axs[1,0].plot(actrw_rw_cl_conc_avg_data2, pos_avg_data2,  linestyle=linestyles[j], linewidth=l_width,color=colors[j])
                axs[0,0].set_ylim((0, 6000))
                axs[1,0].set_ylim((0, 6000))
                axs[0,0].set_xlim((0, 90))
                axs[1,0].set_xlim((0, 90))

                axs[0,1].plot(actrw_rw_cl_avg_data*1e6, pos_avg_data, linestyle=linestyles[j], linewidth=l_width,color=colors[j])
                axs[1,1].plot(actrw_rw_cl_avg_data2*1e6, pos_avg_data2, linestyle=linestyles[j], linewidth=l_width,color=colors[j])
                axs[0,1].set_xlim((0, 10))
                axs[1,1].set_xlim((0, 10))
                
                axs[0,2].plot(disp_r_data, pos_avg_data,  linestyle=linestyles[j], linewidth=l_width,color=colors[j])
                axs[1,2].plot(disp_r_data2, pos_avg_data2, linestyle=linestyles[j], linewidth=l_width,color=colors[j])
                axs[0,2].set_xlim((0, 0.41))
                axs[1,2].set_xlim((0, 0.41))

                axs[0,3].plot(rd_lt_08um_conc_avg_data, pos_avg_data,  linestyle=linestyles[j], linewidth=l_width,color=colors[j])
                axs[1,3].plot(rd_lt_08um_conc_avg_data2, pos_avg_data2,  linestyle=linestyles[j], linewidth=l_width,color=colors[j])
                axs[0,3].set_xlim((50, 150))
                axs[1,3].set_xlim((50, 150))
                if j <4:
                    axs[0,j].text(0.9, 0.95, text_letters[j], fontsize=20,transform=axs[0,j].transAxes)
                    axs[1,j].text(0.9, 0.95, text_letters[j+num_cols], fontsize=20,transform=axs[1,j].transAxes)
    for k in range(len(names)):
        axs[0,0].scatter(-1,-1, color=colors2[k], label=r'$N_\mathrm{SD}^\mathrm{(bin)}$='+names[k], s=150)


    axs[1,0].set_xlabel(r"droplet concentration [cm$^{-3}$]",fontsize=f_size)
    axs[1,1].set_xlabel(r"mean radius [$\mu$m]",fontsize=f_size)
    axs[1,2].set_xlabel("relative dispersion [1]",fontsize=f_size)
    axs[1,3].set_xlabel(r"aerosol concentration [cm$^{-3}$]",fontsize=f_size)
    axs[0,0].legend(loc='upper center', bbox_to_anchor=(2.1, -1.23), ncol=3, fancybox=False, shadow=False, frameon=False, fontsize=28)

    axs[0,0].set_ylabel("height [m]",fontsize=f_size)
    axs[1,0].set_ylabel("height [m]",fontsize=f_size)
    # Add titles spanning two subplots
    fig = axs[0, 1].get_figure()  # Get the figure from one of the subplots
    figtext_HR = (axs[0, 1].get_position().x0 + axs[0, 2].get_position().x1) / 2  # Calculate x-coordinate
    figtext_D = (axs[1, 1].get_position().x0 + axs[1, 2].get_position().x1) / 2  # Calculate x-coordinate
    fig.text(figtext_HR*1.05, 0.95, 'HR', ha='center',fontsize=26, fontweight='bold')  # Add 'HR' title
    fig.text(figtext_D*1.05, 0.5, 'D', ha='center',fontsize=26, fontweight='bold')  # Add 'D' title
    plt.subplots_adjust(left=0.08,
                bottom=0.1,
                right=0.98,
                top=0.92,
                wspace=0.1,
                hspace=0.15)
    fig.savefig(outfile + 'Profiles_relax.pdf', dpi=300)
    plt.close(fig)
path = ""#provide path to DATA folder
parent_directory = [f'{path}/CSV/']

subfolders = ['HR/HR/SD10','HR/OU_HR/SD10','HR/HR/SD100','HR/OU_HR/SD100','HR/HR/SD1000','HR/OU_HR/SD1000']
subfolders2 = ['D/D/SD10','D/OU_D/SD10','D/D/SD100','D/OU_D/SD100','D/D/SD1000','D/OU_D/SD1000']
abreviations = ["10", "100", "1000"]
time_moments = [9600]
outfile_to_plot = ''#provide path to save the figure

multiplot_data(parent_directory, subfolders, subfolders2, [9600], abreviations, outfile_to_plot)
