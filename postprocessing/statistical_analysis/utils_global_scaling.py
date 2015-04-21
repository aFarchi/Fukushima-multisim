import numpy as np
import scipy.stats as st

#
# Utils to scale a global analyse
#

def scalingByMean(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # base on arithmetic mean
    means = []
    for model in modelList:
        data = np.fromfile(model)
        means.append(data.nanmean()**2)
    return np.nanmean(means)

def scalingByGeomMean(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # based on geometric mean
    means = []
    for model in modelList:
        data = np.fromfile(model)
        means.append(data.nanmean()**2)
    return st.gmean(means)

def scalingByVariance(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # based on variance
    var = []
    for model in modelList:
        data = np.fromfile
        var.append(data.nanvar())
    return np.mean(var)

def scalingFM(modelList, level):
    area = []
    for model in modelList:
        data = np.fromfile(model)
        area.append( (data>level).nansum() )
    return np.nanmean(area)

def scalingFMmini(modelList):
    data = np.fromfile(modelList[0])
    maxi = np.copy(data)
    
    for model in modelList:
        data = np.fromfile(model)
        maxi = np.maximum( maxi, data )
    return maxi.sum()

def findNLevelsML(modelList, N, space='lin'):
    data = np.fromfile(modelList[0])
    mini = data.nanmin()
    maxi = data.nanmax()

    for model in modelList:
        data = np.fromfile(model)
        mini = np.min( [ mini , data.nanmin() ] )
        maxi = np.min( [ maxi , data.nanmax() ] )

    if space=='lin':
        return np.linspace(mini, maxi, N)
    elif space=='log':
        return np.exp( np.logspace(np.log10(mini), np.log10(maxi), N) )

