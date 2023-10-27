import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 24})

# Load the saved data from the file
time_start = [6960, 7320, 7680, 8040]
level_start = 500
level_end = 5000
outfile_to_plot = ''#provide path to save the figure
path = '/HR/Fig_12_data'#provide path to DATA folder
text_letters = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)', '(k)', '(l)', '(m)', '(n)', '(o)','(p)','(r)', '(s)']

SDs = [10, 50, 100, 1000, 10000, 40000, 100000]
# Number of colors you need
num_colors = len(SDs)  # You can change this to your desired number
# Create a list of colors from the "gnuplot" colormap
colors = [plt.cm.cool(i / num_colors) for i in range(num_colors)]
fig, axes = plt.subplots(1, 4, figsize=(25, 15), sharey=True)
for k, SD in enumerate(SDs):
    j = 0
    for time_s in time_start:
        var = 'rain_rw_mom3'
        #reading data from the file
        mean_values_mean = np.load(f'{path}/Numpy_SD{SD}/{var}_mean_SD{SD}_{time_s}_{time_s}.npy')

        #setting proper bins
        number_of_bins=50
        bins = (np.logspace(np.log10(1e-15),np.log10(0.1),num=number_of_bins)).tolist()#mom3

        # Histogram data preparation
        bin_widths = np.diff(bins)
        value = mean_values_mean * bin_widths
        bar_centers = bins[:-1] + bin_widths / 2

        #plot data on each subplot
        axes[j].plot(bar_centers, value, label=(r"$N_\mathrm{SD}^\mathrm{(bin)}$="+str(SD)), linewidth=3, color=colors[k])
        axes[j].text(0.93, 0.95, text_letters[j], transform=axes[j].transAxes,
            ha='center', va='center')
        axes[j].set_xlabel('RWM [kg/kg]')
        axes[j].set_xscale('log')
        axes[j].set_xlim(min(bins[:-1]), max(bins[:-1]))
        axes[j].set_title(f'{time_s} s')
        axes[j].set_ylim((0,0.275))
        axes[j].tick_params(axis='both', which='major')

        #create a y and x axis labels for the leftmost plots only
        axes[0].set_ylabel(f'PDF')
        # create a sharable figure legend for all subplots above the 1st row of plots, make it center
        axes[1].legend(loc='upper center', bbox_to_anchor=(1.02, 1.1),ncol=7, fancybox=False, shadow=False, frameon=False)
        j += 1

plt.subplots_adjust(left=0.05,
            bottom=0.08,
            right=0.98,
            top=0.92,
            wspace=0.12,
            hspace=0.15)
fig.savefig(outfile_to_plot + 'Fig_12.pdf', dpi=300)
plt.close(fig)
