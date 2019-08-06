''' a container class for a detector '''

import h5py
import numpy as np


import polyclip
from .beam import Beam
from ..utils import h5Attr

class Detector(object):
    def __init__(self,h5,beams='all'):
        
        # get the name of the detector
        self.detector=h5.name[1:]

        # get a few properties 
        self.extver=h5Attr(h5,'extver')
        self.sciext=h5Attr(h5,'science_ext')
        self.uncext=h5Attr(h5,'errors_ext')
        self.dqaext=h5Attr(h5,'dq_ext')
        

        self.naxis=h5Attr(h5,'naxis')
        self.xr=h5Attr(h5,'xrange')
        self.yr=h5Attr(h5,'yrange')
        
        # define a polygon clipper
        self.clip=polyclip.Polyclip(self.naxis)

        # read the grism
        #try:
        #h5g=h5[grism]
            #self.lamb0=h5Attr(h5g,'lamb0')
            #self.lamb1=h5Attr(h5g,'lamb1')
            #self.dlamb=h5Attr(h5g,'dlamb')
        #except:
        #    raise KeyError("Grism {} not found.".format(grism))


        
        # read the beams
        self.beams={}
        if beams is not None:
            if beams == 'all':
                for bm in h5:
                    self.beams[bm]=Beam(h5[bm],self.clip)
            else:
                if np.isscalar(beams):
                    self.beams[beams]=Beam(h5[beams],self.clip)
                else:
                    for bm in beams:
                        self.beams[bm]=Beam(h5[bm],self.clip) 

        #if beams is None:
        #    for beamname in h5g:
        #        self.beams[beamname]=Beam(h5g[beamname],self.clip)
        #else:
        #    if not isinstance(beams,(list,tuple)):
        #        if beams =='':
        #            return
        #        else:
        #            beams=[beams]
        #    for beamname in beams:
        #        try:
        #            self.beams[beamname]=Beam(h5g[beamname],self.clip)
        #        except:
        #            raise KeyError("Beam {} not found.".format(beamname))
                
        #if not self.beams:
        #    raise RuntimeError("No valid beams found in camera")

    def _fitsExtension(self,data):
        if isinstance(data,np.ndarray):
            if len(data)==2:
                extname=data[0]
                try:
                    extver=int(data[1])
                except:
                    raise ValueError("invalid fits extension")
                out=(extname,extver)                
            else:
                raise ValueError("invalid fits extension")
        elif isinstance(data,np.bytes_):
            out=data.decode('utf-8')
        else:
            raise ValueError("invalid fits extension")

        return out

    def values(self):
        return list(self.beams.values())
    
    def beamOrder(self,order):
        for name,beam in self.beams.items():
            if beam.order == order:
                return name
            
    def __len__(self):
        return len(self.beams)
    
    def __str__(self):
        out='Grism Detector calibration:\n'
        out=out+'{:>4} {:>5}'.format('beam','order')+'\n'
        for k,v in self.beams.items():
            out=out+'{:>4} {:>5}'.format(k,v.order)+'\n'
        return out
    
    def __iter__(self):
        yield from self.beams.items()

    def __contains__(self,beam):
        return beam in self.beams
        
    def __getitem__(self,beam):
        if isinstance(beam,str):
            if beam in self.beams:
                return self.beams[beam]
            else:
                raise KeyError("Beam {})is not found!".format(beam))
        elif isinstance(beam,int):
            name=self.beamOrder(beam)
            if name is not None:
                return self.beams[name]
            else:
                raise KeyError("Order {} is not found!".format(beam))
