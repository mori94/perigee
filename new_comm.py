import sys
from config import MISMATCH
import numpy as np
import random 

def get_broadcast_node(node_hash):
    hash_sum = np.sum(node_hash)
    r = random.random() * hash_sum
    for u, hash_value in enumerate(node_hash):
        if r > hash_value:
            r -= hash_value
        else:
            return u
    return len(node_hash) - 1

def print_debug(i, node, v, peer, ld):
    if node.views[v] <  -1 * MISMATCH:
        print(node.views[v] )
        print('node',i, 'from', node.from_whom, 'recv_time', node.recv_time)
        print('peer', v, 'recv_time', peer.recv_time)
        print('ld[peer][node]', ld[v][i])
        print('ld[node][peer]', ld[i][v])
        print('node', node.node_delay)
        print('peer', peer.node_delay)
        print("peer.recv_time", peer.recv_time)
        print("sum", peer.recv_time + node.node_delay + ld[v][i])
        print("node.recv_time", node.recv_time)
        print()
        sys.exit(1)


def fuzzy_greater(a, b, mismatch):
    if a - b > mismatch:
        return True 
    else:
        return False 

# ld is link delau, bd is broadcasting node, nh is node_hash
def broadcast_msg(u, nodes, ld, nh):
    # precondition
    for i, node in nodes.items():
        node.received = False
        node.recv_time = 0
        node.views = {}
        node.from_whom = None

    nodes[u].received = True
    nodes[u].recv_time = 0
    nodes[u].from_whom = u

    broad_nodes = [u]
    while len(broad_nodes) > 0:
        u = broad_nodes.pop(0)
        node = nodes[u]
        assert(node.received) # a node must have recved to broadcast
        is_updated = False
        for v in node.get_peers():
            peer = nodes[v]
            if not peer.received:
                # if dst has not received it
                peer.recv_time = node.recv_time + ld[u][v] + peer.node_delay 
                peer.received = True
                peer.from_whom = u
                broad_nodes.append(v)
            else:
                t = peer.recv_time + ld[v][u] + node.node_delay
                if fuzzy_greater(node.recv_time, t, MISMATCH):
                    node.recv_time = t
                    node.from_whom = v
                    is_updated = True
        if is_updated:
            for v in node.get_peers():
                peer = nodes[v]
                if fuzzy_greater(
                    peer.recv_time, 
                    node.recv_time + ld[u][v] + peer.node_delay,
                    MISMATCH
                ):
                    broad_nodes.insert(0, v)

    # find relative times for each node
    for i, node in nodes.items():
        for v in node.get_peers():
            peer = nodes[v]
            node.views[v] = peer.recv_time + node.node_delay + ld[v][i] - node.recv_time
            node.views_hist[v].append(node.views[v])
            # safety check
            print_debug(i, node, v, peer, ld)

            # make sure the node actually transmit to me
            # if node.views[v] >= ld[i][v] + ld[v][i] + node.node_delay + peer.node_delay:
                # node.views[v] = unlimit
