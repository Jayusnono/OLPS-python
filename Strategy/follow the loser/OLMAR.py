import sys
import numpy as np
rpath='C:/Users/86196/Desktop/OLPS-P'
sys.path.append(rpath+'/Datatrans')
from datatrans import dataset

class OLMAR():
    def __init__(self,price,S=1.0,version=1,windows=5,smooth=0.5,profit=10):
        self.price=price
        self.tds,self.ns=np.shape(price)
        # self.tds=10
        self.S=np.ones(self.tds+1,dtype=float)
        self.S[0]*=S
        self.b=np.ones([self.tds+1,self.ns],dtype=float)
        self.p=profit
        if version==1:
            self.W=windows
            self.maprice=self.findSMA()
        else:
            self.W=smooth
            self.maprice=self.findEMA()
    def run(self):
        self.b[0]/=self.ns
        i=0
        loss=0
        while i<self.tds:
            self.S[i+1]=self.S[i]*np.dot(self.price[i],self.b[i])
            loss=self.p-np.dot(self.maprice[i],self.b[i])
            if loss<=0:
                self.b[i+1]=self.b[i]
            else:
                self.b[i+1]=self.findOLMAR(i,loss)
                self.b[i+1]=self.project(self.b[i+1])
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
    def project(self,pb):
        c=0.0
        i=0
        pseq=np.argsort(pb)
        while pb[pseq[i]]<-c/(self.ns-i):
            c+=pb[pseq[i]]
            pb[pseq[i]]=0
            i+=1
        for k in range(i,self.ns):
            pb[pseq[k]]+=c/(self.ns-i)
        pb/=np.sum(pb)
        return pb
    def findSMA(self):
        ap=np.ones([self.tds,self.ns])
        for i in range(0,self.W-1):
            ap[i]*=self.W
        for i in range(self.W-1,self.tds):
            op=np.ones(self.ns)
            for j in range(0,self.W-1):
                op*=self.price[i-j]
                ap[i]+=1/op
        ap/=self.W
        return ap
    def getAKNS(self):
        return len(self.b[self.b>1/(self.ns*self.ns)])/len(self.b)/self.ns
    def findEMA(self):
        ap=np.ones([self.tds,self.ns])*self.W
        ap[0]=np.ones(self.ns)
        for i in range(1,self.tds):
            ap[i]+=(1-self.W)*ap[i-1]/self.price[i]
        return ap
    def findOLMAR(self,i,loss):
        tp=self.maprice[i].copy()
        tp-=np.average(tp)
        ab=self.b[i].copy()
        if np.dot(tp,tp)!=0:
            step=loss/np.dot(tp,tp)
            ab+=step*tp
        return ab

# djia=dataset('tse')
# testt=OLMAR(price=djia.prices(),S=1.0,version=1,windows=5,profit=10)
# # testt=OLMAR(price=djia.prices(),S=1.0,version=2,smooth=0.5,profit=10)
# testt.run()
# print(testt.getFS(),testt.getAKNS(),np.sum(testt.getFb()))
# # print(testt.getFS(),testt.getFb(),testt.getS(),np.shape(testt.getS()))