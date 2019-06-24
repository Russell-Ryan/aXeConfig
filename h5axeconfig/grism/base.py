''' Class to support the axe config objects. '''

import numpy as np
import os


class Base(object):
    def __init__(self,h5):
        self.beam=os.path.split(h5.name)[1]

    def __str__(self):
        return '{} for beam: {}'.format(self.__class__.__name__,self.beam)

