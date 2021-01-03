import sys
import numpy as np
import random
import config
from oracle import PeersInfo
from collections import namedtuple

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

class Selector:
    def __init__(self, u, is_adv):
        self.id = u
        self.is_adv = is_adv

        self.conn = set()
        self.desc_conn = set()

        self.worst_compose = None
        self.best_compose = None # subset of 1 hop nodes

        # persistant
        self.scores = {}
        self.seen_out = set() # all peers

    def update(self, out_peers):
        self.conn = set()
        self.desc_conn = set()
        self.worst_compose = None
        self.best_compose = None 
        self.seen_out = self.seen_out.union(out_peers)

    def sort_new_peer_first(self, peers):
        sorted_by_new = []
        for p in peers:
            if p not in self.seen_out:
                sorted_by_new.insert(0, p)
            else:
                sorted_by_new.append(p)
        return sorted_by_new

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
        return list(self.conn)

    # subset
    def get_weighted_score(self, table, compose, num_msg):
        best_times = [999999 for i in range(num_msg)]
        for peer in compose:
            peer_times = table[peer]
            # print(peer_times)
            for i in range(num_msg):
                if best_times[i] > peer_times[i]:
                    best_times[i] = peer_times[i]

        sorted_best_time = sorted(best_times)
        new_score = sorted_best_time[int(num_msg*9.0/10)-1]

        sorted_compose = tuple(sorted(compose))

        if sorted_compose not in self.scores:
            score = new_score
            return score
        else:
            score = config.old_weight*self.scores[sorted_compose] + config.new_weight*new_score
            return score

    def get_score(self, table, compose, num_msg):
        best_times = [999999 for i in range(num_msg)]
        for peer in compose:
            peer_times = table[peer]
            # print(peer_times)
            for i in range(num_msg):
                if best_times[i] > peer_times[i]:
                    best_times[i] = peer_times[i]

        # print('best', best_times)
        sorted_best_time = sorted(best_times)
        return sorted_best_time[int(num_msg*9.0/10)-1]

    # where table belongs to the node i, conn_num makes sure outgoing conn is possible
    def select_1hops(self, table, i, composes, num_msg, network_state):
        # if i == 0:
        #    print('table', sorted(table.keys()))
        best = -1
        best_compose = random.choice(composes)

        worst = -1
        worst_compose = random.choice(composes)

        random.shuffle(composes)
        for compose in composes:
            for peer in compose:
                if not network_state.is_conn_addable(peer):
                    break
                else:
                    if config.use_score_decay:
                        score = self.get_weighted_score(table, compose, num_msg)
                    else:
                        score = self.get_score(table, compose, num_msg)
                     
                    if best == -1 or score < best:
                        best = score 
                        best_compose = compose 

                    if worst == -1 or score > worst:
                        worst = score
                        worst_compose = compose

        for peer in best_compose:
            network_state.add_in_connection(peer)

        if (best == -1):
            print("none of config allows for selection due to incoming neighbor")

        self.worst_compose = worst_compose
        self.best_compose = best_compose

        # for decay
        sorted_compose = tuple(sorted(best_compose))
        self.scores[sorted_compose] = best

        if config.worst_conn_attack and selector.is_adv:
            self.set_1hops(worst_compose)
            return worst_compose
        else:
            self.set_1hops(best_compose)
            return best_compose

    def sort_peers(self, peers):
        if config.is_rand_select:
            random.shuffle(peers)
        if config.is_favor_new:
            peers = self.sort_new_peer_first(peers)
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

    def select_peers(self, num_required, nodes, peers_info, network_state):
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
                sorted_peers = self.sort_peers(peers)
                peer =  self.select_sorted_peers(sorted_peers, candidates, rec, network_state)
                if peer != None:
                    selected.add(peer)
                    self.add_peer(rec, peer)
                    network_state.add_in_connection(peer)
                if len(selected) == num_required:
                    break

        return list(selected)

    # u is src, v is dst
    def is_connectable(self,u, selected, v, network_state):
        if v == u:
            return False
        if v in selected:
            return False
        if network_state.is_conn_addable(v): 
            return True 
        else:
            return False 

    def select_random_peers(self, nodes, num_required, network_state):
        selected = set()
        while len(selected) < num_required:
            w = np.random.randint(len(nodes))
            while not self.is_connectable(self.id, self.conn, w, network_state):
                w = np.random.randint(len(nodes))
            self.add_peer(-1, w)
            selected.add(w)
            network_state.add_in_connection(w)

        assert(len(selected) == num_required)
        return list(selected)


    def select_sorted_peers(self, sorted_peers, candidates, recommender, network_state):
        for p in sorted_peers:
            if not candidates[p]:
                candidates[p] = True
                if self.is_connectable(self.id, self.conn, p, network_state):
                    return p
        return None 
