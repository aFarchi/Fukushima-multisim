import numpy as np
import scipy.stats as st

from utils_statistical_parameters import *
#import utils_global_scaling as ugs
import utils_time_scaling as uts

class TimeScaling:
    '''
    class to save the scalings for a time analyse
    '''

    def __init__(self, modelList, levelsFM, Nt, Nz, Ny, Nx):
        self.mean = uts.scalingByMean(modelList,Nt,Nz,Ny,Nx)
        self.geomMean = uts.scalingByGeomMean(modelList,Nt,Nz,Ny,Nx))
        self.var = uts.scalingByVariance(modelList,Nt,Nz,Ny,Nx))
        self.scalingFMmini = uts.scalingFMmini(modelList,Nt,Nz,Ny,Nx))
        Nlevels = levelsFM.size
        self.scalingFM = np.zeros(shape=(Nt,Nlevels))
        for i in xrange(Nlevels):
            self.scalingFM[:,i] = uts.scalingFM(modelList, levelsFM[i])

    def chooseScaling(self, nt, choose='mean'):
        if choose=='mean':
            return self.mean[nt]
        elif choose=='geomMean':
            return self.geomMean[nt]
        elif choose=='var':
            return self.var[nt]

class LinearTimeAnalyseResult:
    '''
    class to store the result of a linear time analyse
    '''
    def __init__(self, Nmodels, NlevelsFM, NlevelsAlpha, Nt):
        self.Nmodels      = Nmodels
        self.NlevelsFM    = NlevelsFM
        self.NlevelsAlpha = NlevelsAlpha
        self.Nt           = Nt
        self.MSE          = np.zeros(shape=(Nmodels,Nmodels,Nt))
        self.FMmini       = np.zeros(shape=(Nmodels,Nmodels,Nt))
        self.bias         = np.zeros(shape=(Nmodels,Nmodels,Nt))
        self.PCC          = np.zeros(shape=(Nmodels,Nmodels,Nt))
        self.BcMSE        = np.zeros(shape=(Nmodels,Nmodels,Nt))
        self.TSS          = np.zeros(shape=(Nmodels,Nmodels,Nt))        
        self.FOEX         = np.zeros(shape=(Nmodels,Nmodels,Nt))
        self.KS           = np.zeros(shape=(Nmodels,Nmodels,Nt))
        self.FM           = np.zeros(shape=(Nmodels,Nmodels,Nt,NlevelsFM))
        self.FA           = np.zeros(shape=(Nmodels,Nmodels,Nt,NlevelsAlpha))

    def tofile(self,fileName):
        f = open(fileName, 'w')
        mat = np.zeros(4)
        mat[0] = self.Nmodels
        mat[1] = self.NlevelsFM
        mat[2] = self.NlevelsAlpha
        mat[3] = self.Nt
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
        
