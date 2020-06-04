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


# VanillaMinus is a function ran by complete graph information. For all the nodes, make the neighbor selection first and them switch the reamining neighbors with other random selected ones.
def VanillaMinus(G, neighbor, len_of_neigh, len_of_test,HashType, LinkDelay, NodeDelay, IncomingLimit, NodeHash):
    new_neighbor= np.zeros([test_num,len_of_neigh])
    for nodecount in range(test_num):

        # 'new' is an array for the selected neighbor
        new=[0 for j in range(len_of_neigh-len_of_test)]

        # 'G1' is a graph without the node which is making selection, so that the node's connection will not influence its candidate neighbors' performance
        G1=G.copy()
        G1.remove_node(nodecount)

        # an array to store all neighbor's delay to 90% of the graph
        dis_90=np.zeros(len_of_neigh)

        for neighborcount in range(len_of_neigh):
            # run the shortest path from candidate neighbor to all the nodes
            length, path=nx.single_source_dijkstra(G1, neighbor[nodecount][neighborcount])
            # plus the half of the candidate node's processing delay, minus half of the terminal node's delay, so that length is the delay including all nodes precessing and edge connection from 'neighbor[nodecount][neighborcount]' to 'nodeT'
            for nodeT in length.keys():
                length[nodeT]=length[nodeT]+NodeDelay[int(neighbor[nodecount][neighborcount])]/2-NodeDelay[int(nodeT)]/2
            # calculate NodeDelay to 90% of the nodes or 90% of the hash
            dis_90=If_hash(HashType, length, neighborcount, NodeHash, dis_90)

        test=[0 for j in range(len_of_test)]
        # take the connection delay into consideration, '0.01*j' here is to differ the same values, won't influence results
        buff = [LinkDelay[nodecount][int(neighbor[nodecount][j])] + dis_90[j] + 0.01*j for j in range(len_of_neigh)]
        buff1=sorted(buff)

        # Finde the candidate neighbor with lowest delay
        for j in range(len_of_neigh-len_of_test):
            new[j]=neighbor[nodecount][buff.index(buff1[j])]
        # Switch the remaining neighbors
        test=Switch_remain_neighbor(len_of_test, test, neighbor, nodecount, IncomingLimit)

        # update them to new_neighbors
        for j in range(len_of_neigh):
            if j < (len_of_neigh-len_of_test):
                new_neighbor[nodecount][j]=new[j]
            else:
                new_neighbor[nodecount][j]=test[j-len_of_neigh+len_of_test]

        # update the IncomingNeighbor array for neighbor switch
        neighbor = Update_incoming_neighbor(len_of_neigh, IncomingNeighbor, neighbor, nodecount)
    return(new_neighbor)

def If_hash(HashType, length, neighborcount, NodeHash, dis_90):
    if HashType == ('hash' or 'lowlatencyhash'):
        length_buff=list(length.values())
        dis_90[neighborcount] = communicate.delaytopercenthash(NodeHash,length_buff,DelayPercantage)
    else:
        length_buff=sorted(length.values())
        dis_90[neighborcount]=length_buff[int(test_num*DelayPercantage/100)]
    return dis_90

def Switch_remain_neighbor(len_of_test, test, neighbor, nodecount, IncomingLimit):
    for j in range(len_of_test):
        test[j]=np.random.randint(test_num)
    while ((test[j] in neighbor[nodecount])or(test[j] in test[0:j])or test[j]==nodecount or IncomingNeighbor[test[j]]>=IncomingLimit) :
        test[j]=np.random.randint(test_num)
    return test

def Update_incoming_neighbor(len_of_neigh, IncomingNeighbor, neighbor, nodecount):
    for j in range(len_of_neigh):
        IncomingNeighbor[int(neighbor[nodecount][j])]=IncomingNeighbor[int(neighbor[nodecount][j])]-1
    for j in range(len_of_neigh):
        IncomingNeighbor[int(new_neighbor[nodecount][j])]=IncomingNeighbor[int(new_neighbor[nodecount][j])]+1
    return incomingNeighbor

