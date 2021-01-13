import sys
import numpy as np
import copy
from sklearn.decomposition import NMF
import time
import config
import solver

class Optimizer:
    def __init__(self, node_id, num_node, num_region, window):
        self.table = [] # raw relative time records, each element is a dict:peer -> time list
        
        self.id = node_id
        self.N = num_node
        self.L = num_region # region = num out degree
        self.T = window # time window that discard old time data
        self.X = None #np.zeros(self.T, self.N) # array of array, col is num node, row is time
        self.window = window

    def append_time(self, slot):
        # self.table.append(copy.deepcopy(time))
        # for k, v in slot.items():
            # if v[0]< 0:

                # print('v', v)
                # sys.exit(1)

            # if rel_time < MISMATCH:
                # rel_time = 0
        self.table.append(list(slot.items()))

    def construct_table(self):
        X = np.zeros((self.window, self.N)) 
        i = 0 # row

        max_time = 0 
        for slot in self.table[-self.window:]:
            for p, t in slot:
                if t[0] < 0:
                    print('time', t)
                    sys.exit(1)
                X[i, p] = t[0] # t is a single element list, if num_msg is 1
                if t[0] > max_time:
                    max_time = t[0]
            i += 1
        X = max_time - X
        return X

    # return matrix B, i.e. region-node matrix that containing real value score
    def matrix_factor(self):
        # print('matrix factor')
        # sample time from each table, to assemble the matrix X
        start = time.time()
        X = self.construct_table()

        # sklearn nmp 
        # model = NMF(n_components=self.L, init='nndsvd', random_state=0, max_iter=config.max_iter)
        # A = model.fit_transform(X)
        # B = model.components_
        A, B = solver.run_pgd_nmf(self.L, X)

        # then use best neighbor methods to select get neighbors
        out_conns = self.choose_best_neighbor(B)
        return out_conns


    # takes best neighbors from matrix B, currently using argmin, later using bandit
    def choose_best_neighbor(self, B):
        L_neighbors = np.argmin(B, axis=1)
        #for i in range(len(L_neighbors)):
        #    print(list(np.round(B[i,:],2)))
        #print('L_neighbors', L_neighbors)
        outs_conn = set(L_neighbors)
        return outs_conn

