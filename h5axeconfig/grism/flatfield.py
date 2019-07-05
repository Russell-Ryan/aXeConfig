import h5py
import numpy as np

from ..utils import h5Attr



class FlatField(object):
    def __init__(self,h5file):
        self.h5file=h5file
        self.detectors={}
        
        if self.h5file is None:
            self.func=self.unity
        else:
            self.func=self.polynomial
            try:
                with h5py.File(self.h5file,'r') as h5:
                    for detname in h5:
                        group=h5[detname]
                        self.order=h5Attr(group,'order')
                        self.wmin=h5Attr(group,'wmin')
                        self.wmax=h5Attr(group,'wmax')
                        
                        data=[group[str(i)][:] for i in range(self.order+1)]
                        self.detectors[detname]=np.array(data)
            except:
                print("unable to load HDF5 flat field {}".format(self.h5file))
                self.func=self.unity
            
    def __str__(self):
        out='Grism Flat Field\n'
        out+='file: {}\n'.format(self.h5file)
        out+='func: {}\n'.format(self.func)
        return out                    
        
    def __call__(self,x,y,l,d):
        return self.func(x,y,l,d)

    def unity(self,x,y,l,d):
        return np.ones_like(l,dtype=np.float)

    def polynomial(self,x,y,l,d):
        
        ll=(np.array(l)-self.wmin)/(self.wmax-self.wmin)
        ff=np.zeros_like(x,dtype=np.float)
        
        for i,c in enumerate(self.detectors[d]):
            ff+=(c[y,x]*np.power(ll,i))

        return ff


#if __name__=='__main__':
#    path='/Users/rryan/Python/Russell-Ryan/h5axeconfig/data/'
#    ff=FlatField(path+'hst_wfc3_ir_flat.h5')
#    
#    
#    x=[1,2,3]
#    y=[4,5,6]
#    l=[8000.,9000.,10000.]
#    print(ff(x,y,l,'IR'))


    
    
