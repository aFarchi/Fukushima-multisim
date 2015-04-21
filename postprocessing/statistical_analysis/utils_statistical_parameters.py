import numpy as np
import scipy.stats as st

##########################################
# Scalings

def scalingByMean(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # base on arithmetic mean
    means = []
    for model in modelList:
        means.append(model.nanmean()**2)
    return np.nanmean(means)

def scalingByGeomMean(modelList):
    # returns the quadratic scaling of for a list of data from different models
    # based on geometric mean
    means = []
    for model in modelList:
        means.append(model.nanmean()**2)
    return st.gmean(means)

def scalingByVariance(modelList):
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
# FM

def scalingFM(modelList, level):
    area = []
    for model in modelList:
        area.append( (model>level).nansum() )
    return np.nanmean(area)

def FM(X,Y,level):
    return ( ( (X>level) * (Y>level) ).nansum() ) / ( ( (X>level) + (Y>level) ).nansum() )

def FM_corrected(X,Y,level,scaling):
    return ( ( (X>level) * (Y>level) ).nansum() ) / scaling

##########################################
# FMmini

def scalingFMmini(modelList):
    maxi = modelList[0]
    for model in modelList:
        maxi = np.maximum( maxi, model )
    return maxi.sum()

def FMmini(X,Y):
    return np.minimum(X,Y).sum() / np.maximum(X,Y).sum()

def FMmini_corrected(X,Y,scaling):
    return np.minimum(X,Y).sum() / scaling

##########################################
# Arithmetic Bias

def bias(X,Y):
    return (Y.nanmean() - X.nanmean())

def relativeBias(X,Y):
    return ( 2*bias(X,Y) ) / ( X.nanmean() + Y.nanmean() )

def bias_corrected(X,Y,scaling):
    return bias(X,Y)/scaling

##########################################
# Geometric Bias

def geomBias(X,Y):
    Z = X / Y
    return st.gmean(Z)    

##########################################
# Geometric mean variance

def geomVar(X,Y):
    return np.exp( np.power( np.log( X / Y ) , 2 ).nanmean() )

##########################################
# Pearson's correlation coefficient

def PCC(X,Y):
    r,p = st.pearsonr(X,Y)
    return r

def PCClog(X,Y):
    r,p = st.personr(np.log(X),np.log(Y))
    return r

##########################################
# BCRMS

def BcMSE(X,Y):
    np.power( X - X.nanmean() ) - ( Y - Y.nanmean() , 2 ).nanmean()

def BcNMSE_corrected(X,Y,scaling):
    return BC_MSE(X,Y)/scaling

##########################################
# Skill score

def SSSr(X,Y):
    r = PCC(X,Y)
    sigmaX = np.sqrt( X.nanvar() )
    sigmaY = np.sqrt( Y.nanvar() )

    return 2. * ( 1. + r ) / ( sigmaX/sigmaY + sigmaY/sigmaX )**2

def SSSb(X,Y,alpha=10.):
    RB = relativeBias(X,Y)
    return 1. / ( 1. + alpha*RB**2 )

def SSSb_corrected(X,Y,scaling,alpha=10.):
    RB = bias_corrected(X,Y,scaling)
    return 1. / ( 1. + alpha*RB**2 )

# Total skill score
def TSS(X,Y,mr=0.5):
    return mr * SSSr(X,Y) + ( 1. - mr ) * SSSb(X,Y)

def TSS_corrected(X,Y,scaling,mr=0.5):
    return mr * SSSr(X,Y) + ( 1. - mr ) * SSSb_corrected(X,Y,scaling)

##########################################
# Factor of excedence

def FOEX(X,Y):
    return 100. * ( (X > Y).nanmean() - 0.5 )

##########################################
# FAalpha band

def FA(X,Y,alpha):
    return ( ( X < alpha*Y ) * ( Y < alpha*X ) ).nanmean()

##########################################
# Repartition function

def repartitionFunction(X, levels):
    Nlevels = levels.size
    function = np.zeros(Nlevels)
    for i in xrange(Nlevels):
        function[i] = ( X > levels[i] ).nanmean()
    return function

def findNLevels(X, N, space='lin'):
    mini = X.nanmin()
    maxi = X.nanmax()

    if space=='lin':
        return np.linspace(mini, maxi, N)
    elif space=='log':
        return np.exp( np.logspace(np.log10(mini), np.log10(maxi), N) )

def findNLevelsML(modelList, N, space='lin'):
    mini = modelList[0].nanmin()
    maxi = modelList[0].nanmax()

    for model in modelList:
        mini = np.min( [ mini , model.nanmin() ] )
        maxi = np.min( [ maxi , model.nanmax() ] )

    if space=='lin':
        return np.linspace(mini, maxi, N)
    elif space=='log':
        return np.exp( np.logspace(np.log10(mini), np.log10(maxi), N) )
    
##########################################
# Kolmogorov-Smirnov test

def KSLevels(X,Y,levels):
    repartX = repartitionFunction(X, levels)
    repartY = repartitionFunction(Y, levels)
    return np.abs( repartX - repartY ).max()

def KS(X,Y,N=100,space='lin'):
    levels = findNLevels( np.array([X,Y]), N, space)
    return KSLevels(X,Y,levels)
