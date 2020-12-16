#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
    print("need data method, use_node_hash[y/n], round list")
    sys.exit(0)

data_method = [sys.argv[1]]
use_node_hash = sys.argv[2] == 'y'

round_list = []
for i in range(3, len(sys.argv)):
    round_list.append(int(sys.argv[i]))
num_node = 20

def delaytopercenthash(hash_table,length_buff,DelayPercantage):
    LengthDict={}
    for i in range(len(length_buff)):
        length_buff[i]=length_buff[i]*1000+i
        LengthDict[str(length_buff[i])]=hash_table[i]
    sorted_length_buff=sorted(length_buff,reverse=True)
    hashcounter=0
    for i in range(len(length_buff)):
        hashcounter = hashcounter + LengthDict[str(sorted_length_buff[i])]
        # print(hashcounter,LengthDict[str(sorted_length_buff[i])],sorted_length_buff[i])
        if hashcounter>num_node*(DelayPercantage/100.0):
            return(int(sorted_length_buff[i]/1000))
        
def get_num_node():
    num_node = 0
    for datacount in [1]:
        for method in data_method: #,'localucb'
            for r in round_list: #,8,16,32,64,128
                if not use_node_hash:
                    filename="unhash_"+str(method)+"V"+str(datacount)+"Round"+str(r)+".txt"
                    with open(filename) as f:
                        for line in f:
                            num_node += 1
                    return num_node

    return -1


number = get_num_node()
print('num_node', number)

hash=np.zeros(number)

hash1=[]

