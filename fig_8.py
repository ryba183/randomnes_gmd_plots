import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})

def multiplot_data(parent_directories, subfolders, time_moments, names, outfile):
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
    num_rows = 3
    num_cols = 4
    f_size = 20
    l_width = 3

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(25, 20), sharey=True)
    fig.tight_layout(pad=3.0)
    text_letters = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)', '(k)', '(l)']

    # Number of colors you need
    num_colors = len(subfolders)  # You can change this to your desired number

    # Create a list of colors from the "gnuplot" colormap
    colors = [plt.cm.gnuplot(i / num_colors) for i in range(num_colors)]

    for col, (p_dir, name) in enumerate(zip(parent_directories, names)):
        text_name = name
        if 'nc' in text_name:
            text_to_print = f'{text_name.split("_")[0]} no coalescence'
            text_to_save = f'{text_name.split("_")[0]}_no_coalescence'
        else:
            text_to_print = text_name
            text_to_save = text_name

        disp_r_data = []
        pos_avg_data = []
        actrw_rw_cl_conc_avg_data = []
        actrw_rw_cl_avg_data = []

        linestyle_tuple = [
            ('densely dashed', (0, (5, 1))),
            ('densely dashdotted', (0, (3, 1, 1, 1))),
            ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1))),
            ('densely dashed', (0, (5, 1))),
            ('densely dashdotted', (0, (3, 1, 1, 1))),
            ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))
        ]

        for i, time in enumerate(time_moments):
            for j, subfolder in zip(range(6), subfolders):
                filename = os.path.join(p_dir, subfolder, f"prof_{text_name}_{subfolder}_{time}_mean_values_2.csv")
                try:
                    data = np.loadtxt(filename, delimiter=",")
                    disp_r_data.append(data[:, 2])
                    pos_avg_data.append(data[:, 3])
                    actrw_rw_cl_conc_avg_data.append(data[:, 4])
                    actrw_rw_cl_avg_data.append(data[:, 5])
                except OSError:
                    print(f"Error loading file: {filename}")
                axs[2, col].plot(disp_r_data[i + j], pos_avg_data[i + j], label=(r"$N_\mathrm{SD}^\mathrm{(bin)}$ = "+subfolder.split("SD")[1]), linestyle='solid', linewidth=l_width, color=colors[j])
                axs[2, col].set_ylim((500, 5000))
                axs[2, col].set_xlim((0, 0.31))

                axs[0, col].plot(actrw_rw_cl_conc_avg_data[i + j], pos_avg_data[i + j], label=(r"$N_\mathrm{SD}^\mathrm{(bin)}$ = "+subfolder.split("SD")[1]), linestyle='solid', linewidth=l_width, color=colors[j])
                axs[0, col].set_ylim((500, 5000))
                axs[0, col].set_xlim((0, 75))

                axs[1, col].plot(actrw_rw_cl_avg_data[i + j], pos_avg_data[i + j], label=(r"$N_\mathrm{SD}^\mathrm{(bin)}$ = "+subfolder.split("SD")[1]), linestyle='solid', linewidth=l_width, color=colors[j])
                axs[1, col].set_ylim((500, 5000))
                axs[1, col].set_xlim((0, 10))

                axs[2, col].set_xlabel("relative dispersion [1]",fontsize=f_size)
                axs[0, col].set_xlabel(r"droplet concentration [cm$^{-3}$]",fontsize=f_size)
                axs[1, col].set_xlabel(r"mean radius [$\mu$m]",fontsize=f_size)

    axs[0, 1].legend(loc='upper center', bbox_to_anchor=(1.15, 1.16), ncol=6, fancybox=False, shadow=False, frameon=False, fontsize=18)

    # Loop through rows
    for row in range(num_rows):
        # Loop through columns
        for col in range(num_cols):
            axs[0, col].set_title(f'{names[col].split("_")[0]} no coalescence', fontsize=18)
            # Calculate the index in the text_letters list corresponding to the current subplot
            index = row * num_cols + col
            # Use the axs function to add text to the current subplot
            axs[row, col].text(0.95, 0.95, text_letters[index],
                              transform=axs[row, col].transAxes,
                              fontsize=20, ha='center', va='center')

    axs[0, 0].set_ylabel("height [m]",fontsize=f_size)
    axs[1, 0].set_ylabel("height [m]",fontsize=f_size)
    axs[2, 0].set_ylabel("height [m]",fontsize=f_size)

    plt.subplots_adjust(top=0.95)  # Adjust the top spacing to make room for the title

    plt.subplots_adjust(left=0.05,
                bottom=0.05,
                right=0.98,
                top=0.95,
                wspace=0.12,
                hspace=0.15)
    fig.savefig(outfile + 'Fig_8.pdf', dpi=300)
    plt.close(fig)
path = ""#provide path to DATA folder
parent_directory = [f'{path}/...D/CSV',
                    f'{path}/...LR/CSV',
                    f'{path}/...MR/CSV',
                    f'{path}/...HR/CSV']
subfolders = ["SD10", "SD50", "SD100", "SD1000", "SD10000", "SD40000"]
time_moments = [9600]
abreviations = ["D_nc", "LR_nc", "MR_nc", "HR_nc"]
outfile_to_plot = ''#provide path to save the figure

multiplot_data(parent_directory, subfolders, [9600], abreviations, outfile_to_plot)