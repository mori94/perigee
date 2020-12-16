#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import matplotlib.pyplot as plt
import sys
plt.style.use('ggplot')
addr="/Users/maoyifan/Desktop/Result/rereredo/bands/redoband420/"
#addr="/home/yifan/bands/redoband410/"


if len(sys.argv) < 2:
    print("need round list")
    sys.exit(0)

round_list = []
dir_name = sys.argv[1]
for i in range(2, len(sys.argv)):
    round_list.append(int(sys.argv[i]))

subset_data ={}
method = 'subset'

fig, ax = plt.subplots(1,figsize=(24, 12))

colormap = plt.cm.nipy_spectral
colors = [colormap(i) for i in np.linspace(0, 1, len(round_list))]
ax.set_prop_cycle('color', colors)

for r in round_list:
    buff = []
    filename = dir_name + "/result90unhash_" + method + "V1Round" + str(r) + ".txt"
    f = open(filename,'r',errors='replace')
    line=f.readlines()
    striped_line = line[0].strip()
    a=striped_line.split("  ")
    for j in range(len(a)):
        buff.append(int(float(a[j])))
    subset_data[r]=sorted(buff)
    f.close()

sorted_key = sorted(subset_data.keys())
for i in sorted_key:
    d = subset_data[i]
    ax.plot(d, label="round"+str(i))
ax.legend()
plt.show()
#plt.savefig("subset64_2.png")
print("finish")
