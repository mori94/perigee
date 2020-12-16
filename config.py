import random
len_of_subround= 200                    # how may subround under local simulation
num_subround = len_of_subround

network_type = 'unhash'
method = 'subset'

num_node     = 20                   # graph size
out_lim = 4 # 8

# used for 2 hop
num_keep = 2
num_2_hop = 0
num_3_hop = 0
num_random = 2

data_index = 1

reduce_link_ratio = 0.05

use_hash = False
hash_file = "hash1.txt"
link_file = "weight1.txt"
data_file = "data1.txt"

LIMIT = 10 # 40 
 
MISMATCH = 0.00001

# for vis
init_pos = {}
for i in range(num_node):
    init_pos[i] = (random.random(), random.random())
