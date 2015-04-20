import numpy as np
import scipy.stats as st

##########################################
# Scalings

def scaling_by_mean(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # base on arithmetic mean
    means = []
    for model in modelList:
        means.append(model.mean()**2)
    return np.mean(means)

def scaling_by_geom_mean(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # based on geometric mean
    means = []
    for model in modelList:
        means.append(model.mean()**2)
    return st.gmean(means)

def scaling_by_variance(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # based on variance
    var = []
    for model in modelList:
        var.append(model.var())
    return np.mean(var)

##########################################
# RMS

def MSE(X,Y):
    # returns the mean square error of X and Y as np arrays
    return np.power(X-Y,2).mean()

def NMSE(X,Y):
    return MSE(X,Y) / ( X.mean() * Y.mean() )

def NMSE_corrected(X,Y,scale):
    return MSE(X,Y) / scale

##########################################
