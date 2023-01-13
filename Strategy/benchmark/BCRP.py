import sys
import numpy as np
rpath='C:/Users/86196/Desktop/OLPS-P'
sys.path.append(rpath+'/Datatrans')
from datatrans import dataset

class BCRP():
    def __init__(self,price,S=1.0):
        self.price=price
        self.tds,self.ns=np.shape(price)
        self.S=np.ones(self.tds+1,dtype=float)
        self.S[0]*=S
    def run(self):
        self.b=self.findbcrp()
        i=0
        while i<self.tds:
            self.S[i+1]=self.S[i]*np.dot(self.price[i],self.b)
            i+=1
        self.FS=self.S[self.tds]
    def getS(self):
        return self.S
    def getFS(self):
        return self.FS
    def getb(self):
        return self.b
    def findbcrp(self):
        b=np.ones(self.ns,dtype=float)/self.ns
        pr=self.price.copy()
        gap=0.0001
        step=0
        dire=b.copy()
        dmod=1
        timekeep=50
        while(dmod>=gap):
            # 更新权重b
            b+=step*dire
            # 不起作用的约束条件数
            dwc=0
            for i in range(0,self.ns) :
                if b[i]==0: dire[i]=0
                else: 
                    dire[i]=-1
                    dwc+=1
            # 求方向dire
            for i in range(0,self.tds) :
                pr[i]/=np.dot(pr[i],b)
            grad=np.sum(pr,axis=0)
            pseq=np.argsort(grad)
            j=self.ns-1
            while(dwc>0):
                dire[pseq[j]]+=1
                dwc-=1
                if dire[pseq[j]]==0 and dwc>0:
                    dire[pseq[j]]+=1
                    dwc-=1
                j-=1
            dmod=np.dot(grad,dire)
            # 求步长step
            maxstep=float('inf')
            for i in range(0,self.ns) :
                if dire[i]<0:
                    maxstep=min(maxstep,-b[i]/dire[i])
            res=np.dot(dire,pr.T)
            step=np.sum(res)/np.dot(res,res)
            step=min(step,maxstep)
            #时间控制
            timekeep-=1
            if timekeep==0 :break
        return b

# djia=dataset('nyse-n')
# testt=BCRP(price=djia.prices(),S=1)
# testt.run()
# # print(testt.getFS(),testt.getb())
# print(testt.getFS(),testt.getb(),testt.getS(),np.shape(testt.getS()))