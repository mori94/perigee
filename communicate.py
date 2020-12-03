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
import initnetwork
import readfiles
import writefiles
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



# Recursive function on broadcasting. Check whether any neighbors can send a newer block, and boradcast it to the other neighbors
def broad(broad_node, receive_time_table, LinkDelay, delay, NeighborSets):
    new_block=np.zeros(int(NeighborSets[broad_node][0]))
    for node_count in range(int(NeighborSets[broad_node][0])):
        # for each neighbor of this broadcast node
        receive_node_id= int(NeighborSets[broad_node][node_count+1])
        rx_time = receive_time_table[receive_node_id] + LinkDelay[broad_node][receive_node_id] + delay[receive_node_id]
        if rx_time < receive_time_table[broad_node]:
            receive_time_table[broad_node] = rx_time
            
    for node_count in range(int(NeighborSets[broad_node][0])):
        # for each neighbor of this broadcast node
        receive_node_id=int(NeighborSets[broad_node][node_count+1])
        rx_time = receive_time_table[broad_node] + LinkDelay[broad_node][receive_node_id] + delay[broad_node]
        if rx_time < receive_time_table[receive_node_id]:
            receive_time_table[receive_node_id] = rx_time
            new_block[node_count]=1
    if sum(new_block)>0:
        for node_count in range(int(NeighborSets[broad_node][0])):
            if new_block[node_count]==1:
                broad_node=int(NeighborSets[broad_node][node_count+1])
                broad(broad_node,receive_time_table, LinkDelay, delay, NeighborSets)

# Get the delay to the a specific percentage rate of hash
def delaytopercenthash(NodeHash,length_buff,Percantage):
    LengthDict={}
    for i in range(len(length_buff)):
        # the i here will not affect the leng_buff, but will differ the nodes with same delay
        length_buff[i]=length_buff[i]*1000+i
        LengthDict[str(length_buff[i])]=NodeHash[i]
    sorted_length_buff=sorted(length_buff,reverse=True)
    hashcounter=0
    for i in range(len(length_buff)):
        hashcounter=hashcounter+LengthDict[str(sorted_length_buff[i])]
        if hashcounter>test_num*(1-Percantage/100):
            return(int(sorted_length_buff[i]/1000))

# Find the broadcast node by its hash power (all the network's hash power = the network size)
def GenerateNodeWithHash(NodeHash):
    broad_hash_value=np.random.randint(test_num)
    for i in range(test_num):
        broad_hash_value=broad_hash_value-NodeHash[i]
        if broad_hash_value<0:
            return(i)
    return(test_num-1)

