import h5py
import numpy as np

from ..utils import h5Attr

class FlatField(object):
    def __init__(self,h5file,detector):
        with h5py.File(h5file,'r') as h5:
            if detector in h5:
                d=h5[detector]
                self.h5file=h5file
                self.detector=detector
                self.flattype=h5Attr(d,'type')

                if self.flattype=='polynomial':
                    self.wmin=h5Attr(d,'wmin')
                    self.wmax=h5attr(d,'wmax')
                    self.func=self._polynomial
                else:
                    self.func=self._unity
                    
                # read the coefficients
                self.coefs=[d[str(i)][:] for i in range(d.attrs['order']+1)]
                
    def __call__(self,x,y,l):
        assert x.shape == y.shape
        assert l.shape == x.shape
        return self.func(x,y,l)

    def _unity(self,x,y,l):
        return np.ones_like(l)

    def _polynomial(self,x,y,l):
        ll=(l-self.wmin)/(self.wmax-self.wmin)
        ff=np.zeros_like(l)
        for i,coef in enumerate(self.coefs):
            ff+=(coef[y,x]*ll**i)
        return ff

    def __str__(self):
        out='Grism Flat-Field:\n'
        out+='{:>12} {}\n'.format('file',self.h5file)
        out+='{:>12} {}\n'.format('detector',self.detector)
        out+='{:>12} {}\n'.format('type',self.flattype)
        return out


                
if __name__=='__main__':
    f='/Users/rryan/LINEAR/config/HST/WFC3/IR/G102/hst_wfc3_ir_flat.h5'

    q=GrismFF(f,'IR')
    print(q)
    print(q(np.array(1).astype(int),np.array(2).astype(int),np.array(10000.)))
