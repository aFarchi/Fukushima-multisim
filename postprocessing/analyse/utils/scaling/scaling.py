############
# scaling.py
############

import numpy as np

class Scaling:
    pass

def scalingToArray(scale):
    array    = np.zeros(6+len(scale.scalingFM))
    array[0] = scale.mini
    array[1] = scale.maxi
    array[2] = scale.meanMeans
    array[3] = scale.geomMeanMeans
    array[4] = scale.meanVars
    array[5] = scale.sumMaximum
    array[6:] = scale.scalingFM[:]
    return array

def arrayToScaling(array):
    scale               = Scaling()
    scale.mini          = array[0]
    scale.maxi          = array[1]
    scale.meanMeans     = array[2]
    scale.geomMeanMeans = array[3]
    scale.meanVars      = array[4]
    scale.sumMaximum    = array[5]
    scale.scalingFM     = array[6:]
    return scale

def computeScaling(matrix):
    scaling      = Scaling()
    scaling.mini = matrix.min()
    scaling.maxi = matrix.max()
    scaling.mean = matrix.mean()
    scaling.var  = matrix.var()
    return scaling

def computeFMScaling(matrix, levels=None, mini=None, maxi=None, nLevels=32):
    if levels is None:
        levels = np.linspace(mini, maxi, nLevels)
    else:
        nLevels = len(levels)

    FMScaling = np.zeros(nLevels)
    for i in xrange(nLevels):
        FMScaling[i] = ( matrix > levels[i] ).sum()

    return FMScaling

def mergeScalings(scalings, maximums, fieldList, procList):

    mergedScalings = {}

    for field in fieldList:    
        mergedScalings[field] = {}
    
        for lol in ['lin','log']:
            meanMeans     = 0.
            geomMeanMeans = 1.
            meanVars      = 0.
            
            for proc in procList:
                meanMeans     += scalings[lol][field][proc].mean
                geomMeanMeans *= scalings[lol][field][proc].mean
                meanVars      += scalings[lol][field][proc].var

                try:
                    mini = min( mini , scalings[lol][field][proc].mini )
                    maxi = max( maxi , scalings[lol][field][proc].maxi )
                except:
                    mini = scalings[lol][field][proc].mini
                    maxi = scalings[lol][field][proc].maxi

            meanMeans    /= len(procList)
            geomMeanMeans = np.power(max(geomMeanMeans, 0.0), 1./len(procList))
            meanVars     /= len(procList)

            scale                      = Scaling()
            scale.mini                 = mini
            scale.maxi                 = maxi
            scale.meanMeans            = meanMeans
            scale.geomMeanMeans        = geomMeanMeans
            scale.meanVars             = meanVars
            scale.sumMaximum           = maximums[lol][field].sum()
            mergedScalings[field][lol] = scale

    return mergedScalings

def addFMScaling(scaling, scalingFM, fieldList, procList):

    for field in fieldList:
        for lol in ['lin','log']:
            mean = 0.0
            for proc in procList:
                mean += scalingFM[lol][field][proc]
            scaling[field][lol].scalingFM = mean / len(procList)

    return scaling
