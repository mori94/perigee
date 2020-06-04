#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import data
import PathDelay
test_num = 1000


####################
G = nx.Graph()

delay=[0 for i in range(test_num)]
for i in range(test_num):
    delay[i]=data.Node_latency[random.randint(1,3800)]

file = open("data1.txt", 'r', errors='replace')
line = file.readline()
lines = line.split('],')
k=0
for i in range(9559):
    a = lines[i].split(',')
    if(data.con[a[7]]!="Null"):
        G.add_node(k,country=a[7], cluster=data.con[a[7]])
        k=k+1
file.close()
weight1=np.zeros([test_num,test_num])
for i in range(test_num):
    for j in range(i+1,test_num):
        weight1[i][j]=PathDelay.wei(delay,G,i,j)-delay[i]/2-delay[j]/2
        weight1[j][i]=weight1[i][j]

fw=open('weight1.txt','a')
for i in range(test_num):
    for j in range(test_num):
        fw.write(str(int(weight1[i][j]))+'  ')
    fw.write('\n')
fw.close()

weight2=np.zeros([test_num,test_num])
for i in range(test_num):
    for j in range(i+1,test_num):
        weight2[i][j]=PathDelay.wei(delay,G,i,j)-delay[i]/2-delay[j]/2
        weight2[j][i]=weight2[i][j]

fw=open('weight2.txt','a')
for i in range(test_num):
    for j in range(test_num):
        fw.write(str(int(weight2[i][j]))+'  ')
    fw.write('\n')
fw.close()

weight3=np.zeros([test_num,test_num])
for i in range(test_num):
    for j in range(i+1,test_num):
        weight3[i][j]=PathDelay.wei(delay,G,i,j)-delay[i]/2-delay[j]/2
        weight3[j][i]=weight3[i][j]
fw=open('weight3.txt','a')
for i in range(test_num):
    for j in range(test_num):
        fw.write(str(int(weight3[i][j]))+'  ')
    fw.write('\n')
fw.close()

