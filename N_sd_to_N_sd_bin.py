import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 24})


case = '700m'
time_stop = [9600]
time_start = [1800]
level_start = 500
level_end = 5000
outfile_to_plot = '/home/piotr-pc/response/to_share/odp_do_odp/Final/Wykresy/'
main_path = '/home/piotr-pc/response/to_share/odp_do_odp/Final/Dane'
text_letters = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)', '(k)', '(l)', '(m)', '(n)', '(o)','(p)','(r)', '(s)']
linestyle = ['-', '--', '-', '--','-', '--', '-', '--']
SDs_HR = ['HR_SD10', 'GA17_HR_SD10','HR_SD100', 'GA17_HR_SD100','HR_SD1000', 'GA17_HR_SD1000', ]
SDs_D = ['D_SD10', 'GA17_D_SD10','D_SD100', 'GA17_D_SD100','D_SD1000', 'GA17_D_SD1000', ]
labels = ["10", "100", "1000"]
f = plt.figure(figsize=(25, 15))
ax = f.add_subplot(121)
ax2 = f.add_subplot(122, sharey=ax)

colors = ['blue', 'blue', 'red', 'red', 'black', 'black', 'magenta', 'yellow']
colors2 = ['blue', 'red', 'black']

for i, (SD_D, SD_HR) in enumerate(zip(SDs_D, SDs_HR)):
    path_D = f'{main_path}/histo/{SD_D}'
    path_HR = f'{main_path}/histo/{SD_HR}'
    sd = SD_D.split('SD')[-1]
    time_sr = time_start[0]
    time_st = time_stop[0]
    var = 'sd_conc'
    mean_values_mean_D = np.load(f'{path_D}/{var}_mean_SD{sd}_{time_sr}_{time_st}.npy')
    mean_values_mean_HR = np.load(f'{path_HR}/{var}_mean_SD{sd}_{time_sr}_{time_st}.npy')

    # Setting proper bins
    number_of_bins = 18
    bins = (np.arange(0, 2 + 2 / number_of_bins, 2 / number_of_bins)).tolist()


    # Histogram data preparation
    bin_widths = np.diff(bins)
    value_D = mean_values_mean_D * bin_widths
    value_HR = mean_values_mean_HR * bin_widths
    bar_centers = bins[:-1] + bin_widths / 2

    ax.plot(bar_centers, value_D, linewidth=3, color=colors[i],linestyle=linestyle[i] )
    ax2.plot(bar_centers, value_HR, linewidth=3, color=colors[i],linestyle=linestyle[i])
for j in range(len(labels)):
    ax.scatter(-1, 1, label=r'$N_\mathrm{SD}^\mathrm{(bin)}$='+labels[j], color=colors2[j], s=150)

ax.plot([1,1], [0,1], linestyle=':', color='grey', linewidth=1)
ax2.plot([1,1], [0,1], linestyle=':', color='grey', linewidth=1)
ax.set_xlabel(r'$ N_\mathrm{SD} \,/\, N_\mathrm{SD}^\mathrm{(bin)} $')
ax2.set_xlabel(r'$ N_\mathrm{SD} \,/\, N_\mathrm{SD}^\mathrm{(bin)} $')
ax.set_xlim(bar_centers[0], bar_centers[-1])
ax2.set_xlim(bar_centers[0], bar_centers[-1])
ax.set_xlim(0, 2)
ax2.set_xlim(0, 2)
ax.set_ylim((0, 0.8))
ax.set_ylabel(f'PDF')
ax.set_title('D')
ax2.set_title('HR')
ax.legend(loc='upper center', bbox_to_anchor=(1.1, 1.075), frameon=False, ncol=3)
plt.subplots_adjust(left=0.05, bottom=0.08, right=0.98, top=0.92, wspace=0.12, hspace=0.15)

f.savefig(outfile_to_plot + f'N_sd_to_N_sd_bin.pdf', dpi=300)
plt.close(f)
