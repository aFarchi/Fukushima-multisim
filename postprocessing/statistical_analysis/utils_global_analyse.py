import numpy as np
import scipy.stats as st

from utils_statistical_parameters import *
import utils_global_scaling as ugs

class GlobalScaling:
    '''
    class to save the scalings for a global analyse
    '''

    def __init__(self, modelList, levelsFM):
        self.mean = ugs.scalingByMean(modelList)
        self.geomMean = ugs.scalingByGeomMean(modelList)
        self.var = ugs.scalingByVariance(modelList)
        self.scalingFMmini = ugs.scalingFMmini(modelList)
        Nlevels = levelsFM.size
        self.scalingFM = np.zeros(Nlevels)
        for i in xrange(Nlevels):
            self.scalingFM[i] = ugs.scalingFM(modelList, levelsFM[i])

    def chooseScaling(self, choose='mean'):
        if choose=='mean':
            return self.mean
        elif choose=='geomMean':
            return self.geomMean
        elif choose=='var':
            return self.var

class GlobalLinearAnalyseResult:
    '''
    class to store the result of a global linear analyse
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
        print(fileName)
        
class GlobalLinearAnalyse:
    '''
    class to perform a global linear analyse
    '''

    def __init__(self, modelList,
                 chooseScaling='mean',
                 levelsFM=None, NlevelsFM=10, spaceFM='lin',
                 levelsAlpha=None, NlevelsAlpha=3, spacing=2.,
                 levelsKS=None, NlevelsKS=100, spaceKS='lin'):

        self.modelList = modelList

        if levelsFM is None:
            self.levelsFM = ugs.findNLevelsML(modelList,NlevelsFM,spaceFM)
        else:
            self.levelsFM = levelsFM
            NlevelsFM = levelsFM.size

        if levelsAlpha is None:
            self.levelsAlpha = np.power(spacing, 1. + np.arange(NlevelsAlpha))
        else:
            self.levelsAlpha = levelsAlpha
            NlevelsAlpha = levelsAlpha.size

        if levelsKS is None:
            self.levelsKS = ugs.findNLevelsML(modelList,NlevelsKS,spaceKS)
        else:
            self.levelsKS = levelsKS

        self.scaling = GlobalScaling(modelList,self.levelsFM)
        self.results = GlobalLinearAnalyseResult(modelList.size,NlevelsFM,NlevelsAlpha)
        self.chooseScaling = chooseScaling
        self.field1 = 0
        self.field2 = 0

    def performAnalyseOn(self, i, j):
        self.field1 = np.fromfile(self.modelList[i])
        self.field2 = np.fromfile(self.modelList[j])
        
        if not chooseScaling=='none':
            self.results.MSE[i,j]    = NMSE_corrected(   self.field1 , self.field2 , self.scaling.chooseScaling(chooseScaling) )
            self.results.FMmini[i,j] = FMmini_corrected( self.field1 , self.field2 , self.scaling.scalingFMmini )
            self.results.bias[i,j]   = bias_corrected(   self.field1 , self.field2 , self.scaling.chooseScaling(chooseScaling) )
            self.results.BcMSE[i,j]  = BcNMSE_corrected( self.field1 , self.field2 , self.scaling.chooseScaling(chooseScaling) )
            self.results.TSS[i,j]    = TSS_corrected(    self.field1 , self.field2 , self.scaling.chooseScaling(chooseScaling) )
            self.results.KS[i,j]     = KSLevels(         self.field1 , self.field2 , self.levelsKS )
            self.results.PCC[i,j]    = PCC(              self.field1 , self.field2 )
            self.results.FOEX[i,j]   = FOEX(             self.field1 , self.field2 )

            for lev in xrange(self.levelsFM.size):
                self.results.FM[i,j,lev] = FM_corrected( self.field1 , self.field2, self.levelsFM[lev], self.scaling.scalingFM[i] )

            for lev in xrange(self.levelsAlpha.size):
                self.results.FA[i,j,lev] = FA( self.field1 , self.field2, self.levelsAlpha[lev] )
                                
        else:
            self.results.MSE[i,j]    = NMSE(         self.field1 , self.field2 )
            self.results.FMmini[i,j] = FMmini(       self.field1 , self.field2 )
            self.results.bias[i,j]   = ralativeBias( self.field1 , self.field2 )
            self.results.BcMSE[i,j]  = BcNMSE(       self.field1 , self.field2 )
            self.results.TSS[i,j]    = TSS(          self.field1 , self.field2 )
            self.results.KS[i,j]     = KSLevels(     self.field1 , self.field2 , self.levelsKS )
            self.results.PCC[i,j]    = PCC(          self.field1 , self.field2 )
            self.results.FOEX[i,j]   = FOEX(         self.field1 , self.field2 )
            
            for lev in xrange(self.levelsFM.size):
                self.results.FM[i,j,lev] = FM( self.field1 , self.field2, self.levelsFM[lev] )

            for lev in xrange(self.levelsAlpha.size):
                self.results.FA[i,j,lev] = FA( self.field1 , self.field2, self.levelsAlpha[lev] )
                                                                                                                                        
        self.field1 = 0
        self.field2 = 0
                
    def performAnalyse(self, printLog=True):
        Nmodels = self.modelList.size
        print('Starting analyse...')
        print('Nmodels = '+str(Nmodels))
        
        for i in xrange(Nmodels):
            for j in xrange(i):
                if printLog:
                    print('Analysing correlation bewteen model '+str(i)+' and model '+str(j)'.')
                self.performAnalyseOn(i,j)

        return self.results

class GlobalLogAnalyseResult:
    '''
    class to store the result of a global log analyse
    '''
    def __init__(self, Nmodels):
        self.Nmodels  = Nmodels
        self.geomVar  = np.zeros(shape=(Nmodels,Nmodels))
        self.geomBias = np.zeros(shape=(Nmodels,Nmodels))
        self.PCClog   = np.zeros(shape=(Nmodels,Nmodels))
        self.KSlog    = np.zeros(shape=(Nmodels,Nmodels))
        
    def tofile(self,fileName):
        f = open(fileName, 'w')
        mat = np.zeros(1)
        mat[0] = self.Nmodels
        mat.tofile(f)
        self.geomVar.tofile(f)
        self.geomBias.tofile(f)
        self.PCClog.tofile(f)
        self.KSlog.tofile(f)
        f.close()
        print(fileName)
        
class GlobalLogAnalyse:
    '''
    class to perform a global log analyse
    '''

    def __init__(self, modelList,
                 levelsKS=None, NlevelsKS=100, spaceKS='log'):
        
        self.modelList = modelList
        
        if levelsKS is None:
            self.levelsKS = ugs.findNLevelsML(modelList,NlevelsKS,spaceKS)
        else:
            self.levelsKS = levelsKS
            
        self.results = GlobalLogAnalyseResult(modelList.size)
        self.field1 = 0
        self.field2 = 0                
        
    def performAnalyseOn(self, i, j):
        self.field1 = np.fromfile(self.modelList[i])
        self.field2 = np.fromfile(self.modelList[j])
                        
        self.results.geomVar[i,j]  = geomVar(  self.field1 , self.field2 )
        self.results.geomBias[i,j] = geomBias( self.field1 , self.field2 )
        self.results.KSlog[i,j]    = KSLevels( self.field1 , self.field2 , self.levelsKS )
        self.results.PCClog[i,j]   = PCC(      self.field1 , self.field2 )

        self.field1 = 0
        self.field2 = 0
                                                                                                                                                    
    def performAnalyse(self, printLog=True):
        Nmodels = self.modelList.size
        print('Starting analyse...')
        print('Nmodels = '+str(Nmodels))

        for i in xrange(Nmodels):
            for j in xrange(i):
                if printLog:
                    print('Analysing correlation bewteen model '+str(i)+' and model '+str(j)'.')
                self.performAnalyseOn(i,j)
                
        return self.results
                                                                                    
