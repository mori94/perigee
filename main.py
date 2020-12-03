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
import algvanilla
import initnetwork
import readfiles
import writefiles
from perigeeNode import * 
import new_vanilla as reorg_vanilla
import new_subset
from config import *
import time
num_node     = 1000                   # graph size
num_out   = int(sys.argv[3])       # outbound neighbors
#IncomingLimit  = 10                    # maximum incoming neighbors
DelayPercantage= 90                     # how do we score the performance of individual node
pathunlimit    = 2000                   # default delay between node during shortest path
unlimit        = 9999                   # how do we value the unresponded nodes
sys.setrecursionlimit(19999999)

data_index = sys.argv[1]
method = sys.argv[2]
network_type = sys.argv[6]
num_switch = int(sys.argv[5])

np.random.seed(0)
random.seed(0)
    
[ G, NodeDelay, 
  NodeHash, LinkDelay, 
  NeighborSets, IncomingLimit, 
  OutNeighbor, IncomingNeighbor, 
  bandwidth] =initnetwork.GenerateInitialNetwork(
        str(data_index),
        network_type
)

# for i in range(len(OutNeighbor)):
    # print(OutNeighbor[i])
# # sys.exit(0)
start = time.time()

# initnetwork.reduce_link_latency(num_node, int(0.1*num_node), LinkDelay)

nodes = {}
num_keep = 3
num_choose = 3
num_rand = 2
for i in range(num_node):
    node_delay = NodeDelay[i]
    in_lim = IncomingLimit[i]
    nodes[i] = Node(
        i,
        node_delay,
        in_lim,
        out_lim,
        OutNeighbor[i],
        # num_keep,
        # num_choose,
        # num_rand
    )

# create_random_neighbor(nodes)
update_ins_for_all_nodes(nodes)
G = initnetwork.construct_graph(nodes, LinkDelay)

for epoch in range(RoundNum):
    print("round num", epoch)
    if (epoch in set1):
        
        OutputDelayFile = ("AnalyseData/" + 
            str(network_type)+'_' + 
            str(method)+ 
            "V"+str(data_index)+ 
            "Round"+str(epoch)+".txt")
        writefiles.write(OutputDelayFile, G, NodeDelay, NodeDelay, OutNeighbor)

    # vanilla algorithm
    if str(sys.argv[2]) == 'vanilla-old':
        print('vanilla')
        new_neighbor=algvanilla.VanillaSelection(
                nodes, 
                OutNeighbor, 
                num_out, 
                num_switch, 
                str(sys.argv[6]), 
                LinkDelay, 
                NodeDelay, 
                IncomingLimit, 
                NodeHash,  
                NeighborSets, 
                epoch, 
                sys.argv[4], 
                IncomingNeighbor)
    elif str(sys.argv[2]) == 'vanilla':
        

        reorg_vanilla.vanilla_new(nodes, LinkDelay, num_switch, num_subround)    
        G = initnetwork.construct_graph(nodes, LinkDelay)
        OutNeighbor = get_OutNeighbor(nodes, out_lim)


        continue

    # ucb algorithm
    elif str(sys.argv[2]) == 'ucb':
        # initiat hist_score_tales, maintain the historical performance of all the connected nodes
        if epoch==0:
            total_round = len_of_subround*RoundNum
            hist_score_table = np.zeros([num_node, num_out, total_round])
            hist_score_length = np.zeros([num_node, num_out])
        [new_neighbor, hist_score_table, hist_score_length]= algucb.UCBelection(
                G, 
                OutNeighbor, 
                num_out, 
                num_switch, 
                network_type, 
                LinkDelay, 
                NodeDelay, 
                IncomingLimit, 
                NodeHash, 
                hist_score_table, 
                hist_score_length, 
                NeighborSets, 
                IncomingNeighbor)
    # subset algorithm
    elif str(sys.argv[2]) == 'subset':
        print('subset')
        new_neighbor = new_subset.new_subset_complete(nodes, LinkDelay, num_subround)
        # new_neighbor = new_subset.new_subset_two_hop(nodes, LinkDelay, num_subround)
        print('new neighbors')
        update_conn_for_all_nodes(nodes, new_neighbor)
        G = initnetwork.construct_graph(nodes, LinkDelay)
        OutNeighbor = get_OutNeighbor(nodes, out_lim)


        # new_neighbor= algsubset.SubsetSelection(
                # G, 
                # OutNeighbor, 
                # num_out, 
                # num_switch, 
                # network_type, 
                # LinkDelay, 
                # NodeDelay, 
                # IncomingLimit, 
                # NodeHash, 
                # epoch, 
                # IncomingNeighbor
        # )

    # G = initnetwork.GenerateInitialGraph()
    IncomingNeighbor=np.zeros(num_node, dtype=np.int32)
    for i in range(num_node):
        for j in range(num_out):
            # OutNeighbor[i][j] = new_neighbor[i][j]
            IncomingNeighbor[int(OutNeighbor[i][j])] += 1

    nodes_deg = []
    sum_in = 0
    sum_out = 0
    for i in range(len(nodes)):
        nodes_deg.append(len(nodes[i].ins))
        sum_in += len(nodes[i].ins)
        sum_out += len(nodes[i].outs)
    print(sum_in/len(nodes))
    print(sum_out/len(nodes))
    print(max(nodes_deg))
    bins = [i*5 for i in range(int(in_lim/5)+1)]
    print(np.histogram(nodes_deg, bins=bins))
    # print(nodes_deg)


    # for i in IncomingNeighbor:
        # if i > LIMIT :
            # print("close to limit",i)
        # assert(i <= LIMIT)

    # [NeighborSets,LinkDelay,G] = initnetwork.UpdateNetwork( 
            # G,
            # OutNeighbor,
            # LinkDelay,
            # NodeDelay,
            # num_out,
            # NeighborSets,
            # bandwidth)

end = time.time()
print(end - start)






