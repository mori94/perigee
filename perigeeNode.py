import numpy as np
from collections import defaultdict
import random



# update in neighbors
def update_ins_for_all_nodes(nodes):
    for i, node in nodes.items():
        for out in node.outs:
            nodes[out].ins.add(i)

def create_random_neighbor(nodes):
    num_node = len(nodes)
    while True:
        all_nodes = [i for i in range(num_node)]
        random.shuffle(all_nodes) 
        for u in all_nodes:
            if len(nodes[u].outs) == nodes[u].out_lim:
                continue
        
            v = np.random.randint(num_node)
            while not (nodes[u].is_out_addable(v) and nodes[v].is_in_addable(u)):
                v = np.random.randint(num_node)
            nodes[u].add_out(v)
            nodes[v].add_in(u)

        finish = True
        for u in all_nodes:
            if len(nodes[u].outs) < nodes[u].out_lim:
                finish = False

        if finish:
            break
    print('Random neighbor initialization done.')
                

def update_conn_for_all_nodes(nodes, neighbor_set):
    for i, peers in neighbor_set.items():
        if len(set(peers)) != len(peers):
            print(i, peers)


        nodes[i].outs = set(peers)
        nodes[i].ins.clear()
        nodes[i].views.clear()
        nodes[i].views_hist.clear()
        nodes[i].recv_time = 0
        nodes[i].num_in_request = 0
        nodes[i].received = False
    update_ins_for_all_nodes(nodes)

def dynamic_conn_update(nodes):
    # shuffle randomness
    all_nodes = [i for i, _ in nodes.items()]
    random.shuffle(all_nodes)
    for i in all_nodes:
        node = nodes[i]
        proposed_peers = node.propose
        node.adapt_neighrbors(node.candidates[:node.out_lim])

def get_OutNeighbor(nodes, num_out):
    num_node = len(nodes)
    out_neighbor = np.zeros((num_node, num_out))
    for i in range(num_node):
        out_neighbor[i] = list(nodes[i].outs)
    return out_neighbor


class Node:
    def __init__(self, nid, n_delay, in_lim, out_lim, init_outs): #, num_keep, num_rand, num_choose
        self.ins = set()
        self.outs = set(init_outs)
        # they are out candidates
        # self.num_keep = 0 #num_keep
        # self.keep = []
        # self.num_choose = num_choose
        # self.choose = [] 
        # self.num_rand = num_rand
        # self.rand = []

        self.id = nid
        self.node_delay = n_delay
        self.in_lim =  in_lim
        self.out_lim = out_lim 

        self.received = False
        self.from_whom = None # earliest recv peer
        self.recv_time = 0

        # every epoch, a msg is broadcasted and hence values equals to number of message
        self.views = {} # key is peer id, value is current relative time 
        self.views_hist = defaultdict(list) # key is peer id, value is a list of time for all sub round
        self.prev_score = {} #key is combination, value is previous score

        self.num_in_request = 0

        # candidates subject to disconn
        # self.candidates = [] # for current epoch from lead to least
        # self.accepted = []

        # configs
        # configs = self.get_configs_3(self.out_lim, self.num_keep)

    def set_epoch_precondition(self):
        self.views_hist.clear()
        self.candidates.clear()
        self.accepted.clear()

    def remove_lowest_out(self):
        low_peer = self.candidates.pop(len(self.candidates)-1)
        self.outs.remove(low_peer)
        return low_peer

    def add_new_peers(self, peer):
        assert((peer not in self.outs) and (peer not in self.ins))
        self.outs.add(peer)
        self.accepted.append(peer)
        pass

    def update_neighbors(self, outs):
        self.outs = outs

    # apply command from network
    def adapt_neighbor(self, out):
        peer_removed = None
        if (out in self.outs) or (peer in self.ins):
            self.candidates.remove(out)
            self.accepted.add(out)
        else:
            peer_removed = self.remove_lowest_out()
            self.add_new_peers(out)

        return peer_removed

    def propose_peers(self):
        num_required = self.out_lim - len(self.accepted) 
        proposed = []
        if len(self.candidates) >= num_required:
            proposed = self.candidates[:num_required]
        else:
            proposed = self.candidates[len(self.candidates)]
            
        return self.candidates[:]

    # return out neighbors for this round
    def one_hop_vanilla(self):
        candidates = []
        for peer, time_list in self.views_hist():
            sorted_times = sorted(time_list)
            percentile90 = int(len(sorted_times)*9/10)
            time_90 = sorted_times[percentile90]
            candidates.append((peer, time_90))

        sorted_cands = sorted(candidates, key=lambda x: x[1])
        self.candidates = [t for t, s in sorted_cands]

        # the rest for code legacy
        candidates = self.candidates[:self.out_lim]
        return outs

    def two_hop_vanilla(self):
        conn = []
        disconn = []
        return conn, disconn
    
    def get_configs_3(self):
        used = 0
        configs = []
        num_out = len(self.outs)
        neighbors = list(self.outs)
        for i in range(num_out):
            for j in range(i+1, num_out):
                for k in range(j+1, num_out):
                    config = (neighbors[i], neighbors[j], neighbors[k])
                    configs.append(config)
        return configs

    def one_hop_subset(self, num_msg):
        config_rank = self.subset_retain(self, num_msg)
        self.keep = config_rank
        return config_rank

    def subset_retain(self, num_msg):
        configs = self.get_configs_3()
        config_score = {}

        for config in configs:
            for peer, time_list in self.views_hist:
                table = [] 
                if peer in config:
                    # if peers
                    if len(table) == 0:
                        table = time_list
                    else:
                        for i, a in enumerate(table):
                            if a > time_list[i]:
                                table[i] = time_list[i]
            idx = int(num_msg*9.0/10)
            config_score[config] = table[idx]

        config_rank = sorted(config_score.items(), key=lambda item: item[1])
        return config_rank

    def subset_choose(self, config_rank):
        pass
            




    def two_hop_subset(self):
        pass
        

    def set_recv_time(self, t):
        self.recv_time = t
    def get_recv_time(self):
        return self.recv_time

    def get_peers(self):
        return self.outs | self.ins # get union

    def get_deg(self):
        return len(self.ins) + len(self.outs)

    def add_out(self, v):
        assert(v not in self.outs)
        self.outs.add(v)

    def add_in(self, v):
        assert(v not in self.ins)
        self.ins.add(v)

    def update_outs(self, dropped, added):
        for u in dropped:
            self.outs.remove(u)
        for u in added:
            self.outs.add(u)
    def update_ins(self, dropped, added):
        for u in dropped:
            self.ins.remove(u)
        for u in added:
            self.ins.add(u)

    # return removed
    def reset_outs(self, added):
        removed = self.outs.difference(added)
        self.outs = set(added)
        return removed

    def is_out_addable(self, u):
        if u == self.id:
            return False
        if u in self.ins:
            return False
        if u in self.outs:
            return False
        # if len(self.outs)+1 > self.out_lim:
        #     return False
        return True

    def is_in_addable(self, u):
        if u == self.id:
            return False
        if u in self.ins:
            return False
        if u in self.outs:
            return False
        if len(self.ins)+1 > self.in_lim:
            return False
        return True




