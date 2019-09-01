import numpy as np
import os

from .base import Base
from .trace import Trace
from .dispersion import Dispersion
from .sensitivity import Sensitivity
from ..utils import h5Attr


class Beam(Base):
    __INT__=np.uint64
    
    def __init__(self,h5,clip,xr=[-np.inf,np.inf],yr=[-np.inf,np.inf]):
        Base.__init__(self,h5)
        
        # the dispersion order
        self.order=h5Attr(h5,'order')

        # load the beam primatives
        self.trace=Trace(h5)
        self.dispersion=Dispersion(h5)
        self.sensitivity=Sensitivity(h5)
        
        # save the clipper and the ranges of the detector
        self.polyclip=clip
        self.xr=xr
        self.yr=yr        
        
        # record this
        self.naxis=self.polyclip.naxis

        
    def __str__(self):
        msg='Grism beam object:\n(beam,order)=({},{})'
        return msg.format(self.beam,self.order)

        
    def specDrizzle(self,xd,yd,lamb,ignore='minmax'):
        ''' run the polyclip to get the fractional pixel areas '''

        # output data products
        xyg=[]
        lam=[]
        val=[]
        
        # ignore the pixel if it is outside the bounding box.  
        ignore=ignore.lower()
        if ignore=='average':
            # if average of pixel is in bounding box
            xave=np.average(xd)
            yave=np.average(yd)
            if (xave<self.xr[0]) or (xave>self.xr[1]) or \
               (yave<self.yr[0]) or (yave>self.yr[1]):
                return xyg,lam,val
        elif ignore=='minmax':
            # test min/max in range
            x0,x1=np.amin(xd),np.amax(xd)
            y0,y1=np.amin(yd),np.amax(yd) 
            if (x1<self.xr[0]) or (x0>self.xr[1]) or \
               (y1<self.yr[0]) or (y0>self.yr[1]):
                return xyg,lam,val
        else:
            pass
        
        # convert from (x0,y0) & lamb to (xg,yg,lamb) triplets
        xg,yg=self.xyd2xyg(xd,yd,lamb)

        print('[debug]Put pixfrac here')
        
        # clip against the edge
        xg=np.clip(xg,0,self.naxis[0])
        yg=np.clip(yg,0,self.naxis[1])
        
        # run the polygon clipper
        x,y,area,indices=self.polyclip(xg,yg)
        
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

        
    
