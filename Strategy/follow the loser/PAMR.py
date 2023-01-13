import sys
import numpy as np
rpath='C:/Users/86196/Desktop/OLPS-P'
sys.path.append(rpath+'/Datatrans')
from datatrans import dataset

class PAMR():
    def __init__(self,price,S=1.0,version=0,profit=0.5,C=500):
        self.price=price
        self.tds,self.ns=np.shape(price)
        # self.tds=100
        self.S=np.ones(self.tds+1,dtype=float)
        self.S[0]*=S
        self.b=np.ones([self.tds+1,self.ns],dtype=float)
        self.v=version
        self.p=profit
        self.C=C
    def run(self):
        self.b[0]/=self.ns
        i=0
        loss=0
        while i<self.tds:
            self.S[i+1]=self.S[i]*np.dot(self.price[i],self.b[i])
            loss=np.dot(self.price[i],self.b[i])-self.p
            if loss<=0:
                self.b[i+1]=self.b[i]
            else:
                self.b[i+1]=self.findPAMR(i,loss)
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
    def getAKNS(self):
        return len(self.b[self.b>1/(self.ns*self.ns)])/len(self.b)/self.ns
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
    def findPAMR(self,i,loss):
        tp=self.price[i].copy()
        tp-=np.average(tp)
        ab=self.b[i].copy()
        if np.dot(tp,tp)!=0:step=loss/np.dot(tp,tp)
        else:step=self.C
        if self.v==1:step=min(step,self.C)
        elif self.v==2:step=loss/(np.dot(tp,tp)+1/(2*self.C))
        ab-=step*tp
        return ab

# djia=dataset('msci')
# # testt=PAMR(price=djia.prices(),S=1.0,version=0,profit=0.5)
# testt=PAMR(price=djia.prices(),S=1.0,version=0,profit=0.5)
# # testt=PAMR(price=djia.prices(),S=1.0,version=2,profit=0.5,C=500)
# testt.run()
# print(testt.getFS(),testt.getAKNS(),np.sum(testt.getFb()))
# # print(testt.getFS(),testt.getFb(),testt.getS(),np.shape(testt.getS()))