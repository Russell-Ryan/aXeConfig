import os
import h5py
from collections import OrderedDict


from ..utils import h5Attr
from .detector import Detector

class SIAF(object):
    def __init__(self,siaffile,path=None):
        self.siaffile=siaffile
        
        # this is hard-coded w.r.t. h5axeconfig
        if path is None:
            path,FILE=os.path.split(__file__)
            path=os.path.join(path,'..','..','data')
            
        fullfile=os.path.join(path,siaffile)

        self.detectors=OrderedDict()

        with h5py.File(fullfile,'r') as h5:
            self.telescope=h5Attr(h5,'telescope')
            self.instrument=h5Attr(h5,'instrument')
            self.camera=h5Attr(h5,'camera')
            
            for detname in h5:
                self.detectors[detname]=Detector(h5[detname])

        self.setReference(0)

                
    def setReference(self,ref):
        
        # update with reference positions
        update=True
        if isinstance(ref,int):
            refdet=self.index(ref)
            V2ref,V3ref=refdet.V2,refdet.V3
        elif isinstance(ref,str):
            refdet=self.detectors[ref]
            V2ref,V3ref=refdet.V2,refdet.V3
        elif isinstance(ref,function):
            V2,V3=[],[]
            for det in self.detectors.items():
                V2.append(det.V2)
                V3.append(det.V3)
            V2ref,V3ref=ref(np.array(V2)),ref(np.array(V3))
        else:
            update=False
            
            
        if update:
            for k,v in self.detectors.items():
                v.V2ref=V2ref
                v.V3ref=V3ref


    def index(self,i):
        keys=list(self.detectors.keys())
        return self.detectors[keys[i]]
                
    def __len__(self):
        return len(self.detectors)

    def __iter__(self):
        for k,v in self.detectors.items():
            yield k,v

    def __contains__(self,k):
        return k in self.detectors
            
    def __str__(self):
        out='SIAF: {} {} {}\n'.format(self.telescope,self.camera, self.instrument)
        out=out+'{} detectors'.format(len(self))
        return out
