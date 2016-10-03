import numpy as np
import numpy.random as rd
from numpy.random import *
import matplotlib.pyplot as plt
import sys
#definition of constants
GUNMA=0.95
ALFA=0.4
class Condition:
    def __init__(self,gyo,ret):
        self.gyo=gyo
        self.ret=ret
        self.pos=[0,0]
        self.past=[0,0]
        self.Map = np.zeros([self.gyo+2,self.ret+2])
        self.qua = np.zeros([self.gyo+2,self.ret+2])
        self.e = np.zeros([self.gyo*self.ret,4]) 
        self.Start=[0,0]
        self.Goal=[0,0]
        self.proba=np.array([0,0,0,0])#[right,left,up down]
        self.Trial=0
        self.Count=0
        self.reword=np.zeros([self.gyo+2,self.ret+2])
        self.x=[]
def first():
    m=0
    n=0
    f = open('map.txt')
    line = f.readline()
    while line:
        while m < a.ret+2:
            if line[m]=='#':
                a.Map[m,n]=-1
                #a.reword[m,n]=-1
            elif line[m]=='S':
                a.Map[m,n]=-3
                a.Start=[m,n]
            elif line[m]=='G':
                a.Map[m,n]=-4
                a.reword[m,n]=1
                a.Goal=[m,n]
            elif line[m]==',':a.Map[m,n]=0
            else:pass
            m=m+1
        m=0
        n=n+1
        line = f.readline()
    f.close
    a.Map=a.Map.transpose()
    a.reword=a.reword.transpose()
    a.qua=a.qua.transpose()
    a.Start=[a.Start[1],a.Start[0]]
    a.Goal=[a.Goal[1],a.Goal[0]]
    print "Start:%s, Goal:%s" % (a.Start, a.Goal)
    a.pos=a.Start
    a.past=a.Start

def disp():
    m=0
    n=0
    for i in range(a.ret + 2):
        for j in range(a.gyo + 2):
            if a.Map[n,m] == -1: print('#'),
            elif a.Map[n,m]==-3: print('S'),
            elif a.Map[n,m]==-4: print('G'),
            elif a.Map[n,m]==1: print('@'),
            else: print(' '),
            m += 1
        print(' ')
        m=0
        n += 1

def soft_max():
    k=0
    j=1
    Sum=0.0
    flug=np.array([0.0,0.0,0.0,0.0])
    arg=np.array(0.0)
    Sum=np.array(0.0)
    if a.pos[1]!=a.ret:
        if a.Map[a.pos[0],a.pos[1]+1] != -1:
            if a.Map[a.pos[0],a.pos[1]+1] == 0 or a.Map[a.pos[0],a.pos[1]+1] == -4:#right
                a.proba[0]=np.exp(a.qua[a.pos[0],a.pos[1]+1])
                Sum = Sum+ a.proba[0]
            else:a.proba[0]=-1
        else:a.proba[0]=-1
    else:a.proba[0]=-1

    if a.pos[1]!= 1:
        if a.Map[a.pos[0],a.pos[1]-1] != -1:
            if a.Map[a.pos[0],a.pos[1]-1] == 0 or a.Map[a.pos[0],a.pos[1]-1] == -4:#left
                a.proba[1]=np.exp(a.qua[a.pos[0],a.pos[1]-1])
                Sum = Sum+ a.proba[1]
            else:a.proba[1]=-1
        else:a.proba[1]=-1
    else:a.proba[1]=-1

    if a.pos[0]!=1:
        if a.Map[a.pos[0]-1,a.pos[1]] != -1:
            if a.Map[a.pos[0]-1,a.pos[1]] == 0 or a.Map[a.pos[0]-1,a.pos[1]] == -4:#up
                a.proba[2]=np.exp(a.qua[a.pos[0]-1,a.pos[1]])
                Sum = Sum+ a.proba[2]
            else:a.proba[2]=-1
        else:a.proba[2]=-1
    else:a.proba[2]=-1

    if a.pos[0]!= a.gyo:
        if a.Map[a.pos[0]+1,a.pos[1]] != -1:
            if a.Map[a.pos[0]+1,a.pos[1]] == 0 or a.Map[a.pos[0]+1,a.pos[1]] == -4:#down
                a.proba[3]=np.exp(a.qua[a.pos[0]+1,a.pos[1]])
                Sum = Sum+ a.proba[3]
            else:a.proba[3]=-1
        else:a.proba[3]=-1
    else:a.proba[3]=-1
    Sum = 1/Sum
    a.proba=[a.proba[0]*Sum,a.proba[1]*Sum,a.proba[2]*Sum,a.proba[3]*Sum]
    k=choice()
    
    if k==0: #right
        a.past=a.pos
        a.pos=[a.past[0],a.past[1]+1]
    if k==1:#left
        a.past=a.pos
        a.pos=[a.past[0],a.past[1]-1]
    if k==2:#up
        a.past=a.pos
        a.pos=[a.past[0]-1,a.past[1]]
    if k==3:#down
        a.past=a.pos
        a.pos=[a.past[0]+1,a.past[1]]
    a.Count=a.Count+1

    sarsa()

    if a.past==a.Goal:
        a.Trial=a.Trial+1
        a.x.append(a.Count)
        a.Map[a.pos[0],a.pos[1]]=a.Map[a.past[0],a.past[1]]=0
        a.Map[a.Goal[0],a.Goal[1]]=-4
        a.pos=a.past=a.Start
        a.Count=0
        #print("quality function:")
        #print(a.qua)
    else:a.Map[a.pos[0],a.pos[1]]=1

    a.Map[a.past[0],a.past[1]]=0
    a.Map[a.Start[0],a.Start[1]]=-3
    a.proba=[0.0,0.0,0.0,0.0]
