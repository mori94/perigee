import random
len_of_subround= 10                    # how may subround under local simulation
num_subround = len_of_subround

network_type = 'unhash'
method = 'subset'

# experiment config
use_sequential = False 
use_reduce_link = False
use_score_decay = False 

reduce_link_ratio = 0.05

# network config
num_node = 1000
out_lim = 8 
LIMIT = 40 

# node config
num_keep = 3
num_2_hop = 5
num_3_hop = 0
num_random = 0

is_sort_hop = False

assert(num_2_hop >= num_3_hop)

# history decay
old_weight = 0.7 #0.85
new_weight = 1 - old_weight

# graph info
data_index = 1
hash_file = "hash1.txt"
link_file = "weight1.txt" # "datacenter5_nodes4_inter200_intra10.txt" # "weight1.txt"
data_file = "data1.txt"

# broadcast detail
MISMATCH = 0.00001

# for vis
init_pos = {}
for i in range(num_node):
    init_pos[i] = (random.random(), random.random())




