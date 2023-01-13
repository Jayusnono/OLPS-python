import sys
import numpy as np
rpath='C:/Users/86196/Desktop/OLPS-P'
sys.path.append(rpath+'/Datatrans')
from datatrans import dataset

class EG():
    def __init__(self,price,step=0.05,S=1.0):
        self.price=price
        self.tds,self.ns=np.shape(price)
        # self.tds=100
        self.S=np.ones(self.tds+1,dtype=float)
        self.S[0]*=S
        self.b=np.ones([self.tds+1,self.ns],dtype=float)
        self.d=step
    def run(self):
        self.b[0]/=self.ns
        i=0
        while i<self.tds:
            self.S[i+1]=self.S[i]*np.dot(self.price[i],self.b[i])
            self.b[i+1]=self.findEG(i)
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
    def findEG(self,i):
        ab=self.price[i]/np.dot(self.price[i],self.b[i])
        ab*=self.d
        ab=np.exp(ab)
        ab*=self.b[i]
        ab/=np.sum(ab)
        return ab

# djia=dataset('tse')
# testt=EG(price=djia.prices(),step=0.05)
# testt.run()
# print(testt.getFS(),testt.getAKNS(),np.sum(testt.getFb()))
# # print(testt.getFS(),testt.getFb(),testt.getS(),np.shape(testt.getS()))