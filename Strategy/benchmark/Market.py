import sys
import numpy as np
rpath='C:/Users/86196/Desktop/OLPS-P'
sys.path.append(rpath+'/Datatrans')
from datatrans import dataset

class Market():
    def __init__(self,price,S=1.0):
        self.price=price
        self.tds,self.ns=np.shape(price)
        self.S=np.ones([self.tds+1,self.ns],dtype=float)
        self.MS=np.ones(self.tds+1,dtype=float)
        self.S[0]*=S
        self.MS[0]*=S
    def run(self):
        i=0
        while i<self.tds:
            self.S[i+1]=self.price[i]*self.S[i]
            self.MS[i+1]=sum(self.S[i+1])/self.ns
            i+=1
        self.FS=self.MS[self.tds]
    def getS(self):
        return self.MS
    def getFS(self):
        return self.FS

# djia=dataset('djia')
# testt=Market(price=djia.prices(),S=1)
# testt.run()
# print(testt.getFS(),testt.getS(),np.shape(testt.getS()))