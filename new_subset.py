import numpy as np
import new_comm
import sys
import random
import config 
import visualizer
# choose 6 out of 8
def get_configs_ind_6():
    return [[0,0,1,1,1,1,1,1],[0,1,0,1,1,1,1,1],[0,1,1,0,1,1,1,1],[0,1,1,1,0,1,1,1],[0,1,1,1,1,0,1,1],[0,1,1,1,1,1,0,1],[0,1,1,1,1,1,1,0],[1,0,0,1,1,1,1,1],[1,0,1,0,1,1,1,1],[1,0,1,1,0,1,1,1],[1,0,1,1,1,0,1,1],[1,0,1,1,1,1,0,1],[1,0,1,1,1,1,1,0],[1,1,0,0,1,1,1,1],[1,1,0,1,0,1,1,1],[1,1,0,1,1,0,1,1],[1,1,0,1,1,1,0,1],[1,1,0,1,1,1,1,0],[1,1,1,0,0,1,1,1],[1,1,1,0,1,0,1,1],[1,1,1,0,1,1,0,1],[1,1,1,0,1,1,1,0],[1,1,1,1,0,0,1,1],[1,1,1,1,0,1,0,1],[1,1,1,1,0,1,1,0],[1,1,1,1,1,0,0,1],[1,1,1,1,1,0,1,0],[1,1,1,1,1,1,0,0]]

def get_configs(configs_ind, node):
    composes = []
    neighbors = list(node.outs)
    for config_ind in configs_ind:
        compose = []
        for i, v in enumerate(config_ind):
            if v == 1:
                compose.append(neighbors[i])
        composes.append(compose)
    return composes

def get_configs_7(neighbors):
    composes = []
    num_out = config.out_lim
    for i in range(num_out):
        for j in range(i+1, num_out):
            for k in range(j+1, num_out):
                for w in range(k+1, num_out):
                    for r in range(w+1, num_out):
                        for t in range(r+1, num_out):
                            for o in range(t+1, num_out):
                                compose = [neighbors[i], neighbors[j], neighbors[k], neighbors[w], neighbors[r], neighbors[t], neighbors[o]]
                                composes.append(compose)
    return composes 

def get_configs_8(neighbors):
    composes = []
    num_out = config.out_lim
    for i in range(num_out):
        for j in range(i+1, num_out):
            for k in range(j+1, num_out):
                for w in range(k+1, num_out):
                    for r in range(w+1, num_out):
                        for t in range(r+1, num_out):
                            for o in range(t+1, num_out):
                                for p in range(o+1, num_out):
                                    compose = [neighbors[i], neighbors[j], neighbors[k], neighbors[w], neighbors[r], neighbors[t], neighbors[o], neighbors[p]]
                                    composes.append(compose)
    return composes 

def get_configs_6(neighbors):
    composes = []
    num_out = config.out_lim
    for i in range(num_out):
        for j in range(i+1, num_out):
            for k in range(j+1, num_out):
                for w in range(k+1, num_out):
                    for r in range(w+1, num_out):
                        for t in range(r+1, num_out):
                            compose = [neighbors[i], neighbors[j], neighbors[k], neighbors[w], neighbors[r], neighbors[t]]
                            composes.append(compose)
    return composes 

def get_configs_5(neighbors):
    composes = []
    num_out = config.out_lim
    for i in range(num_out):
        for j in range(i+1, num_out):
            for k in range(j+1, num_out):
                for w in range(k+1, num_out):
                    for r in range(w+1, num_out):
                        compose = [neighbors[i], neighbors[j], neighbors[k], neighbors[w], neighbors[r]]
                        composes.append(compose)
    return composes 
def get_configs_4(neighbors):
    composes = []
    num_out = config.out_lim
    for i in range(num_out):
        for j in range(i+1, num_out):
            for k in range(j+1, num_out):
                for w in range(k+1, num_out):
                    compose = [neighbors[i], neighbors[j], neighbors[k], neighbors[w]]
                    composes.append(compose)
    return composes

# input is a list of neighbor
def get_configs_3(neighbors):
    composes = []
    num_out = config.out_lim
    for i in range(num_out):
        for j in range(i+1, num_out):
            for k in range(j+1, num_out):
                compose = [neighbors[i], neighbors[j], neighbors[k]]
                composes.append(compose)
    return composes

def get_configs_2(neighbors):
    composes = []
    num_out = config.out_lim
    for i in range(num_out):
        for j in range(i+1, num_out):
            compose = [neighbors[i], neighbors[j]]
            composes.append(compose)
    return composes 

def get_configs_1(neighbors):
    composes = []
    num_out = config.out_lim
    for i in range(num_out):
        compose = [neighbors[i]]
        composes.append(compose)
    return composes
# config rule is a tuple, (num_retain, num_new, num_random)
# num msgs is used for stats collection
def new_subset_complete(nodes, ld, num_msg, nh):
    num_nodes = len(nodes)
    # collect stats
    for _ in range(num_msg):
        broad_node = -1
        if nh is None:
            broad_node = np.random.randint(num_nodes)
        else:
            broad_node = new_comm.get_broadcast_node(nh)
        new_comm.broadcast_msg(broad_node, nodes, ld, nh)
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



