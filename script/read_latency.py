#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

filename = 'weight1.txt'
latency_mat = []
with open(filename) as f:
    for line in f:
        tokens = line.strip().split()
        lat = []
        for t in tokens:
            lat.append(float(t))
        latency_mat.append(lat)



def ReadWeightFile(num_node):
    WeightFileName="weight1.txt"
    LinkDelay=np.zeros([num_node,num_node])
    filew=open(WeightFileName,'r',errors='replace')
    line=filew.readlines()
    for i in range(num_node):
        a=line[i].split("  ")
        for j in range(num_node):
            LinkDelay[i][j]=a[j]
    filew.close()
    return(LinkDelay)

links = ReadWeightFile(20)
for i in links:
    print(sum(i)/len(i), max(i), min(i))
    # n, bins, petches = plt.hist(i, 50, density=False, facecolor='g', alpha=0.75)
    # plt.show()
