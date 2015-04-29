import numpy as np
import scipy.stats as st

#
# Utils to scale a global analyse
#

def scalingByMean(modelList, fileScaling=None):
    # returns the quadratic scaling of for a list of data from different models
    # base on arithmetic mean
    try:
        scaling = np.fromfile(scalingFile)
        return scaling[0]
    except:
        means = []
        print ('Computing scaling by mean for a list of models')
        for model in modelList:
            data = np.load(model)
            means.append(np.mean(data)**2)
        return np.mean(means)

def scalingByGeomMean(modelList, fileScaling=None):
    # returns the quadratic scaling of for a list of data from different models
    # based on geometric mean
    try:
        scaling = np.fromfile(scalingFile)
        return scaling[1]
    except:
        means = []
        print ('Computing scaling by geometric mean for a list of models')
        for model in modelList:
            data = np.load(model)
            means.append(np.mean(data)**2)
        return st.gmean(means)

def scalingByVariance(modelList, fileScaling=None):
    # returns the quadratic scaling of for a list of data from different models
    # based on variance
    try:
        scaling = np.fromfile(scalingFile)
        return scaling[2]
    except:
        var = []
        print ('Computing scaling by var for a list of models')    
        for model in modelList:
            data = np.load(model)
            var.append(np.var(data))
        return np.mean(var)

def scalingFM(modelList, level):
    area = []
    print ('Computing scaling for FM for a list of models')    
    for model in modelList:
        data = np.load(model)
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

def findNLevelsML(modelList, N, space='lin', scalingFile=None, epsilon=1e-10):
    print ('Finding levels for a list of models')    

    try:
        scaling = np.fromfile(scalingFile)
        mini    = scaling[4]
        maxi    = scaling[3]
    except:
        data = np.fromfile(modelList[0])
        mini = np.min(data)
        maxi = np.max(data)
        for model in modelList:
            data = np.fromfile(model)
            mini = np.min( [ mini , np.min(data) ] )
            maxi = np.max( [ maxi , np.max(data) ] )

    if space=='lin':
        return np.linspace(mini, maxi, N)
    elif space=='log':
        mini = np.max([mini,epsilon]) 
        return np.logspace(np.log10(mini), np.log10(maxi), N)

