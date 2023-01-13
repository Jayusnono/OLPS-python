import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
dataname=['nyse-o','nyse-n','tse','sp500','msci','djia']
modelname=['Market','Best','BCRP','UP','EG','ONS','Anticor','BK','BNN','CORN-U','CORN-K1','CORN-K2','PMAR','PMAR-1','CWMR-Var','CWMR-Stdev','PMAR-2','OLMAR-1','OLMAR-2','DSR']
chose=np.ones(len(modelname))
chose[[3,7,8,5,19]]=0
markers=['+','*',',','o','.','s','p','P','h','H','x','X','d','D','1','2','3','4','8']
l=[]
for i in range(0,len(dataname)):
    l.append(np.load('all S of '+dataname[i]+'.npz')['data'])
    print(l[i].T[-1])
# plt.figure()
# plt.rcParams['font.sans-serif']='SimHei'
# pn=len(dataname)
# axl=[]
# for i in range(0,pn):
#     alldata=l[i]
#     mn,tds=np.shape(alldata)
#     plt.subplot(3,2,i+1)
#     plt.title(dataname[i])
#     # plt.ylim(0,)
#     plt.yscale('log')
#     plt.xlim(0,tds)
#     plt.xlabel('交易天数')
#     plt.ylabel('累积财富')
#     mn,tds=np.shape(l[i])
#     cy=math.floor(tds/10)
#     for j in range(0,mn):
#         if chose[j]==1:
#             x=[z for z in range(0,tds,cy)]+[tds-1]
#             y=alldata[j][x]
#             plt.plot(x,y,marker=markers[j],label=modelname[j])
# plt.legend(loc='lower right', bbox_to_anchor=(1,-0.5),borderaxespad=0,ncol=8) 
# plt.show()

# top=0.96,
# bottom=0.14,
# left=0.435,
# right=0.9,
# hspace=0.31,
# wspace=0.235











# plt.figure()
# plt.rcParams['font.sans-serif']='SimHei'
# x=range(0,tds,50)
# for i in range(0,mn):
#     if chose[i]==1:
#         y=alldata[i][x]
#         plt.plot(x,y,marker=,label=modelname[i])
# plt.legend('y1=1','y2=2')
# plt.title(dataname[k])
# plt.xlabel('交易天数')
# plt.ylabel('累积财富')
# xml=plt.MultipleLocator(100)
# yml=plt.MultipleLocator(1)
# ax=plt.gca()
# ax.xaxis.set_major_locator(xml)
# ax.yaxis.set_major_locator(yml)
# plt.ylim(0,3)
# plt.xlim(1,tds)
# # plt.legend(loc='lower center',bbox_to_anchor=(2,2),borderaxespad=0.)
# plt.legend(loc='lower center')
# plt.show()