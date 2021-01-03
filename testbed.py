#!/usr/bin/env python
import numpy as np
import sys
import random 

seed_num = int(sys.argv[2])
np.random.seed(seed_num)
random.seed(seed_num)

import time
import config
import initnetwork
import readfiles

from experiment import Experiment
if len(sys.argv) < 4:
    print('Need arguments.')
    print('./testbed subcommand[run/complete_graph] seed[int] output_dir[str] use_node_hash[y/n] rounds[intList]')
    print('./testbed run 1 n 0 1 2 3 4 5')
    print('./testbed complete_graph 1 n 0 1 2 3 4 5')
    sys.exit()

subcommand = sys.argv[1]
data_path = sys.argv[3]
out_lim = int(sys.argv[4])
use_node_hash = sys.argv[5]=='y'

record_epochs = [int(i) for i in sys.argv[6:]]
max_epoch = max(record_epochs) +1

print('Setup Graph')
[ node_delay, 
  node_hash, link_delay, 
  neighbor_set, IncomingLimit, 
  outs_neighbors, in_lims, 
  bandwidth] = initnetwork.GenerateInitialNetwork(
        config.network_type,
        config.num_node, 
        subcommand,
        out_lim)

if config.use_reduce_link:
    print('Use reduced link latency')
    initnetwork.reduce_link_latency(config.num_node, int(0.2*config.num_node), link_delay)
else:
    print('Not use reduced link latency')

# print(node_hash)
# for i in range(len(link_delay)):
    # print(link_delay[i])
# for i in range(len(outs_neighbors)):
    # print(i, outs_neighbors[i])

if not use_node_hash:
    print('Not Use asymmetric node hash')
    node_hash = None 
else:
    print('Use asymmetric node hash')


if subcommand == 'run':
    start = time.time()
    adv_nodes = [i for i in range(config.num_adv)]
    perigee = Experiment(
        node_hash,
        link_delay,
        node_delay,
        config.num_node,
        config.in_lim,
        out_lim, 
        data_path,
        adv_nodes
        )
    perigee.init_graph(outs_neighbors)
    perigee.start(max_epoch, record_epochs)
elif subcommand == 'complete_graph':
    if out_lim != config.num_node-1:
        print('Error. A complete graph need correct out lim')
        sys.exit(1)
   
    outs_neighbors = {}
    for i in range(config.num_node):
        connections = []
        for j in range(config.num_node):
            if i != j:
                connections.append(j)
        outs_neighbors[i] = connections

    print('setup experiment')
    perigee = Experiment(
            node_hash,
            link_delay,
            node_delay,
            config.num_node,
            config.in_lim,
            out_lim, 
            data_path,
            [] 
            )
    print('init graph')   
    perigee.init_graph(outs_neighbors)
    print('start')
    perigee.start_complete_graph(max_epoch, record_epochs)
    # perigee.analytical_complete_graph()
else:
    print('Error. Unknown subcommand')
    sys.exit(1)



