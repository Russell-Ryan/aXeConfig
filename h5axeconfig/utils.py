import h5py
import numpy as np
import os


def resolveFile(filename,path=None):
    ''' get a filename to a config file based the hardcoded path 

    Parameters
    ----------
    filename : str
        filename to the h5 reference file

    path : str
        relative path to the h5 file.  default is './'
    
    Returns
    -------
    fullfile : str
         fully resolved path
    
    '''
        
    if path is None:
        path,theFile=os.path.split(__file__)
        path=os.path.join(path,'data')

    fullfile=os.path.join(path,filename)
    return fullfile



def detectorData(filename,*args):
    ''' get the detector data

    This reads the groups in the h5 file (e.g. detector name) and 
    returns the data with that group.

    Parameters
    ----------
    filename : str 
        name of the h5 config file

    *args : tuple
        which items to read
    '''


    fullfile=resolveFile(filename)
    
    det={}
    with h5py.File(fullfile,'r') as h5:
        h5g=list(h5.values())[0]   # just check the first grism 
        for detname,h5d in h5g.items():
            det[detname]=tuple(h5Attr(h5d,arg) for arg in args)

    return det


def h5Attr(h5,key):
    ''' Extract an attribute from the h5 and retype it 

    Parameters
    ----------

    h5 : h5 dictionary
        The dictionary from an open h5 file.

    key : str
        A string to parse out of the dictionary, this module will
        retype strings.

    Returns
    -------
    val : str, int, float, np.array
        The datum associated with that keyword entry, the type is not 
        known until the key is read.
    '''
    
    
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
        """ Vectorized method to solve non-linear equations with 
            Newton's method 

        This method is deprecated, but works just fine. It solves
        a set of non-linear equations using Newton's method, but where
        the system fo equations is itself a vector.  For example
        
        y0 = a + b * x0 + c * x0^2
        y1 = d + e * x1 + f * x1^2
        
        where (y0,y1) and (a,b,c,d,e,f) are known, and you want to find 
        (x0,x1).
        """

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
        
