import numpy as np
import scipy.stats as st

#
# Utils to scale a space analyse
# i.e. the analyse will be peformed at each grid point
#

def scalingByMean(modelList, Nt, Nz, Ny, Nx):
    # returns the quadratic scaling of for a list of data from different models
    # base on arithmetic mean
    scaling = np.zeros(shape=(Nz,Ny,Nx))
    for model in modelList:
        data = np.fromfile(model)
        data = data.reshape((Nt,Nz,Ny,Nx))
        scaling += np.power(data.nanmean(axis=0),2)
    return scaling / len(modelList)

def scalingByGeomMean(modelList, Nt, Nz, Ny, Nx):
    # returns the quadratic scaling of for a list of data from different models
    # based on geometric mean
    scaling = np.ones(shape=(Nz,Ny,Nx))
    for model in modelList:
        data = np.fromfile(model)
        data = data.reshape(Nt,Nz,Ny,Nx)
        scaling *= np.power(data.nanmean(axis=0),2)
    return np.power(scaling, 1./len(modelList))
                                
def scalingByVariance(modelList, Nt, Nz, Ny, Nx):
    # returns the quadratic scaling of for a list of data from different models
    # based on variance
    scaling = np.zeros(shape=(Nz,Ny,Nx))
    for model in modelList:
        data = np.fromfile(model)
        data = data.reshape((Nt,Nz,Ny,Nx))
        scaling += data.nanvar(axis=0)
    return scaling / len(modelList)

def scalingFM(modelList, level, Nt, Nz, Ny, Nx):
    scaling = np.zeros(shape=(Nz,Ny,Nx))
    for model in modelList:
        data = np.fromfile(model)
        data = data.reshape((Nt,Nz,Ny,Nx))
        scaling += (data>level).nansum(axis=0)
    return scaling / len(modelList)
                                
def scalingFMmini(modelList, Nt, Nz, Ny, Nx):
    data = np.fromfile(modelList[0])
    maxi = np.copy(data)
    
    for model in modelList:
        data = np.fromfile(model)
        maxi = np.maximum( maxi, data )

    maxi = maxi.reshape((Nt,Nz,Ny,Nx))
    return maxi.nansum(axis=0)

def findNLevelsML(modelList, N, Nt, Nz, Ny, Nx, space='lin'):
    data = np.fromfile(modelList[0])
    data = data.reshape((Nt,Nz,Ny,Nx))
    mini = data.nanmin(axis=0)
    maxi = data.nanmax(axis=0)

    for model in modelList:
        data = np.fromfile(model)
        data = data.reshape((Nt,Nz,Ny,Nx))
            
        mini = np.minimum( mini, data.nanmin(axis=0) )
        maxi = np.maximum( maxi, data.nanmax(axis=0) )


    levels = np.zeros(shape=(Nz,Ny,Nx,N))
    for k in xrange(Nz):
        for j in xrange(Ny):
            for i in xrange(Nx):
                if space=='lin':
                    levels[k,j,i,:] = np.linspace(mini[k,j,i], maxi[k,j,i], N)
                elif space=='log':
                    levels[k,j,i,:] = np.exp( np.logspace(np.log10(mini[k,j,i]), np.log10(maxi[k,j,i]), N) )
    return levels
