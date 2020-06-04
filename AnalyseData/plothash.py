#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
test_num=100
x=range(test_num)
plt.style.use('ggplot')
addr="/Users/maoyifan/Desktop/Result/rereredo/bands/redoband420/"
#addr="/home/yifan/bands/redoband410/"
buff=np.zeros(test_num)
plt.rcParams['savefig.dpi'] = 300 #图片像素
plt.rcParams['figure.dpi'] = 300 #分辨率
plt.figure(figsize=(10,8))

file = open(addr+"result90hash_global8+4V1Round0.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_0=sorted(buff)
file.close()

file = open(addr+"result90hash_global8+4V1Round4.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_4=sorted(buff)
file.close()

file = open(addr+"result90hash_global8+4V1Round16.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_8=sorted(buff)
file.close()

file = open(addr+"result90hash_global8+4V1Round32.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_16=sorted(buff)
file.close()

file = open(addr+"result90hash_global8+4V1Round64.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_64=sorted(buff)
file.close()

file = open(addr+"result90hash_global8+4V1Round128.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_128=sorted(buff)
file.close()
'''
file = open("result90_hash_ideal3.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_ideal=sorted(buff)
file.close()
'''

file = open(addr+"result90hash_global8+2V2Round0.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_0=sorted(buff)
file.close()


file = open(addr+"result90hash_global8+2V2Round4.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_4=sorted(buff)
file.close()

file = open(addr+"result90hash_global8+2V2Round16.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_8=sorted(buff)
file.close()

file = open(addr+"result90hash_global8+2V2Round32.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_16=sorted(buff)
file.close()

file = open(addr+"result90hash_global8+2V2Round64.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_64=sorted(buff)
file.close()

file = open(addr+"result90hash_global8+2V2Round128.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_128=sorted(buff)
file.close()
'''
file = open("result50_hash_ideal3.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_ideal=sorted(buff)
file.close()
'''
###

plt.subplot(2,3,4)
plt.xlabel('Delay to 50%')
x=range(test_num)

upperline_0=np.zeros(test_num)
lowerline_0=np.zeros(test_num)
meanline_0=np.zeros(test_num)
for i in range(test_num):
    meanline_0[i]=mean1_0[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )


upperline_4=np.zeros(test_num)
lowerline_4=np.zeros(test_num)
meanline_4=np.zeros(test_num)
for i in range(test_num):
    meanline_4[i]=mean1_4[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='orange',label="Round 4", linestyle=":" )


upperline_8=np.zeros(test_num)
lowerline_8=np.zeros(test_num)
meanline_8=np.zeros(test_num)
for i in range(test_num):
    meanline_8[i]=mean1_8[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_8[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_8,color='yellow',label="Round 8", linestyle=":" )

upperline_16=np.zeros(test_num)
lowerline_16=np.zeros(test_num)
meanline_16=np.zeros(test_num)
for i in range(test_num):
    meanline_16[i]=mean1_16[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_16[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_16,color='green',label="Round 16", linestyle=":" )

upperline_64=np.zeros(test_num)
lowerline_64=np.zeros(test_num)
meanline_64=np.zeros(test_num)
for i in range(test_num):
    meanline_64[i]=mean1_64[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

upperline_128=np.zeros(test_num)
lowerline_128=np.zeros(test_num)
meanline_128=np.zeros(test_num)
for i in range(test_num):
    meanline_128[i]=mean1_128[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_128[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_128,color='purple',label="Round 128", linestyle=":" )

#plt.plot(x,mean1_ideal  ,color='black',label="Ideal", linestyle=":" )
plt.ylim((0,300))
my_y_ticks=np.arange(0,300,60)
plt.yticks(my_y_ticks)

plt.grid(True)
plt.legend()

plt.subplot(2,3,1)
plt.xlabel('Delay to 90%')
upperline_0=np.zeros(test_num)
lowerline_0=np.zeros(test_num)
meanline_0=np.zeros(test_num)
for i in range(test_num):
    meanline_0[i]=top101_0[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )

upperline_4=np.zeros(test_num)
lowerline_4=np.zeros(test_num)
meanline_4=np.zeros(test_num)
for i in range(test_num):
    meanline_4[i]=top101_4[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='orange',label="Round 4", linestyle=":" )

upperline_8=np.zeros(test_num)
lowerline_8=np.zeros(test_num)
meanline_8=np.zeros(test_num)
for i in range(test_num):
    meanline_8[i]=top101_8[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_8[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_8,color='yellow',label="Round 8", linestyle=":" )

upperline_16=np.zeros(test_num)
lowerline_16=np.zeros(test_num)
meanline_16=np.zeros(test_num)
for i in range(test_num):
    meanline_16[i]=top101_16[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_16[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_16,color='green',label="Round 16", linestyle=":" )

upperline_64=np.zeros(test_num)
lowerline_64=np.zeros(test_num)
meanline_64=np.zeros(test_num)
for i in range(test_num):
    meanline_64[i]=top101_64[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

upperline_128=np.zeros(test_num)
lowerline_128=np.zeros(test_num)
meanline_128=np.zeros(test_num)
for i in range(test_num):
    meanline_128[i]=top101_128[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_128[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_128,color='purple',label="Round 128", linestyle=":" )

#plt.plot(x,top101_ideal  ,color='black',label="Ideal", linestyle=":" )

plt.ylim((0,300))
my_y_ticks=np.arange(0,300,60)
plt.yticks(my_y_ticks)

plt.grid(True)


file = open(addr+"result90hash_localucbV1Round0.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_0=sorted(buff)
file.close()

file = open(addr+"result90hash_localucbV1Round4.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_4=sorted(buff)
file.close()

file = open(addr+"result90hash_localucbV1Round16.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_8=sorted(buff)
file.close()

file = open(addr+"result90hash_localucbV1Round32.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_16=sorted(buff)
file.close()

file = open(addr+"result90hash_localucbV1Round64.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_64=sorted(buff)
file.close()

file = open(addr+"result90hash_localucbV1Round128.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_128=sorted(buff)
file.close()
'''
file = open("result90_hash_ideal3.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_ideal=sorted(buff)
file.close()
'''

file = open(addr+"result90hash_localucbV2Round0.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_0=sorted(buff)
file.close()


file = open(addr+"result90hash_localucbV2Round4.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_4=sorted(buff)
file.close()

file = open(addr+"result90hash_localucbV2Round16.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_8=sorted(buff)
file.close()

file = open(addr+"result90hash_localucbV2Round32.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_16=sorted(buff)
file.close()

file = open(addr+"result90hash_localucbV2Round64.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_64=sorted(buff)
file.close()

file = open(addr+"result90hash_localucbV2Round128.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_128=sorted(buff)
file.close()
'''
file = open("result50_hash_ideal3.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_ideal=sorted(buff)
file.close()
'''
###

plt.subplot(2,3,5)
x=range(test_num)

upperline_0=np.zeros(test_num)
lowerline_0=np.zeros(test_num)
meanline_0=np.zeros(test_num)
for i in range(test_num):
    meanline_0[i]=mean1_0[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )


upperline_4=np.zeros(test_num)
lowerline_4=np.zeros(test_num)
meanline_4=np.zeros(test_num)
for i in range(test_num):
    meanline_4[i]=mean1_4[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='orange',label="Round 4", linestyle=":" )


upperline_8=np.zeros(test_num)
lowerline_8=np.zeros(test_num)
meanline_8=np.zeros(test_num)
for i in range(test_num):
    meanline_8[i]=mean1_8[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_8[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_8,color='yellow',label="Round 8", linestyle=":" )

upperline_16=np.zeros(test_num)
lowerline_16=np.zeros(test_num)
meanline_16=np.zeros(test_num)
for i in range(test_num):
    meanline_16[i]=mean1_16[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_16[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_16,color='green',label="Round 16", linestyle=":" )

upperline_64=np.zeros(test_num)
lowerline_64=np.zeros(test_num)
meanline_64=np.zeros(test_num)
for i in range(test_num):
    meanline_64[i]=mean1_64[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

upperline_128=np.zeros(test_num)
lowerline_128=np.zeros(test_num)
meanline_128=np.zeros(test_num)
for i in range(test_num):
    meanline_128[i]=mean1_128[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_128[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_128,color='purple',label="Round 128", linestyle=":" )

#plt.plot(x,mean1_ideal  ,color='black',label="Ideal", linestyle=":" )
plt.ylim((0,300))
my_y_ticks=np.arange(0,300,60)
plt.yticks(my_y_ticks)

plt.grid(True)
plt.legend()

plt.subplot(2,3,2)
upperline_0=np.zeros(test_num)
lowerline_0=np.zeros(test_num)
meanline_0=np.zeros(test_num)
for i in range(test_num):
    meanline_0[i]=top101_0[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )

upperline_4=np.zeros(test_num)
lowerline_4=np.zeros(test_num)
meanline_4=np.zeros(test_num)
for i in range(test_num):
    meanline_4[i]=top101_4[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='orange',label="Round 4", linestyle=":" )

upperline_8=np.zeros(test_num)
lowerline_8=np.zeros(test_num)
meanline_8=np.zeros(test_num)
for i in range(test_num):
    meanline_8[i]=top101_8[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_8[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_8,color='yellow',label="Round 8", linestyle=":" )

upperline_16=np.zeros(test_num)
lowerline_16=np.zeros(test_num)
meanline_16=np.zeros(test_num)
for i in range(test_num):
    meanline_16[i]=top101_16[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_16[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_16,color='green',label="Round 16", linestyle=":" )

upperline_64=np.zeros(test_num)
lowerline_64=np.zeros(test_num)
meanline_64=np.zeros(test_num)
for i in range(test_num):
    meanline_64[i]=top101_64[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

upperline_128=np.zeros(test_num)
lowerline_128=np.zeros(test_num)
meanline_128=np.zeros(test_num)
for i in range(test_num):
    meanline_128[i]=top101_128[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_128[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_128,color='purple',label="Round 128", linestyle=":" )

#plt.plot(x,top101_ideal  ,color='black',label="Ideal", linestyle=":" )

plt.ylim((0,300))
my_y_ticks=np.arange(0,300,60)
plt.yticks(my_y_ticks)

plt.grid(True)


file = open(addr+"result90hash_subsetV1Round0.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_0=sorted(buff)
file.close()

file = open(addr+"result90hash_subsetV1Round4.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_4=sorted(buff)
file.close()

file = open(addr+"result90hash_subsetV1Round16.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_8=sorted(buff)
file.close()

file = open(addr+"result90hash_subsetV1Round32.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_16=sorted(buff)
file.close()

file = open(addr+"result90hash_subsetV1Round64.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_64=sorted(buff)
file.close()

file = open(addr+"result90hash_subsetV1Round128.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_128=sorted(buff)
file.close()
'''
file = open("result90_hash_ideal3.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_ideal=sorted(buff)
file.close()
'''

file = open(addr+"result90hash_subsetV2Round0.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_0=sorted(buff)
file.close()


file = open(addr+"result90hash_subsetV2Round4.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_4=sorted(buff)
file.close()

file = open(addr+"result90hash_subsetV2Round16.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_8=sorted(buff)
file.close()

file = open(addr+"result90hash_subsetV2Round32.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_16=sorted(buff)
file.close()

file = open(addr+"result90hash_subsetV2Round64.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_64=sorted(buff)
file.close()

file = open(addr+"result90hash_subsetV2Round128.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_128=sorted(buff)
file.close()
'''
file = open("result50_hash_ideal3.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_ideal=sorted(buff)
file.close()
'''
###

plt.subplot(2,3,6)
x=range(test_num)

upperline_0=np.zeros(test_num)
lowerline_0=np.zeros(test_num)
meanline_0=np.zeros(test_num)
for i in range(test_num):
    meanline_0[i]=mean1_0[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )


upperline_4=np.zeros(test_num)
lowerline_4=np.zeros(test_num)
meanline_4=np.zeros(test_num)
for i in range(test_num):
    meanline_4[i]=mean1_4[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='orange',label="Round 4", linestyle=":" )


upperline_8=np.zeros(test_num)
lowerline_8=np.zeros(test_num)
meanline_8=np.zeros(test_num)
for i in range(test_num):
    meanline_8[i]=mean1_8[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_8[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_8,color='yellow',label="Round 8", linestyle=":" )

upperline_16=np.zeros(test_num)
lowerline_16=np.zeros(test_num)
meanline_16=np.zeros(test_num)
for i in range(test_num):
    meanline_16[i]=mean1_16[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_16[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_16,color='green',label="Round 16", linestyle=":" )

upperline_64=np.zeros(test_num)
lowerline_64=np.zeros(test_num)
meanline_64=np.zeros(test_num)
for i in range(test_num):
    meanline_64[i]=mean1_64[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

upperline_128=np.zeros(test_num)
lowerline_128=np.zeros(test_num)
meanline_128=np.zeros(test_num)
for i in range(test_num):
    meanline_128[i]=mean1_128[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_128[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_128,color='purple',label="Round 128", linestyle=":" )

#plt.plot(x,mean1_ideal  ,color='black',label="Ideal", linestyle=":" )
plt.ylim((0,300))
my_y_ticks=np.arange(0,300,60)
plt.yticks(my_y_ticks)

plt.grid(True)
plt.legend()

plt.subplot(2,3,3)
upperline_0=np.zeros(test_num)
lowerline_0=np.zeros(test_num)
meanline_0=np.zeros(test_num)
for i in range(test_num):
    meanline_0[i]=top101_0[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )

upperline_4=np.zeros(test_num)
lowerline_4=np.zeros(test_num)
meanline_4=np.zeros(test_num)
for i in range(test_num):
    meanline_4[i]=top101_4[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='orange',label="Round 4", linestyle=":" )

upperline_8=np.zeros(test_num)
lowerline_8=np.zeros(test_num)
meanline_8=np.zeros(test_num)
for i in range(test_num):
    meanline_8[i]=top101_8[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_8[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_8,color='yellow',label="Round 8", linestyle=":" )

upperline_16=np.zeros(test_num)
lowerline_16=np.zeros(test_num)
meanline_16=np.zeros(test_num)
for i in range(test_num):
    meanline_16[i]=top101_16[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_16[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_16,color='green',label="Round 16", linestyle=":" )

upperline_64=np.zeros(test_num)
lowerline_64=np.zeros(test_num)
meanline_64=np.zeros(test_num)
for i in range(test_num):
    meanline_64[i]=top101_64[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

upperline_128=np.zeros(test_num)
lowerline_128=np.zeros(test_num)
meanline_128=np.zeros(test_num)
for i in range(test_num):
    meanline_128[i]=top101_128[i]

errorx=[int(test_num*0.1),int(test_num*0.3),int(test_num*0.5),int(test_num*0.7),int(test_num*0.9)]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_128[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_128,color='purple',label="Round 128", linestyle=":" )

#plt.plot(x,top101_ideal  ,color='black',label="Ideal", linestyle=":" )

plt.ylim((0,300))
my_y_ticks=np.arange(0,300,60)
plt.yticks(my_y_ticks)

plt.grid(True)



plt.savefig("band_global8+4.png")



