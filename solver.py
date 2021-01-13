import sys
import numpy as np
from numpy import linalg as LA
from scipy.sparse.linalg import svds

tol_obj = 1e-4
tol_normA = 1e-2
tol_normB = 1e-2
num_alt = 100
max_step = 50

# A is W, B is H, k is rank which is L, X is observation
def run_pgd_nmf(L, X):
    # init A_init, B_init with svd
    A_init, B_init = init_matrix(X, L)
    A_est, B_est = alternate_minimize(A_init, B_init, X, L)
    return A_est, B_est

# mask out non date entry
def alternate_minimize(A_init, B_init, X, L):
    A = A_init
    B = B_init
    I = X > 0 
    P = (A.dot(B) - X) * I 
    prev_opt = 9999
    for _ in range(num_alt):
        norm_delta_A = 9999
        step = 0
        # update A
        while norm_delta_A>tol_normA and step < max_step:
            prev_A = np.copy(A)
            grad_A = P.dot(B.T)
            t_A = 0.25 * LA.norm(grad_A, 'fro')**2 / LA.norm( grad_A.dot(B) * I, 'fro')**2

            # update
            A_tilde = A - t_A * grad_A
            A_tilde[A_tilde<0] = 0
            A_tilde[A_tilde>1] = 1
            A = A_tilde
            P = (A.dot(B) - X) * I 
            norm_delta_A = LA.norm(A-prev_A, 'fro')
            step += 1

        # update B
        norm_delta_B = 9999
        step = 0
        while norm_delta_B>tol_normB and step < max_step:
            prev_B = np.copy(B)
            grad_B = (A.T).dot(P)
            t_B = 0.25 * LA.norm(grad_B, 'fro')**2 / LA.norm( A.dot(grad_B) * I, 'fro')**2
            B_tilde = B - t_B * grad_B
            B[:L, :] = B_tilde[:L, :]
            P = (A.dot(B) - X) * I
            step += 1
            norm_delta_B = LA.norm(B-prev_B, 'fro')

        
        opt = 0.5 * LA.norm(P, 'fro')
        if prev_opt - opt < tol_obj:
            print('opt', prev_opt - opt)
            break
        prev_opt = opt

    return A, B

# init A, B, X is observation matrix
def init_matrix(X, L):
    A, _, B = svds(X, L)
    I = np.sign(A.sum(axis=0)) # 2 * int(A.sum(axis=0) > 0) - 1
    A = A.dot(np.diag(I))
    B = np.transpose((B.T).dot(np.diag(I)))
    return A, B



