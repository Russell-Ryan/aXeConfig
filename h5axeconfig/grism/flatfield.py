import h5py
import numpy as np

from ..utils import h5Attr



class FlatField(object):
    def __init__(self,h5file,grism):
        self.h5file=h5file
        
        if self.h5file is None:
            self._order=None
            self.func=self.unity
        else:
            self.func=self.polynomial
            try:
                with h5py.File(self.h5file,'r') as h5:

                    grismgrp=h5[grism]
                    self.wmin=h5Attr(grismgrp,'wmin')
                    self.wmax=h5Attr(grismgrp,'wmax')
                    self.order=h5Attr(grismgrp,'order')
                    self.powers=np.arange(self.order+1)
                    
                    # read all the data
                    self.detectors={det:grismgrp[det][:] for det in grismgrp}
                    
                    #self.detectors={}
                    #for detname in grismgrp:
                    #    self.detectors[detname]=grismgrp[detname][:]

                        
                        #group=h5[detname]
                        #self.order=h5Attr(group,'order')
                        #self.wmin=h5Attr(group,'wmin')
                        #self.wmax=h5Attr(group,'wmax')
                        
                        #data=[group[str(i)][:] for i in range(self.order+1)]
                        #self.detectors[detname]=np.array(data)
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
        n=len(x)
        assert (n==len(y)==len(l)),'Invalid flatfield triplet'
        
        ll=(np.array(l)-self.wmin)/(self.wmax-self.wmin)

        data=self.detectors[d]
        data=data[y,x,:]
        

        q=np.power(np.broadcast_to(ll,(self.order+1,n)).T,self.powers)

        ff=np.sum(data*q,axis=1)

        
        #ff2=np.zeros_like(x,dtype=np.float64)
        #data=self.detectors[d]
        #for i,(xx,yy,lll) in enumerate(zip(x,y,ll)):
        #    dd=np.flip(data[yy,xx,:],axis=0)
        #    ff2[i]=np.polyval(dd,lll)


        #ff=np.zeros_like(x,dtype=np.float)
        #
        #for i,c in enumerate(self.detectors[d]):
        #    ff+=(c[y,x]*np.power(ll,i))

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


    
    
