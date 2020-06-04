#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
test_num = 1000

parent=[0]
children=[(i+1) for i in range(99)]

TreeFileName="tree"+str(1)+".txt"
fwt=open(TreeFileName,'a')
for i in range(99):
    SelectedChildren=random.sample(children, 1)
    SelectedParent=random.sample(parent,1)
    fwt.write(str(SelectedChildren[0])+'  '+str(SelectedParent[0])+'\n')
    children.remove(SelectedChildren[0])
    parent=parent+[SelectedChildren[0]]
fwt.close()

parent=[0]
children=[(i+1) for i in range(99)]

TreeFileName="tree"+str(2)+".txt"
fwt=open(TreeFileName,'a')
for i in range(99):
    SelectedChildren=random.sample(children, 1)
    SelectedParent=random.sample(parent,1)
    fwt.write(str(SelectedChildren[0])+'  '+str(SelectedParent[0])+'\n')
    children.remove(SelectedChildren[0])
    parent=parent+[SelectedChildren[0]]
fwt.close()

parent=[0]
children=[(i+1) for i in range(99)]

TreeFileName="tree"+str(3)+".txt"
fwt=open(TreeFileName,'a')
for i in range(99):
    SelectedChildren=random.sample(children, 1)
    SelectedParent=random.sample(parent,1)
    fwt.write(str(SelectedChildren[0])+'  '+str(SelectedParent[0])+'\n')
    children.remove(SelectedChildren[0])
    parent=parent+[SelectedChildren[0]]
fwt.close()
