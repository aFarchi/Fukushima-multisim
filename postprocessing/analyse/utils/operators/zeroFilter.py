###############
# zeroFilter.py
###############

import numpy as np

class ZeroFilter:
    
    def __init__(self, minValues=None):
        if minValues is None:
            minValues            = {}
            minValues['air/']    = 1.e-10 # in Bq/m^2
            minValues['ground/'] = 1.e-10 # in Bq/m^3

        self.minValues = minValues

    def __call__(self, matrix, dataType):
        try:
            minVal = self.minValue[dataType]
            return np.maximum(matrix, minVal)
        except:
            return matrix
