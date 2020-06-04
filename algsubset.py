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
import writefiles
import communicate
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

    

            
def SubsetSelection(G, OutNeighbor, len_of_neigh, len_of_test, NetworkType, LinkDelay, NodeDelay, IncomingLimit, NodeHash, r, IncomingNeighbor):
    # all the subset selections
    if len_of_neigh==6:
        SubGroups = [[0,0,1,1,1,1],[0,1,0,1,1,1],[0,1,1,0,1,1],[0,1,1,1,0,1],[0,1,1,1,1,0],[1,0,0,1,1,1],[1,0,1,0,1,1],[1,0,1,1,0,1],[1,0,1,1,1,0],[1,1,0,0,1,1],[1,1,0,1,0,1],[1,1,0,1,1,0],[1,1,1,0,0,1],[1,1,1,0,1,0],[1,1,1,1,0,0]]
    elif len_of_neigh==8:
        SubGroups = [[0,0,1,1,1,1,1,1],[0,1,0,1,1,1,1,1],[0,1,1,0,1,1,1,1],[0,1,1,1,0,1,1,1],[0,1,1,1,1,0,1,1],[0,1,1,1,1,1,0,1],[0,1,1,1,1,1,1,0],[1,0,0,1,1,1,1,1],[1,0,1,0,1,1,1,1],[1,0,1,1,0,1,1,1],[1,0,1,1,1,0,1,1],[1,0,1,1,1,1,0,1],[1,0,1,1,1,1,1,0],[1,1,0,0,1,1,1,1],[1,1,0,1,0,1,1,1],[1,1,0,1,1,0,1,1],[1,1,0,1,1,1,0,1],[1,1,0,1,1,1,1,0],[1,1,1,0,0,1,1,1],[1,1,1,0,1,0,1,1],[1,1,1,0,1,1,0,1],[1,1,1,0,1,1,1,0],[1,1,1,1,0,0,1,1],[1,1,1,1,0,1,0,1],[1,1,1,1,0,1,1,0],[1,1,1,1,1,0,0,1],[1,1,1,1,1,0,1,0],[1,1,1,1,1,1,0,0]]
    elif len_of_neigh==10:
        SubGroups = [[0,0,1,1,1,1,1,1,1,1],[0,1,0,1,1,1,1,1,1,1],[0,1,1,0,1,1,1,1,1,1],[0,1,1,1,0,1,1,1,1,1],[0,1,1,1,1,0,1,1,1,1],[0,1,1,1,1,1,0,1,1,1],[0,1,1,1,1,1,1,0,1,1],[0,1,1,1,1,1,1,1,0,1],[0,1,1,1,1,1,1,1,1,0],[1,0,0,1,1,1,1,1,1,1],[1,0,1,0,1,1,1,1,1,1],[1,0,1,1,0,1,1,1,1,1],[1,0,1,1,1,0,1,1,1,1],[1,0,1,1,1,1,0,1,1,1],[1,0,1,1,1,1,1,0,1,1],[1,0,1,1,1,1,1,1,0,1],[1,0,1,1,1,1,1,1,1,0],[1,1,0,0,1,1,1,1,1,1],[1,1,0,1,0,1,1,1,1,1],[1,1,0,1,1,0,1,1,1,1],[1,1,0,1,1,1,0,1,1,1],[1,1,0,1,1,1,1,0,1,1],[1,1,0,1,1,1,1,1,0,1],[1,1,0,1,1,1,1,1,1,0],[1,1,1,0,0,1,1,1,1,1],[1,1,1,0,1,0,1,1,1,1],[1,1,1,0,1,1,0,1,1,1],[1,1,1,0,1,1,1,0,1,1],[1,1,1,0,1,1,1,1,0,1],[1,1,1,0,1,1,1,1,1,0],[1,1,1,1,0,0,1,1,1,1],[1,1,1,1,0,1,0,1,1,1],[1,1,1,1,0,1,1,0,1,1],[1,1,1,1,0,1,1,1,0,1],[1,1,1,1,0,1,1,1,1,0],[1,1,1,1,1,0,0,1,1,1],[1,1,1,1,1,0,1,0,1,1],[1,1,1,1,1,0,1,1,0,1],[1,1,1,1,1,0,1,1,1,0],[1,1,1,1,1,1,0,0,1,1],[1,1,1,1,1,1,0,1,0,1],[1,1,1,1,1,1,0,1,1,0],[1,1,1,1,1,1,1,0,0,1],[1,1,1,1,1,1,1,0,1,0],[1,1,1,1,1,1,1,1,0,0]]
    new_neighbor= np.zeros([test_num,len_of_neigh])
    neighbor_forward_table=np.zeros([test_num,len_of_neigh,len_of_subround])
    for sbcount in range(len_of_subround):
        # make the selection based on hash or not
        if str(NetworkType) == ('hash' or 'lowlatencyhash' or 'treehash'):
            broad_node=int(communicate.GenerateNodeWithHash(NodeHash))
        else:
            broad_node=np.random.randint(test_num)
        # receive_time_table is an array to store the broadcast's first arriving time to all nodes
        receive_time_table=[pathunlimit for i in range(test_num)]
        receive_time_table[int(broad_node)]=0
        NeighborSets=initnetwork.GenerateInitialConnection(OutNeighbor,len_of_neigh)
        # receive_time_table will keep updating during broadcasting
        communicate.broad(broad_node,receive_time_table, LinkDelay, NodeDelay, NeighborSets)
        # node 'i' take the first arrived one as time 0, and calculated the reference time for the others. If 'i' broadcast arrives before the node 'neighbor[i][j]', this candidate will not broadcast to 'i' any more, take 'unlimit' for such unresponded issues
        for i in range(test_num):
            for j in range(len_of_neigh):
                referencetime = receive_time_table[int(OutNeighbor[i][j])] + NodeDelay[int(OutNeighbor[i][j])] + LinkDelay[i][int(OutNeighbor[i][j])] - receive_time_table[i]
                if referencetime < 0:
                    receive_time_table[i]=int(receive_time_table[int(OutNeighbor[i][j])]) + int(NodeDelay[int(OutNeighbor[i][j])]) + int(LinkDelay[i][int(OutNeighbor[i][j])])
        for i in range(test_num):
            for j in range(len_of_neigh):
                referencetime = receive_time_table[int(OutNeighbor[i][j])] + NodeDelay[int(OutNeighbor[i][j])] + LinkDelay[i][int(OutNeighbor[i][j])] - receive_time_table[i]
                if referencetime<=2*LinkDelay[i][int(OutNeighbor[i][j])]+NodeDelay[i]+NodeDelay[int(OutNeighbor[i][j])]:
                    neighbor_forward_table[i][j][sbcount]=referencetime
                else:
                    neighbor_forward_table[i][j][sbcount]=unlimit
    # Make the selection on the best subset based on greedy algorithm
    for nodecount in range(test_num):
        GroupScores=np.zeros(len(SubGroups))
        for groupid in range(len(SubGroups)):
            subgroup=[unlimit for i in range(len_of_subround)]
            for neighborid in range(len_of_neigh):
                if SubGroups[groupid][neighborid]==1:
                    for subroundcount in range(len_of_subround):
                        if subgroup[subroundcount]>neighbor_forward_table[nodecount][neighborid][subroundcount]:
                            subgroup[subroundcount]=neighbor_forward_table[nodecount][neighborid][subroundcount]
            GroupScores[groupid]=sorted(subgroup)[int(len_of_subround*0.9)]
        SelectedScore=min(GroupScores)
        for groupid in range(len(SubGroups)):
            if GroupScores[groupid]==SelectedScore:
                SelectedGroup=groupid
        SelectedNodeSet=np.zeros(len_of_neigh-len_of_test)
        order=0
        for neighborid in range(len_of_neigh):
            if SubGroups[SelectedGroup][neighborid]==1:
                SelectedNodeSet[order]=neighborid
                order=order+1
        # switch the reamining nodes with random selected ones
        test=np.zeros(len_of_test)
        for j in range(len_of_test):
            test[j]=np.random.randint(test_num)
            while ((test[j] in OutNeighbor[i])or(test[j] in test[0:j])or test[j]==nodecount or IncomingNeighbor[int(test[j])]>=IncomingLimit[int(test[j])]):
                test[j]=np.random.randint(test_num)
            IncomingNeighbor[int(test[j])]=IncomingNeighbor[int(test[j])]+1
        # updates 'the new_neighbor'
        for j in range(len_of_neigh):
            if j < (len_of_neigh-len_of_test):
                new_neighbor[nodecount][j]=OutNeighbor[nodecount][int(SelectedNodeSet[j])]
            else:
                new_neighbor[nodecount][j]=test[j-len_of_neigh+len_of_test]
    return(new_neighbor)



