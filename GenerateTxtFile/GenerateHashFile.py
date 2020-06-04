#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
test_num = 1000


hash=[np.random.exponential(1)  for i in range(test_num)]

fw=open('hash1.txt','a')
s=test_num/sum(hash)
for i in range(test_num):
    hash[i]=hash[i]*s
    fw.write(str(hash[i])+'  ')
fw.close()
print(sum(hash))
hash=[np.random.exponential(1)  for i in range(test_num)]

fw=open('hash2.txt','a')
s=test_num/sum(hash)
for i in range(test_num):
    hash[i]=hash[i]*s
    fw.write(str(hash[i])+'  ')
fw.close()
print(sum(hash))
hash=[np.random.exponential(1)  for i in range(test_num)]

fw=open('hash3.txt','a')
s=test_num/sum(hash)
for i in range(test_num):
    hash[i]=hash[i]*s
    fw.write(str(hash[i])+'  ')
fw.close()
print(sum(hash))
'''
hash=[np.random.pareto(1.1, 1)  for i in range(test_num)]

fw=open('hash4.txt','a')
s=test_num/sum(hash)
for i in range(test_num):
    hash[i]=hash[i]*s
    fw.write(str(hash[i])+'  ')
fw.close()
print(sum(hash))
hash=[np.random.pareto(1.1, 1)  for i in range(test_num)]

fw=open('hash5.txt','a')
s=test_num/sum(hash)
for i in range(test_num):
    hash[i]=hash[i]*s
    fw.write(str(hash[i])+'  ')
fw.close()
print(sum(hash))
hash=[np.random.pareto(1.1, 1)  for i in range(test_num)]

fw=open('hash6.txt','a')
s=test_num/sum(hash)
for i in range(test_num):
    hash[i]=hash[i]*s
    fw.write(str(hash[i])+'  ')
fw.close()
print(sum(hash))
'''