file = open("../hash1.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(number):
    hash1.append(float(a[j]))
file.close()

# hash2=np.zeros(number)
# file = open("../hash2.txt",'r',errors='replace')
# line=file.readlines()
# a=line[0].split("  ")
# for j in range(number):
    # hash2[j]=float(a[j])
# file.close()

# hash3=np.zeros(number)
# file = open("../hash3.txt",'r',errors='replace')
# line=file.readlines()
# a=line[0].split("  ")
# for j in range(number):
    # hash3[j]=float(a[j])
# file.close()
'''
low1=np.zeros(number)
for i in range(number):
    low1[i]=hash1[i]
fileh=open(address+"node1.txt",'r',errors='replace')
line=fileh.readlines()
a=line[0].split("  ")
for i in range(len(a)-1):
    lowlatencynode = int(a[i])-1
    low1[int(lowlatencynode)] =   81*low1[int(lowlatencynode)]
low1=low1/9
fileh.close()

low2=np.zeros(number)
for i in range(number):
    low2[i]=hash2[i]
fileh=open(address+"node2.txt",'r',errors='replace')
line=fileh.readlines()
a=line[0].split("  ")
for i in range(len(a)-1):
    lowlatencynode = int(a[i])-1
    low2[int(lowlatencynode)] =   81*low2[int(lowlatencynode)]
low2=low2/9
fileh.close()

low3=np.zeros(number)
for i in range(number):
    low3[i]=hash3[i]
fileh=open(address+"node3.txt",'r',errors='replace')
line=fileh.readlines()
a=line[0].split("  ")
for i in range(len(a)-1):
    lowlatencynode = int(a[i])-1
    low3[int(lowlatencynode)] =   81*low3[int(lowlatencynode)]
low3=low3/9
fileh.close()

'''

for datacount in [1]:
    for method in data_method: #,'localucb'
        for r in round_list: #,8,16,32,64,128
            if not use_node_hash:
                print('not using node hash')
                filename="unhash_"+str(method)+"V"+str(datacount)+"Round"+str(r)+".txt"
                file = open(filename,'r',errors='replace')
                top101=np.zeros(number)
                mean1=np.zeros(number)
                buff=np.zeros(number)
                line=file.readlines()
                for i in range(number):
                    stripped_a = line[i].strip()
                    a=stripped_a.split("  ")
                    for j in range(number):
                        print(a[j])
                        buff[j]=int(float(a[j]))
                    buff=sorted(buff)
                    num_node =len(buff) 
                    top101[i]= buff[int(num_node*0.9)]
                    # mean1[i]= buff[int(test_num*0.5)]
                top101_0=sorted(top101)
                # mean1_0=sorted(mean1)
                file.close()
                outputfilename="result90"+filename
                fwl=open(outputfilename,'w')
                for i in range(num_node):
                    fwl.write(str(top101_0[i])+'  ')
                fwl.close()
            else:
                filename="unhash_"+str(method)+"V"+str(datacount)+"Round"+str(r)+".txt"
                file = open(filename,'r',errors='replace')
                top101=np.zeros(number)
                mean1=np.zeros(number)
                buff=np.zeros(number)
                line=file.readlines()
                for i in range(number):
                    a=line[i].split("  ")
                    for j in range(number):
                        buff[j]=int(float(a[j]))
                    hash_buff=locals()['hash'+str(datacount)]
                    mean1[i]= delaytopercenthash(hash_buff,buff,50)
                buff=np.zeros(number)
                for i in range(number):
                    a=line[i].split("  ")
                    for j in range(number):
                        buff[j]=int(float(a[j]))
                    hash_buff=locals()['hash'+str(datacount)]
                    top101[i]= delaytopercenthash(hash_buff,buff,90)
                top101_0=sorted(top101)
                mean1_0=sorted(mean1)
                num_node = len(top101_0)
                file.close()
                outputfilename="result90"+filename
                fwl=open(outputfilename,'w')
                for i in range(num_node):
                    fwl.write(str(top101_0[i])+'  ')
                fwl.close()
            '''
            outputfilename="result50"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(mean1_0[i])+'  ')
            fwl.close()
            '''
    '''
            filename="treehash_"+str(method)+"V"+str(datacount)+"Round"+str(r)+".txt"
            file = open(filename,'r',errors='replace')
            top101=np.zeros(number)
            mean1=np.zeros(number)
            buff=np.zeros(number)
            line=file.readlines()
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                hash_buff=locals()['hash'+str(datacount)]
                mean1[i]= delaytopercenthash(hash_buff,buff,50)
            buff=np.zeros(number)
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                hash_buff=locals()['hash'+str(datacount)]
                top101[i]= delaytopercenthash(hash_buff,buff,90)
            top101_0=sorted(top101)
            mean1_0=sorted(mean1)
            file.close()
            outputfilename="result90"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(top101_0[i])+'  ')
            fwl.close()
            outputfilename="result50"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(mean1_0[i])+'  ')
            fwl.close()
            filename="lowlatencyhash_"+str(method)+"V"+str(datacount)+"Round"+str(r)+".txt"
            file = open(filename,'r',errors='replace')
            top101=np.zeros(number)
            mean1=np.zeros(number)
            buff=np.zeros(number)
            line=file.readlines()
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                hash_buff=locals()['low'+str(datacount)]
                mean1[i]= delaytopercenthash(hash_buff,buff,50)
            buff=np.zeros(number)
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                hash_buff=locals()['low'+str(datacount)]
                top101[i]= delaytopercenthash(hash_buff,buff,90)
            top101_0=sorted(top101)
            mean1_0=sorted(mean1)
            file.close()
            outputfilename="result90"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(top101_0[i])+'  ')
            fwl.close()
            outputfilename="result50"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(mean1_0[i])+'  ')
            fwl.close()
    for method in ['localucb']:
        for r in [0,4,32,64]:
            filename="unhash_"+str(method)+"V"+str(datacount)+"Round"+str(r)+".txt"
            file = open(filename,'r',errors='replace')
            top101=np.zeros(number)
            mean1=np.zeros(number)
            buff=np.zeros(number)
            line=file.readlines()
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                buff=sorted(buff)
                top101[i]= buff[int(test_num*0.9)]
                mean1[i]= buff[int(test_num*0.5)]
            top101_0=sorted(top101)
            mean1_0=sorted(mean1)
            file.close()
            outputfilename="result90"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(top101_0[i])+'  ')
            fwl.close()
            outputfilename="result50"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(mean1_0[i])+'  ')
            fwl.close()
            
            filename="hash_"+str(method)+"V"+str(datacount)+"Round"+str(r)+".txt"
            file = open(filename,'r',errors='replace')
            top101=np.zeros(number)
            mean1=np.zeros(number)
            buff=np.zeros(number)
            line=file.readlines()
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                hash_buff=locals()['hash'+str(datacount)]
                mean1[i]= delaytopercenthash(hash_buff,buff,50)
            buff=np.zeros(number)
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                hash_buff=locals()['hash'+str(datacount)]
                top101[i]= delaytopercenthash(hash_buff,buff,90)
            top101_0=sorted(top101)
            mean1_0=sorted(mean1)
            file.close()
            outputfilename="result90"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(top101_0[i])+'  ')
            fwl.close()
            outputfilename="result50"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(mean1_0[i])+'  ')
            fwl.close()
            filename="treehash_"+str(method)+"V"+str(datacount)+"Round"+str(r)+".txt"
            file = open(filename,'r',errors='replace')
            top101=np.zeros(number)
            mean1=np.zeros(number)
            buff=np.zeros(number)
            line=file.readlines()
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                hash_buff=locals()['hash'+str(datacount)]
                mean1[i]= delaytopercenthash(hash_buff,buff,50)
            buff=np.zeros(number)
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                hash_buff=locals()['hash'+str(datacount)]
                top101[i]= delaytopercenthash(hash_buff,buff,90)
            top101_0=sorted(top101)
            mean1_0=sorted(mean1)
            file.close()
            outputfilename="result90"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(top101_0[i])+'  ')
            fwl.close()
            outputfilename="result50"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(mean1_0[i])+'  ')
            fwl.close()
            filename="lowlatencyhash_"+str(method)+"V"+str(datacount)+"Round"+str(r)+".txt"
            file = open(filename,'r',errors='replace')
            top101=np.zeros(number)
            mean1=np.zeros(number)
            buff=np.zeros(number)
            line=file.readlines()
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                hash_buff=locals()['low'+str(datacount)]
                mean1[i]= delaytopercenthash(hash_buff,buff,50)
            buff=np.zeros(number)
            for i in range(number):
                a=line[i].split("  ")
                for j in range(number):
                    buff[j]=int(float(a[j]))
                hash_buff=locals()['low'+str(datacount)]
                top101[i]= delaytopercenthash(hash_buff,buff,90)
            top101_0=sorted(top101)
            mean1_0=sorted(mean1)
            file.close()
            outputfilename="result90"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(top101_0[i])+'  ')
            fwl.close()
            outputfilename="result50"+filename
            fwl=open(outputfilename,'a')
            for i in range(test_num):
                fwl.write(str(mean1_0[i])+'  ')
            fwl.close()


'''
