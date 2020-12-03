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
import algucb
import algsubset
import initnetwork
import readfiles
import writefiles
import communicate
from config import *
from perigeeNode import *
import time
test_num       = 1000                   # graph size
num_node = test_num
len_of_neigh   = int(sys.argv[3])       # outbound neighbors
len_of_test    = int(sys.argv[5])       # maximum neighbors may switch each round
DelayPercantage= 90                     # how do we score the performance of individual node
pathunlimit    = 2000                   # default delay between node during shortest path
unlimit        = 9999                   # how do we value the unresponded nodes
num_subround = len_of_subround # better name
sys.setrecursionlimit(19999999)


# VanillaMinus is a function ran by complete graph information. For all the nodes, 
# make the neighbor selection first and them switch the reamining neighbors with other random selected ones.
def VanillaMinus(G, neighbor, len_of_neigh, len_of_test,HashType, LinkDelay, NodeDelay, IncomingLimit, NodeHash):
    new_neighbor= np.zeros([test_num,len_of_neigh])
    for nodecount in range(test_num):
        # 'new' is an array for the selected neighbor
        new=[0 for j in range(len_of_neigh-len_of_test)]

        # 'G1' is a graph without the node which is making selection, 
        # so that the node's connection will not influence its candidate neighbors' performance
        G1=G.copy()
        G1.remove_node(nodecount)

        # an array to store all neighbor's delay to 90% of the graph
        dis_90=np.zeros(len_of_neigh)

        for neighborcount in range(len_of_neigh):
            # run the shortest path from candidate neighbor to all the nodes
            length, path=nx.single_source_dijkstra(G1, neighbor[nodecount][neighborcount])
            # plus the half of the candidate node's processing delay, minus half of the terminal node's delay, 
            # so that length is the delay including all nodes precessing 
            # and edge connection from 'neighbor[nodecount][neighborcount]' to 'nodeT'
            for nodeT in length.keys():
                length[nodeT]=length[nodeT]+NodeDelay[int(neighbor[nodecount][neighborcount])]/2-NodeDelay[int(nodeT)]/2
            # calculate NodeDelay to 90% of the nodes or 90% of the hash
            dis_90=If_hash(HashType, length, neighborcount, NodeHash, dis_90)

        test=[0 for j in range(len_of_test)]
        # take the connection delay into consideration, 
        # '0.01*j' here is to differ the same values, won't influence results
        buff = [LinkDelay[nodecount][int(neighbor[nodecount][j])] + dis_90[j] + 0.01*j for j in range(len_of_neigh)]
        buff1=sorted(buff)

        # Finde the candidate neighbor with lowest delay
        for j in range(len_of_neigh-len_of_test):
            new[j]=neighbor[nodecount][buff.index(buff1[j])]
        # Switch the remaining neighbors
        test=Switch_remain_neighbor(len_of_test, test, neighbor, nodecount, IncomingLimit, IncomingNeighbor)

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

def Switch_remain_neighbor(len_of_test, test, neighbor, nodecount, IncomingLimit, IncomingNeighbor):
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

