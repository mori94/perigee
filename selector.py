import sys
import numpy as np
import random
import config
from messages import PeersInfo


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
    if (is_out_addable(node, selected, v) and 
        nodes[v].num_in_request < nodes[v].in_lim ):
        return True
    else:
        return False


def is_out_addable(node, selected, u):
    if u == node.id:
        return False
    # if u in node.ins:
    #    return False
    if u in node.outs:
        return False
    if u in selected:
        return False
    return True


class Selector:
    def __init__(self, u):
        self.id = u
        self.conn_1s = [] 
        self.conn_2s = [] 

    def set_1hops(self, one_hops):
        self.conn_1s = one_hops.copy()

    def count_2hop(self, all_2hop_peers):
        num_tried = 0
        for k, is_tried in all_2hop_peers.items():
            if is_tried:
                num_tried += 1
        return num_tried

    def get_selected(self):
        selected = set()
        selected.union(set(self.conn_1s))
        selected.union(set(self.conn_2s))
        return list(selected)

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
    def get_2hops(self, two_hops, v, nodes, u):
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

    def add_conn_2s(self, t):
        if t in self.conn_2s:
            print(t, 'in', self.conn_2s)
            sys.exit(1)
        self.conn_2s.append(t)

    # peers info are info allowed for this node to know to make peers decision 
    def select_two_hops(self, num_required, nodes, peers_info):
        u = self.id
        all_2hop_peers = {} # key is 2hop id, value is tried:
        # print("self.conn_1s", self.conn_1s)

        for v in self.conn_1s:
            assert(v in peers_info.two_hops)
            two_hops = peers_info.two_hops[v]
            for p in two_hops:
                all_2hop_peers[p] = False

        num_added = 0
        while (self.count_2hop(all_2hop_peers)<len(all_2hop_peers) and
            num_added < num_required
        ):
            assert(len(self.conn_1s) == config.num_keep)

            one_hops = self.get_1hops(nodes, u)
            for v in one_hops:
                one_hop_peers = peers_info.two_hops[v].copy()
                two_hops = self.get_2hops(one_hop_peers, v, nodes, u)
                for w in two_hops:
                    if not all_2hop_peers[w]:
                        all_2hop_peers[w] = True
                        selected = self.get_selected()
                        if is_connectable(nodes, u, selected, w):
                            self.add_conn_2s(w)
                            nodes[w].num_in_request += 1
                            num_added += 1
                            break
                if num_added == num_required:
                    break

        num_nodes = len(nodes)
        while num_added < num_required:
            w = np.random.randint(num_nodes)
            selected = self.get_selected()
            while not is_connectable(nodes, u, selected, w):
                w = np.random.randint(len(nodes))
    
            self.add_conn_2s(w)
            nodes[w].num_in_request += 1
            num_added += 1
        
        return self.conn_2s.copy()
