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
import initnetwork
import readfiles
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


# Generate the shortest delay between all node pairs
def WriteDelay(OutputDelayFile, G, delay):
    fwl=open(OutputDelayFile,'a')
    for i in range(test_num):
        length, path=nx.single_source_dijkstra(G, i)
        for j in range(test_num):
            length[j]=round(length[j]+delay[int(i)]/2-delay[int(j)]/2,6)
            fwl.write(str(length[j])+'  ')
        fwl.write('\n')
    fwl.close()
    
def WriteConnection(OutputDelayFile, G, delay, neighbor):
    OutputDelayFile="Edge_"+OutputDelayFile
    fwl=open(OutputDelayFile,'a')
    for (u,v,d) in G.edges(data=True):
        fwl.write(str(round(d['weight'],0))+'  ')
    fwl.close()


def write(OutputDelayFile, G, NodeDelay,delay, neighbor):
    WriteDelay(OutputDelayFile, G, NodeDelay)
    #WriteConnection(OutputDelayFile, G, NodeDelay, neighbor)
       
