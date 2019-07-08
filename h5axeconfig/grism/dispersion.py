import numpy as np

from .base import Base
from .polynomials import Poly1d

class Dispersion(Base):
    def __init__(self,h5):#conf,beam):
        Base.__init__(self,h5)
        
        self.dldp=Poly1d(h5,'dispersion')
        assert (self.dldp.order >0),"Invalid dispersion model"
            
        
    def arclength(self,l,x0,y0):
        ''' compute the arclength along the trace '''
        assert (x0.shape==y0.shape),"Invalid (x,y) pairs."
        
        dldp=self.dldp(x0,y0)

        
        if self.dldp.order==1:
            # first order dispersion can be analyticall inverted
            b=dldp[1]
            m=dldp[0]
                        
            s=(l[:,None]-b)/m
        else:
            # higher order dispersions must be numerically inverted
            dldp=list(zip(*dldp))
            s=np.zeros((len(l),len(dldp)))
            for i,coef in enumerate(dldp):
                for j,lam in enumerate(l):
                    this=np.copy(coef)     # save the coefs
                    this[-1]-=lam          # remove the lam to find lam=lam(s)
                    roots=np.roots(this)   # find the solution

                    # the first real root
                    phases=np.angle(roots)
                    g=np.where((np.abs(phases) <= thr) | \
                               (np.abs(phases-np.pi) <= thr))[0]
                    if len(g) ==0:
                        raise ValueError('unable to invert polynomial')
                    else:
                        s[j,i]=np.amin(roots[g]).real


        return s


    #def wavelength(self,s,x0,y0):
    #    ''' compute the wavelength from the arclength '''
    #    assert (x0.shape==y0.shape),"Invalid (x,y) pairs."
    #
    #    
    #    return l


    def __call__(self,x0,y0):
        ''' return the dispersion (first order term) at some position '''

        return self.dldp(x0,y0,order=1)
