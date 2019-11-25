import numpy as np
import os


from .base import Base
from .polynomials import Poly1d


class Trace(Base):
    def __init__(self,h5):
        '''Load aXe-like trace data for a given beam.

        Parameters
        ----------
        h5 : h5-like dict
           Dictionary to read the parameters `xoff`, `yoff`, and `trace` 
           from, each of which is an aXe-like polynomial


        This class computes the position of a grism trace that is
        represented as a polynomial in x, but this requires
        computing/inverting arclength definitions.  For certain
        orders, the arclength computations are analytic, and in which
        case those are used for performance.  For higher order terms,
        a closed form cannot be found and/or inverted, therefore these
        evaluations are performed computationally (which is likely
        much slower). 

        '''
        
        
        Base.__init__(self,h5)

        self.xoff=Poly1d(h5,'xoff')
        self.yoff=Poly1d(h5,'yoff')
        self.dydx=Poly1d(h5,'trace')

    def slope(self,x0,y0):
        ''' Computes the slope of the trace.

        Parameters
        ----------
        x0,y0 : float
            coordinate pair where to compute the slope.

        Returns
        -------
        m : float
            slope in pixel per pixel
        '''
        
        return self.dydx(x0,y0,order=1)
    
    def _arcLengthIntegrand(self,x,ones=None,poly=None,arc=None):
        ''' helper function to compute the integrand of the arclength

        This method is not intended to be used on its own.
        '''
        

        p=np.polyval(poly,x)
        y=np.sqrt(1.+p*p)
        return y 

    def _arcLength(self,x,ones=None,poly=None,arc=None):
        ''' helper function to compute the arglength
        
        This method is not intended to be used on its own.
        '''

        xx=ones[:,None]*x
        yy=self._arcLengthIntegrand(xx,poly)
        delta=np.trapz(yy,xx,axis=0)-arc
        return delta
        
    def _xTrace(self,s,coef):
        ''' invert arclength definition to get x on the trace 
        
        This method is not intended to be used on its own.
        '''
        
        if self.dydx.order ==0:
            raise NotImplementedError
        elif self.dydx.order == 1:
            m=coef[0]
            x=s/np.sqrt(1.+m*m)
        else:

            N=101        # to do the trapezoidal integration
            ones=np.linspace(0,1,N)

            # output x coordinates
            x=np.zeros_like(s)
            
            # use the first order as the initial guess
            slope=coef[-2]

            
            dydx=list(zip(*coef))
            for i,c in enumerate(dydx):
                # compute the derivative of the coeffiecents
                dc=coef*np.arange(len(c))
                poly=np.flip(dc[1:],0)

                arc=s[:,i]
                
                x0=arc/np.sqrt(1.+slope*slope)

                x[:,i]=self.vNewton(self._arcLength,self._arcLengthIntegrand,\
                                    x0,poly=poly,ones=ones,arc=arc)
                                    
                           
                           
        return x
        
        
    def _yTrace(self,x,coef):
        ''' evaluate the trace to get the y-position
        
        This method is not intended to be used on its own.
        '''


        ''' apply trace to get y '''
        y=np.zeros_like(x)
        for i,c in enumerate(reversed(coef)):
            y+=(c*x**i)
        return y

        
    def __call__(self,s,x0,y0):
        ''' return the x,y pairs along the trace for a set of arclengths 
        
        Parameters
        ----------
        s : np.array
           the arclength for which to compute the trace

        x0,y0 : float
           the pixel coordinate for where to compute the trace

        Returns
        -------
        x,y : np.array
           the spectral trace
        '''

        assert(x0.shape==y0.shape)

        
        # compute the trace polynomial and save it
        coef=self.dydx(x0,y0)
        
        # compute the trace positions
        xhat=self._xTrace(s,coef)
        yhat=self._yTrace(xhat,coef)
        
        # compute the offsets
        xoff=self.xoff(x0,y0)
        yoff=self.yoff(x0,y0)
        
        # add back the ooffsets
        x=np.zeros_like(xhat)
        y=np.zeros_like(yhat)
        for i in range(len(x0)):
            x[:,i]=xhat[:,i]+xoff[:,i]+x0[i]
            y[:,i]=yhat[:,i]+yoff[:,i]+y0[i]
                    

        return x,y
                         
    


    
