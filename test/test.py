import h5axeconfig
import numpy as np

# set the inputs
beamfile='hst_wfc3_ir_beams.h5'
grism='G102'
nx=1014     # number of x-pixels

# read the configuration
conf=h5axeconfig.Camera(beamfile,grism)


# define a pixel in the pre-image
xd=np.array([55,55,56,56],dtype=np.float)
yd=np.array([78,79,79,78],dtype=np.float)

# define a set of wavelengths
l=np.arange(7000,12001,1.)

# iterate over the detectors in this camera
for detname,detconf in conf:

    # iterate over beams in this detector
    for beamname,beamconf in detconf:

        # compute where those pixel corners land as a function of wavelength
        xg,yg=beamconf.xyd2xyg(xd,yd,l)

        
        # instead, let's drizzle the pixels
        xyg,lam,val=beamconf.specDrizzle(xd,yd,l)

        # xyg = 1d pixel index
        # lam = indices of l
        # val = area of overlap

        
        # check if there are valid pixels:
        if len(xyg)!=0:        
            # decompose the xyg (1d pixel index) into x,y pairs
            y,x=np.divmod(xyg,nx)








            
#siaf=h5axeconfig.SIAF('hst_wfc3_ir_detector.h5')
#h=siaf.detectors['IR'].mkhdr((189.1792282504428,62.28646067642324),131.924)

