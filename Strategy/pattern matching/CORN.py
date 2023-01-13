import sys
import numpy as np
rpath='C:/Users/86196/Desktop/OLPS-P'
sys.path.append(rpath+'/Datatrans')
sys.path.append(rpath+'/Strategy/benchmark')
from datatrans import dataset
from BCRP import BCRP
import heapq

class CORN():
    def __init__(self,price,S=1.0,version='U',P=10,K=5,windows=5):
        self.price=price
        self.tds,self.ns=np.shape(price)
        # self.tds=101
        self.S=np.ones(self.tds+1,dtype=float)
        self.S[0]*=S
        self.b=np.ones([self.tds+1,self.ns],dtype=float)
        self.v=version
        self.k=K
        self.W=windows
        if self.v=='U':
            self.p=1/P
            self.CS=np.ones(self.W,dtype=float)
            self.Cb=np.ones([self.W,self.ns],dtype=float)/self.ns
        else:
            self.p=np.zeros(P)
            self.CS=np.ones(self.W*P,dtype=float)
            self.Cb=np.ones([self.W*P,self.ns],dtype=float)/self.ns
            for i in range(1,P):
                self.p[i]=i/P
    def run(self):
        self.b[0]/=self.ns
        i=0
        while i<self.tds:
            self.S[i+1]=self.S[i]*np.dot(self.price[i],self.b[i])
            self.CS*=np.dot(self.Cb,self.price[i])
            if self.v=='U':self.updateU(i)
            else:self.updateK(i)
            if i%50==0:print(i/50)
            i+=1
        self.FS=self.S[self.tds]
    def getS(self):
        return self.S
    def getFS(self):
        return self.FS
    def getb(self):
        return self.b
    def getFb(self):
        return self.b[self.tds]
    def getAKNS(self):
        return len(self.b[self.b>1/(self.ns*self.ns)])/len(self.b)/self.ns
    def findCORN(self,w,p,t):
        ab=np.ones(self.ns)/self.ns
        if t>=w:
            l=[]
            nowx=self.price[t-w+1:t+1].copy()
            nowx-=np.average(nowx)
            nowstd=np.std(nowx)
            prestd=np.zeros(t-w+1)
            acov=np.zeros(t-w+1)
            alist=[]
            amean=np.zeros(t-w+1)
            for i in range(0,w):
                alist.append(self.price[i:t-w+1+i])
                amean+=np.average(alist[i],axis=1)
            amean/=w
            for i in range(0,w):
                atemp=(alist[i].T-amean).T
                prestd+=np.average(atemp*atemp,axis=1)
                acov+=np.average(atemp*nowx[i],axis=1)
            prestd/=w
            prestd=np.sqrt(prestd)
            acov/=w
            acor=acov/(prestd*nowstd)
            acor=np.nan_to_num(acor,posinf=0,neginf=0)
            l=np.where(acor>=p)
            l2=np.reshape(np.array(l),len(l[0]))+w
            temp=self.price[l2]
            bcrp=BCRP(temp)
            bcrp.run()
            ab=bcrp.getb()
        return ab
    def updateU(self,t):
        for i in range(0,self.W):
            self.Cb[i]=self.findCORN(i+1,self.p,t)
        self.b[t+1]=np.dot(self.CS,self.Cb)
        self.b[t+1]/=np.sum(self.b[t+1])
    def updateK(self,t):
        for i in range(0,self.W):
            for j in range(0,len(self.p)):
                self.Cb[i*self.W+j]=self.findCORN(i+1,self.p[j],t)
        pkq=heapq.nlargest(self.k,range(len(self.CS)),self.CS.take)
        pkb=np.zeros(len(self.CS))
        pkb[pkq]=1.0
        pkb*=self.CS
        self.b[t+1]=np.dot(pkb,self.Cb)
        self.b[t+1]/=np.sum(self.b[t+1])

# djia=dataset('tse')
# # testt=CORN(price=djia.prices(),S=1,version='U')
# # testt=CORN(price=djia.prices(),S=1.0,version='K2',P=10,K=5,windows=5)
# testt=CORN(price=djia.prices(),S=1.0,version='K1',P=10,K=50,windows=5)
# testt.run()
# print(testt.getFS(),testt.getAKNS(),np.sum(testt.getFb()))
# # print(testt.getFS(),testt.getFb(),testt.getS(),np.shape(testt.getS()))