# nh is node hash
def new_subset_two_hop(nodes, ld, num_msg, nh):
    num_nodes = len(nodes)
    for _ in range(num_msg):
        broad_node = -1
        if nh is None:
            broad_node = np.random.randint(num_nodes)
        else:
            broad_node = new_comm.get_broadcast_node(nh)
        new_comm.broadcast_msg(broad_node, nodes, ld, nh)

    outs_neighbors = {}

    update_nodes = [i for i in range(len(nodes))]
    random.shuffle(update_nodes)
    

    # direct peers
    for i in update_nodes:
        composes = None
        if config.num_keep == 3:
            composes =  get_configs_3(list(nodes[i].outs))
        elif config.num_keep == 2: 
            composes =  get_configs_2(list(nodes[i].outs))
        elif config.num_keep == 1: 
            composes =  get_configs_1(list(nodes[i].outs))
        elif config.num_keep == 4: 
            composes =  get_configs_4(list(nodes[i].outs))
        elif config.num_keep == 5: 
            composes =  get_configs_5(list(nodes[i].outs))
        elif config.num_keep == 6: 
            composes =  get_configs_6(list(nodes[i].outs))
        elif config.num_keep == 7: 
            composes =  get_configs_7(list(nodes[i].outs))
        elif config.num_keep == 8: 
            composes =  get_configs_8(list(nodes[i].outs))
        else:
            print('Error. choose a valid configs setting')
            sys.exit(0)
        outs_neighbors[i] = subset_complete_choose(nodes, i, composes, num_msg)

    # two hop peers
    if config.num_2_hop > 0:
        for u in update_nodes:
            subset_two_hop_choose(nodes, u, outs_neighbors)

    # three jop
    if config.num_3_hop > 0:
        for u in update_nodes:
            subset_three_hop_choose(nodes, u, outs_neighbors)

    # random peers
    if config.num_random > 0:
        for i in update_nodes:
            for _ in range(config.num_random):
                random_add(nodes, i, outs_neighbors[i])

    return outs_neighbors

def sort_new_peer_first(nodes, u, peers):
    outs = nodes[u].outs
    sorted_by_new = []
    for p in peers:
        if p not in nodes[u].views_hist:
            sorted_by_new.insert(0, p)
        else:
            sorted_by_new.append(p)
    return sorted_by_new


def subset_two_hop_choose(nodes, u, outs_neighbors):
    one_hop_peers = outs_neighbors[u].copy()
    random.shuffle(one_hop_peers)
   
    # favor high score peers
    if config.is_sort_hop:
        one_hop_peers = sort_neighbor_by_score(nodes, u, one_hop_peers)

    # favor new peers not seen before
    one_hop_peers = sort_new_peer_first(nodes, u, one_hop_peers)
   
    num_required = config.num_2_hop
    num_added = 0

    all_2hop_peers = set()
    for v in one_hop_peers:
        for p in outs_neighbors[v]:
            all_2hop_peers.add(p)
    all_2hop_peers = list(all_2hop_peers)

    for v in one_hop_peers:
        peers_2 = outs_neighbors[v].copy()
        random.shuffle(peers_2)
        # take one per peers
        for w in peers_2:
            if 

            if ( is_out_addable(nodes[u], outs_neighbors[u], w) and
                nodes[w].num_in_request < nodes[w].in_lim 
            ):
                outs_neighbors[u].append(w)
                nodes[w].num_in_request += 1
                num_added += 1
                break
            else:
                if nodes[w].num_in_request < nodes[w].in_lim :
                    print(u, " cannot add 2hop", w, "reach conn bound")
                else:
                    print(u, " cannot add 2hop", w, "selected")
        # have enough 2hop nodes 
        if num_added == num_required:
            break
    # if there is not
    while num_added < num_required:
        print(u, '2hop not enough, random choose')
        w = np.random.randint(len(nodes))
        while not (is_out_addable(nodes[u], outs_neighbors[u], w) and 
                   nodes[w].num_in_request < nodes[w].in_lim):
            w = np.random.randint(len(nodes))

        outs_neighbors[u].append(w)
        nodes[w].num_in_request += 1
        num_added += 1

def add_peer(nodes, u, w, out_neighbors):
    


# since subset nodes are grouped, we need to sort the group
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

