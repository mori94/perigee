import sys
import numpy as np
import random
import config
from oracle import PeersInfo
from collections import namedtuple
from collections import defaultdict 
# for multithread
# from threading import Thread
# import concurrent.futures

import copy

# return None if invalid
def threaded_function(arg):
    compose, table, num_msg, u, scores = arg
    if config.use_score_decay:
        score = get_weighted_score(table, compose, num_msg, scores)
        return score
    else:
        score = get_score(table, compose, num_msg)
        return score

# subset
def get_weighted_score(table, compose, num_msg, scores):
    best_times = table[compose[0]].copy()
    for peer in compose[1:]:
        peer_times = table[peer]
        # print(peer_times)
        for i in range(num_msg):
            if best_times[i] > peer_times[i]:
                best_times[i] = peer_times[i]

    sorted_best_time = sorted(best_times)
    new_score = sorted_best_time[int(num_msg*9.0/10)-1]

    if compose not in scores:
        score = new_score
        return score
    else:
        score = config.old_weight*scores[compose] + config.new_weight*new_score
        return score

def get_score(table, compose, num_msg):
    best_times = table[compose[0]].copy()
    for peer in compose[1:]:
        peer_times = table[peer]
        # print(peer_times)
        for i in range(num_msg):
            if best_times[i] > peer_times[i]:
                best_times[i] = peer_times[i]

    # print('best', best_times)
    sorted_best_time = sorted(best_times)
    return sorted_best_time[int(num_msg*9.0/10)-1]

