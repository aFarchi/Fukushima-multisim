##############
# greyScale.py
##############

import numpy as np

def computeGreyScale(matrix, levels=None, mini=None, maxi=None, nLevels=32, threshold=True):
    if levels is None:
        levels = np.linspace(mini, maxi, nLevels)
    else:
        nLevels = len(levels)

    if threshold:
        detection = 0.01
        threshold = levels[0] + detection * ( levels[1] - levels[0] )
    else:
        threshold = matrix.min() - 1.0
        
    CDF = np.zeros(nLevels+1)

    for i in xrange(nLevels):
        CDF[i+1] = ( ( matrix < levels[i] ) * ( matrix > threshold ) ).mean()

    if CDF[nLevels] == 0:
        CDF = np.zeros(nLevels+1)
    else:
        CDF /= CDF[nLevels]

    PDF = CDF[1:nLevels+1] - CDF[0:nLevels]
    return PDF

