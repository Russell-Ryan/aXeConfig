import h5py
import numpy as np


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
        
