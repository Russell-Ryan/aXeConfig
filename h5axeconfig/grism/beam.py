import numpy as np
import os

from .base import Base
from .trace import Trace
from .dispersion import Dispersion
from .sensitivity import Sensitivity
from ..utils import h5Attr


class Beam(Base):
    __INT__=np.uint64
    
    def __init__(self,h5,clip):
        Base.__init__(self,h5)

        
        # the dispersion order
        self.order=h5Attr(h5,'order')

        # load the beam primatives
        self.trace=Trace(h5)
        self.dispersion=Dispersion(h5)
        self.sensitivity=Sensitivity(h5)
        
        # build the clipper
        self.polyclip=clip

        # record this
        self.naxis=self.polyclip.naxis

        
    def __str__(self):
        return 'Grism beam object:\n(beam,order)=({},{})'.format(self.beam,self.order)

        
    def specDrizzle(self,xd,yd,lamb):
        ''' run the polyclip to get the fractional pixel areas '''

        
        # convert from (x0,y0) & lamb to (xg,yg,lamb) triplets
        xg,yg=self.xyd2xyg(xd,yd,lamb)

        #print("beamconf> put in pix frac here")
        #print(np.amin(xg),np.amax(xg))
        #print(np.amin(yg),np.amax(yg))
        
        
        # clip against the edge
        xg=np.clip(xg,0,self.naxis[0])
        yg=np.clip(yg,0,self.naxis[1])

                
        
        # run the polygon clipper
        x,y,area,indices=self.polyclip(xg,yg)

        
        # output data products
        xyg=[]
        lam=[]
        val=[]

        # only continue if there drizzled pixels
        if len(x) != 0:
            pix=x.astype(self.__INT__)+self.naxis[0]*y.astype(self.__INT__)
            
            # process each wavelength
            for j,l in enumerate(lamb):
                j0,j1=indices[j],indices[j+1]
                if j1 > j0:
                    xyg.extend(pix[j0:j1])
                    lam.extend(list(np.full(j1-j0,j)))
                    val.extend(area[j0:j1])
        return xyg,lam,val
            
    def wavelengths(self,x,y,nsub):
        disp=np.abs(self.dispersion(x,y))/nsub
        delta=self.sensitivity.wmax-self.sensitivity.wmin
        
        nwave=int(delta/disp)+2
        dwave=delta/(nwave-1.)
        
        wave=np.arange(nwave)*dwave+self.sensitivity.wmin
        return wave
        

    
    def xyd2xyg(self,xd,yd,lamb):
        ''' convert the (x,y) pair in the equivalent direct image FLT to a 
            a collection of (x,y) pairs on a grism image at a collection of 
            wavelengths '''

        # compute the arclength from the dispersion model
        s=self.dispersion.arclength(lamb,xd,yd)

        # compute the grism (x,y) pairs along the trace
        xg,yg=self.trace(s,xd,yd)

        return xg,yg

        
    
