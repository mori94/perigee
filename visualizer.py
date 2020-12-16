import networkx as nx
import matplotlib.pyplot as plt
from config import init_pos
def show(out_neighbors):
    G = nx.Graph()
    for k in out_neighbors.keys():
        G.add_node(k)
    for k, peers in out_neighbors.items():
        for p in peers:
            G.add_edge(k, p)
    nx.draw(G, pos=init_pos, with_labels=True)
    plt.show()
