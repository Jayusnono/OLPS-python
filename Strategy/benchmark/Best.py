import sys
import numpy as np
rpath='C:/Users/86196/Desktop/OLPS-P'
sys.path.append(rpath+'/Datatrans')
from datatrans import dataset
# djia=dataset('djia')
# djia.brief()
# print(djia.prices())

class Best():
    def __init__(self,price,S=1.0):
        self.price=price
        self.tds,self.ns=np.shape(price)
        self.S=np.ones([self.tds+1,self.ns],dtype=float)
        self.S[0]*=S
    def run(self):
        i=0
        while i<self.tds:
            self.S[i+1]=self.price[i]*self.S[i]
            i+=1
        i=1
        self.FS=self.S[self.tds][0]
        self.bestone=0
        while i<self.ns:
            if self.S[self.tds][i]>self.FS:
                self.FS=self.S[self.tds][i]
                self.bestone=i
            i+=1
    def getS(self):
        return self.S[:,self.bestone]
    def getFS(self):
        return self.FS

# djia=dataset('djia')
# testt=Best(price=djia.prices(),S=1)
# testt.run()
# print(testt.getFS(),testt.getS(),np.shape(testt.getS()))
