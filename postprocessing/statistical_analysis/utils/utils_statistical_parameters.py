import numpy as np
import scipy.stats as st

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
# FM

def FM(X,Y,level):
    return ( ( (X>level) * (Y>level) ).sum() ) / ( ( (X>level) + (Y>level) ).sum() )

def FM_corrected(X,Y,level,scaling):
    return ( ( (X>level) * (Y>level) ).sum() ) / scaling

##########################################
# FMmini

def FMmini(X,Y):
    return np.minimum(X,Y).sum() / np.maximum(X,Y).sum()

def FMmini_corrected(X,Y,scaling):
    return np.minimum(X,Y).sum() / scaling

##########################################
# Arithmetic Bias

def bias(X,Y):
    return (Y.mean() - X.mean())

def relativeBias(X,Y):
    return ( 2*bias(X,Y) ) / ( X.mean() + Y.mean() )

def bias_corrected(X,Y,scaling):
    return bias(X,Y)/scaling

##########################################
# Geometric Bias

def geomBias(X,Y,epsilon):
    Z = X / np.maximum(Y,epsilon)
    return st.gmean(Z)    

##########################################
# Geometric mean variance

def geomVar(X,Y,epsilon):
    return np.exp( np.power( np.log( np.maximum( X / np.maximum(Y,epsilon) , epsilon ) ) , 2 ).mean() )

##########################################
# Pearson's correlation coefficient

def PCC(X,Y):
    r,p = st.pearsonr(X,Y)
    return r

def PCClog(X,Y):
    r,p = st.personr(np.log(np.maximum(X,epsilon)),np.log(np.maximum(Y,epsilon)))
    return r

##########################################
# BCRMS

def BcMSE(X,Y):
    return np.power( ( X - X.mean() ) - ( Y - Y.mean() ) , 2 ).mean()

def BcNMSE_corrected(X,Y,scaling):
    return BcMSE(X,Y)/scaling

##########################################
# Skill score

def SSSr(X,Y):
    r = PCC(X,Y)
    sigmaX = np.sqrt( X.var() )
    sigmaY = np.sqrt( Y.var() )

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
    return 100. * ( (X > Y).mean() - 0.5 )

##########################################
# FAalpha band

def FA(X,Y,alpha):
    return ( ( X < alpha*Y ) * ( Y < alpha*X ) ).mean()

##########################################
# Repartition function

def repartitionFunction(X, levels):
    Nlevels = levels.size
    function = np.zeros(Nlevels)
    for i in xrange(Nlevels):
        function[i] = ( X > levels[i] ).mean()
    return function

def findNLevels(X, N, space='lin'):
    mini = X.min()
    maxi = X.max()

    if space=='lin':
        return np.linspace(mini, maxi, N)
    elif space=='log':
        return np.logspace(np.log10(mini), np.log10(maxi), N)
    
##########################################
# Kolmogorov-Smirnov test

def KSLevels(X,Y,levels):
    repartX = repartitionFunction(X, levels)
    repartY = repartitionFunction(Y, levels)
    return np.abs( repartX - repartY ).max()

def KS(X,Y,N=100,space='lin'):
    levels = findNLevels( np.array([X,Y]), N, space)
    return KSLevels(X,Y,levels)