class Selector:
    def __init__(self, u, is_adv, curr_outs, curr_ins, pools):
        self.id = u
        self.is_adv = is_adv

        self.conn = set()
        self.desc_conn = set()

        self.worst_compose = None
        self.best_compose = None # subset of 1 hop nodes

        # persistant
        self.scores = {}
        self.seen_nodes = set() # all peers
        self.curr_ins = curr_ins.copy()
        self.curr_outs = curr_outs.copy()
        # self.seen_nodes = self.seen_nodes.union(curr_ins)
        self.seen_nodes = self.seen_nodes.union(curr_outs)

        self.seen_compose = set()

        self.pools = pools


    def update(self, out_peers, in_peers):
        # if self.id == 778:
        #    print(self.id, self.desc_conn)
        self.conn = set()
        self.desc_conn = set()
        self.worst_compose = None
        self.best_compose = None 
        self.seen_nodes = self.seen_nodes.union(out_peers)
        # self.seen_nodes = self.seen_nodes.union(in_peers)
        self.curr_outs = out_peers.copy()
        self.curr_ins = in_peers.copy()


    def sort_new_peer_first(self, peers):
        sorted_by_new = []
        for p in peers:
            if p not in self.seen_nodes:
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


    def get_best_compose(self, table, composes, num_msg):
        best = None 
        worst = None
        for compose in composes:
            score = None 
            if config.use_score_decay:
                score = get_weighted_score(table, compose, num_msg, self.scores)
            else:
                score = get_score(table, compose, num_msg)
             
            if best == None or score < best:
                best = score 
                best_compose = compose 

            if worst == None or score > worst:
                worst = score
                worst_compose = compose

        return best_compose, best, worst_compose, worst, best==None



    # where table belongs to the node i, conn_num makes sure outgoing conn is possible
    def select_1hops(self, table, composes, num_msg, network_state):
        best_compose, best, worst_compose, worst, is_random = None, None, None, None, None
        if config.num_thread == 1:
            best_compose, best, worst_compose, worst, is_random = self.get_best_compose(
                    table, composes, 
                    num_msg)
        else:
            best_compose, best, worst_compose, worst, is_random = self.get_compose_multithread(
                    table, composes, 
                    num_msg, network_state)
        if is_random:
            print("none of compose is suitable, after filter. Bug")
            print(self.id, len(composes), best_compose, worst_compose)
            assert(len(set(worst_compose)) == len(worst_compose))
            assert(len(set(best_compose)) == len(best_compose))
            sys.exit(1)

        if not self.is_adv: 
            for peer in best_compose:
                network_state.add_in_connection(self.id, peer)
        elif config.worst_conn_attack:
            for peer in worst_compose:
                network_state.add_in_connection(self.id, peer)

        self.worst_compose = list(worst_compose)
        self.best_compose = list(best_compose)

        # for decay
        self.scores[best_compose] = best

        if config.worst_conn_attack and self.is_adv:
            self.set_1hops(worst_compose)
            return list(worst_compose)
        else:
            self.set_1hops(best_compose)
            return list(best_compose)

    def sort_peers(self, peers):
        if config.is_rand_select:
            random.shuffle(peers)
        if config.is_favor_new:
            peers = self.sort_new_peer_first(peers)
        # if config.is_sort_score:
            # peers = self.sort_neighbor_by_score(peers)
            # pass
        return peers

    def sort_neighbor_by_score( u, peers, table):
        node = nodes[u]
        scores = []
        for v, time_list in node.views_hist.items():
            if v in peers:
                sorted_time_list = sorted(time_list)
                scores.append((v, sorted_time_list[int(config.num_msg*9/10)-1]))
        
        sorted_peer_score = sorted(scores, key=lambda x: x[1])
        sorted_peers = [i for i, s in sorted_peer_score]
        return sorted_peers

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
        assert(t not in self.conn)
        self.conn.add(t)
        self.desc_conn.add((s,t))

    def select_peers_per_recommender(self, num_required, nodes, peers_info, network_state):
        total_num_not_seen = 0
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
                peer = self.select_sorted_peers(sorted_peers, candidates, rec, network_state)

                if peer != None:
                    # trace
                    if peer not in self.seen_nodes:
                        total_num_not_seen += 1 

                    selected.add(peer)
                    self.add_peer(rec, peer)
                    network_state.add_in_connection(self.id, peer)
                if len(selected) == num_required:
                    break
        return selected, total_num_not_seen

    def select_peers(self, num_required, nodes, peers_info, network_state):
        if num_required == 0:
            return [], 0 
        selected, total_num_not_seen = None, None
        if config.is_per_recommeder_select:
            selected, total_num_not_seen = self.select_peers_per_recommender(
                num_required, 
                nodes, 
                peers_info, 
                network_state)

        if config.is_rank_occurance:
            selected, total_num_not_seen = self.select_ranked_peers(
                num_required, 
                nodes, 
                peers_info, 
                network_state)
        assert(selected != None)
        return list(selected), total_num_not_seen

    def select_ranked_peers(self, num_required, nodes, peers_info, network_state):
        assert(num_required > 0)
        candidates = {} # key is candidate id, value is occurance
        selected = []

        for v, peers in peers_info.items():
            for p in peers:
                if self.is_connectable(p, network_state):
                    if p not in candidates:
                        candidates[p] = 1
                    else:
                        candidates[p] += 1
        num_cand = len(candidates)
        groups = defaultdict(list)
        sorted_occurance = None
        if num_cand <= num_required:
            selected = [k for k in candidates.keys()]
        else: 
            
            for peer, o in candidates.items():
                groups[o].append(peer)

            sorted_occurance = sorted(groups.keys(), reverse=True)
            for occ in sorted_occurance:
                group = groups[occ].copy()
                if len(selected) + len(group) > num_required:
                    random.shuffle(group)
                    selected += group[:num_required-len(selected)]
                    break
                else:
                    selected += group
            
        if num_cand <= num_required:
            assert(num_cand == len(selected))
        else:
            assert(len(selected) == num_required)
            # if sorted_occurance != None and sorted_occurance[0] > 1:
                # print('System bug')
                # print(sorted_occurance)
                # print('groups', groups)
                # print('candidates', candidates)
                # print('num_required', num_required)
                # print('selected', selected)
                # sys.exit(1)

        for peer in selected:
            if peer in self.conn:   
                print(peer, 'in conn', self.desc_conn)
                print(selected)
                print(candidates)
                print(groups)
                print(sorted_occurance)
                sys.exit(1)
            self.add_peer(-2, peer)
            network_state.add_in_connection(self.id, peer)

        return selected, 0


    def subset_select(self, recommenders, candidates):
        for node in candidates:
            pass
            # if node belongs to any subset
            
            # else:

    # u is src, v is dst
    def is_connectable(self, v, network_state):
        if v == self.id:
            return False
        if v in self.conn:
            return False
        if v in self.curr_outs:
            return False
        if v in self.curr_ins:
            return False
        if network_state.is_conn_addable(self.id, v): 
            return True 
        else:
            return False 

    def select_random_peers(self, nodes, num_required, network_state):
        selected = set()
        while len(selected) < num_required:
            w = np.random.randint(len(nodes))
            while not self.is_connectable(w, network_state):
                w = np.random.randint(len(nodes))
            self.add_peer(-1, w)
            selected.add(w)
            network_state.add_in_connection(self.id, w)

        assert(len(selected) == num_required)
        return list(selected)


    def select_sorted_peers(self, sorted_peers, candidates, recommender, network_state):
        for p in sorted_peers:
            if not candidates[p]:
                candidates[p] = True
                if self.is_connectable(p, network_state):
                    return p
        return None 

    def get_compose_multithread(self, table, composes, num_msg, network_state):
        scores = {}
        # print('start multihread', self.id)
        
        futures = []
        for compose in composes:
            arg = (compose, table, num_msg, self.id, None)
            future = self.pools.submit(threaded_function, arg)
            futures.append(future)

        assert(len(futures) == len(composes))
        for i in range(len(futures)):
            score = futures[i].result()
            compose = composes[i]

            if score != None:
                scores[compose] = score
            else:
                sys.exit(1)
        
        # get the best and worst compose
        best, worst = None, None
        for compose, score in scores.items():
            if best == None or best > score:
                best_compose = compose
                best = score
            if worst == None or worst < score:
                worst_compose = compose
                worst = score

        return  best_compose, best, worst_compose, worst, best==None