def sarsa():
    if a.past==a.Goal:
        a.qua[a.past[0],a.past[1]]=a.qua[a.past[0],a.past[1]]+ALFA*(a.reword[a.past[0],a.past[1]])
    else:
        a.qua[a.past[0],a.past[1]]=a.qua[a.past[0],a.past[1]]+ALFA*(a.reword[a.pos[0],a.pos[1]]+GUNMA*(a.qua[a.pos[0],a.pos[1]])-a.qua[a.past[0],a.past[1]])
def learning():
    soft_max()
    #disp()    
def choice():
    flug=0
    j=1
    m=0
    Max=0.0
    k=[0,0,0,0]#ikenekoukouwosimesu
    f=[0,0,0,0]#ikeruhoukouwosimesu
    i=0
    print(a.proba)
    while i<4:
        if a.proba[i]<0: k[i]=-1
        i=i+1
    i=1
    Max=a.proba[0]
    f=[1,0,0,0]
    while i<4:
        if k[i]>-1:
            if Max < a.proba[i]:
                Max=a.proba[i]
                flug=i
                f=[0,0,0,0]
                f[i]=1
            elif Max==a.proba[i]:f[flug]=f[i]=1
        i=i+1
    print('k:')
    print(k)
    print('f:')
    print(f)
    if np.count_nonzero(f)==1: return flug
    else:     
        flug = randint(3)
        while f[flug] != 1: flug = randint(3)        
        return flug

if __name__ == "__main__":
    print("190")
    i=0
    z=[]
    #syokisettei
    a = Condition(5,5)
    first()
    #gakusyuu
    while a.Trial< 30:
        learning()
    disp()
    print("LINE 202")
    z=a.x
    print"count:%d"%a.Count 
    print" Trial:%d" %a.Trial
    print("quality function:")
    print(a.qua)
    print("map:")
    print(a.Map)
    print("LINE 210")
    print(z)
    plt.plot(z)
    print("LINE 213")
    plt.ylim(0, 50)
    plt.legend()
    plt.xlabel("Trial")
    plt.ylabel("Counts")
    plt.title("N=5,"+"GUNMA="+str(GUNMA)+", ALPHA="+str(ALFA), fontsize=16, fontname='serif')
    plt.savefig("GUNMA="+str(GUNMA)+"ALFA="+str(ALFA)+".png")