class LinearTimeAnalyse:
    '''
    class to perform a linear time analyse
    '''

    def __init__(self, modelList,
                 Nt, Nz, Ny, Nx,
                 chooseScaling='mean',
                 levelsFM=None, NlevelsFM=10, spaceFM='lin',
                 levelsAlpha=None, NlevelsAlpha=3, spacing=2.,
                 levelsKS=None, NlevelsKS=100, spaceKS='lin'):

        self.modelList = modelList

        if levelsFM is None:
            self.levelsFM = uts.findNLevelsML(modelList,NlevelsFM,spaceFM,Nt,Nz,Ny,Nx)
        else:
            self.levelsFM = levelsFM
            a,NlevelsFM = levelsFM.shape

        if levelsAlpha is None:
            self.levelsAlpha = np.power(spacing, 1. + np.arange(NlevelsAlpha))
        else:
            self.levelsAlpha = levelsAlpha
            NlevelsAlpha = levelsAlpha.size

        if levelsKS is None:
            self.levelsKS = uts.findNLevelsML(modelList,NlevelsKS,spaceKS,Nt,Nz,Ny,Nx)
        else:
            self.levelsKS = levelsKS

        self.scaling = TimeScaling(modelList,self.levelsFM,Nt,Nz,Ny,Nx)
        self.results = LinearTimeAnalyseResult(modelList.size,NlevelsFM,NlevelsAlpha,Nt)
        self.chooseScaling = chooseScaling
        self.field1 = 0
        self.field2 = 0
        self.Nt = Nt
        self.Nz = Nz
        self.Ny = Ny
        self.Nx = Nx
        self.NlevelsAlpha = NlevelsAlpha
        self.NlevelsFM = NlevelsFM

    def performAnalyseOn(self, i, j):
        self.field1 = np.fromfile(self.modelList[i])
        self.field2 = np.fromfile(self.modelList[j])

        self.field1 = self.field1.reshape((self.Nt,self.Nz*self.Ny*self.Nx))
        self.field2 = self.field2.reshape((self.Nt,self.Nz*self.Ny*self.Nx))
        
        if not chooseScaling=='none':
            for nt in xrange(Nt):
                self.results.MSE[i,j,nt]    = NMSE_corrected(   self.field1[nt,:] , self.field2[nt,:] , self.scaling.chooseScaling(nt,chooseScaling) )
                self.results.FMmini[i,j,nt] = FMmini_corrected( self.field1[nt,:] , self.field2[nt,:] , self.scaling.scalingFMmini[nt] )
                self.results.bias[i,j,nt]   = bias_corrected(   self.field1[nt,:] , self.field2[nt,:] , self.scaling.chooseScaling(nt,chooseScaling) )
                self.results.BcMSE[i,j,nt]  = BcNMSE_corrected( self.field1[nt,:] , self.field2[nt,:] , self.scaling.chooseScaling(nt,chooseScaling) )
                self.results.TSS[i,j,nt]    = TSS_corrected(    self.field1[nt,:] , self.field2[nt,:] , self.scaling.chooseScaling(nt,chooseScaling) )
                self.results.KS[i,j,nt]     = KSLevels(         self.field1[nt,:] , self.field2[nt,:] , self.levelsKS[nt,:] )
                self.results.PCC[i,j,nt]    = PCC(              self.field1[nt,:] , self.field2[nt,:] )
                self.results.FOEX[i,j,nt]   = FOEX(             self.field1[nt,:] , self.field2[nt,:] )

                for lev in xrange(self.NlevelsFM):
                    self.results.FM[i,j,nt,lev] = FM_corrected( self.field1[nt,:] , self.field2[nt,:], self.levelsFM[nt,lev], self.scaling.scalingFM[nt,i] )

                for lev in xrange(self.NlevelsAlpha):
                    self.results.FA[i,j,nt,lev] = FA( self.field1[nt,:] , self.field2[nt,:], self.levelsAlpha[lev] )
                                
        else:
            for nt in xrange(Nt):
                self.results.MSE[i,j,nt]    = NMSE(         self.field1[nt,:] , self.field2[nt,:] )
                self.results.FMmini[i,j,nt] = FMmini(       self.field1[nt,:] , self.field2[nt,:] )
                self.results.bias[i,j,nt]   = ralativeBias( self.field1[nt,:] , self.field2[nt,:] )
                self.results.BcMSE[i,j,nt]  = BcNMSE(       self.field1[nt,:] , self.field2[nt,:] )
                self.results.TSS[i,j,nt]    = TSS(          self.field1[nt,:] , self.field2[nt,:] )
                self.results.KS[i,j,nt]     = KSLevels(     self.field1[nt,:] , self.field2[nt,:] , self.levelsKS[nt,:] )
                self.results.PCC[i,j,nt]    = PCC(          self.field1[nt,:] , self.field2[nt,:] )
                self.results.FOEX[i,j,nt]   = FOEX(         self.field1[nt,:] , self.field2[nt,:] )
            
                for lev in xrange(self.NlevelsFM):
                    self.results.FM[i,j,nt,lev] = FM( self.field1[nt,:] , self.field2[nt,:], self.levelsFM[nt,lev] )

                for lev in xrange(self.NlevelsAlpha):
                    self.results.FA[i,j,nt,lev] = FA( self.field1[nt,:] , self.field2[nt,:], self.levelsAlpha[lev] )
                                                                                                                                        
        self.field1 = 0
        self.field2 = 0
                
    def performAnalyse(self, printLog=True):
        Nmodels = self.modelList.size
        print('Starting linear time analyse...')
        print('Nmodels = '+str(Nmodels))
        
        for i in xrange(Nmodels):
            for j in xrange(i):
                if printLog:
                    print('Analysing correlation bewteen model '+str(i)+' and model '+str(j)'.')
                self.performAnalyseOn(i,j)

        return self.results

