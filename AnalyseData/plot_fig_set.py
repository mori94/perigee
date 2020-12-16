#!/usr/bin/env python
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import matplotlib.patches as mpatches
import math

if len(sys.argv) < 1:
    print('Require data directory')
    sys.exit(0)

method = 'subset'

def plot_figure(dirname, method, ax, snapshot_point, title, ylim):
    subset_data ={}

    ax.set_prop_cycle('color', colors)
    for r in snapshot_point:
        filename = dirname + "/result90unhash_" + method + "V1Round" + str(r) + ".txt"
        buff = []

        f = open(filename,'r',errors='replace')
        line=f.readlines()
        a=line[0].strip().split("  ")
        for j in range(len(a)):
            buff.append(int(float(a[j])))
        subset_data[r]=sorted(buff)
        f.close()
    
    all_round = list(subset_data.keys())
    all_round = sorted(all_round)
    for i in all_round:
        ax.grid(True)
        ax.plot(subset_data[i]) #, label="r"+str(i))
    ax.set_ylim(ylim)
    ax.set_title(title, fontsize='small')
    ax.legend()

def get_y_lim(dirname, method, snapshot_point, min_y, max_y):
    for r in snapshot_point:
        filename = dirname + "/result90unhash_" + method + "V1Round" + str(r) + ".txt"
        with open(filename,'r') as f:
            line=f.readlines()
            a=line[0].strip().split("  ")
            for j in range(len(a)):
                n = int(float(a[j]))
                if max_y == None or n > max_y:
                    max_y = n
                if min_y == None or n < min_y:
                    min_y = n
    return min_y, max_y


repetition_dir = sys.argv[1]
snapshot_point = []
for i in range(2, len(sys.argv)):
    snapshot_point.append(int(sys.argv[i]))
snapshot_point = sorted(snapshot_point)

data_dirname = []
for filepath in  os.listdir(repetition_dir):
    if filepath[-3:] == 'png':
        continue
    data_dirname.append(filepath)
    # start_idx = filepath.find('Round') + 5 # count of Round
    # end_idx = filepath.find('.')
    # num = int(filepath[start_idx:end_idx])
    # data_dirname.append((filepath, num))

data_dirname= sorted(data_dirname)
# data_dirname = [i for i,j in sorted_data_dirname]

min_y = None 
max_y = None
for dirname in data_dirname:
    dirpath = repetition_dir+'/'+dirname
    min_y, max_y = get_y_lim(dirpath, method, snapshot_point, min_y, max_y)
ylim = [min_y, max_y]

num_row = 2
num_col = 3
num_exp = len(data_dirname)
print('num_exp', num_exp)
if num_exp <= 1:
    num_row = 1
    num_col = 1
elif num_exp <= 2:
    num_row = 1
    num_col = 2
elif num_exp <= 4:
    num_row = 2
    num_col = 2
elif num_exp <=6:
    num_row = 2
    num_col = 3
elif num_exp <=8:
    num_row = 2
    num_col = 4   
else:
    print('Warn. More room to plot')
    sys.exit(0)

fig, axs = plt.subplots(ncols=num_col, nrows=num_row, constrained_layout=False, figsize=(18,9))
colormap = plt.cm.nipy_spectral
colors = [colormap(i) for i in np.linspace(0, 0.9, len(snapshot_point))]
patches = []

for i in range(len(snapshot_point)):
    p =  mpatches.Patch(color=colors[i], label=str(snapshot_point[i]))
    patches.append(p) 

max_patch = mpatches.Patch(color='red', label='max')
min_patch = mpatches.Patch(color='green', label='min')
mean_patch = mpatches.Patch(color='blue', label='mean')

# print('h',len(axs), num_exp)
i = 0
c = 0
r = 0
for dirname in data_dirname:
    c = int(i / num_col)
    r = i % num_col
    #print(c, r)
    dirpath = repetition_dir+'/'+dirname
    
    if num_row ==1 and num_col == 1:
        plot_figure(dirpath, method, axs, snapshot_point, dirname, ylim)
    elif len(axs) == num_exp:
        plot_figure(dirpath, method, axs[i], snapshot_point, dirname, ylim)
    else:
        plot_figure(dirpath, method, axs[c, r], snapshot_point, dirname, ylim)
    i += 1
    if i >= num_row* num_col:
        break

#plt.show()
#lines, labels = axs[c,r].get_legend_handles_labels()
fig.legend(loc='lower center', handles=patches, fontsize='small', ncol= math.ceil(len(patches)/2))

fig.savefig(repetition_dir+ '/' + "result.png")
print("finish")
