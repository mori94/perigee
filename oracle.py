from collections import namedtuple
from collections import defaultdict 
import config

# messages that a node has information about other nodes, all two, three hops contains RecNote
PeersInfo = namedtuple('PeersInfo', ['one_hops', 'two_hops', 'three_hops']) 
RecNote = namedtuple('RecNote', ['rec', 'id']) # rec for recommender id, id is the node

class NetworkOracle:
    def __init__(self, is_dynamic, sybils, selectors):
        self.outs_keeps = {} # key is node id, value is a list of keep ids
        self.conn_2 = {} # key is node, it is confirmed direct connection
        self.conn_3 = {}
        self.is_dynamic = is_dynamic
        self.sybils = sybils
        self.selectors = selectors


    def update_1_hop_peers(self, u, peers):
        assert(u not in self.outs_keeps)
        self.outs_keeps[u] = list(peers)

    # used when peers set 2hop peers
    def update_2_hop_peers(self, u, peers):
        if u in self.conn_2:
            print(u, 'already in conn_2', self.conn_2)
            sys.exit(1)
        self.conn_2[u] = peers.copy()

    def update_3_hop_peers(self, u, peers):
        if u in self.conn_3:
            print(u, 'already in conn_3', self.conn_3)
            sys.exit(1)
        self.conn_3[u] = peers.copy()

    # get one hop peers for that node, which include keep and newly added 2info node
    def get_1_hop_peers(self, v):
        if not self.is_dynamic:
            if config.recommend_worst_attack:
                if v in self.sybils:
                    # give worst neighbors, TODO
                    assert(self.selectors[v].worst_compose != None)
                    return self.selectors[v].worst_compose.copy()
                else:
                    return self.outs_keeps[v].copy() # copy
            else:
                # honest case
                # print('honest', self.outs_keeps[v].copy())
                return self.outs_keeps[v].copy() # copy
        else:
            # print('is dynamic')
            return self.outs_keeps[v].copy() + self.conn_2[v].copy()

    # used to give nodes info
    def get_multi_hop_info(self, u):
        # all honest case
        one_hops = self.outs_keeps[u].copy()
        two_hops_map = {} # key is 1hop, values are 2hops
        three_hops_map = {} # key is 2hop, values 3hops
        for v in one_hops:
            peers = self.get_1_hop_peers(v)
            two_hops_map[v] = peers
        for v, two_hops in two_hops_map.items():
            
            for w in two_hops:
                if w not in three_hops_map:
                    peers = self.get_1_hop_peers(w)
                    three_hops_map[w] = peers
        return PeersInfo(one_hops, two_hops_map, three_hops_map)