# a is the edge switching nodes
def subset_three_hop_choose(nodes, a, outs_neighbors):
    one_hop_peers = outs_neighbors[a].copy()

    one_hop_peers = sort_neighbor_by_score(nodes, a, one_hop_peers)
   

    num_required = 0
    num_needed = config.num_3_hop

    for u in one_hop_peers:
        two_hop_peers = outs_neighbors[u].copy()
        two_hop_peers = sort_neighbor_by_score(nodes, u, two_hop_peers)
        # choose one peer for each layer 2 peer
        v =  two_hop_peers[0]

        peers_3 = outs_neighbors[v].copy()
        # random.shuffle(peers_2)
        found = False
        for w in peers_3:
            if ( is_out_addable(nodes[a], outs_neighbors[a], w) and
                nodes[w].num_in_request < nodes[w].in_lim ):
                outs_neighbors[a].append(w)
                nodes[w].num_in_request += 1
                num_3_hop += 1
                # two_hop_peers.append(w)
                found = True
                break
        if not found:
            w = np.random.randint(len(nodes))
            while not (is_out_addable(nodes[a], outs_neighbors[a], w) and 
                       nodes[w].num_in_request < nodes[w].in_lim):
                w = np.random.randint(len(nodes))

            outs_neighbors[a].append(w)
            nodes[w].num_in_request += 1
            num_3_hop += 1

        if num_3_hop >= config.num_3_hop:
            return

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
    for compose in selects:
        is_avail = True 
        for peer in compose:
            if nodes[peer].num_in_request >= nodes[peer].in_lim:
                # print("nodes[peer].num_in_request", nodes[peer].num_in_request)
                is_avail = False
                break
        if is_avail:
            if config.use_score_decay:
                score = get_weighted_score(nodes[i], compose, num_msg)
            else:
                score = get_score(nodes[i], compose, num_msg)
             
            if best == -1 or score < best:
                best = score 
                best_compose = compose 

    for peer in best_compose:
         nodes[peer].num_in_request += 1
    if (best == -1):
        print("none of config allows for selection due to incoming neighbor")

    sorted_compose = tuple(sorted(best_compose))
    prev_score = nodes[i].prev_score
    prev_score[sorted_compose] = best

    return best_compose

def get_weighted_score(node, compose, num_msg):
    # print("use weighted score")
    best_times = [999999 for i in range(num_msg)]
    for peer in compose:
        peer_times = node.views_hist[peer]
        # print(peer_times)
        for i in range(num_msg):
            if best_times[i] > peer_times[i]:
                best_times[i] = peer_times[i]

    # print('best', best_times)
    sorted_best_time = sorted(best_times)
    new_score = sorted_best_time[int(num_msg*9.0/10)]


    sorted_compose = tuple(sorted(compose))
    # print('compose', compose)
    # print('sorted_compose', sorted_compose)
    # print('node.prev_score', node.prev_score)

    score = -1

    if sorted_compose not in node.prev_score:
        score = new_score
    else:
        score = config.old_weight*node.prev_score[sorted_compose] + config.new_weight*new_score

    return score



def get_score(node, compose, num_msg):
    best_times = [999999 for i in range(num_msg)]
    for peer in compose:
        peer_times = node.views_hist[peer]
        # print(peer_times)
        for i in range(num_msg):
            if best_times[i] > peer_times[i]:
                best_times[i] = peer_times[i]

    # print('best', best_times)
    sorted_best_time = sorted(best_times)
    return sorted_best_time[int(num_msg*9.0/10)]

def new_subset_two_hop_sequential(nodes, ld, num_msg, nh, schedule_node):
    num_nodes = len(nodes)
    for _ in range(num_msg):
        broad_node = -1
        if nh is None:
            broad_node = np.random.randint(num_nodes)
        else:
            broad_node = new_comm.get_broadcast_node(nh)
        new_comm.broadcast_msg(broad_node, nodes, ld, nh)

    outs_neighbors = {}
    update_nodes = schedule_node
    for i in range(len(nodes)):
        if i not in update_nodes:
            outs_neighbors[i] = list(nodes[i].outs)

    for i in update_nodes:
        composes = None
        if config.num_keep == 3:
            composes =  get_configs_3(list(nodes[i].outs))
        elif config.num_keep == 2: 
            composes =  get_configs_2(list(nodes[i].outs))
        elif config.num_keep == 1: 
            composes =  get_configs_1(list(nodes[i].outs))
        elif config.num_keep == 4: 
            composes =  get_configs_4(list(nodes[i].outs))
        elif config.num_keep == 5: 
            composes =  get_configs_5(list(nodes[i].outs))
        elif config.num_keep == 6: 
            composes =  get_configs_6(list(nodes[i].outs))
        elif config.num_keep == 7: 
            composes =  get_configs_7(list(nodes[i].outs))
        elif config.num_keep == 8: 
            composes =  get_configs_8(list(nodes[i].outs))
        else:
            print('Error. choose a valid configs setting')
            sys.exit(0)
        outs_neighbors[i] = subset_complete_choose(nodes, i, composes, num_msg)

    # two hop peers
    if config.num_2_hop > 0:
        for u in update_nodes:
            subset_two_hop_choose(nodes, u, outs_neighbors)

    # three jop
    if config.num_3_hop > 0:
        for u in update_nodes:
            subset_three_hop_choose(nodes, u, outs_neighbors)

    # random peers
    if config.num_random > 0:
        for i in update_nodes:
            for _ in range(config.num_random):
                random_add(nodes, i, outs_neighbors[i])
    return outs_neighbors


    # all_nodes = sorted(list(outs_neighbors.keys()))

    # for k in all_nodes:
        # print(k, outs_neighbors[k])
    # visualizer.show(outs_neighbors)