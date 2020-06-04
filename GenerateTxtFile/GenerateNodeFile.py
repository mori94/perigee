#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
test_num = 1000


hash=random.sample(range(0,test_num),100)

fw=open('activenode1.txt','a')
for i in range(100):
    fw.write(str(hash[i])+'  ')
fw.close()

hash=random.sample(range(0,test_num),100)

fw=open('activenode2.txt','a')
for i in range(100):
    fw.write(str(hash[i])+'  ')
fw.close()

hash=random.sample(range(0,test_num),100)

fw=open('activenode3.txt','a')
for i in range(100):
    fw.write(str(hash[i])+'  ')
fw.close()


