#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import matplotlib.pyplot as plt
import random
import data
import PathDelay
import sys
import math
import readfiles
from collections import defaultdict
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
from config import *

def construct_graph(nodes, ld):
    num_nodes = len(nodes)
    G = nx.Graph()
    for i, node in nodes.items():
        for u in node.outs:
            delay = ld[i][u] + node.node_delay/2 + nodes[u].node_delay/2
            assert(i != u)
            G.add_edge(i, u, weight=delay)

    return G

def reduce_link_latency(num_node, num_low_latency, ld):
    all_nodes = [i for i in range(num_node)]
    random.shuffle(all_nodes)
    all_nodes = list(all_nodes)
    low_lats = all_nodes[:num_low_latency]

    for i in low_lats:
        for j in low_lats:
            if i != j:
                ld[i][j] *= 0.1 




# Generate the initial graph with all the lawful users
def GenerateInitialGraph():
    G = nx.Graph()
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
    return(G)

# Generate nodes' processing delay
def GenerateInitialDelay():
    delay=[0 for i in range(test_num)]
    for i in range(test_num):
        buff=np.random.normal(50, 4.5)
        delay[i]=round(buff,6)
    return(delay)

# Generate the random neighbor connection
def GenerateOutNeighbor(len_of_neigh,IncomingLimit):
    OutNeighbor= np.zeros([test_num,len_of_neigh], dtype=np.int32)
    IncomingNeighbor=np.zeros(test_num, dtype=np.int32)
    for i in range(test_num):
        for j in range(len_of_neigh):
            OutNeighbor[i][j]=np.random.randint(test_num)
            out_peer = int(OutNeighbor[i][j])
            while( (out_peer in OutNeighbor[i][:j]) or 
                   (out_peer==i) or 
                   IncomingNeighbor[out_peer]>=IncomingLimit[out_peer]):
                OutNeighbor[i][j]=np.random.randint(test_num)
                out_peer = int(OutNeighbor[i][j])
            IncomingNeighbor[out_peer]=IncomingNeighbor[out_peer]+1
    return(OutNeighbor,IncomingNeighbor)
    
    
# NeighborSets, contains connectionconuts and  all neighbor ids (including the incomings)
def GenerateInitialConnection(OutNeighbor,len_of_neigh):
    NeighborSets = np.zeros([test_num, LIMIT+1+len_of_neigh ]) #225+len_of_neigh]) #225+len_of_neigh 1001
    for i in range(test_num):
        NeighborSets[i][0]=8
        for j in range(len_of_neigh):
            NeighborSets[i][1+j]=int(OutNeighbor[i][j])

    for i in range(test_num):
        for j in range(len_of_neigh):
            peer = int(OutNeighbor[i][j])
            peer_conn_count = int(NeighborSets[peer][0])
            # print("node",i, "peer",  peer, "peer_conn_count", peer_conn_count)
            # TODO is it not a bug?
            if i not in NeighborSets[peer][1:peer_conn_count+1]:
                NeighborSets[peer][peer_conn_count+1]=i
                NeighborSets[peer][0] += 1
    return(NeighborSets)

# if the block size is large enough, get linkdelays by the bandwidth
def DelayByBandwidth(NeighborSets,bandwidth):
    weight_table=np.zeros([test_num,test_num])
    for i in range(test_num):
        for j in range(len_of_neigh):
            if i != j :
                weight_table[i][int(OutNeighbor[i][j])] = 8 / min(bandwidth[i]/int(NeighborSets[i][0]) , bandwidth[int(OutNeighbor[i][j])]/int(NeighborSets[int(OutNeighbor[i][j])][0]))
    return(weight_table)
    
# Build graph edges
def BuildNeighborConnection(G,OutNeighbor,LinkDelay,delay,len_of_neigh):
    for i in range(test_num):
        for j in range(len_of_neigh):
            # plus half of both two sides' processing delay so that the node's processing delay can also be considered during shortest path searching
            G.add_edge(i,OutNeighbor[i][j],weight=LinkDelay[i][int(OutNeighbor[i][j])]+delay[i]/2+delay[int(OutNeighbor[i][j])]/2)
    return(G)

def InitBandWidth():
    bandwidth=np.zeros(test_num)
    for i in range(test_num):
        if (random.random()<0.33):
            bandwidth[i]=50
        else:
            bandwidth[i]=12.5
    return(bandwidth)

def InitIncomLimit():
    IncomingLimit=np.zeros(test_num)
    for i in range(test_num):
        #IncomingLimit[i]=min(int(bandwidth[i]*1.5),200)
        IncomingLimit[i]=LIMIT
    return(IncomingLimit)


def GenerateInitialNetwork(Datafile, NetworkType):
    bandwidth=InitBandWidth()
    IncomingLimit   =   InitIncomLimit()
    G               =   GenerateInitialGraph()
    NodeDelay       =   GenerateInitialDelay()
    [OutNeighbor,IncomingNeighbor]     =   GenerateOutNeighbor(len_of_neigh,IncomingLimit)
    NeighborSets    =   GenerateInitialConnection(OutNeighbor,len_of_neigh)

    #NodeDelay      = DelayByBandwidth(NeighborSets,bandwidth)
    # print(Datafile)
    # print(NodeDelay)
    # print(NetworkType)
    [LinkDelay,NodeHash,NodeDelay] = readfiles.Read(Datafile,NodeDelay, NetworkType)
    G               =   BuildNeighborConnection(G,OutNeighbor,LinkDelay,NodeDelay,len_of_neigh)
    return(G,NodeDelay,NodeHash,LinkDelay,NeighborSets,IncomingLimit,OutNeighbor,IncomingNeighbor,bandwidth)
 
# Update graph by the latest neighbor connections
def UpdateNetwork(G,OutNeighbor,LinkDelay,NodeDelay,len_of_neigh,NeighborSets,bandwidth):
    NeighborSets=   GenerateInitialConnection(OutNeighbor,len_of_neigh)
    #LinkDelay=   initnetwork.DelayByBandwidth(NeighborSets,bandwidth)
    G           =   BuildNeighborConnection(G,OutNeighbor,LinkDelay,NodeDelay,len_of_neigh)
    return(NeighborSets,LinkDelay,G)

