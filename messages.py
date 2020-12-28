from collections import namedtuple

# messages that a node has information about other nodes
PeersInfo = namedtuple('PeersInfo', ['one_hops', 'two_hops'])
