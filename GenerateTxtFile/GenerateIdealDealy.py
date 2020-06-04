#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import data
import PathDelay
import sys
import math
test_num       = 1000
len_of_subround= 100
IncomingLimit  = 20
round          = 260
DelayPercantage= 90
pathunlimit    = 3999
unlimit        = 9999
sys.setrecursionlimit(10000)
len_of_neigh   = 8

def broad(broad_node,receive_time_table):
    for node_count in range(int(NeighborSets[broad_node][0])):
        receive_node_id=int(NeighborSets[broad_node][node_count+1])
        if receive_time_table[broad_node] + weight_table[broad_node][receive_node_id] + delay[broad_node] < receive_time_table[receive_node_id]:
            receive_time_table[receive_node_id] = receive_time_table[broad_node] + weight_table[broad_node][receive_node_id] + delay[broad_node]
            broad(receive_node_id,receive_time_table)
            
def delaytopercenthash(hash_table,length_buff,DelayPercantage):
    LengthDict={}
    for i in range(len(length_buff)):
        length_buff[i]=length_buff[i]*1000+i
        LengthDict[str(length_buff[i])]=hash_table[i]
    sorted_length_buff=sorted(length_buff,reverse=True)
    hashcounter=0
    for i in range(len(length_buff)):
        hashcounter=hashcounter+LengthDict[str(sorted_length_buff[i])]
        if hashcounter>test_num*0.1:
            return(int(sorted_length_buff[i]/1000))
            
def GenerateNodeWithHash(hash_table):
    broad_hash_value=np.random.randint(test_num)
    for i in range(test_num):
        broad_hash_value=broad_hash_value-hash_table[i]
        if broad_hash_value<0:
            return(i)
    
    
for i in [1,2,3]:
    
    G = nx.Graph()
    delay=[0 for i in range(test_num)]
    for i in range(test_num):
        delay[i]    =   data.Node_latency[random.randint(1,3800)]

    file = open("data1.txt", 'r', errors='replace')
    line = file.readline()
    lines = line.split('],')
    k=0
    for i in range(9559):
        a = lines[i].split(',')
        if(data.con[a[7]]!="Null"):
            G.add_node(k, country=a[7], cluster=data.con[a[7]])
            k=k+1
    file.close()

    WeightFileName="weight"+str(r)+".txt"
    weight_table=np.zeros([test_num,test_num])
    filew=open(WeightFileName,'r',errors='replace')
    line=filew.readlines()
    for i in range(test_num):
        a=line[i].split("  ")
        for j in range(test_num):
            weight_table[i][j]  =   a[j]
    filew.close()

    LowLatenncyNodeFileName="node"+str(r)+".txt"
    fileh=open(LowLatenncyNodeFileName,'r',errors='replace')
    line=fileh.readlines()
    a=line[0].split("  ")
    lowlatencynode=np.zeros(100)
    for i in range(len(a)-1):
        lowlatencynode[i]=int(a[i])-1
        if int(lowlatencynode[i]) < test_num:
            delay[int(lowlatencynode[i])]      =   0.1*delay[int(lowlatencynode[i])]
    for i in range(len(lowlatencynode)):
        for j in range(len(lowlatencynode)):
            weight_table[i][j]      =   0.1*weight_table[i][j]
    # keep mean hash as 1
    fileh.close()

    for i in range(test_num):
        for j in range(i+1,test_num):
            G.add_edge(i,j,weight=weight_table[i][j]+delay[int(i)]/2+delay[int(j)]/2)

    OutputDelayFile = "ideallow"+str(r)+".txt"
    fwl=open(OutputDelayFile,'a')
    for i in range(test_num):
        length, path  =  nx.single_source_dijkstra(G, i)
        for j in range(test_num):
            if i==j:
                length[j]   =   0
            else:
                length[j]   =   length[j]+delay[int(i)]/2-delay[int(j)]/2
            fwl.write(str(length[j])+'  ')
        fwl.write('\n')
    fwl.close()

