import sys
import numpy as np
rpath='C:/Users/86196/Desktop/OLPS-P'
sys.path.append(rpath+'/Datatrans')
from datatrans import dataset
# class anticor_bah():
#     def __init__(self,price,S=1.0,windows=2):
class Anticor():
    def __init__(self,price,S=1.0,windows=5):
        self.price=price
        self.tds,self.ns=np.shape(price)
        # self.tds=62
        self.S=np.ones(self.tds+1,dtype=float)
        self.S[0]*=S
        self.b=np.ones([self.tds+1,self.ns],dtype=float)
        self.W=windows
    def run(self):
        self.b[0]/=self.ns
        i=0
        while i<2*self.W-1 and i<self.tds:
            self.S[i+1]=self.S[i]*np.dot(self.price[i],self.b[i])
            self.b[i+1]=self.b[i]*self.price[i]/np.dot(self.price[i],self.b[i])
            i+=1
        while i<self.tds:
            self.S[i+1]=self.S[i]*np.dot(self.price[i],self.b[i])
            self.b[i+1]=self.findanticor(i)
            self.b[i+1]=self.project(self.b[i+1])
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
        return pb
    def findanticor(self,t):
        aprice=self.price[t-2*self.W+1:t+1].copy()
        ans=self.ns
        ab=self.b[t]*self.price[t]/np.dot(self.b[t],self.price[t])
        aprice=np.log(aprice)
        y1=aprice[0:self.W]
        y2=aprice[self.W:2*self.W]
        acor=np.zeros([ans,ans])
        trans=np.zeros([ans,ans])
        amean1,amean2=np.average(y1,axis=0),np.average(y2,axis=0)
        astd1,astd2=np.std(y1,axis=0),np.std(y2,axis=0)
        y1-=np.reshape(amean1,[1,ans])
        y2-=np.reshape(amean2,[1,ans])
        acor=np.dot(y1.T,y2)/self.W
        acor/=np.reshape(astd1,[ans,1])
        acor/=np.reshape(astd2,[1,ans])
        acor=np.nan_to_num(acor,posinf=0,neginf=0)
        for i in range(0,ans):
            for j in range(0,ans):
                if amean2[i]>=amean2[j] and acor[i][j]>0:
                    trans[i][j]=acor[i][j]-min(0,acor[i][i])-min(0,acor[j][j])
        for i in range(0,ans):
            if np.sum(trans[i])!=0:
                trans[i]/=np.sum(trans[i])
            trans[i]*=self.b[t][i]
            # trans[i]*=ab[i]
        ab+=np.sum(trans,axis=0)-np.sum(trans,axis=1)
        return ab

# djia=dataset('nyse-o')
# testt=Anticor(price=djia.prices(),S=1,windows=25)
# testt.run()
# print(testt.getFS(),testt.getAKNS(),testt.getFb(),np.sum(testt.getFb()),np.shape(testt.getFb()))
# # print(testt.getFS(),testt.getFb(),testt.getS(),np.shape(testt.getS()))