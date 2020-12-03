import sys

def print_debug(i, node, v, peer):
    if round(node.views[v], 5) < 0:
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
        sys.exit(0)

# ld is link delau, bd is broadcasting node
def broadcast_msg(u, nodes, ld):
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
                if round(node.recv_time, 5) > round(t, 5):
                    node.recv_time = t
                    node.from_whom = v
                    is_updated = True
        if is_updated:
            for v in node.get_peers():
                peer = nodes[v]
                if (round(peer.recv_time, 5) > 
                        round(node.recv_time + ld[u][v] + peer.node_delay, 5)):
                    broad_nodes.insert(0, v)

    # find relative times for each node
    for i, node in nodes.items():
        for v in node.get_peers():
            peer = nodes[v]
            node.views[v] = peer.recv_time + node.node_delay + ld[v][i] - node.recv_time
            node.views_hist[v].append(node.views[v])
            # safety check
            print_debug(i, node, v, peer)

            # make sure the node actually transmit to me
            # if node.views[v] >= ld[i][v] + ld[v][i] + node.node_delay + peer.node_delay:
                # node.views[v] = unlimit
