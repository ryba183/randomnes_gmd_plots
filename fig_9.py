import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 24})

def multiplot_ds_c_data(parent_directories, subfolders, time_moments, names, path):
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
    # Number of colors you need
    num_colors = len(subfolders)  # You can change this to your desired number
    # Create a list of colors from the "gnuplot" colormap
    colors = [plt.cm.cool(i / num_colors) for i in range(num_colors)]
    rows = len(names)
    #create subplots with as many subplot to plot mean_r, sigma_r, disp_r, actrw_rw_cl_conc, rliq separately and to have rows equal to the number of names
    fig, axs = plt.subplots(1, rows, figsize=(25, 15), sharey=True)
    fig.tight_layout(pad=3.0)
    #create list of letters to put in the subplots of a length = rows * 6
    text_letters = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)', '(k)', '(l)', '(m)', '(n)',
                     '(o)','(p)','(r)', '(s)', '(t)', '(u)', '(v)', '(w)', '(x)', '(y)', '(z)']
    for row, (p_dir, name) in enumerate(zip(parent_directories, names)):
        text_name = name
        if 'nc' in text_name:
          text_to_print = f'{text_name.split("_")[0]} no coalescence'
        else:
          text_to_print = f'{text_name.split("_")[0]} with coalescence'

        # Initialize lists to store the values of prflux and position
        prflux_data = []
        position_data = []

        for time in time_moments:
            for j, subfolder in enumerate(subfolders):
                filename = os.path.join(p_dir, subfolder, f"prflux_prof_{text_name}_{subfolder}_{time}_mean_values_2_prflux.csv")
                try:
                    data = np.loadtxt(filename, delimiter=",")
                    #read data by columns from csv file in which it is stored in this order: mean_r_avg, sigma_r_avg, disp_r_avg, actrw_rw_cl_conc_avg, rliq_avg, prflux_avg, position_avg
                    prflux_data.append(data[:, 5])
                    position_data.append(data[:, 6])                 

                except OSError:
                    print(f"Error loading file: {filename}")
                #plot 1st subplot with mean_r_avg
                letter_index = int(row)
                #plot 6th subplot with prflux_avg
                axs[row].plot(prflux_data[j], position_data[j], label=(r"$N_\mathrm{SD}^\mathrm{(bin)}$="+subfolder.split("SD")[1]), linewidth=3, color=colors[j])
                axs[row].text(0.9, 0.95, text_letters[letter_index], transform=axs[row].transAxes,
                                    ha='center', va='center')
                #set y axis limits for all subplots
                axs[row].set_ylim((0, 5000))
                axs[row].set_xlim(left=0)

                #set y axis labels for only the subplots in 1st column
                axs[row].set_xlabel(r"precipitation flux [W/m^2]")
                axs[row].set_title(name)

    axs[1].legend(loc='upper center', bbox_to_anchor=(1, 1.1), ncol=7, fancybox=False, shadow=False, frameon=False)
    axs[0].set_ylabel("height [m]")

    plt.subplots_adjust(left=0.06,
            bottom=0.08, 
            right=0.98, 
            top=0.92, 
            wspace=0.12, 
            hspace=0.15)

    name = f"Fig_9"
    fig.savefig(f"{path}/{name}.pdf", dpi=300)
    plt.close(fig)

path = ""#provide path to DATA folder
parent_directory = [f"{path}/D/CSV", 
                    f"{path}/LR/CSV",
                    f"{path}/MR/CSV",
                    f"{path}/HR/CSV"]

subfolders = ["SD10", "SD50", "SD100", "SD1000", "SD10000", "SD40000", "SD100000"]
time_moments = [9600]
abreviations = ["D","LR","MR","HR"]
outfile_to_plot = ''#provide path to save the figure

multiplot_ds_c_data(parent_directory, subfolders, [9600], abreviations, outfile_to_plot)