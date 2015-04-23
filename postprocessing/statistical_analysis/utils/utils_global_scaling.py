import numpy as np
import scipy.stats as st

#
# Utils to scale a global analyse
#

def scalingByMean(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # base on arithmetic mean
    means = []
    print ('Computing scaling by mean for a list of models')
    for model in modelList:
        data = np.fromfile(model)
        means.append(np.mean(data)**2)
    return np.mean(means)

def scalingByGeomMean(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # based on geometric mean
    means = []
    print ('Computing scaling by geometric mean for a list of models')
    for model in modelList:
        data = np.fromfile(model)
        means.append(np.mean(data)**2)
    return st.gmean(means)

def scalingByVariance(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # based on variance
    var = []
    print ('Computing scaling by var for a list of models')    
    for model in modelList:
        data = np.fromfile(model)
        var.append(np.var(data))
    return np.mean(var)

def scalingFM(modelList, level):
    area = []
    print ('Computing scaling for FM for a list of models')    
    for model in modelList:
        data = np.fromfile(model)
        area.append( np.sum(data>level) )
    return np.mean(area)

def scalingFMmini(modelList):
    print ('Computing scaling for FMmini for a list of models')
    data = np.fromfile(modelList[0])
    maxi = np.copy(data)
    
    for model in modelList:
        data = np.fromfile(model)
        maxi = np.maximum( maxi, data )
    return maxi.sum()

def findNLevelsML(modelList, N, space='lin'):
    print ('Finding levels for a list of models')    
    data = np.fromfile(modelList[0])
    mini = np.nanmin(data)
    maxi = np.nanmax(data)

    for model in modelList:
        data = np.fromfile(model)
        mini = np.nanmin( [ mini , np.nanmin(data) ] )
        maxi = np.nanmax( [ maxi , np.nanmax(data) ] )

    if space=='lin':
        return np.linspace(mini, maxi, N)
    elif space=='log':
        return np.exp( np.logspace(np.log10(mini), np.log10(maxi), N) )

