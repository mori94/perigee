#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import data
test_num = 1000
len_of_neigh=8
len_of_test=4
#####

#####
def wei(delay, G, Ni, Nj):
    if (int(Ni)==int(Nj)):
        return(0)
    Cluster1=G.node[Ni]['cluster']
    Cluster2=G.node[Nj]['cluster']
    latency_array=[]
    if Cluster1=="North America":
        if Cluster2=="North America":
            latency_array=data.GEO_NA_NA_LATENCIES
        elif Cluster2=="Europe":
            latency_array=data.GEO_NA_EU_LATENCIES
        elif Cluster2=="Oceania":
            latency_array=data.GEO_NA_OC_LATENCIES
        elif Cluster2=="Africa":
            latency_array=data.GEO_NA_AF_LATENCIES
        elif Cluster2=="South America":
            latency_array=data.GEO_NA_SA_LATENCIES
        elif Cluster2=="China":
            latency_array=data.GEO_NA_CN_LATENCIES
        elif Cluster2=="Asia":
            latency_array=data.GEO_NA_AS_LATENCIES
    elif Cluster1=="Europe":
        if Cluster2=="North America":
            latency_array=data.GEO_NA_EU_LATENCIES
        elif Cluster2=="Europe":
            latency_array=data.GEO_EU_EU_LATENCIES
        elif Cluster2=="Oceania":
            latency_array=data.GEO_EU_OC_LATENCIES
        elif Cluster2=="Africa":
            latency_array=data.GEO_EU_AF_LATENCIES
        elif Cluster2=="South America":
            latency_array=data.GEO_EU_SA_LATENCIES
        elif Cluster2=="China":
            latency_array=data.GEO_EU_CN_LATENCIES
        elif Cluster2=="Asia":
            latency_array=data.GEO_EU_AS_LATENCIES
    elif Cluster1=="Oceania":
        if Cluster2=="North America":
            latency_array=data.GEO_NA_OC_LATENCIES
        elif Cluster2=="Europe":
            latency_array=data.GEO_EU_OC_LATENCIES
        elif Cluster2=="Oceania":
            latency_array=data.GEO_OC_OC_LATENCIES
        elif Cluster2=="Africa":
            latency_array=data.GEO_OC_AF_LATENCIES
        elif Cluster2=="South America":
            latency_array=data.GEO_OC_SA_LATENCIES
        elif Cluster2=="China":
            latency_array=data.GEO_OC_CN_LATENCIES
        elif Cluster2=="Asia":
            latency_array=data.GEO_AS_OC_LATENCIES
    elif Cluster1=="Africa":
        if Cluster2=="North America":
            latency_array=data.GEO_NA_AF_LATENCIES
        elif Cluster2=="Europe":
            latency_array=data.GEO_EU_AF_LATENCIES
        elif Cluster2=="Oceania":
            latency_array=data.GEO_OC_AF_LATENCIES
        elif Cluster2=="Africa":
            latency_array=data.GEO_AF_AF_LATENCIES
        elif Cluster2=="South America":
            latency_array=data.GEO_SA_AF_LATENCIES
        elif Cluster2=="China":
            latency_array=data.GEO_AF_CN_LATENCIES
        elif Cluster2=="Asia":
            latency_array=data.GEO_AS_AF_LATENCIES
    elif Cluster1=="South America":
        if Cluster2=="North America":
            latency_array=data.GEO_NA_SA_LATENCIES
        elif Cluster2=="Europe":
            latency_array=data.GEO_EU_AS_LATENCIES
        elif Cluster2=="Oceania":
            latency_array=data.GEO_OC_SA_LATENCIES
        elif Cluster2=="Africa":
            latency_array=data.GEO_SA_AF_LATENCIES
        elif Cluster2=="South America":
            latency_array=data.GEO_SA_SA_LATENCIES
        elif Cluster2=="China":
            latency_array=data.GEO_SA_CN_LATENCIES
        elif Cluster2=="Asia":
            latency_array=data.GEO_AS_SA_LATENCIES
    elif Cluster1=="China":
        if Cluster2=="North America":
            latency_array=data.GEO_NA_CN_LATENCIES
        elif Cluster2=="Europe":
            latency_array=data.GEO_EU_CN_LATENCIES
        elif Cluster2=="Oceania":
            latency_array=data.GEO_OC_CN_LATENCIES
        elif Cluster2=="Africa":
            latency_array=data.GEO_AF_CN_LATENCIES
        elif Cluster2=="South America":
            latency_array=data.GEO_SA_CN_LATENCIES
        elif Cluster2=="China":
            latency_array=data.GEO_CN_CN_LATENCIES
        elif Cluster2=="Asia":
            latency_array=data.GEO_AS_CN_LATENCIES
    elif Cluster1=="Asia":
        if Cluster2=="North America":
            latency_array=data.GEO_NA_AS_LATENCIES
        elif Cluster2=="Europe":
            latency_array=data.GEO_EU_AS_LATENCIES
        elif Cluster2=="Oceania":
            latency_array=data.GEO_AS_OC_LATENCIES
        elif Cluster2=="Africa":
            latency_array=data.GEO_AS_AF_LATENCIES
        elif Cluster2=="South America":
            latency_array=data.GEO_AS_SA_LATENCIES
        elif Cluster2=="China":
            latency_array=data.GEO_AS_CN_LATENCIES
        elif Cluster2=="Asia":
            latency_array=data.GEO_AS_AS_LATENCIES
    sum_weight=sum(latency_array)
    k=random.randint(1,sum_weight)
    current_weight=0
    for i in range(200):
        current_weight=current_weight+latency_array[i]
        if current_weight>=k:
            latency=data.GEO_INTERVALS[i]
            return(latency+delay[int(Ni)]/2+delay[int(Nj)]/2)
###################
