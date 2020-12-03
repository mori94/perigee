from config import *
from perigeeNode import *
import new_comm
import time
def add_preference(node, times):
    new_times = []
    for dst, t in times:
        if dst in node.outs:
            new_times.append((dst, t+0.001)) 
        else:
            new_times.append((dst, t+0.01))
    return new_times

def vanilla_new(nodes, LinkDelay, num_new, num_msg):
    # precondition
    num_node = len(nodes)
    for u, node in nodes.items():
        # node.views_hist.clear()
        # node.candidates.clear()
        for _ in range(num_new):
            v = np.random.randint(num_node)
            # get new nodes
            while not (node.is_out_addable(v) and nodes[v].is_in_addable(u)):
                v = np.random.randint(num_node)
            nodes[u].add_out(v)
            nodes[v].add_in(u)

    # each subround is a msg
    records = {} # key is node pair, value is a list of time for all sub round
    for k in range(num_msg):
        print("msg", k)
        broad_node = np.random.randint(num_node)
        start = time.time()
        new_comm.broadcast_msg(broad_node, nodes, LinkDelay)
        # print('broadcast finish', time.time() - start)
        for i, node in nodes.items():
            for peer, t in node.views.items():
                pair = (i, peer)
                if pair not in records:
                    records[pair] = [t]
                else:
                    records[pair].append(t)
    outs_neighbors = {}
    # for i, node in nodes.items():
        # outs = node.one_hop_vanilla()
        # outs_neighbors[i] = outs
    outs_neighbors = old_select(nodes, records)
    # outs_neighbors = two_hop_select(nodes, records, 3)
    update_conn_for_all_nodes(nodes, outs_neighbors)
    return outs_neighbors



def old_select(nodes, records):
    peers_p90 = {} # key is node is, value is (peer id, p90 time)
    for pair, time_list in records.items():
        src, dst = pair
        sorted_times = sorted(time_list)
        time_p90 = sorted_times[int(num_subround*9/10)] # floor
        if src not in peers_p90:
            peers_p90[src] = [(dst, time_p90)]
        else:
            peers_p90[src].append((dst, time_p90))

    outs = {}
    for i, times in peers_p90.items():
        new_times = times # add_preference(nodes[i], times)
        sorted_time = sorted(new_times, key=lambda x: x[1])
        num_out = nodes[i].out_limit
        candidates = sorted_time[:num_out]
        outs[i] = [t for t, s in candidates]


    return outs


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

def is_in_addable(node, u):
    # if len(node.ins) + 1 > node.in_limit:
    #     return False
    # if u in node.outs:
    #    return False
    if u in node.ins:
       return False
    return True

def two_hop_select(nodes, records, best_x):
    out_neighs = old_select(nodes, records)
    updated_neighs = {}

    all_nodes = [i for i in range(len(nodes))]
    random.shuffle(all_nodes)
    for i in all_nodes:
        node = nodes[i]
        best_peers = out_neighs[i][:best_x]
        selected = [] 
        for s in best_peers:
            if nodes[s].num_in_request < nodes[s].in_limit:
                selected.append(s)
                nodes[s].num_in_request += 1

        for u in best_peers:
            peer = nodes[u]
            # choose best of the best peers
            c = np.random.randint(best_x)
            s = out_neighs[u][c]
            trial = 0
            is_found = True
            while not (is_out_addable(nodes[i], selected, s) and 
                       is_in_addable(nodes[s], i) and
                       nodes[s].num_in_request < nodes[s].in_lim):
                c = np.random.randint(best_x)
                s = out_neighs[u][c]
                trial += 1
                if trial > 10:
                    is_found = False
                    break
            if is_found:
                selected.append(s)
                nodes[s].num_in_request += 1
        for _ in range(node.out_limit - len(selected)):
            s = np.random.randint(len(nodes))
            while not (is_out_addable(nodes[i], selected, s) and 
                       is_in_addable(nodes[s], i) and 
                       nodes[s].num_in_request < nodes[s].in_lim):
                s = np.random.randint(len(nodes))
            selected.append(s)
            nodes[s].num_in_request += 1
        updated_neighs[i] = selected
    return updated_neighs
