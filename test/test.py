import h5axeconfig


#f='/Users/rryan/Python/Russell-Ryan/h5axeconfig/data/hst_wfc3_ir_beams.h5'
f='hst_wfc3_uvis_beams.h5'
grism='G280'

conf=h5axeconfig.Camera(f,grism)


for (name1,det1),(name2,det2) in zip(conf,conf):
    print(type(det1))


#siaf=h5axeconfig.SIAF('hst_wfc3_ir_detector.h5')
#h=siaf.detectors['IR'].mkhdr((189.1792282504428,62.28646067642324),131.924)

