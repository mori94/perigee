import sys
import config
from messages import PeersInfo
from perigeeNode import Node
import networkx as nx
import writefiles
import new_subset
import time
import numpy as np

class Experiment:
    def __init__(self, node_hash, link_delay, node_delay, num_node, in_lim, out_lim, name):
        self.nh = node_hash
        self.ld = link_delay
        self.nd = node_delay
        self.num_node = num_node
        self.nodes = {} # nodes are used for communicating msg in network
        self.selectors = {} # selectors for choosing outgoing conn for next time
        self.in_lim = in_lim
        self.out_lim = out_lim
        self.outdir = name

        self.timer = time.time()

    # generate networkx graph instance
    def construct_graph(self):
        num_nodes = len(self.nodes)
        G = nx.Graph()
        for i, node in self.nodes.items():
            for u in node.outs:
                delay = self.ld[i][u] + node.node_delay/2 + self.nodes[u].node_delay/2
                assert(i != u)
                G.add_edge(i, u, weight=delay)
        return G

    def update_ins_conns(self):
        all_nodes = list(self.nodes.keys())
        for i in all_nodes:
            node = self.nodes[i]
            for out in node.outs:
                self.nodes[out].ins.add(i)

    def update_conns(self, out_conns):
        nodes = self.nodes
        for i, peers in out_conns.items():
            if len(set(peers)) != len(peers):
                print(i, peers)
            nodes[i].seen.union(peers) 
            nodes[i].outs = set(peers)
            nodes[i].ins.clear()
            nodes[i].views.clear()
            nodes[i].views_hist.clear()
            nodes[i].recv_time = 0
            nodes[i].num_in_request = 0
            nodes[i].received = False
        self.update_ins_conns()

    def get_outs_neighbors(self):
        out_neighbor = np.zeros((self.num_node, self.out_lim))
        for i in range(self.num_node):
            out_neighbor[i] = list(self.nodes[i].outs)
        return out_neighbor

    def init_graph(self, outs_neighbors):
        for i in range(self.num_node):
            node_delay = self.nd[i]
            in_lim = self.in_lim
            self.nodes[i] = Node(
                i,
                node_delay,
                self.in_lim,
                self.out_lim,
                outs_neighbors[i]
            )
        self.update_ins_conns()
        print('Finish. init graph')

    def take_snapshot(self, epoch):
        print("Start recording")
        name =  str(config.network_type)+'_'+str(config.method)+"V1"+"Round"+str(epoch)+".txt"
        outpath = self.outdir + "/" + name
            
        G = self.construct_graph()
        outs_neighbors = self.get_outs_neighbors()
        writefiles.write(outpath, G, self.nd, outs_neighbors, self.num_node)
        curr_time = time.time()
        elapsed = curr_time - self.timer 
        self.timer = curr_time
        print("Finish. Recording", epoch, "using time", elapsed)

    def start(self, max_epoch, record_epochs):
        for epoch in range(max_epoch):
            if epoch in record_epochs:
                self.take_snapshot(epoch)

            outs_conns = new_subset.new_subset_two_hop(
                self.nodes, 
                self.ld, 
                config.num_msg, 
                self.nh, 
                self.selectors)
            self.update_conns(outs_conns)




