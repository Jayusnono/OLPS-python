import sys
rpath='C:/Users/86196/Desktop/OLPS-P'
sys.path.append(rpath+'/Datatrans')
sys.path.append(rpath+'/Strategy/benchmark')
sys.path.append(rpath+'/Strategy/follow the loser')
sys.path.append(rpath+'/Strategy/follow the winner')
sys.path.append(rpath+'/Strategy/pattern matching')
from datatrans import dataset
from Market import Market
from Best import Best
from BCRP import BCRP
from UP import UP
from EG import EG
from ONS import ONS
from Anticor import Anticor
from BK import BK
from BNN import BNN
from CORN import CORN
from PAMR import PAMR
from CWMR import CWMR
from OLMAR import OLMAR
from DSR import DSR
import numpy as np
dataname=['nyse-o','nyse-n','tse','sp500','msci','djia']
modelname=['Market','Best','BCRP','UP','EG','ONS','Anticor','BK','BNN','CORN-U','CORN-K1','CORN-K2','PMAR','PMAR-1','CWMR-Var','CWMR-Stdev','PMAR-2','OLMAR-1','OLMAR-2','DSR']
datalist=list(map(dataset,dataname))
# list(map(lambda i:i.brief(),datalist))
dataprices=list(map(lambda i:i.prices(),datalist))
# print(np.shape(dataprices[0]))
Slist=[]
for i in range(0,len(dataname)):
    tds,ns=np.shape(dataprices[i])
    Slist.append(np.zeros([len(modelname),tds+1]))
def allset(ni):

    if ni==0:AM=list(map(lambda i:Market(i,S=1.0),dataprices))
    if ni==1:AM=list(map(lambda i:Best(i,S=1.0),dataprices))
    if ni==2:AM=list(map(lambda i:BCRP(i,S=1.0),dataprices))

    if ni==3:AM=list(map(lambda i:UP(i,S=1.0),dataprices))
    if ni==4:AM=list(map(lambda i:EG(i,S=1.0,step=0.05),dataprices))
    if ni==5:AM=list(map(lambda i:ONS(i),dataprices))

    if ni==6:AM=list(map(lambda i:Anticor(i,S=1.0,windows=2),dataprices))
    if ni==7:AM=list(map(lambda i:BK(i,S=1.0,P=10,windows=5,C=1.0),dataprices))
    if ni==8:AM=list(map(lambda i:BNN(i,S=1.0,P=10,C=1.0,windows=5),dataprices))

    if ni==9:AM=list(map(lambda i:CORN(i,S=1.0,version='U',P=10,K=5,windows=5),dataprices))
    if ni==10:AM=list(map(lambda i:CORN(i,S=1.0,version='K1',P=10,K=50,windows=5),dataprices))
    if ni==11:AM=list(map(lambda i:CORN(i,S=1.0,version='K2',P=10,K=5,windows=5),dataprices))

    if ni==12:AM=list(map(lambda i:PAMR(i,S=1.0,version=0,profit=0.5),dataprices))
    if ni==13:AM=list(map(lambda i:PAMR(i,S=1.0,version=1,profit=0.5,C=500),dataprices))
    if ni==14:AM=list(map(lambda i:PAMR(i,S=1.0,version=2,profit=0.5,C=500),dataprices))

    if ni==15:AM=list(map(lambda i:CWMR(i,S=1.0,version='Var',profit=0.5,confidence=2.0),dataprices))
    if ni==16:AM=list(map(lambda i:CWMR(i,S=1.0,version='Stdev',profit=0.5,confidence=2.0),dataprices))

    if ni==17:AM=list(map(lambda i:OLMAR(i,S=1.0,version=1,windows=5,profit=10),dataprices))
    if ni==18:AM=list(map(lambda i:OLMAR(i,S=1.0,version=2,smooth=0.5,profit=10),dataprices))

    if ni==19:AM=list(map(lambda i:DSR(i),dataprices))
    list(map(lambda i:i.run(),AM))
    AS=list(map(lambda i:i.getS(),AM))
    for i in range(0,len(datalist)):
        Slist[i][ni]=AS[i]

chose=np.ones(len(modelname))
chose[[7,8,5,19]]=0
# chose=np.zeros(len(modelname))
# chose[[7,8]]=1
for i in range(0,len(modelname)):
    if chose[i]==1:allset(i)
for i in range(0,len(Slist)):
    np.savez('all S of '+dataname[i],data=Slist[i])
