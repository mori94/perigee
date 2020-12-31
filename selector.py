import sys
import numpy as np
import random
import config
from oracle import PeersInfo
from collections import namedtuple
ConnInfo = namedtuple('ConnInfo', ['src', 'dst']) 

def sort_new_peer_first(nodes, u, peers):
    outs = nodes[u].outs
    sorted_by_new = []
    for p in peers:
        if p not in nodes[u].views_hist:
            sorted_by_new.insert(0, p)
        else:
            sorted_by_new.append(p)
    return sorted_by_new

def sort_neighbor_by_score(nodes, u, peers):
    node = nodes[u]
    scores = []
    for v, time_list in node.views_hist.items():
        if v in peers:
            sorted_time_list = sorted(time_list)
            scores.append((v, sorted_time_list[int(config.num_subround*9/10)-1]))
    
    sorted_peer_score = sorted(scores, key=lambda x: x[1])
    sorted_peers = [i for i, s in sorted_peer_score]
    return sorted_peers

# u is src, v is dst
def is_connectable(nodes, u, selected, v):
    node = nodes[u]
    if v == u:
        return False
    if v in node.outs:
        return False
    if v in selected:
        return False

    if nodes[v].num_in_request < nodes[v].in_lim:
        return True 
    else:
        return False 


class Selector:
    def __init__(self, u, is_adv):
        self.id = u
        self.is_adv = is_adv
        self.conn = set()
        self.desc_conn = set()
        self.worst_compose = None
        self.best_compose = None # subset of 1 hop nodes
        # self.conn_1s = one_hops.copy()
        # self.conn_2s = [] 

    def set_1hops(self, one_hops):
        for p in one_hops:
            self.add_peer(self.id, p)

    def count_checked(self, all_2hop_peers):
        num_tried = 0
        for k, is_tried in all_2hop_peers.items():
            if is_tried:
                num_tried += 1
        return num_tried

    def get_selected(self):
        # selected = set(self.conn_1s).union(set(self.conn_2s))
        return list(self.conn)

    def get_1hops(self, nodes, u):
        one_hops = self.conn_1s.copy()
        if config.is_rand_select:
            random.shuffle(one_hops)
        if config.is_favor_new:
            one_hops = sort_new_peer_first(nodes, u, one_hops)
        if config.is_sort_hop:
            one_hops_re = sort_neighbor_by_score(nodes, u, one_hops)
            if len(one_hops_re) == len(one_hops):
                one_hops = one_hops_re
            else:
                print('1hop', len(one_hops_re), len(one_hops))
                sys.exit(1)
        return one_hops

    # two hops might have more than 
    def select_2hops(self, two_hops, v, nodes, u):
        if config.is_rand_select:
            random.shuffle(two_hops)
        if config.is_favor_new:
            two_hops = sort_new_peer_first(nodes, u, two_hops)

        if config.is_sort_hop:
            two_hops_re = sort_neighbor_by_score(nodes, v, two_hops)
            if len(two_hops_re) == len(two_hops):
                two_hops = two_hops_re
            else:
                print('2hop', len(two_hops_re), len(two_hops))
                sys.exit(1)
        return two_hops

    def sort_peers(self, peers, nodes, u):
        if config.is_rand_select:
            random.shuffle(peers)
        if config.is_favor_new:
            peers = sort_new_peer_first(nodes, u, peers)
        return peers 

    def add_conn_2s(self, t):
        if t in self.conn_2s:
            print(t, 'in', self.conn_2s)
            print(self.conn_1s)
            selected = self.get_selected()
            print(selected)
            sys.exit(1)
        self.conn_2s.append(t)

    # src is recommender, t is the node id
    def add_peer(self, s, t):
        self.conn.add(t)
        self.desc_conn.add((s,t))

    def select_peers(self, num_required, nodes, peers_info):
        if num_required == 0:
            return []

        candidates = {}
        selected = set()
        recommenders = list(peers_info.keys())

        for v, peers in peers_info.items():
            for p in peers:
                candidates[p] = False
        num_cand = len(candidates)
        
        while len(selected)<num_required and self.count_checked(candidates)<num_cand:
            random.shuffle(recommenders)
            for rec in recommenders:
                peers = peers_info[rec]
                sorted_peers = self.sort_peers(peers, nodes, self.id)
                peer =  self.select_sorted_peers(sorted_peers, candidates, rec, nodes)
                if peer != None:
                    selected.add(peer)
                    self.add_peer(rec, peer)
                    nodes[peer].num_in_request += 1
                if len(selected) == num_required:
                    break

        num_nodes = len(nodes)
        # while len(selected) < num_required:
            # print('Insufficient peer')
            # w = np.random.randint(num_nodes)
            # while not is_connectable(nodes, self.id, self.conn, w):
                # w = np.random.randint(len(nodes))
    
            # self.add_peer(-1, w)
            # selected.add(w)
            # nodes[w].num_in_request += 1

        # assert(len(selected) == num_required)
        return list(selected)

    def select_random_peers(self, nodes, num_required):
        selected = set()
        while len(selected) < num_required:
            w = np.random.randint(len(nodes))
            while not is_connectable(nodes, self.id, self.conn, w):
                w = np.random.randint(len(nodes))
            self.add_peer(-1, w)
            selected.add(w)
        assert(len(selected) == num_required)
        return list(selected)


    def select_sorted_peers(self, sorted_peers, candidates, recommender, nodes):
        for p in sorted_peers:
            if not candidates[p]:
                candidates[p] = True
                if is_connectable(nodes, self.id, self.conn, p):
                    return p
        return None 


    # peers info are info allowed for this node to know to make peers decision 
    # def select_two_hops(self, num_required, nodes, peers_info):
        # u = self.id
        # all_2hop_peers = {} # key is 2hop id, value is tried:
        # # print("self.conn_1s", self.conn_1s)

        # for v in self.conn_1s:
            # assert(v in peers_info.two_hops)
            # two_hops = peers_info.two_hops[v]
            # for p in two_hops:
                # all_2hop_peers[p] = False

        # num_added = 0
        # while (self.count_checked(all_2hop_peers)<len(all_2hop_peers) and
            # num_added < num_required
        # ):
            # assert(len(self.conn_1s) == config.num_keep)

            # one_hops = self.get_1hops(nodes, u)
            # for v in one_hops:
                # one_hop_peers = peers_info.two_hops[v].copy()
                # two_hops = self.select_2hops(one_hop_peers, v, nodes, u)
                # for w in two_hops:
                    # if not all_2hop_peers[w]:
                        # all_2hop_peers[w] = True
                        # selected = self.get_selected()
                        # if is_connectable(nodes, u, selected, w):
                            # self.add_conn_2s(w)
                            # nodes[w].num_in_request += 1
                            # num_added += 1
                            # break
                # if num_added == num_required:
                    # break

        # num_nodes = len(nodes)
        # while num_added < num_required:
            # w = np.random.randint(num_nodes)
            # selected = self.get_selected()
            # while not is_connectable(nodes, u, selected, w):
                # w = np.random.randint(len(nodes))
    
            # self.add_conn_2s(w)
            # nodes[w].num_in_request += 1
            # num_added += 1
        
        # return self.conn_2s.copy()
