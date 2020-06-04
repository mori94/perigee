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
    
    
    
for r in [1,2,3]:
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

    WeightFileName="weight"+str(sys.argv[1])+".txt"
    weight_table=np.zeros([test_num,test_num])
    filew=open(WeightFileName,'r',errors='replace')
    line=filew.readlines()
    for i in range(test_num):
        a=line[i].split("  ")
        for j in range(test_num):
            weight_table[i][j]=a[j]
    filew.close()


    NodeFileName="node"+str(sys.argv[1])+".txt"
    filen=open(NodeFileName,'r',errors='replace')
    node=np.zeros(100)
    line=filen.readlines()
    a=line[0].split("  ")
    for j in range(100):
        node[j]=a[j]
    filen.close()

    TreeFileName="tree"+str(sys.argv[1])+".txt"
    filet=open(TreeFileName,'r',errors='replace')
    line=filet.readlines()
    for i in range(99):
        a=line[i].split("  ")
        weight_table[int(node[int(a[0])])][int(node[int(a[1])])]=0.1 * weight_table[int(node[int(a[0])])][int(node[int(a[1])])]
        weight_table[int(node[int(a[1])])][int(node[int(a[0])])]=0.1 * weight_table[int(node[int(a[1])])][int(node[int(a[0])])]
    filet.close()

    for i in range(test_num):
        for j in range(i+1,test_num):
            G.add_edge(i,j,weight=weight_table[i][j]+delay[int(i)]/2+delay[int(j)]/2)


    OutputDelayFile = "idealtree"+str(sys.argv[1])+".txt"
    fwl=open(OutputDelayFile,'a')
    for i in range(test_num):
        print(i)
        length, path=nx.single_source_dijkstra(G, i)
        for j in range(test_num):
            if i==j:
                length[j]=0
            else:
                length[j]=length[j]+delay[int(i)]/2-delay[int(j)]/2
            fwl.write(str(length[j])+'  ')
        fwl.write('\n')
    fwl.close()

