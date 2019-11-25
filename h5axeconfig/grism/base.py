import numpy as np
import os

''' 
Base class for h5axeconfig package.

Code is based on the standard aXe configuration polynomials, but repackaged
in the h5 format by Russell Ryan.  This format works better (than the 
ascii-based system) for dealing with instruments with multiple detectors 
(e.g. WFIRST).
'''


class Base(object):
    """ Base class for h5axeconfig objects. """
    
    def __init__(self,h5):
        ''' Load the h5axeconfig module
        
        Parameters
        ----------
        h5 : h5-like dictionary
           This establishes the name of the base class
        '''

        self.beam=os.path.split(h5.name)[1]

    def __str__(self):
        ''' Simple overloading of the print function '''
        
        
        return '{} for beam: {}'.format(self.__class__.__name__,self.beam)

