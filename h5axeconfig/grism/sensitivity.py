import numpy as np
#from astropy.io import fits
import os

from .base import Base

class Sensitivity(Base):
    def __init__(self,h5):
        Base.__init__(self,h5)

        hf=h5['sensitivity']        
        self.wavelength=hf['wavelength']
        self.sensitivity=hf['sensitivity']
        self.error=hf['error']

        # compute the range
        g=np.where(self.sensitivity != 0.)
        self.wmin=np.amin(self.wavelength[g])
        self.wmax=np.amax(self.wavelength[g])


        
    def __call__(self,l,left=0.,right=0.):
        s=np.interp(l,self.wavelength,self.sensitivity,left=left,right=right)
        return s
        
    def __mul__(self,a):
        self.sensitivity*=a
        self.error*=a
        return self

    def __rmul__(self,a):
        return self.__mul__(a)


    
    @property
    def average(self):
        return np.average(self.sensitivity)
