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


# LocalUCBSelection is to make the selection based on the limited information during subround. Count all the reference responded times for the candidate neighbors, estimate their upper and lower confidence, make neighbor switching
def UCBelection(G, neighbor, len_of_neigh, len_of_test, NetworkType, LinkDelay, NodeDelay, IncomingLimit, NodeHash, hist_score_table, hist_score_length, NeighborSets, IncomingNeighbor):
    new_neighbor= np.zeros([test_num,len_of_neigh])
    neighbor_forward_table=np.zeros([test_num,len_of_neigh,len_of_subround])
    # the neighbor switching can happen during subround, and round is only the time to update the graph G so as to write down the node delays
    for sbcount in range(len_of_subround):
        # make the selection based on hash or not
        if str(NetworkType) == ('hash' or 'lowlatencyhash' or 'treehash'):
            broad_node=int(communicate.GenerateNodeWithHash(NodeHash))
        else:
            broad_node=np.random.randint(test_num)
        # receive_time_table is an array to store the broadcast's first arriving time to all nodes
        receive_time_table=[pathunlimit for i in range(test_num)]
        receive_time_table[int(broad_node)]=0
        NeighborSets=initnetwork.GenerateInitialConnection(neighbor,len_of_neigh)
        # receive_time_table will keep updating during broadcast
        communicate.broad(broad_node,receive_time_table, LinkDelay, NodeDelay, NeighborSets)
        for i in range(test_num):
            for j in range(len_of_neigh):
                referencetime = receive_time_table[int(neighbor[i][j])] + NodeDelay[int(neighbor[i][j])] + LinkDelay[i][int(neighbor[i][j])] - receive_time_table[i]
                if referencetime<=2*LinkDelay[i][int(neighbor[i][j])]+NodeDelay[i]+NodeDelay[int(neighbor[i][j])]:
                    neighbor_forward_table[i][j][sbcount]=referencetime
                else:
                    neighbor_forward_table[i][j][sbcount]=unlimit
        for i in range(test_num):
        # calculte the empircal 90% delays, and estimate the upper and lower confidence bounds based on the responded times. If one nneighbor's lower confidence bound is higher than some neighbors' upper confidence bound, switch it
            
            #upper_score_table=np.zeros([test_num,len_of_neigh])
            #lower_score_table=np.zeros([test_num,len_of_neigh])

            upper_score_hashTable=dick()
            lower_score_hashTable=dick()
            for j in range(len_of_neigh):
                hist_score_table[i][j][int(hist_score_length[i][j])] = neighbor_forward_table[i][j][sbcount]
                hist_score_length[i][j] = hist_score_length[i][j]+1
                hist_score_table[i][j][0:int(hist_score_length[i][j])] = sorted(hist_score_table[i][j][0:int(hist_score_length[i][j])])
                upper_score_hashTable.add(hash(upper_score_hashTable),hist_score_table[i][j][int(hist_score_length[i][j]*DelayPercantage/100)] + 125*np.sqrt(math.log(100)/(2*int(hist_score_length[i][j]))))
                lower_score_hashTable.add(hash(lower_score_hashTable),hist_score_table[i][j][int(hist_score_length[i][j]*DelayPercantage/100)] - 125*np.sqrt(math.log(100)/(2*int(hist_score_length[i][j]))))
            # check is the node with worst lower confidence bound need to be switchde
            min_upper_score = min(upper_score_table[i])
            max_lower_score = max(lower_score_table[i])
            if min_upper_score < max_lower_score:
            # if so, initiate its correspond hist_score_table, switch it to other nodes,update 'IncomingNeighbor'
                for count in range(len_of_neigh):
                    if lower_score_table[i][count]==max_lower_score:
                        switch_node=neighbor[i][count]
                        switch_node_order=count
                for j in range(int(hist_score_length[i][switch_node_order])+100):
                    hist_score_table[i][switch_node_order][j]=0
                # the connection change can be updated at the end of round(not subround), since we make the broadcasting here so that the graph connection will not affect our resuls
                hist_score_length[i][switch_node_order]=0
                IncomingNeighbor[int(switch_node)]=IncomingNeighbor[int(switch_node)]-1
                test=np.random.randint(test_num)
                while ((test in neighbor[i])or test==i or IncomingNeighbor[test]>=IncomingLimit[test]) :
                    test=np.random.randint(test_num)
                neighbor[i][switch_node_order]=test
                IncomingNeighbor[int(test)]=IncomingNeighbor[int(test)]+1
    for i in range(test_num):
        for j in range(len_of_neigh):
            new_neighbor[i][j]=neighbor[i][j]
    return(new_neighbor, hist_score_table, hist_score_length)

def hash(table):
    total = test_num*len_of_neigh
    for x in range(total):
        key = x
        if not table.has_key(key):
            return key
    return key
   
