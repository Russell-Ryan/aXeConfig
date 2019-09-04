# h5axeconfig

A python API for implementing aXe-style calibration and common grism functions.

## Installation

1. h5axeconfig has three key dependencies that must be resolved first: [h5py](https://pypi.org/project/h5py/), [ruamel](https://pypi.org/project/ruamel.yaml/), and [wget](https://pypi.org/project/wget/).

```
pip install h5py
pip install wget
pip install ruamel.yaml
```
2. Now you can install h5axeconfig using the standard:
```
python setup.py install
```

## Calibration Files

To facilitate cameras with multiple detectors (such as WFC3/UVIS with its two CCDs), I felt it necessary to extend the ascii-formatted calibration files to a more advanced format.  I choose the [hdf5](https://www.hdfgroup.org/solutions/hdf5/) format, and have provided a few of the common detectors that I have worked with.  Given the file size, I provide these on a [personal webpage](http://www.stsci.edu/~rryan/pyLINEAR/):

* [WFC3-IR](http://www.stsci.edu/~rryan/pyLINEAR/calibrations/WFC3-IR/)
* [WFC3-UVIS](http://www.stsci.edu/~rryan/pyLINEAR/calibrations/WFC3-UVIS/)

** These files will be downloaded automatically by the setup.py step above. **

## Example Usage

```


TBD


```
## Additional Details

For more information on the mathematics, please see the appropriate documentation for [aXe](http://axe-info.stsci.edu/extract_calibrate), but also my paper on [LINEAR](https://github.com/Russell-Ryan/pyLINEAR) contains a basic grism primer ([Ryan, Casertano, & Pirzkal 2018, PASP, 130, 4501](https://ui.adsabs.harvard.edu/abs/2018PASP..130c4501R/abstract)).













