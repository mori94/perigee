#!/usr/bin/env python
import sys
import json
from collections import namedtuple
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
Node = namedtuple('Node', ['id', 'center_id'])

# complete bipartite connect all of them
def connect_centers(src_c, tgt_c, lat, centers, G):
    src_nodes = centers[src_c]
    tgt_nodes = centers[tgt_c]
    for u in src_nodes:
        for v in tgt_nodes:
            G.add_edge(u, v, lat = lat)

def write_adj_matrix(G, num_node, outfile):
    with open(outfile, 'w') as w:
        for i in range(num_node):
            node_dist = nx.shortest_path_length(G, source=i, weight = 'lat')
            for j in range(num_node):
                w.write(str(float(node_dist[j])) + "  ")
            w.write("\n")

if len(sys.argv) < 5:
    print('Error need more args')
    print('./gen-datacenter.py num_center[int] num_node_per_center[int] lat_among_center[float] lat_in_center[int]')
    sys.exit(0)

num_center = int(sys.argv[1])
num_node_per_center = int(sys.argv[2])
lat_among_centers = float(sys.argv[3])
lat_in_center = float(sys.argv[4])
outfile = sys.argv[5]

num_node = num_center * num_node_per_center
centers = defaultdict(list)
for i in range(num_node):
    center_id = int(i/num_node_per_center)
    centers[center_id].append(i)

G = nx.Graph()
# build intracenter lat
for cid, cluster in centers.items():
    num = len(cluster)
    for i in range(0, num):
        for j in range(i+1, num):
            G.add_edge(cluster[i], cluster[j], lat = lat_in_center)

assert(num_center == len(centers))
center_list = list(centers.keys())
# build intercenter lat
for i in range(0, num_center):
    src_center = center_list[i]
    for j in range(i+1, num_center):
        tgt_center = center_list[j] 
        connect_centers(src_center, tgt_center, lat_among_centers, centers, G)

#pos = nx.kamada_kawai_layout(G)
#nx.draw(G, pos=pos, with_labels=True)
#edge_labels = nx.get_edge_attributes(G,'lat')
#nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
#plt.show()

write_adj_matrix(G, num_node, outfile)
