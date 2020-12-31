#!/usr/bin/env python
import numpy as np
import sys
import random 

seed_num = int(sys.argv[1])
np.random.seed(seed_num)
random.seed(seed_num)

import time
import config
import initnetwork
import readfiles

from experiment import Experiment
if len(sys.argv) < 4:
    print('Need arguments.')
    print('./testbed seed[int] output_dir[str] use_node_hash[y/n] rounds[intList]')
    print('./testbed 1 n 0 1 2 3 4 5')
    sys.exit()

data_path = sys.argv[2]
use_node_hash = sys.argv[3]=='y'
record_epochs = [int(i) for i in sys.argv[4:]]
max_epoch = max(record_epochs) +1


print('Setup Graph')
[ G, node_delay, 
  node_hash, link_delay, 
  neighbor_set, IncomingLimit, 
  outs_neighbors, in_lims, 
  bandwidth] = initnetwork.GenerateInitialNetwork(
        config.network_type,
        config.num_node)

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

start = time.time()

perigee = Experiment(
    node_hash,
    link_delay,
    node_delay,
    config.num_node,
    config.in_lim,
    config.out_lim, 
    data_path,
    config.num_adv
    )
perigee.init_graph(outs_neighbors)
perigee.start(max_epoch, record_epochs)




