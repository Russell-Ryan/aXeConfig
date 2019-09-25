from setuptools import setup,find_packages
import os
import shutil
import urllib.request
import wget


# the data dir
datadir='h5axeconfig/data'
if not os.path.isdir(datadir):
    os.mkdir(datadir)

rooturl='http://www.stsci.edu/~rryan/pyLINEAR/calibrations/'
with urllib.request.urlopen(rooturl+'all.txt') as www:
    for line in www:
        name=line.strip().decode('utf-8')
        base=os.path.basename(name)
        if not os.path.isfile(os.path.join(datadir,base)):
            print("Downloading: {}\n".format(base))
            thisFile=wget.download(rooturl+name)
            #os.rename(thisFile,datadir)
            shutil.move(thisFile,os.path.join(datadir,thisFile))

PKG = 'h5axeconfig'
AUTHOR = 'Russell Ryan'
info = {
    '__author__': AUTHOR,
    '__version__': '1.0',
    '__maintainer__': AUTHOR,
    '__email__': 'rryan@stsci.edu',
    '__credits__': AUTHOR,
}

# Generate package metadata
with open(os.path.join(PKG, 'info.py'), 'w+') as fp:
    for k, v in info.items():
        fp.write('{} = "{}"{}'.format(k, v, os.linesep))

# call setup
setup(name=PKG,
      version=info['__version__'],
      author=info['__author__'],
      author_email=info['__email__'],
      keywords='grism aXe python hdf5',
      description='Python API for working with grism configuration in aXe format written as HDF5',
      license='MIT',
      setup_requires=['wget'],
      install_requires=['h5py','astropy','numpy', 'polyclip @ git+https://github.com/russell-ryan/polyclip#egg=polyclip'],
      classifiers=['Development Status :: 5 Production/Stable',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Astronomy',],
      packages=find_packages(),
      package_dir={'h5axeconfig': 'h5axeconfig'},
      package_data={'h5axeconfig':['data/*.h5']})
