import numpy as np
import new_comm
import sys
import random
# choose 6 out of 8
def get_configs_ind_6():
    return [[0,0,1,1,1,1,1,1],[0,1,0,1,1,1,1,1],[0,1,1,0,1,1,1,1],[0,1,1,1,0,1,1,1],[0,1,1,1,1,0,1,1],[0,1,1,1,1,1,0,1],[0,1,1,1,1,1,1,0],[1,0,0,1,1,1,1,1],[1,0,1,0,1,1,1,1],[1,0,1,1,0,1,1,1],[1,0,1,1,1,0,1,1],[1,0,1,1,1,1,0,1],[1,0,1,1,1,1,1,0],[1,1,0,0,1,1,1,1],[1,1,0,1,0,1,1,1],[1,1,0,1,1,0,1,1],[1,1,0,1,1,1,0,1],[1,1,0,1,1,1,1,0],[1,1,1,0,0,1,1,1],[1,1,1,0,1,0,1,1],[1,1,1,0,1,1,0,1],[1,1,1,0,1,1,1,0],[1,1,1,1,0,0,1,1],[1,1,1,1,0,1,0,1],[1,1,1,1,0,1,1,0],[1,1,1,1,1,0,0,1],[1,1,1,1,1,0,1,0],[1,1,1,1,1,1,0,0]]

def get_configs(configs_ind, node):
    configs = []
    neighbors = list(node.outs)
    for config_ind in configs_ind:
        config = []
        for i, v in enumerate(config_ind):
            if v == 1:
                config.append(neighbors[i])
        configs.append(config)
    return configs

# input is a list of neighbor
def get_configs_3(neighbors):
    used = 0
    configs = []
    num_out = 8
    for i in range(num_out):
        for j in range(i+1, num_out):
            for k in range(j+1, num_out):
                config = [neighbors[i], neighbors[j], neighbors[k]]
                configs.append(config)
    return configs

# config rule is a tuple, (num_retain, num_new, num_random)
# num msgs is used for stats collection
def new_subset_complete(nodes, ld, num_msg):
    num_nodes = len(nodes)
    # collect stats
    for _ in range(num_msg):
        broad_node = np.random.randint(num_nodes)
        new_comm.broadcast_msg(broad_node, nodes, ld)
    print("after broadcast")

    outs_neighbors = {}
    all_nodes = [i for i in range(len(nodes))]
    random.shuffle(all_nodes)
    for i in all_nodes:
        configs_ind =  get_configs_ind_6()
        configs = get_configs(configs_ind, nodes[i])
        # print(nodes[i].outs)
        # print(configs_ind)
        # print(configs)
        outs_neighbors[i] = subset_complete_choose(nodes, i, configs.copy(), num_msg) 

        for _ in range(2):
            random_add(nodes, i, outs_neighbors[i])

    return outs_neighbors

def new_subset_two_hop(nodes, ld, num_msg):
    num_nodes = len(nodes)
    for _ in range(num_msg):
        broad_node = np.random.randint(num_nodes)
        new_comm.broadcast_msg(broad_node, nodes, ld)

    outs_neighbors = {}
    all_nodes = [i for i in range(len(nodes))]
    random.shuffle(all_nodes)
    # direct peers
    for i in all_nodes:
        configs =  get_configs_3(list(nodes[i].outs))
        outs_neighbors[i] = subset_complete_choose(nodes, i, configs, num_msg)
       
    # two hop peers
    for u in all_nodes:
        subset_two_hop_choose(nodes, u, outs_neighbors)

    # random peers
    for i in all_nodes:
        for _ in range(2):
            random_add(nodes, i, outs_neighbors[i])

    for i, v in outs_neighbors.items():
        # print(i, v)
        assert(len(v) == 8)
    print("finish")
    return outs_neighbors

def subset_two_hop_choose(nodes, u, outs_neighbors):
    one_hop_peers = outs_neighbors[u].copy()
    # two_hop_peers = []
    for v in one_hop_peers:
        peers_2 = outs_neighbors[v].copy()
        random.shuffle(peers_2)
        found = False
        for w in peers_2:
            if ( is_out_addable(nodes[u], outs_neighbors[u], w) and
                nodes[w].num_in_request < nodes[w].in_lim ):
                outs_neighbors[u].append(w)
                nodes[w].num_in_request += 1
                # two_hop_peers.append(w)
                found = True
                break
        if not found:
            w = np.random.randint(len(nodes))
            while not (is_out_addable(nodes[u], outs_neighbors[u], w) and 
                       nodes[w].num_in_request < nodes[w].in_lim):
                w = np.random.randint(len(nodes))

            outs_neighbors[u].append(w)
            nodes[w].num_in_request += 1


def random_add(nodes, i, neighbors):
    num_node = len(nodes)
    s = np.random.randint(num_node)
    while not (is_out_addable(nodes[i], neighbors, s) and 
               nodes[s].num_in_request < nodes[s].in_lim):
        s = np.random.randint(num_node)
    nodes[s].num_in_request += 1
    neighbors.append(s)

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


# for each node, what is the best config
def subset_complete_choose(nodes, i, selects, num_msg):
    num_node = len(nodes)
    best = -1
    best_config = random.choice(selects)
    random.shuffle(selects)
    # print('***node', i)
    # print("init", nodes[i].outs)
    for config in selects:
        is_avail = True 
        for peer in config:
            if nodes[peer].num_in_request >= nodes[peer].in_lim:
                # print("nodes[peer].num_in_request", nodes[peer].num_in_request)
                is_avail = False
                break
        if is_avail:
            score = get_score(nodes[i], config, num_msg)
            if best == -1 or score < best:
                # print('prev score', best, 'new', score)
                best = score 
                best_config = config

    for peer in best_config:
         nodes[peer].num_in_request += 1

    # print("afte", best_config, 'score', best)
    if (best == -1):
        print("none of config allows for selection due to incoming neighbor")
    return best_config


def get_score(node, config, num_msg):
    best_times = [999999 for i in range(num_msg)]
    for peer in config:
        peer_times = node.views_hist[peer]
        # print(peer_times)
        for i in range(num_msg):
            if best_times[i] > peer_times[i]:
                best_times[i] = peer_times[i]

    # print('best', best_times)
    sorted_best_time = sorted(best_times)
    return sorted_best_time[int(num_msg*9.0/10)]


    

# def apply_proposed(nodes, proposed_outs):
    # denied = {} # keys is node id, values is a list of failed conn
    


    # return denied


# def node_seperated():
# # choose best neighbor set based on group scores
    # # random give priority to nodes
    # all_nodes = [i for i in range(num_nodes)]
    # random.shuffle(all_nodes) 
    # all_finish = False
    # proposed_outs = {}

    # random.shuffle(all_nodes) 
    # for u in all_nodes:
        # node = nodes[u]
        # # requests
        # conns = node.one_hop_subset()
        # proposed_outs[u] = conns
    # denied = apply_proposed(nodes, proposed_outs)
    # while len(denied) != 0:
        # for u, _ in proposed_outs.items():
            # if u not in denied:
                # conns = proposed_outs[u]
                # nodes[u].update_neighbors(conns)
            # else:
                # failed_conns = denied[u]
                # proposed_outs.clear()
                # conns = nodes[u].retry_conn(failed_conn)
                # proposed_outs[u] = conns