class LogTimeAnalyseResult:
    '''
    class to store the result of a log time analyse
    '''
    def __init__(self, Nmodels, Nt):
        self.Nmodels  = Nmodels
        self.geomVar  = np.zeros(shape=(Nmodels,Nmodels, Nt))
        self.geomBias = np.zeros(shape=(Nmodels,Nmodels, Nt))
        self.PCClog   = np.zeros(shape=(Nmodels,Nmodels, Nt))
        self.KSlog    = np.zeros(shape=(Nmodels,Nmodels, Nt))
        self.Nt       = Nt
        
    def tofile(self,fileName):
        f = open(fileName, 'w')
        mat = np.zeros(2)
        mat[0] = self.Nmodels
        mat[1] = self.Nt
        mat.tofile(f)
        self.geomVar.tofile(f)
        self.geomBias.tofile(f)
        self.PCClog.tofile(f)
        self.KSlog.tofile(f)
        f.close()
        print(fileName)
        
class LogTimeAnalyse:
    '''
    class to perform a log time analyse
    '''

    def __init__(self, modelList,
                 Nt, Nz, Ny, Nx,
                 levelsKS=None, NlevelsKS=100, spaceKS='log'):
        
        self.modelList = modelList
        
        if levelsKS is None:
            self.levelsKS = uts.findNLevelsML(modelList,NlevelsKS,spaceKS,Nt,Nz,Ny,Nx)
        else:
            self.levelsKS = levelsKS
            
        self.results = LogAnalyseResult(modelList.size,Nt)
        self.field1 = 0
        self.field2 = 0                
        self.Nt = Nt
        self.Nz = Nz
        self.Ny = Ny
        self.Nx = Nx
        
    def performAnalyseOn(self, i, j):
        self.field1 = np.fromfile(self.modelList[i])
        self.field2 = np.fromfile(self.modelList[j])
        
        self.field1 = self.field1.reshape((self.Nt,self.Nz*self.Ny*self.Nx))
        self.field2 = self.field2.reshape((self.Nt,self.Nz*self.Ny*self.Nx))

        for nt in xrange(Nt):
            self.results.geomVar[i,j,nt]  = geomVar(  self.field1[nt,:] , self.field2[nt,:] )
            self.results.geomBias[i,j,nt] = geomBias( self.field1[nt,:] , self.field2[nt,:] )
            self.results.KSlog[i,j,nt]    = KSLevels( self.field1[nt,:] , self.field2[nt,:] , self.levelsKS[nt,:] )
            self.results.PCClog[i,j,nt]   = PCC(      self.field1[nt,:] , self.field2[nt,:] )

        self.field1 = 0
        self.field2 = 0
                                                                                                                                                    
    def performAnalyse(self, printLog=True):
        Nmodels = self.modelList.size
        print('Starting logarithmic time analyse...')
        print('Nmodels = '+str(Nmodels))

        for i in xrange(Nmodels):
            for j in xrange(i):
                if printLog:
                    print('Analysing correlation bewteen model '+str(i)+' and model '+str(j)'.')
                self.performAnalyseOn(i,j)
                
        return self.results
                                                                                    
