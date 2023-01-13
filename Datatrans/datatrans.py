import scipy.io as scio
import h5py
import numpy as np
class dataset():
    def __init__(self,key):
        self.name=key
        self.road='./data/'+key+'.mat'
        try:self.price=scio.loadmat(self.road)['data']
        except NotImplementedError:self.price=np.transpose(h5py.File(self.road)['data'])
        self.tradedays,self.stocknum=np.shape(self.price)
    def brief(self):
        print("数据集:",self.name,"交易天数:",self.tradedays,"股票数量:",self.stocknum)
    def prices(self):
        return self.price

# tt=dataset(key='nyse-o')
# yy=dataset(key='nyse-n')
# tt.brief()
# yy.brief()