# VanillaPlus is a function ran by complete graph information. 
# For all the nodes, they randomly add more candidate neighbor, 
# them make the selection among all the candidate neighbors
def VanillaPlus(nodes, neighbor, len_of_neigh, num_new,HashType, LinkDelay, NodeDelay, IncomingLimit, NodeHash,  NeighborSets, r , IncomingNeighbor):
    new_neighbor= np.zeros([num_node, len_of_neigh])

    neighbor_forward_table = np.zeros([num_node, len_of_neigh+num_new, len_of_subround])

    new=[0 for j in range(len_of_neigh)]

    table = np.zeros([num_node, num_new])

    for u in range(num_node):
        # 'new' is an array for the selected neighbor. Find random nodes first, and them make selection
        for j in range(num_new):
            table[u][j] = np.random.randint(num_node)
            new_peer = int(table[u][j])
            while ((new_peer in neighbor[u]) or 
                   (new_peer in table[u][0:j]) or 
                   new_peer == u or 
                   IncomingNeighbor[new_peer] >= IncomingLimit[new_peer]) :
                table[u][j] = np.random.randint(num_node)
                new_peer = int(table[u][j])

            # forget to add incoming to neighbor set
            IncomingNeighbor[new_peer] += 1
            NeighborSets[u][0] += 1
            NeighborSets[u][int(NeighborSets[u][0])]= new_peer 

    

    # so that the node's connection will not influence its candidate neighbors' performance
    for sbcount in range(len_of_subround):
        # make the selection based on hash or not, if it's hash, the probability is node's hash/ graph's hash(which is test num)
        if HashType == ('hash' or 'lowlatencyhash' or 'treehash'):
            broad_node=int(communicate.GenerateNodeWithHash(NodeHash))
        else:
            broad_node=np.random.randint(num_node)

        receive_time_table=[pathunlimit for i in range(num_node)]
        receive_time_table[int(broad_node)]=0

        NeighborSets = initnetwork.GenerateInitialConnection(neighbor,len_of_neigh)
        # receive_time_table will keep updating during broadcast
        communicate.broad(broad_node, receive_time_table, LinkDelay, NodeDelay, NeighborSets)

        for i in range(num_node):
            for j in range(len_of_neigh):
                out = int(neighbor[i][j])
                referencetime = receive_time_table[out] + \
                        NodeDelay[out] + \
                        LinkDelay[i][out] - \
                        receive_time_table[i]
                if referencetime  < 0:
                    print(referencetime)

                if referencetime <= 2*LinkDelay[i][out]+NodeDelay[i]+NodeDelay[out]:
                    neighbor_forward_table[i][j][sbcount] = referencetime
                else:
                    neighbor_forward_table[i][j][sbcount] = unlimit

            for j in range(num_new):
                referencetime = receive_time_table[int(table[i][j])] + NodeDelay[int(table[i][j])] + LinkDelay[i][int(table[i][j])] - receive_time_table[i]
                if referencetime <= 2*LinkDelay[i][int(table[i][j])]+NodeDelay[i]+NodeDelay[int(table[i][j])]:
                    neighbor_forward_table[i][j+len_of_neigh][sbcount]=referencetime
                else:
                    neighbor_forward_table[i][j+len_of_neigh][sbcount]=unlimit

    dis_90=np.zeros(len_of_neigh+num_new)
    nodes_best_x = np.zeros([num_node, BEST_X])
    for u in range(num_node):
        SelectedNodeSet = np.zeros(len_of_neigh)
        for j in range(len_of_neigh):
            buff = sorted(neighbor_forward_table[u][j])
            dis_90[j] = buff[int(len_of_subround*DelayPercantage/100)]

        for j in range(num_new):
            buff=sorted(neighbor_forward_table[u][j+len_of_neigh])
            dis_90[j+len_of_neigh]=buff[int(len_of_subround*DelayPercantage/100)]

        buff1=[dis_90[j] + 0.001*j for j in range(len_of_neigh)]
        buff2=[dis_90[j+len_of_neigh]+0.01*(j+1) for j in range(num_new)]
        buff=buff1+buff2
        buff=sorted(buff)
        my_neighbors = NeighborSets[u]
        num_neighbor =  int(my_neighbors[0])
        # update them to new_neighbors
        best_x = []
        for j in range(len_of_neigh):
            if buff[j] in buff1:
                new[j]=neighbor[u][buff1.index(buff[j])]
                # TODO some hack

                if len(best_x) < BEST_X : #and (new[j] not in my_neighbors[1:1+num_neighbor])
                    best_x.append(new[j])
            else:
                new[j]=table[u][buff2.index(buff[j])]
                if len(best_x) < BEST_X :
                    best_x.append(new[j])
        nodes_best_x[u] = best_x

    # for u in range(num_node):
        # # best of best of x 
        # best_of_best = []
        # for k in range(BEST_X):
            # peer = int(nodes_best_x[u][k])
            # rand_best_x = random.choice([0,1,2])
            # best_of_peer = int(nodes_best_x[peer][rand_best_x])
            # trial = 0
            # is_found = True
            # while ((best_of_peer in neighbor[u]) or (best_of_peer== u) or (IncomingNeighbor[best_of_peer] >= IncomingLimit[best_of_peer])):
                # rand_best_x = random.choice([0,1,2])
                # best_of_peer = int(nodes_best_x[peer][rand_best_x])
                # trial += 1
                # if trial > 10:
                    # is_found = False
                    # break
            # if is_found:
                # best_of_best.append(best_of_peer)

            # IncomingNeighbor[best_of_peer] += 1
        
        # acc_n = list(nodes_best_x[u]) + best_of_best
        # new_ran = []
        # for j in range(len_of_neigh - len(acc_n)):
            # a = np.random.randint(num_node)
            # while ((a in acc_n) or a==u or IncomingNeighbor[a]>=IncomingLimit[a]) :
                # a = np.random.randint(num_node)
            # acc_n.append(a)
            # IncomingNeighbor[a] += 1
            # #print(IncomingNeighbor[a])

        # new_neighbor[u] = acc_n

        for j in range(len_of_neigh):
            new_neighbor[u][j]=new[j]


    # update the IncomingNeighbor array for neighbor switch
        for j in range(len_of_neigh):
            IncomingNeighbor[int(neighbor[u][j])] -=1
        for j in range(len_of_neigh):
            IncomingNeighbor[int(new_neighbor[u][j])] += 1

    # out of first 4, get its neighbors

    return(new_neighbor)







def VanillaSelection(nodes, OutNeighbor, len_of_neigh, len_of_test, HashType, LinkDelay, NodeDelay, IncomingLimit, NodeHash,  NeighborSets, r, VanillaType, IncomingNeighbor):
    if str(VanillaType) == '-':
        new_neighbor=VanillaMinus(nodes, OutNeighbor, len_of_neigh, len_of_test, HashType, LinkDelay, NodeDelay, IncomingLimit, NodeHash)
    elif str(VanillaType) == '+':
        new_neighbor=VanillaPlus(nodes, OutNeighbor, len_of_neigh, len_of_test, HashType, LinkDelay, NodeDelay, IncomingLimit, NodeHash,  NeighborSets, r ,IncomingNeighbor)
    return(new_neighbor)

