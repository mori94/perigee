#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

filename = 'hash1.txt'
nodes_hash = []
with open(filename) as f:
    data = f.readlines()
    tokens = data[0].split('  ')
    for t in tokens:
        nodes_hash.append(float(t))

# sum_hash = sum(nodes_hash)
# print('len node hash',len(nodes_hash))
# print(nodes_hash[:20])
# print(sum_hash)
# print(max(nodes_hash))
# n, bins, patches = plt.hist(nodes_hash[:20], 50, density=True, facecolor='g', alpha=0.75)
# print(bins)
# plt.title('node hash power normalized histogram')
# plt.xlabel('node hash')
# plt.ylabel('density')
# plt.show()

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
    print(i)
    # n, bins, petches = plt.hist(i, 50, density=False, facecolor='g', alpha=0.75)
    # plt.show()
