from astropy.io import fits
from astropy.coordinates import SkyCoord,Angle
import numpy as np
import os

from ..utils import h5Attr


class SIP(object):
    def __init__(self,h5,name):
        self.name=name
        self.valid=name in h5
        if self.valid:
            self.order=h5Attr(h5[name],'order')
            self.data=np.array(h5[name])
            
            
    def updateHeader(self,hdr):
        ''' update the fits header with the SIP data '''
        new=hdr.copy()
        if self.valid:        
            new['{}_ORDER'.format(self.name)]=(self.order,'polynomial order')
            
            for (i,j,v) in self.data:
                new['{}_{}_{}'.format(self.name,i,j)]=v
        
        return new

    def __str__(self):
        return 'SIP model for {}'.format(self.name)
    
    
class Detector(object):
    def __init__(self,h5,V2ref=0.,V3ref=0.):
        self.detector=os.path.split(h5.name)[1]

        # record the reference data
        self.V2ref=V2ref
        self.V3ref=V3ref

        # get the contents of the h5        
        self.V2=h5Attr(h5,'V2')
        self.V3=h5Attr(h5,'V3')
        self.cd=h5Attr(h5,'cd')
        self.crpix=h5Attr(h5,'crpix')
        self.crval=h5Attr(h5,'crval')
        self.ctype=h5Attr(h5,'ctype')
        self.equinox=h5Attr(h5,'equinox')
        self.latpole=h5Attr(h5,'latpole')
        self.longpole=h5Attr(h5,'longpole')
        self.naxis=h5Attr(h5,'naxis')
        self.a=SIP(h5,'A')
        self.b=SIP(h5,'B')
        self.ap=SIP(h5,'AP')
        self.bp=SIP(h5,'BP')
        

        
        
        
    def rotmat(self,ang):
        # make a rotation matrix
        cs=np.cos(ang*np.pi/180)
        sn=np.sin(ang*np.pi/180)
        R=np.array([[cs,sn],[-sn,cs]])        
        return R

    def mkhdr(self,crvals,orientat):

        # direction of offset
        ang=Angle(orientat,unit='degree')

        # compute offsets
        V2=self.V2-self.V2ref
        V3=self.V3-self.V3ref
        delta=Angle(np.sqrt(V2*V2+V3*V3),unit='arcsec')

        # compute new position        
        coord=SkyCoord(crvals[0],crvals[1],frame='icrs',unit='degree')
        crval=coord.directional_offset_by(ang,delta)

        
        # compute CD matrix for a given rotation
        cd=np.dot(self.cd,self.rotmat(orientat))
        
        # make the output header
        hdr=fits.Header()        
        hdr['NAXIS1']=(self.naxis[0],'number of pixels in x')
        hdr['NAXIS2']=(self.naxis[1],'number of pixels in y')
        hdr['CRPIX1']=(self.crpix[0],'x-coordinate of reference pixel')
        hdr['CRPIX2']=(self.crpix[1],'y-coordinate of reference pixel')
        hdr['CRVAL1']=(crval.ra.degree,'first axis value at reference pixel')
        hdr['CRVAL2']=(crval.dec.degree,'second axis value at reference pixel')
        hdr['CD1_1']=(cd[0,0],'partial of first axis coordinate w.r.t. x')
        hdr['CD1_2']=(cd[0,1],'partial of first axis coordinate w.r.t. y')
        hdr['CD2_1']=(cd[1,0],'partial of second axis coordinate w.r.t. x')
        hdr['CD2_2']=(cd[1,1],'partial of second axis coordinate w.r.t. y')
        hdr['CTYPE1']=(self.ctype[0],'the coordinate type for the first axis')
        hdr['CTYPE2']=(self.ctype[1],'the coordinate type for the second axis')
        hdr['EQUINOX']=(self.equinox,'equinox of coordinates')
        hdr['LATPOLE']=(self.latpole,' ')
        hdr['LONGPOLE']=(self.longpole,' ')
        hdr['ORIENTAT']=(-orientat,'position angle of image y axis (deg. e of n)')

        # put on SIP
        hdr=self.a.updateHeader(hdr)
        hdr=self.b.updateHeader(hdr)
        hdr=self.ap.updateHeader(hdr)
        hdr=self.bp.updateHeader(hdr)
        
        return hdr



    def __str__(self):
        return 'SIAF for {}'.format(self.detector)
