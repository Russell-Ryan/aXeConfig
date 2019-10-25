import numpy as np


class Poly2d(object):
    def __init__(self,v,name=None):
        self.name=name
        self.coefs={}
        if isinstance(v,np.ndarray):
            count=int((np.sqrt(1+8*len(v))-1)/2)
            ii=0
            for j in range(count):
                for k in range(j+1):
                    self.coefs[(j-k,k)]=v[ii]
                    ii+=1
        else:
            self.coefs[(0,0)]=np.array([v])

            
                
    @property
    def order(self):
        return self.npar-1

    @property
    def npar(self):
        return len(self.coefs)
        
    def __str__(self):
        return self.name
        
    def __call__(self,x,y):

        #for coef in self.coefs:
        #print(list(zip(*x.keys())))
   
        #i,j=*list(zip(*self.coefs.keys()))
        #i=list(i)
        #j=list(j)
        #v=list(self.coefs.values())

        p=0. if np.isscalar(x) else np.zeros_like(x,dtype=float)

        for (i,j),v in self.coefs.items():
            p+=(v*x**i*y**j)
                       
        return p

     
class Poly1d(object):
#    def __init__(self,conf,key,beam):
#        self.name=key.lower()+'_'+beam.lower()
#        self.coefs=[]
#        for k,v in conf.items():
#            k=k.lower()
#            if k.startswith(key+'_'+beam.lower()):
#                self.coefs.append(Poly2d(k,v))
#        self.order=len(self.coefs)-1
    def __init__(self,h5,key):
        self.name=key
        hf=h5[self.name]
        self.coefs=[Poly2d(hf[order][()]) for order in hf]

        #self.coefs=[]
        #for order in hf:
        #    d=hf[order][()]
        #    self.coefs.append(Poly2d(d))
            
    @property
    def order(self):
        return len(self.coefs)-1
            
    def __str__(self):
        return '{}: order={}'.format(self.name,self.order)

    def __call__(self,x,y,order=None):
        if order is None:
            #for coef in reversed(self.coefs):
            #    print(self.name,coef(x,y))
            
            p=np.array([coef(x,y) for coef in reversed(self.coefs)])
        else:
            #coef=self.coefs[order]
            #p=coef(x,y)
            p=self.coefs[order](x,y)
        return p
    
                
