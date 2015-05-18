#########################
# statisticalOperators.py
#########################

import numpy as np
import scipy.stats as st

##########################################
# RMS

def MSE(X,Y):
    return np.power(X-Y,2).mean()

def NMSE(X,Y):
    scaling = X.mean() * Y.mean()
    if scaling == 0.0:
        return 0.0
    else:
        return MSE(X,Y) / scaling

def NMSE_corrected(X,Y,scale):
    return MSE(X,Y) / scale

##########################################
# FM

def NFM(X,Y,level):
    scaling = ( (X>level) + (Y>level) ).sum()
    if scaling == 0.0:
        return 0.0
    else:
        return ( ( (X>level) * (Y>level) ).sum() ) / scaling

def NFM_corrected(X,Y,level,scaling):
    return ( ( (X>level) * (Y>level) ).sum() ) / scaling

##########################################
# FMmini

def NFMmini(X,Y):
    scaling = np.maximum(X,Y).sum()
    if scaling == 0.0:
        return 0.0
    else:
        return np.minimum(X,Y).sum() / scaling

def NFMmini_corrected(X,Y,scaling):
    return np.minimum(X,Y).sum() / scaling

##########################################
# Arithmetic Bias

def bias(X,Y):
    return (Y.mean() - X.mean())

def Nbias(X,Y):
    scaling = X.mean() + Y.mean()
    if scaling == 0.0:
        return 0.0
    else:
        return ( 2*bias(X,Y) ) / scaling

def Nbias_corrected(X,Y,scaling):
    return bias(X,Y) / scaling

##########################################
# Pearson's correlation coefficient

def PCC(X,Y):
    r,p = st.pearsonr(X.reshape(X.size),Y.reshape(Y.size))

    # corrects bad behavior of pearsonr : in case there is no variance at all, it returns a nan
    if r == r:
        return r
    else:
        return 1.0

def PCClog(X,Y,epsilon):
    r,p = st.pearsonr(np.log(np.maximum(X.reshape(X.size),epsilon)),np.log(np.maximum(Y.reshape(Y.size),epsilon)))
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
    if sigmaX == 0.0 or sigmaY == 0.0:
        return 0.0
    else:
        return 2. * ( 1. + r ) / ( sigmaX/sigmaY + sigmaY/sigmaX )**2

def SSSb(X,Y,alpha=10.):
    RB = bias(X,Y)
    return 1. / ( 1. + alpha*RB**2 )

def SSSb_corrected(X,Y,scaling,alpha=10.):
    RB = Nbias_corrected(X,Y,scaling)
    return 1. / ( 1. + alpha*RB**2 )

# Total skill score
def TSS(X,Y,mr=0.5):
    return mr * SSSr(X,Y) + ( 1. - mr ) * SSSb(X,Y)

def TSS_corrected(X,Y,scaling,mr=0.5):
    return mr * SSSr(X,Y) + ( 1. - mr ) * SSSb_corrected(X,Y,scaling)

##########################################
# Factor of excedence

def FOEX(X,Y):
    return ( (X > Y).mean() - (Y < X).mean() )

##########################################
# FAalpha band

def FA(X,Y,alpha):
    return ( ( X < alpha*Y ) * ( Y < alpha*X ) ).mean()

##########################################
# Geometric Bias

def geomBias(X,Y,epsilon):
    Z = X / np.maximum(Y,epsilon)
    return st.gmean(Z.reshape(Z.size))    

##########################################
# Geometric mean variance

def geomVar(X,Y,epsilon):
    return np.exp( np.power( np.log( np.maximum( X / np.maximum(Y,epsilon) , epsilon ) ) , 2 ).mean() )