# VanillaPlus is a function ran by complete graph information. For all the nodes, they randomly add more candidate neighbor, them make the selection among all the candidate neighbors
def VanillaPlus(G, neighbor, len_of_neigh, len_of_test,HashType, LinkDelay, NodeDelay, IncomingLimit, NodeHash,  NeighborSets, r , IncomingNeighbor):
    
    new_neighbor= np.zeros([test_num,len_of_neigh])
    neighbor_forward_table=np.zeros([test_num,len_of_neigh+len_of_test,len_of_subround])
    new=[0 for j in range(len_of_neigh)]
    test=np.zeros([test_num,len_of_test])
    for nodecount in range(test_num):
        # 'new' is an array for the selected neighbor. Find random nodes first, and them make selection
        for j in range(len_of_test):
            test[nodecount][j]=np.random.randint(test_num)
            while ((test[nodecount][j] in neighbor[nodecount]) or (test[nodecount][j] in test[nodecount][0:j]) or test[nodecount][j]==nodecount or IncomingNeighbor[int(test[nodecount][j])]>=IncomingLimit[int(test[nodecount][j])]) :
                test[nodecount][j]=np.random.randint(test_num)
            IncomingNeighbor[int(test[nodecount][j])]=IncomingNeighbor[int(test[nodecount][j])]+1
            NeighborSets[int(nodecount)][0]=NeighborSets[int(nodecount)][0]+1
            NeighborSets[int(nodecount)][int(NeighborSets[int(nodecount)][0])]=test[nodecount][j]
        # 'G1' is a graph without the node which is making selection, so that the node's connection will not influence its candidate neighbors' performance
    for sbcount in range(len_of_subround):
        # make the selection based on hash or not, if it's hash, the probability is node's hash/ graph's hash(which is test num)
        if HashType == ('hash' or 'lowlatencyhash' or 'treehash'):
            broad_node=int(communicate.GenerateNodeWithHash(NodeHash))
        else:
            broad_node=np.random.randint(test_num)
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
            for j in range(len_of_test):
                referencetime = receive_time_table[int(test[i][j])] + NodeDelay[int(test[i][j])] + LinkDelay[i][int(test[i][j])] - receive_time_table[i]
                if referencetime<=2*LinkDelay[i][int(test[i][j])]+NodeDelay[i]+NodeDelay[int(test[i][j])]:
                    neighbor_forward_table[i][j+len_of_neigh][sbcount]=referencetime
                else:
                    neighbor_forward_table[i][j+len_of_neigh][sbcount]=unlimit
    dis_90=np.zeros(len_of_neigh+len_of_test)
    for nodecount in range(test_num):
        SelectedNodeSet=np.zeros(len_of_neigh)
        for j in range(len_of_neigh):
            buff=sorted(neighbor_forward_table[nodecount][j])
            dis_90[j]=buff[int(len_of_subround*DelayPercantage/100)]
        for j in range(len_of_test):
            buff=sorted(neighbor_forward_table[nodecount][j+len_of_neigh])
            dis_90[j+len_of_neigh]=buff[int(len_of_subround*DelayPercantage/100)]
        buff1=[dis_90[j] + 0.001*j for j in range(len_of_neigh)]
        buff2=[dis_90[j+len_of_neigh]+0.01*(j+1) for j in range(len_of_test)]
        buff=buff1+buff2
        buff=sorted(buff)
        # update them to new_neighbors
        for j in range(len_of_neigh):
            if buff[j] in buff1:
                new[j]=neighbor[nodecount][buff1.index(buff[j])]
            else:
                new[j]=test[nodecount][buff2.index(buff[j])]
        for j in range(len_of_neigh):
            new_neighbor[nodecount][j]=new[j]
    # update the IncomingNeighbor array for neighbor switch
        for j in range(len_of_neigh):
            IncomingNeighbor[int(neighbor[nodecount][j])]=IncomingNeighbor[int(neighbor[nodecount][j])]-1
        for j in range(len_of_neigh):
            IncomingNeighbor[int(new_neighbor[nodecount][j])]=IncomingNeighbor[int(new_neighbor[nodecount][j])]+1
    return(new_neighbor)
    



def VanillaSelection(G, OutNeighbor, len_of_neigh, len_of_test, HashType, LinkDelay, NodeDelay, IncomingLimit, NodeHash,  NeighborSets, r, VanillaType, IncomingNeighbor):
    if str(VanillaType) == '-':
        new_neighbor=VanillaMinus(G, OutNeighbor, len_of_neigh, len_of_test, HashType, LinkDelay, NodeDelay, IncomingLimit, NodeHash)
    elif str(VanillaType) == '+':
        new_neighbor=VanillaPlus(G, OutNeighbor, len_of_neigh, len_of_test, HashType, LinkDelay, NodeDelay, IncomingLimit, NodeHash,  NeighborSets, r ,IncomingNeighbor)
    return(new_neighbor)

