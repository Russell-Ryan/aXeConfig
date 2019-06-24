#from distutils.core import setup, Extension
from setuptools import setup,find_packages

#import numpy.distutils.misc_util
import os
import glob

import h5axeconfig.__init__ as info


# conf dir
confdir='data'

# get the configuration files
conffiles=glob.glob(os.path.join(confdir,'*.h5'))

# call setup
setup(name='h5axeconfig',\
      version=info.__version__,\
      author=info.__author__,\
      author_email=info.__email__,\
      keywords='grism aXe python hdf5',\
      description='Python API for working with grism configuration in aXe format written as HDF5',\
      license='MIT',
      install_requires=['h5py','astropy','numpy','polyclip'],
      classifiers=['Development Status :: 1 Planning',\
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Astronomy',],\
      packages=find_packages())
      #package_dir={'axeconfig':'axeconfig'},
      #qpackage_data={confdir:conffiles})
      

      
