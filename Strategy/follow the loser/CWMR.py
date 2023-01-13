import sys
import numpy as np
rpath='C:/Users/86196/Desktop/OLPS-P'
sys.path.append(rpath+'/Datatrans')
from datatrans import dataset
import math

class CWMR():
    def __init__(self,price,S=1.0,version='Var',profit=0.5,confidence=2.0):
        self.price=price
        self.tds,self.ns=np.shape(price)
        # self.tds=101
        self.S=np.ones(self.tds+1,dtype=float)
        self.S[0]*=S
        self.b=np.ones([self.tds+1,self.ns],dtype=float)
        self.v=version
        self.p=profit
        self.C=confidence
        self.Sigma=np.ones(self.ns)/(self.ns*self.ns)
        self.step=0.0
        self.u=1.0
    def run(self):
        self.b[0]/=self.ns
        i=0
        while i<self.tds:
            self.S[i+1]=self.S[i]*np.dot(self.price[i],self.b[i])
            self.updatestep(i)
            self.b[i+1]=self.findCWMR(i)
            self.b[i+1]=self.project(self.b[i+1])
            self.updateSigma(i)
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
    def findCWMR(self,i):
        tp=self.price[i].copy()
        tp-=(np.dot(self.price[i],self.Sigma)/np.sum(self.Sigma))
        ab=self.b[i].copy()
        ab-=self.step*self.Sigma*tp
        return ab
    def updatestep(self,i):
        M=np.dot(self.b[i],self.price[i])
        V=np.dot(self.price[i]*self.Sigma,self.price[i])
        W=np.dot(self.Sigma,self.price[i])
        if self.v=='Var':
            ta=V-W*(np.dot(self.price[i],self.Sigma)/np.sum(self.Sigma))
            tb=self.C*V
            tc=self.p-M
            a=2*tb*ta
            b=2*tb*tc
            c=tc-tb
            delt=b*b-4*a*c
            if delt<0:
                self.step=0.0
            elif delt==0 or a==0:
                self.step=max(0,-c/b)
            else:
                self.step=max(0,(-b+math.sqrt(delt))/(2*a),(-b-math.sqrt(delt))/(2*a))
        else:
            ta=V-W*(np.dot(self.price[i],self.Sigma)/np.sum(self.Sigma))
            tb=self.C*self.C*V
            tc=self.p-M
            a=(ta+tb/2)*(ta+tb/2)-tb*tb/4
            b=2*tc*(ta+tb/2)
            c=tc*tc-tb
            delt=b*b-4*a*c
            if delt<0:
                self.step=0.0
            elif delt==0 or a==0:
                self.step=max(0,-c/b)
            else:
                self.step=max(0,(-b+math.sqrt(delt))/(2*a),(-b-math.sqrt(delt))/(2*a))
            utemp=self.step*self.C*V
            self.u=(-utemp+math.sqrt(utemp*utemp+4*V))/2
            if self.u==0:
                self.u=1.0
                self.step=0.0
    def updateSigma(self,i):
        if self.v=='Var':temp=2*self.step*self.C
        else:temp=self.step*self.C/self.u
        self.Sigma=1/(1/self.Sigma+temp*np.square(self.price[i]))
        self.Sigma/=np.sum(self.Sigma)*self.ns
# djia=dataset('msci')
# testt=CWMR(price=djia.prices(),S=1,version='Var')
# testt.run()
# print(testt.getFS(),testt.getAKNS(),testt.getFb())
# # print(testt.getFS(),testt.getFb(),testt.getS(),np.shape(testt.getS()))