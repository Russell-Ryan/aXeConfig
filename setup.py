from setuptools import setup,find_packages
import os
import shutil
import urllib.request
import h5axeconfig.__init__ as info

try:
    import wget
except:
    print('Must install wget:\npip install wget')
    exit()


# the data dir 
datadir='h5axeconfig/data'
if not os.path.isdir(datadir):
  os.mkdir(datadir)

print("You will need to download the HDF5 files made by Russell Ryan")
print("Do you want the setup.py to download these files? [y]/n")
q=input()
if (q=='y') | (q=='Y') | (q=='') :
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

# call setup
setup(name='h5axeconfig',\
      version=info.__version__,\
      author=info.__author__,\
      author_email=info.__email__,\
      keywords='grism aXe python hdf5',\
      description='Python API for working with grism configuration in aXe format written as HDF5',\
      license='MIT',
      install_requires=['h5py','wget','astropy','numpy','polyclip'],
      classifiers=['Development Status :: 5 Production/Stable',\
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Astronomy',],\
      packages=find_packages(),\
      package_dir={'h5axeconfig': 'h5axeconfig'},\
      package_data={'h5axeconfig':['data/*.h5']})

      

      
