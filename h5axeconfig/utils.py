import h5py
import numpy as np
import os


def resolveFile(filename,path=None):
    ''' get a filename to a config file based the hardcoded path '''
    if path is None:
        path,theFile=os.path.split(__file__)
        path=os.path.join(path,'data')

    fullfile=os.path.join(path,filename)
    return fullfile



def detectorData(filename,*args):
    fullfile=resolveFile(filename)
    
    det={}
    with h5py.File(fullfile,'r') as h5:
        h5g=list(h5.values())[0]   # just check the first grism 
        for detname,h5d in h5g.items():
            det[detname]=tuple(h5Attr(h5d,arg) for arg in args)

    return det


def h5Attr(h5,key):
    ''' Extract an attribute from the h5 and retype it '''
    
    try:
        val=h5.attrs[key]
        if isinstance(val,np.bytes_):
            val=val.decode('utf-8')
            low=val.lower()
            if low =='none':
                val=None
            elif low == 'true':
                val=True
            elif low == 'false':
                val=False
            else:
                pass
        else:
            pass
    except:
        val=None
    return val



def vNewton(funct,deriv,x0,itmax=1000,tolerance=1e-3,**kwargs):
        ''' Vectorized method to solve non-linear equations with 
            Newton's method '''

        # store the output and perturbations
        x=np.copy(x0)
        dx=np.zeros_like(x0)

        itn=0                                     # number of iterations
        g=np.where(np.abs(dx) >= tolerance)[0]
        while g.size != 0 and itn != itmax:
            num=funct(x[g],**kwargs)              # the function call
            den=deriv(x[g],**kwargs)              # the derivative call

            # compute perturbations and new positions
            dx[g]=num/den
            x[g]-=dx[g]

            # update the counter and elements to iterate on
            itn+=1
            g=np.where(np.abs(dx)>=tolerance)[0]

        if itn == itmax:
            print("Warning> max iterations reached.")

        return x,itn



if __name__=='__main__':
    with h5py.File('../data/hst_wfc3_ir_beams.h5','r') as h5:
        v=getAttr(h5['IR']['G102'],'nbeam')
        print(v,type(v))
        
