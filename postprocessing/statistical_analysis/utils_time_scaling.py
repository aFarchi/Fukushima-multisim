import numpy as np
import scipy.stats as st

#
# Utils to scale a time analyse
# i.e. the analyse will be peformed at each time step
#

def scalingByMean(modelList, Nt, Nz, Ny, Nx):
    # returns the quadratic scaling of for a list of data from different models
    # base on arithmetic mean
    scaling = np.zeros(Nt)
    for model in modelList:
        data = np.fromfile(model)
        data = data.reshape((Nt,Nz*Ny*Nx))
        scaling += np.power(data.nanmean(axis=1),2)
    return scaling / len(modelList)

def scalingByGeomMean(modelList, Nt, Nz, Ny, Nx):
    # returns the quadratic scaling of for a list of data from different models
    # based on geometric mean
    scaling = np.ones(Nt)
    for model in modelList:
        data = np.fromfile(model)
        data = data.reshape(Nt,Nz*Ny*Nx)
        scaling *= np.power(data.nanmean(axis=1),2)
    return np.power(scaling, 1./len(modelList))
                                
def scalingByVariance(modelList, Nt, Nz, Ny, Nx):
    # returns the quadratic scaling of for a list of data from different models
    # based on variance
    scaling = np.zeros(Nt)
    for model in modelList:
        data = np.fromfile(model)
        data = data.reshape((Nt,Nz*Ny*Nx))
        scaling += data.nanvar(axis=1)
    return scaling / len(modelList)

def scalingFM(modelList, level, Nt, Nz, Ny, Nx):
    scaling = np.zeros(Nt)
    for model in modelList:
        data = np.fromfile(model)
        data = data.reshape((Nt,Nz*Ny*Nx))
        scaling += (data>level).nansum(axis=1)
    return scaling / len(modelList)
                                
def scalingFMmini(modelList, Nt, Nz, Ny, Nx):
    data = np.fromfile(modelList[0])
    maxi = np.copy(data)
    
    for model in modelList:
        data = np.fromfile(model)
        maxi = np.maximum( maxi, data )

    maxi = maxi.reshape((Nt,Nz*Ny*Nx))
    return maxi.nansum(axis=1)

def findNLevelsML(modelList, N, Nt, Nz, Ny, Nx, space='lin'):
    data = np.fromfile(modelList[0])
    data = data.reshape((Nt,Nz*Ny*Nx))
    mini = data.nanmin(axis=1)
    maxi = data.nanmax(axis=1)

    for model in modelList:
        data = np.fromfile(model)
        data = data.reshape((Nt,Nz*Ny*Nx))
            
        mini = np.minimum( mini, data.nanmin(axis=1) )
        maxi = np.maximum( maxi, data.nanmax(axis=1) )


    levels = np.zeros(shape=(Nt,N))
    for i in xrange(Nt):
        if space=='lin':
            levels[i,:] = np.linspace(mini[i], maxi[i], N)
        elif space=='log':
            levels[i,:] = np.exp( np.logspace(np.log10(mini[i]), np.log10(maxi[i]), N) )
    return levels
