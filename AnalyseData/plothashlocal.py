#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
number=1000
x=range(number)
hash=np.zeros(number)

hash1=np.zeros(number)
file = open("/home/yifan/115-hash/hash1.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(number):
    hash1[j]=float(a[j])
file.close()

hash2=np.zeros(number)
file = open("/home/yifan/115-hash/hash2.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(number):
    hash2[j]=float(a[j])
file.close()

hash3=np.zeros(number)
file = open("/home/yifan/115-hash/hash3.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(number):
    hash3[j]=float(a[j])
file.close()


file = open("/home/yifan/115-hash/hash_localucpV1Round0.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_0=sorted(top101)
mean1_0=sorted(mean1)
file.close()

file = open("/home/yifan/115-hash/hash_localucpV1Round4.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_4=sorted(top101)
mean1_4=sorted(mean1)
file.close()

file = open("/home/yifan/115-hash/hash_localucpV1Round64.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_64=sorted(top101)
mean1_64=sorted(mean1)
file.close()

###
plt.rcParams['savefig.dpi'] = 300 #图片像素
plt.rcParams['figure.dpi'] = 300 #分辨率
plt.figure(figsize=(15,8))


plt.subplot(2,5,1)
plt.title('8-4 alg global')
x=range(number)

upperline_0=np.zeros(number)
lowerline_0=np.zeros(number)
meanline_0=np.zeros(number)
for i in range(number):
    meanline_0[i]=mean1_0[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )


upperline_4=np.zeros(number)
lowerline_4=np.zeros(number)
meanline_4=np.zeros(number)
for i in range(number):
    meanline_4[i]=mean1_4[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )



upperline_64=np.zeros(number)
lowerline_64=np.zeros(number)
meanline_64=np.zeros(number)
for i in range(number):
    meanline_64[i]=mean1_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.ylim((0,1500))
my_y_ticks=np.arange(0,1500,300)
plt.yticks(my_y_ticks)
plt.ylabel('Latency to 50% hash')


plt.grid(True)
plt.legend()




###
plt.subplot(2,5,6)


upperline_0=np.zeros(number)
lowerline_0=np.zeros(number)
meanline_0=np.zeros(number)
for i in range(number):
    meanline_0[i]=top101_0[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )

upperline_4=np.zeros(number)
lowerline_4=np.zeros(number)
meanline_4=np.zeros(number)
for i in range(number):
    meanline_4[i]=top101_4[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )

upperline_64=np.zeros(number)
lowerline_64=np.zeros(number)
meanline_64=np.zeros(number)
for i in range(number):
    meanline_64[i]=top101_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.ylim((0,1500))
my_y_ticks=np.arange(0,1500,300)
plt.yticks(my_y_ticks)
plt.ylabel('Latency to 90% hash')

plt.grid(True)



file = open("/home/yifan/115-hash/unhash_localucpV1Round0.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_0=sorted(top101)
mean1_0=sorted(mean1)
file.close()

file = open("/home/yifan/115-hash/unhash_localucpV1Round4.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_4=sorted(top101)
mean1_4=sorted(mean1)
file.close()

file = open("/home/yifan/115-hash/unhash_localucpV1Round64.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_64=sorted(top101)
mean1_64=sorted(mean1)
file.close()

###

plt.subplot(2,5,2)
plt.title('8-4 alg global')
x=range(number)

upperline_0=np.zeros(number)
lowerline_0=np.zeros(number)
meanline_0=np.zeros(number)
for i in range(number):
    meanline_0[i]=mean1_0[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )


upperline_4=np.zeros(number)
lowerline_4=np.zeros(number)
meanline_4=np.zeros(number)
for i in range(number):
    meanline_4[i]=mean1_4[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )



upperline_64=np.zeros(number)
lowerline_64=np.zeros(number)
meanline_64=np.zeros(number)
for i in range(number):
    meanline_64[i]=mean1_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.ylim((0,1500))
my_y_ticks=np.arange(0,1500,300)
plt.yticks(my_y_ticks)


plt.grid(True)
plt.legend()




###
plt.subplot(2,5,7)


upperline_0=np.zeros(number)
lowerline_0=np.zeros(number)
meanline_0=np.zeros(number)
for i in range(number):
    meanline_0[i]=top101_0[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )

upperline_4=np.zeros(number)
lowerline_4=np.zeros(number)
meanline_4=np.zeros(number)
for i in range(number):
    meanline_4[i]=top101_4[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )

upperline_64=np.zeros(number)
lowerline_64=np.zeros(number)
meanline_64=np.zeros(number)
for i in range(number):
    meanline_64[i]=top101_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.ylim((0,1500))
my_y_ticks=np.arange(0,1500,300)
plt.yticks(my_y_ticks)

plt.grid(True)














file = open("/home/yifan/115-hash/hash_global8+2V1Round0.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_0=sorted(top101)
mean1_0=sorted(mean1)
file.close()

file = open("/home/yifan/115-hash/hash_global8+2V1Round4.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_4=sorted(top101)
mean1_4=sorted(mean1)
file.close()

file = open("/home/yifan/115-hash/hash_global8+2V1Round64.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_64=sorted(top101)
mean1_64=sorted(mean1)
file.close()


###


plt.subplot(2,5,3)
plt.title('8+4 alg hash')
x=range(number)

upperline_0=np.zeros(number)
lowerline_0=np.zeros(number)
meanline_0=np.zeros(number)
for i in range(number):
    meanline_0[i]=mean1_0[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )


upperline_4=np.zeros(number)
lowerline_4=np.zeros(number)
meanline_4=np.zeros(number)
for i in range(number):
    meanline_4[i]=mean1_4[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )



upperline_64=np.zeros(number)
lowerline_64=np.zeros(number)
meanline_64=np.zeros(number)
for i in range(number):
    meanline_64[i]=mean1_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.ylim((0,1500))
my_y_ticks=np.arange(0,1500,300)
plt.yticks(my_y_ticks)


plt.grid(True)
plt.legend()




###
plt.subplot(2,5,8)


upperline_0=np.zeros(number)
lowerline_0=np.zeros(number)
meanline_0=np.zeros(number)
for i in range(number):
    meanline_0[i]=top101_0[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )

upperline_4=np.zeros(number)
lowerline_4=np.zeros(number)
meanline_4=np.zeros(number)
for i in range(number):
    meanline_4[i]=top101_4[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )

upperline_64=np.zeros(number)
lowerline_64=np.zeros(number)
meanline_64=np.zeros(number)
for i in range(number):
    meanline_64[i]=top101_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.ylim((0,1500))
my_y_ticks=np.arange(0,1500,300)
plt.yticks(my_y_ticks)

plt.grid(True)


file = open("/home/yifan/115-hash/unhash_global8+2V1Round0.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_0=sorted(top101)
mean1_0=sorted(mean1)
file.close()

file = open("/home/yifan/115-hash/unhash_global8+2V1Round4.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_4=sorted(top101)
mean1_4=sorted(mean1)
file.close()

file = open("/home/yifan/115-hash/unhash_global8+2V1Round64.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101_64=sorted(top101)
mean1_64=sorted(mean1)
file.close()


###


plt.subplot(2,5,9)
plt.title('8+4 alg hash')
x=range(number)

upperline_0=np.zeros(number)
lowerline_0=np.zeros(number)
meanline_0=np.zeros(number)
for i in range(number):
    meanline_0[i]=mean1_0[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )


upperline_4=np.zeros(number)
lowerline_4=np.zeros(number)
meanline_4=np.zeros(number)
for i in range(number):
    meanline_4[i]=mean1_4[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )



upperline_64=np.zeros(number)
lowerline_64=np.zeros(number)
meanline_64=np.zeros(number)
for i in range(number):
    meanline_64[i]=mean1_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.ylim((0,1500))
my_y_ticks=np.arange(0,1500,300)
plt.yticks(my_y_ticks)


plt.grid(True)
plt.legend()




###
plt.subplot(2,5,10)


upperline_0=np.zeros(number)
lowerline_0=np.zeros(number)
meanline_0=np.zeros(number)
for i in range(number):
    meanline_0[i]=top101_0[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_0[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='red')

plt.plot(x,meanline_0,color='red',label="Random selection", linestyle=":" )

upperline_4=np.zeros(number)
lowerline_4=np.zeros(number)
meanline_4=np.zeros(number)
for i in range(number):
    meanline_4[i]=top101_4[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )

upperline_64=np.zeros(number)
lowerline_64=np.zeros(number)
meanline_64=np.zeros(number)
for i in range(number):
    meanline_64[i]=top101_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.ylim((0,1500))
my_y_ticks=np.arange(0,1500,300)
plt.yticks(my_y_ticks)

plt.grid(True)








file = open("/home/yifan/newversion2/geoset/geo1/best8_len_0.txt",'r',errors='replace')
top101=np.zeros(number)
mean1=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top101[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean1[i]=buff1[number-1-j]
top101=sorted(top101)
mean1=sorted(mean1)
file.close()


file = open("/home/yifan/newversion2/geoset/geo2/best8_len_0.txt",'r',errors='replace')
top102=np.zeros(number)
mean2=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top102[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean2[i]=buff1[number-1-j]
top102=sorted(top102)
mean2=sorted(mean2)
file.close()

file = open("/home/yifan/newversion2/geoset/geo3/best8_len_0.txt",'r',errors='replace')
top103=np.zeros(number)
mean3=np.zeros(number)
buff=np.zeros(number)
line=file.readlines()
for i in range(number):
    a=line[i].split("  ")
    for j in range(number):
        buff[j]=int(float(a[j]))+0.0001*j
    buff1=sorted(buff)
    hashsum=0
    flag10=0
    flag50=0
    for j in range(number):
        for k in range(number):
            if buff1[number-1-j]==buff[k]:
                hashsum=hashsum+hash1[k]
                if hashsum>0.1 and flag10==0:
                    flag10=1
                    top103[i]=buff1[number-1-j]
                if hashsum>0.5 and flag50==0:
                    flag50=1
                    mean3[i]=buff1[number-1-j]
top103=sorted(top103)
mean3=sorted(mean3)
file.close()



upperline=np.zeros(number)
lowerline=np.zeros(number)
meanline=np.zeros(number)
for i in range(number):
    meanline[i]=(mean1[i]+mean2[i]+mean3[i])/3
    upperline[i]=max(mean1[i],mean2[i],mean3[i])
    lowerline[i]=min(mean1[i],mean2[i],mean3[i])


plt.subplot(2,3,3)
plt.title('GeoAlgDelay')
x=range(number)

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline[errorx[i]]
    erroryerr[0][i]=upperline[errorx[i]]-meanline[errorx[i]]
    erroryerr[1][i]=meanline[errorx[i]]-lowerline[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".")

plt.plot(x,meanline,color='black',label="mean delay", linestyle=":" )

plt.ylim((0,1500))
my_y_ticks=np.arange(0,1500,300)
plt.yticks(my_y_ticks)


plt.grid(True)
plt.legend()


upperline=np.zeros(number)
lowerline=np.zeros(number)
meanline=np.zeros(number)
for i in range(number):
    meanline[i]=(top101[i]+top102[i]+top103[i])/3
    upperline[i]=max(top101[i],top102[i],top103[i])
    lowerline[i]=min(top101[i],top102[i],top103[i])


###
errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline[errorx[i]]
    erroryerr[0][i]=upperline[errorx[i]]-meanline[errorx[i]]
    erroryerr[1][i]=meanline[errorx[i]]-lowerline[errorx[i]]
plt.subplot(2,3,6)

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".")

plt.plot(x,meanline,color='black',label="mean delay", linestyle=":" )



plt.ylim((0,1500))
my_y_ticks=np.arange(0,1500,300)
plt.yticks(my_y_ticks)

plt.grid(True)








plt.savefig("hash_local.png")



