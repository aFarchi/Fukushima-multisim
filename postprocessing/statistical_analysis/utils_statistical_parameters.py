import numpy as np
import scipy.stats as st

##########################################
# Scalings

def scaling_by_mean(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # base on arithmetic mean
    means = []
    for model in modelList:
        means.append(model.nanmean()**2)
    return np.nanmean(means)

def scaling_by_geom_mean(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # based on geometric mean
    means = []
    for model in modelList:
        means.append(model.nanmean()**2)
    return st.gmean(means)

def scaling_by_variance(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # based on variance
    var = []
    for model in modelList:
        var.append(model.nanvar())
    return np.mean(var)

##########################################
# RMS

def MSE(X,Y):
    # returns the mean square error of X and Y as np arrays
    return np.power(X-Y,2).nanmean()

def NMSE(X,Y):
    return MSE(X,Y) / ( X.nanmean() * Y.nanmean() )

def NMSE_corrected(X,Y,scale):
    return MSE(X,Y) / scale

##########################################
# FMS

def scaling_FMS(modelList, level):
    area = []
    for model in modelList:
        area.append( (model>level).nansum() )
    return np.nanmean(area)

def FMS(X,Y,level):
    return ( ( (X>level) * (Y>level) ).nansum() ) / ( ( (X>level) + (Y>level) ).nansum() )

def FMS_corrected(X,Y,level,scaling):
    return ( ( (X>level) * (Y>level) ).nansum() ) / scaling

##########################################
# Bias

def bias(X,Y):
    return (Y.nanmean() - X.nanmean())

def relative8bias(X,Y):
    return ( 2*bias(X,Y) ) / ( X.nanmean() + Y.nanmean() )

def bias_corrected(X,Y,scaling):
    return bias(X,Y)/scaling

