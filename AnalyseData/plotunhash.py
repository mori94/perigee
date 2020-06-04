#!/usr/bin/env python
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
test_num=1000
x=range(test_num)
addr="/Users/maoyifan/Downloads/btc/"
buff=np.zeros(test_num)
plt.rcParams['savefig.dpi'] = 300 #图片像素
plt.rcParams['figure.dpi'] = 300 #分辨率
plt.figure(figsize=(15,8))

file = open(addr+"result90unhash_global8-2V1Round0.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_0=sorted(buff)
file.close()

file = open(addr+"result90unhash_global8-2V1Round4.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_4=sorted(buff)
file.close()

file = open(addr+"result90unhash_global8-2V1Round64.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_64=sorted(buff)
file.close()

file = open(addr+"result90_unhash_ideal1.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_ideal=sorted(buff)
file.close()


file = open(addr+"result50unhash_global8-2V1Round0.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_0=sorted(buff)
file.close()

file = open(addr+"result50unhash_global8-2V1Round4.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_4=sorted(buff)
file.close()

file = open(addr+"result50unhash_global8-2V1Round64.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_64=sorted(buff)
file.close()

file = open(addr+"result50_unhash_ideal1.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_ideal=sorted(buff)
file.close()

###

plt.subplot(2,3,1)
plt.title('8-2 global')
x=range(test_num)

upperline_0=np.zeros(test_num)
lowerline_0=np.zeros(test_num)
meanline_0=np.zeros(test_num)
for i in range(test_num):
    meanline_0[i]=mean1_0[i]

errorx=[100,300,500,700,900]
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

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )



upperline_64=np.zeros(test_num)
lowerline_64=np.zeros(test_num)
meanline_64=np.zeros(test_num)
for i in range(test_num):
    meanline_64[i]=mean1_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.plot(x,mean1_ideal  ,color='black',label="Ideal", linestyle=":" )

plt.ylim((0,750))
my_y_ticks=np.arange(0,750,150)
plt.yticks(my_y_ticks)

plt.grid(True)
plt.legend()

plt.subplot(2,3,4)


upperline_0=np.zeros(test_num)
lowerline_0=np.zeros(test_num)
meanline_0=np.zeros(test_num)
for i in range(test_num):
    meanline_0[i]=top101_0[i]

errorx=[100,300,500,700,900]
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

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )

upperline_64=np.zeros(test_num)
lowerline_64=np.zeros(test_num)
meanline_64=np.zeros(test_num)
for i in range(test_num):
    meanline_64[i]=top101_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.plot(x,top101_ideal  ,color='black',label="Ideal", linestyle=":" )

plt.ylim((0,750))
my_y_ticks=np.arange(0,750,150)
plt.yticks(my_y_ticks)

plt.grid(True)




file = open(addr+"result90unhash_subsetV1Round0.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_0=sorted(buff)
file.close()

file = open(addr+"result90unhash_subsetV1Round4.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_4=sorted(buff)
file.close()

file = open(addr+"result90unhash_subsetV1Round64.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_64=sorted(buff)
file.close()

file = open(addr+"result90_unhash_ideal1.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
top101_ideal=sorted(buff)
file.close()


file = open(addr+"result50unhash_subsetV1Round0.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_0=sorted(buff)
file.close()

file = open(addr+"result50unhash_subsetV1Round4.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_4=sorted(buff)
file.close()

file = open(addr+"result50unhash_subsetV1Round64.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_64=sorted(buff)
file.close()

file = open(addr+"result50_unhash_ideal1.txt",'r',errors='replace')
line=file.readlines()
a=line[0].split("  ")
for j in range(test_num):
    buff[j]=int(float(a[j]))
mean1_ideal=sorted(buff)
file.close()

###

plt.subplot(2,3,2)
plt.title('subset')
x=range(test_num)

upperline_0=np.zeros(test_num)
lowerline_0=np.zeros(test_num)
meanline_0=np.zeros(test_num)
for i in range(test_num):
    meanline_0[i]=mean1_0[i]

errorx=[100,300,500,700,900]
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

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )



upperline_64=np.zeros(test_num)
lowerline_64=np.zeros(test_num)
meanline_64=np.zeros(test_num)
for i in range(test_num):
    meanline_64[i]=mean1_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]

plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.plot(x,mean1_ideal  ,color='black',label="Ideal", linestyle=":" )

plt.ylim((0,750))
my_y_ticks=np.arange(0,750,150)
plt.yticks(my_y_ticks)

plt.grid(True)
plt.legend()

plt.subplot(2,3,5)


upperline_0=np.zeros(test_num)
lowerline_0=np.zeros(test_num)
meanline_0=np.zeros(test_num)
for i in range(test_num):
    meanline_0[i]=top101_0[i]

errorx=[100,300,500,700,900]
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

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_4[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='green')

plt.plot(x,meanline_4,color='green',label="Round 4", linestyle=":" )

upperline_64=np.zeros(test_num)
lowerline_64=np.zeros(test_num)
meanline_64=np.zeros(test_num)
for i in range(test_num):
    meanline_64[i]=top101_64[i]

errorx=[100,300,500,700,900]
errory=np.zeros(5)
erroryerr=np.zeros([2,5])
for i in range(5):
    errory[i]=meanline_64[errorx[i]]
    
plt.errorbar(errorx,errory,yerr=erroryerr,fmt=".",color='blue')

plt.plot(x,meanline_64,color='blue',label="Round 64", linestyle=":" )

plt.plot(x,top101_ideal  ,color='black',label="Ideal", linestyle=":" )

plt.ylim((0,750))
my_y_ticks=np.arange(0,750,150)
plt.yticks(my_y_ticks)

plt.grid(True)






















plt.savefig("unhash_global.png")



