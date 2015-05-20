##############
# greyScale.py
##############

import numpy as np

class GreyScaleMaker:

    def __init__(self, minValues=None, threshold=True):
        if minValues is None:
            minValues            = {}
            minValues['air/']    = 1.e-10 # in Bq/m^2
            minValues['ground/'] = 1.e-10 # in Bq/m^3
        self.minValues = minValues
        self.threshold = threshold
        
    def __call__(self, matrix, dataType, levels=None, mini=None, maxi=None, nLevels=32):
        if levels is None:
            levels = np.linspace(mini, maxi, nLevels)
        else:
            nLevels = len(levels)

        if self.threshold:
            threshold = self.minValues[dataType]
        else:
            threshold = matrix.min() - 1
            
        CDF = np.zeros(nLevels+1)
        
        for i in xrange(nLevels-1):
            CDF[i+1] = ( ( matrix < levels[i] ) * ( matrix > threshold ) ).mean()
            
        CDF[nLevels] = ( matrix > threshold ).mean()
            
        if CDF[nLevels] == 0:
            CDF    = np.ones(nLevels+1)
            CDF[0] = 0.0
        else:
            CDF /= CDF[nLevels]
            
        PDF = CDF[1:nLevels+1] - CDF[0:nLevels]
        return PDF
