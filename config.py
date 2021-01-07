# reduced link  
use_reduce_link = False 
reduce_link_ratio = 0.1

# load conns state from prev experiment 
is_load_conn = False 
conn_path = 'inputs/conn.txt'

# network config
num_node = 1000
num_adv = 0             # out of num node
adv_hash = 0.1          # percentage adversarial power
in_lim = 40 
num_msg = 20 

# node config
num_keep = 3
num_2_hop = 3
num_3_hop = 0
num_random = 2

# how to choose 1 hops
both_in_and_out = True 

# how to choose two,three hops
is_sort_score = False   
is_favor_new = False 
is_per_recommeder_select = False 
is_rank_occurance = True 

# history decay
use_score_decay = False 
old_weight = 0.75 
new_weight = 1 - old_weight

# attack
worst_conn_attack = False 
recommend_worst_attack = False 
sybil_update_priority = False 

# peers info. If dynamic, some peers in the loop may already 
# have num_keep+ peers, while early node only knows num_keep 
# peers from other nodes.
is_dynamic = False #True

# num thread for heavy duty, not useful after experiment
num_thread = 1

network_type = 'unhash'
method = 'subset'
use_sequential = False 

# graph info
data_index = 1
hash_file = "inputs/hash1.txt"
link_file = "inputs/weight1.txt" # "datacenter5_nodes4_inter200_intra10.txt" # "weight1.txt"
data_file = "inputs/data1.txt"
data_dir = "data"

# broadcast detail
MISMATCH = 0.00001
