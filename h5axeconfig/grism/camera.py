''' container class for a grism camera '''
import h5py
import os
import pkgutil

from .detector import Detector
from ..utils import h5Attr,resolveFile

class Camera(object):
    
    def __init__(self,conffile,grism,detectors=None,beams=None,path=None):
        self.conffile=conffile
        fullfile=resolveFile(self.conffile,path=path)

        with h5py.File(fullfile,'r') as h5:
            self.telescope=h5Attr(h5,'telescope')
            self.instrument=h5Attr(h5,'instrument')
            self.camera=h5Attr(h5,'camera')
            self.grism=grism
            self.bandpass=None


            # read the detectors
            self.detectors={}

            
            if detectors is None:
                for detname in h5:
                    self.detectors[detname]=Detector(h5[detname],grism,\
                                                     beams=beams)
            else:
                if not isinstance(detectors,(list,tuple)):
                    detectors=[detectors]
                    
                for detname in detectors:
                    try:
                        self.detectors[detname]=Detector(h5[detname],grism,\
                                                         beams=beams)
                    except:
                        raise KeyError("Detector {} not found.".format(detname))

                    
                
            if not self.detectors:
                raise RuntimeError("No detectors found in config file")


    def __str__(self):
        out='Grism Camera calibration:\n'
        for x in ['telescope','instrument','camera','grism']:
            out=out+'{:>12}: {}'.format(x,getattr(self,x))+'\n'
        #out=out+"{:>12}: {}".format('detectors',len(self))+'\n'
        label='detectors:'
        for detname,det in self.detectors.items():
            for beamname,beam in det:
                out=out+"{:>13}  {}: {},{}".format(label,detname,\
                                                   beamname,beam.order)+'\n'
                detname=' '*len(detname)
                label=' '*len(label)
            
        return out
    
    def __len__(self):
        return len(self.detectors)

    def items(self):
        return self.detectors.items()

    
    #def __iter__(self):
    #    for detname,detector in self.detectors.items():
    #        for beamname,beam in detector:
    #            yield (detname,beamname),beam

    def __iter__(self):
        for detname,detector in self.detectors.items():
            yield detname,detector

    
    def __contains__(self,detector):
        return detector in self.detectors

    @property
    def beams(self):
        beams=[]
        for name,det in self:
            beams=[b for b,c in det]

            
        out=sorted(set(beams),key=beams.index)
        return out
            
    def __getitem__(self,detector):
        return self.detectors[detector]
        #print(detector)
        #print(self.detectors.keys())

        #try:
        #    return self.detectors[detector]
        #except:
        #    raise KeyError("Detector ({}) is not found".format(detector))

    
if __name__=='__main__':
    conf=Camera('/Users/rryan/LINEAR/config/HST/WFC3/IR/G102/hst_wfc3_ir_g102.h5')

#    q=next(conf)
#    print(q)
    #print(conf['IR']['A'].trace)

    for (det,beam),obj in conf:
        print(det,beam,obj)
