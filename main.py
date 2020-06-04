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
import algucb
import algsubset
import algvanilla
import initnetwork
import readfiles
import writefiles
from scipy.stats import  truncexpon
test_num       = 1000                   # graph size
len_of_neigh   = int(sys.argv[3])       # outbound neighbors
len_of_test    = int(sys.argv[5])       # maximum neighbors may switch each round
len_of_subround= 100                    # how may subround under local simulation
#IncomingLimit  = 10                    # maximum incoming neighbors
RoundNum       = 130                    # how many rounds in simulation
DelayPercantage= 90                     # how do we score the performance of individual node
pathunlimit    = 2000                   # default delay between node during shortest path
unlimit        = 9999                   # how do we value the unresponded nodes
sys.setrecursionlimit(19999999)
    
[G,NodeDelay,NodeHash,LinkDelay,NeighborSets,IncomingLimit,OutNeighbor,IncomingNeighbor,bandwidth]=initnetwork.GenerateInitialNetwork(str(sys.argv[1]),sys.argv[6])
# store specific round results
set1=[0,4,8,16,32,64,128,256,384,512]
for r in range(RoundNum):
    # write delay tp percenttage and all the link delays
    if (r in set1):
        if str(sys.argv[2])=='vanilla':
            OutputDelayFile = str(sys.argv[6]) + '_' + str(sys.argv[2]) + str(sys.argv[3]) + str(sys.argv[4]) + str(sys.argv[5]) + "V" + str(sys.argv[1]) + "Round" + str(r) + ".txt"
        else:
            OutputDelayFile = str(sys.argv[6]) + '_' + str(sys.argv[2]) + "V" + str(sys.argv[1]) + "Round" + str(r)+".txt"
        writefiles.write(OutputDelayFile, G, NodeDelay, NodeDelay, OutNeighbor)
    # vanilla algorithm
    if str(sys.argv[2]) == 'vanilla':
        new_neighbor=algvanilla.VanillaSelection(G, OutNeighbor, len_of_neigh, len_of_test, str(sys.argv[6]), LinkDelay, NodeDelay, IncomingLimit, NodeHash,  NeighborSets, r, sys.argv[4], IncomingNeighbor)
    # ucb algorithm
    elif str(sys.argv[2]) == 'ucb':
        # initiat hist_score_tales, maintain the historical performance of all the connected nodes
        if r==0:
            hist_score_table=np.zeros([test_num,len_of_neigh,len_of_subround*RoundNum])
            hist_score_length=np.zeros([test_num,len_of_neigh])
        [new_neighbor, hist_score_table, hist_score_length]= algucb.UCBelection(G, OutNeighbor, len_of_neigh, len_of_test, str(sys.argv[6]), LinkDelay, NodeDelay, IncomingLimit, NodeHash, hist_score_table, hist_score_length, NeighborSets, IncomingNeighbor)
    # subset algorithm
    elif str(sys.argv[2]) == 'subset':
        new_neighbor= algsubset.SubsetSelection(G, OutNeighbor, len_of_neigh, len_of_test, str(sys.argv[6]), LinkDelay, NodeDelay, IncomingLimit, NodeHash, r, IncomingNeighbor)
    # initiate graph G, updates outbound neighbors
    G           =   initnetwork.GenerateInitialGraph()
    IncomingNeighbor=np.zeros(test_num)
    for i in range(test_num):
        for j in range(len_of_neigh):
            OutNeighbor[i][j]=new_neighbor[i][j]
            IncomingNeighbor[int(OutNeighbor[i][j])]=IncomingNeighbor[int(OutNeighbor[i][j])]+1
    [NeighborSets,LinkDelay,G]=initnetwork.UpdateNetwork(G,OutNeighbor,LinkDelay,NodeDelay,len_of_neigh,NeighborSets,bandwidth)



