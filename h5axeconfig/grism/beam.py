'''
The beam class, which contains the trace, dispersion, and sensitivity.

'''

import numpy as np
import os
import pdb

from .base import Base
from .trace import Trace
from .dispersion import Dispersion
from .sensitivity import Sensitivity
from ..utils import h5Attr


class Beam(Base):
    __INT__=np.uint64
    
    def __init__(self,h5,clip,xr=[-np.inf,np.inf],yr=[-np.inf,np.inf]):
        ''' Read the aXe-like configuration data from an h5 file.

        Parameters
        ----------
        h5 : h5-like dict
           h5-like dictionary from which to get the beam info

        clip : polyclip
           polyclipping module from R. Ryan library

        xr,yr : np.array([2])
           array to specify the max range for this beam to disperse onto 
           a detector.  DEFAULT = [-inf,inf]

        '''
        

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
        ''' Overload the pring function. '''
        
        msg='Grism beam object:\n(beam,order)=({},{})'
        return msg.format(self.beam,self.order)


    def applyPixfrac(self,xd,yd,pixfrac):
        ''' Shrink a pixel by pixfrac.

        Paramters
        ---------
        xd,yd : np.array
           array of x-coordinates
        pixfrac : float
           amount by which to shrink the area of a pixel

        Returns
        -------
        x,y : np.array
           array of output x-coordinates.  same shape as xd
        '''

        # force pixfrac to be in range
        #pixfrac=max(min(pixfrac,1.),0.01)
        p=np.sqrt(pixfrac)
        
        x=p*xd+(1.-p)*np.mean(xd)
        y=p*yd+(1.-p)*np.mean(yd)

        return x,y
        
    def specDrizzle(self,xd,yd,lamb,ignore='average',pixfrac=1.):
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

        # shrink the pixel according to the pixfrac
        #xd,yd=self.applyPixfrac(xd,yd,pixfrac)

        # convert from (x0,y0) & lamb to (xg,yg,lamb) triplets
        xg,yg=self.xyd2xyg(xd,yd,lamb)
        
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
        ''' Compute the wavelengths given a coordinate and subsampling

        Parameters
        ----------
        x,y : float
            coordinate pair

        nsub : int
            subsampling intervals.  Should be positive.
        
        Returns
        -------
        wave : np.array
            wavelengths from min/max range of the sensitivity curve sampled
            at the native dispersion divided by the `nsub` frequency.
        '''

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

        
    
