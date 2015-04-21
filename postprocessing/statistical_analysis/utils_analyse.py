import numpy as np
import scipy.stats as st

from utils_statistical_parameters import *

class Scaling:
    '''
    class to save the scalings for an analyse
    '''

    def __init__(self, modelList, levelsFM):
        self.mean = scalingByMean(modelList)
        self.geomMean = scalingByGeomMean(modelList)
        self.var = scalingByVariance(modelList)
        self.scalingFMmini = scalingFMmini(modelList)
        Nlevels = levelsFM.size
        self.scalingFM = np.zeros(Nlevels)
        for i in xrange(Nlevels):
            self.scalingFM[i] = scalingFM(modelList, levelsFM[i])

    def chooseScaling(self, choose='mean'):
        if choose=='mean':
            return self.mean
        elif choose=='geomMean':
            return self.geomMean
        elif choose=='var':
            return self.var

class LinearAnalyseResult:
    '''
    class to store the result of a linear analyse
    '''
    def __init__(self, Nmodels, NlevelsFM, NlevelsAlpha):
        self.Nmodels      = Nmodels
        self.NlevelsFM    = NlevelsFM
        self.NlevelsAlpha = NlevelsAlpha
        self.MSE          = np.zeros(shape=(Nmodels,Nmodels))
        self.FMmini       = np.zeros(shape=(Nmodels,Nmodels))
        self.bias         = np.zeros(shape=(Nmodels,Nmodels))
        self.PCC          = np.zeros(shape=(Nmodels,Nmodels))
        self.BcMSE        = np.zeros(shape=(Nmodels,Nmodels))
        self.TSS          = np.zeros(shape=(Nmodels,Nmodels))        
        self.FOEX         = np.zeros(shape=(Nmodels,Nmodels))
        self.KS           = np.zeros(shape=(Nmodels,Nmodels))
        self.FM           = np.zeros(shape=(Nmodels,Nmodels,NlevelsFM))
        self.FA           = np.zeros(shape=(Nmodels,Nmodels,NlevelsAlpha))

    def tofile(self,fileName):
        f = open(fileName, 'w')
        mat = np.zeros(3)
        mat[0] = self.Nmodels
        mat[1] = self.NlevelsFM
        mat[2] = self.NlevelsAlpha
        mat.tofile(f)
        self.MSE.tofile(f)
        self.FMmini.tofile(f)
        self.bias.tofile(f)
        self.PCC.tofile(f)
        self.BcMSE.tofile(f)
        self.TSS.tofile(f)
        self.FOEX.tofile(f)
        self.KS.tofile(f)
        self.FM.tofile(f)
        self.FA.tofile(f)
        f.close()
        print fileName
        
class LinearAnalyse:
    '''
    class to perform a linear analyse
    '''

    def __init__(self, modelList,
                 chooseScaling='mean',
                 levelsFM=None, NlevelsFM=10, spaceFM='lin',
                 levelsAlpha=None, NlevelsAlpha=3, spacing=2.,
                 levelsKS=None, NlevelsKS=100, spaceKS='lin'):

        self.modelList = modelList

        if levelsFM is None:
            self.levelsFM = findNLevels(modelList,NlevelsFM,spaceFM)
        else:
            self.levelsFM = levelsFM
            NlevelsFM = levelsFM.size

        if levelsAlpha is None:
            self.levelsAlpha = np.power(spacing, 1. + np.arange(NlevelsAlpha))
        else:
            self.levelsAlpha = levelsAlpha
            NlevelsAlpha = levelsAlpha.size

        if levelsKS is None:
            self.levelsKS = findNLevelsML(modelList,NlevelsKS,spaceKS)
        else:
            self.levelsKS = levelsKS

        self.scaling = Scaling(modelList,self.levelsFM)
        self.results = LinearAnalyseResult(modelList.size,NlevelsFM,NlevelsAlpha)
        self.chooseScaling = chooseScaling

    def performAnalyseOn(self, i, j):
        if not chooseScaling=='none':
            self.results.MSE[i,j]    = NMSE_corrected(   self.modelList[i] , self.modelList[j] , self.scaling.chooseScaling(chooseScaling) )
            self.results.FMmini[i,j] = FMmini_corrected( self.modelList[i] , self.modelList[j] , self.scaling.scalingFMmini )
            self.results.bias[i,j]   = bias_corrected(   self.modelList[i] , self.modelList[j] , self.scaling.chooseScaling(chooseScaling) )
            self.results.BcMSE[i,j]  = BcNMSE_corrected( self.modelList[i] , self.modelList[j] , self.scaling.chooseScaling(chooseScaling) )
            self.results.TSS[i,j]    = TSS_corrected(    self.modelList[i] , self.modelList[j] , self.scaling.chooseScaling(chooseScaling) )
            self.results.KS[i,j]     = KS(               self.modelList[i] , self.modelList[j] , self.levelsKS )
            self.results.PCC[i,j]    = PCC(              self.modelList[i] , self.modelList[j] )
            self.results.FOEX[i,j]   = FOEX(             self.modelList[i] , self.modelList[j] )

            for lev in xrange(self.levelsFM.size):
                self.results.FM[i,j,lev] = FM_corrected( self.modelList[i] , self.modelList[j], self.levelsFM[lev], self.scaling.scalingFM[i] )

            for lev in xrange(self.levelsAlpha.size):
                self.results.FA[i,j,lev] = FA( self.modelList[i] , self.modelList[j], self.levelsAlpha[lev] )
                                
        else:
            self.results.MSE[i,j]    = NMSE(         self.modelList[i] , self.modelList[j] )
            self.results.FMmini[i,j] = FMmini(       self.modelList[i] , self.modelList[j] )
            self.results.bias[i,j]   = ralativeBias( self.modelList[i] , self.modelList[j] )
            self.results.BcMSE[i,j]  = BcNMSE(       self.modelList[i] , self.modelList[j] )
            self.results.TSS[i,j]    = TSS(          self.modelList[i] , self.modelList[j] )
            self.results.KS[i,j]     = KS(           self.modelList[i] , self.modelList[j] , self.levelsKS )
            self.results.PCC[i,j]    = PCC(          self.modelList[i] , self.modelList[j] )
            self.results.FOEX[i,j]   = FOEX(         self.modelList[i] , self.modelList[j] )
            
            for lev in xrange(self.levelsFM.size):
                self.results.FM[i,j,lev] = FM( self.modelList[i] , self.modelList[j], self.levelsFM[lev] )

            for lev in xrange(self.levelsAlpha.size):
                self.results.FA[i,j,lev] = FA( self.modelList[i] , self.modelList[j], self.levelsAlpha[lev] )
                                                                                                                                        
                
    def performAnalyse(self, printLog=True):
        Nmodels = modelList.size
        print('Starting analyse...')
        print('Nmodels = '+str(Nmodels))
        
        for i in xrange(Nmodels):
            for j in xrange(i):
                if printLog:
                    print('Analysing correlation bewteen model '+str(i)+' and model '+str(j)'.'
                self.performAnalyseOn(i,j)

        return self.results
