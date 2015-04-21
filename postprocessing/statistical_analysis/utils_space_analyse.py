import numpy as np
import scipy.stats as st

from utils_statistical_parameters import *
import utils_space_scaling as uss

class SpaceScaling:
    '''
    class to save the scalings for a space analyse
    '''

    def __init__(self, modelList, levelsFM, Nt, Nz, Ny, Nx):
        self.mean = uss.scalingByMean(modelList,Nt,Nz,Ny,Nx)
        self.geomMean = uss.scalingByGeomMean(modelList,Nt,Nz,Ny,Nx))
        self.var = uss.scalingByVariance(modelList,Nt,Nz,Ny,Nx))
        self.scalingFMmini = uss.scalingFMmini(modelList,Nt,Nz,Ny,Nx))
        Nlevels = levelsFM.size
        self.scalingFM = np.zeros(shape=(Nz,Ny,Nx,Nlevels))
        for i in xrange(Nlevels):
            self.scalingFM[:,:,:,i] = uss.scalingFM(modelList, levelsFM[i])

    def chooseScaling(self, nz, ny, nx, choose='mean'):
        if choose=='mean':
            return self.mean[nz, ny, nx]
        elif choose=='geomMean':
            return self.geomMean[nz, ny, nx]
        elif choose=='var':
            return self.var[nz, ny, nx]

class LinearSpaceAnalyseResult:
    '''
    class to store the result of a linear space analyse
    '''
    def __init__(self, Nmodels, NlevelsFM, NlevelsAlpha, Nz, Ny, Nx):
        self.Nmodels      = Nmodels
        self.NlevelsFM    = NlevelsFM
        self.NlevelsAlpha = NlevelsAlpha
        self.Nz           = Nz
        self.Ny           = Ny
        self.Nx           = Nx
        self.MSE          = np.zeros(shape=(Nmodels,Nmodels,Nz,Ny,Nx))
        self.FMmini       = np.zeros(shape=(Nmodels,Nmodels,Nz,Ny,Nx))
        self.bias         = np.zeros(shape=(Nmodels,Nmodels,Nz,Ny,Nx))
        self.PCC          = np.zeros(shape=(Nmodels,Nmodels,Nz,Ny,Nx))
        self.BcMSE        = np.zeros(shape=(Nmodels,Nmodels,Nz,Ny,Nx))
        self.TSS          = np.zeros(shape=(Nmodels,Nmodels,Nz,Ny,Nx))        
        self.FOEX         = np.zeros(shape=(Nmodels,Nmodels,Nz,Ny,Nx))
        self.KS           = np.zeros(shape=(Nmodels,Nmodels,Nz,Ny,Nx))
        self.FM           = np.zeros(shape=(Nmodels,Nmodels,Nz,Ny,Nx,NlevelsFM))
        self.FA           = np.zeros(shape=(Nmodels,Nmodels,Nz,Ny,Nx,NlevelsAlpha))

    def tofile(self,fileName):
        f = open(fileName, 'w')
        mat = np.zeros(6)
        mat[0] = self.Nmodels
        mat[1] = self.NlevelsFM
        mat[2] = self.NlevelsAlpha
        mat[3] = self.Nz
        mat[4] = self.Ny
        mat[5] = self.Nx
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
        
class LinearSpaceAnalyse:
    '''
    class to perform a linear space analyse
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
            a,b,c,NlevelsFM = levelsFM.shape

        if levelsAlpha is None:
            self.levelsAlpha = np.power(spacing, 1. + np.arange(NlevelsAlpha))
        else:
            self.levelsAlpha = levelsAlpha
            NlevelsAlpha = levelsAlpha.size

        if levelsKS is None:
            self.levelsKS = uts.findNLevelsML(modelList,NlevelsKS,spaceKS,Nt,Nz,Ny,Nx)
        else:
            self.levelsKS = levelsKS

        self.scaling = SpaceScaling(modelList,self.levelsFM,Nt,Nz,Ny,Nx)
        self.results = LinearSpaceAnalyseResult(modelList.size,NlevelsFM,NlevelsAlpha,Nz,Ny,Nx)
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

        self.field1 = self.field1.reshape((self.Nt,self.Nz,self.Ny,self.Nx))
        self.field2 = self.field2.reshape((self.Nt,self.Nz,self.Ny,self.Nx))
        
        if not chooseScaling=='none':
            for nz in xrange(Nz):
                for ny in xrange(Ny):
                    for nx in xrange(Nx):
                        self.results.MSE[i,j,nz,ny,nx]    = NMSE_corrected(   self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] , self.scaling.chooseScaling(nz,ny,nx,chooseScaling) )
                        self.results.FMmini[i,j,nz,ny,nx] = FMmini_corrected( self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] , self.scaling.scalingFMmini[nz,ny,nx] )
                        self.results.bias[i,j,nz,ny,nx]   = bias_corrected(   self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] , self.scaling.chooseScaling(nz,ny,nx,chooseScaling) )
                        self.results.BcMSE[i,j,nz,ny,nx]  = BcNMSE_corrected( self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] , self.scaling.chooseScaling(nz,ny,nx,chooseScaling) )
                        self.results.TSS[i,j,nz,ny,nx]    = TSS_corrected(    self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] , self.scaling.chooseScaling(nz,ny,nx,chooseScaling) )
                        self.results.KS[i,j,nz,ny,nx]     = KSLevels(         self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] , self.levelsKS[nz,ny,nx,:] )
                        self.results.PCC[i,j,nz,ny,nx]    = PCC(              self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )
                        self.results.FOEX[i,j,nz,ny,nx]   = FOEX(             self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )

                        for lev in xrange(self.NlevelsFM):
                            self.results.FM[i,j,nz,ny,nx,lev] = FM_corrected( self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx], self.levelsFM[nz,ny,nx,lev], self.scaling.scalingFM[nz,ny,nx,i] )

                        for lev in xrange(self.NlevelsAlpha):
                            self.results.FA[i,j,nz,ny,nx,lev] = FA( self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx], self.levelsAlpha[lev] )
                                
        else:
            for nz in xrange(Nz):
                for ny in xrange(Ny):
                    for nx in xrange(Nx):
                        self.results.MSE[i,j,nz,ny,nx]    = NMSE(         self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )
                        self.results.FMmini[i,j,nz,ny,nx] = FMmini(       self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )
                        self.results.bias[i,j,nz,ny,nx]   = ralativeBias( self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )
                        self.results.BcMSE[i,j,nz,ny,nx]  = BcNMSE(       self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )
                        self.results.TSS[i,j,nz,ny,nx]    = TSS(          self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )
                        self.results.KS[i,j,nz,ny,nx]     = KSLevels(     self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] , self.levelsKS[nz,ny,nx,:] )
                        self.results.PCC[i,j,nz,ny,nx]    = PCC(          self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )
                        self.results.FOEX[i,j,nz,ny,nx]   = FOEX(         self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )
            
                        for lev in xrange(self.NlevelsFM):
                            self.results.FM[i,j,nz,ny,nx,lev] = FM( self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx], self.levelsFM[nz,ny,nx,lev] )

                        for lev in xrange(self.NlevelsAlpha):
                            self.results.FA[i,j,nz,ny,nx,lev] = FA( self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx], self.levelsAlpha[lev] )
                                                                                                                                        
        self.field1 = 0
        self.field2 = 0
                
    def performAnalyse(self, printLog=True):
        Nmodels = self.modelList.size
        print('Starting linear space analyse...')
        print('Nmodels = '+str(Nmodels))
        
        for i in xrange(Nmodels):
            for j in xrange(i):
                if printLog:
                    print('Analysing correlation bewteen model '+str(i)+' and model '+str(j)'.')
                self.performAnalyseOn(i,j)

        return self.results

class LogSpaceAnalyseResult:
    '''
    class to store the result of a log space analyse
    '''
    def __init__(self, Nmodels, Nz, Ny, Nx):
        self.Nmodels  = Nmodels
        self.geomVar  = np.zeros(shape=(Nmodels,Nmodels, Nz, Ny, Nx))
        self.geomBias = np.zeros(shape=(Nmodels,Nmodels, Nz, Ny, Nx))
        self.PCClog   = np.zeros(shape=(Nmodels,Nmodels, Nz, Ny, Nx))
        self.KSlog    = np.zeros(shape=(Nmodels,Nmodels, Nz, Ny, Nx))
        self.Nz       = Nz
        self.Ny       = Ny
        self.Nx       = Nx
        
    def tofile(self,fileName):
        f = open(fileName, 'w')
        mat = np.zeros(4)
        mat[0] = self.Nmodels
        mat[1] = self.Nz
        mat[2] = self.Ny
        mat[3] = self.Nx
        mat.tofile(f)
        self.geomVar.tofile(f)
        self.geomBias.tofile(f)
        self.PCClog.tofile(f)
        self.KSlog.tofile(f)
        f.close()
        print(fileName)
        
class LogSpaceAnalyse:
    '''
    class to perform a log space analyse
    '''

    def __init__(self, modelList,
                 Nt, Nz, Ny, Nx,
                 levelsKS=None, NlevelsKS=100, spaceKS='log'):
        
        self.modelList = modelList
        
        if levelsKS is None:
            self.levelsKS = findNLevelsML(modelList,NlevelsKS,spaceKS)
        else:
            self.levelsKS = levelsKS
            
        self.results = LogAnalyseResult(modelList.size,Nz,Ny,Nx)
        self.field1 = 0
        self.field2 = 0                
        self.Nt = Nt
        self.Nz = Nz
        self.Ny = Ny
        self.Nx = Nx
        
    def performAnalyseOn(self, i, j):
        self.field1 = np.fromfile(self.modelList[i])
        self.field2 = np.fromfile(self.modelList[j])
        
        self.field1 = self.field1.reshape((self.Nt,self.Nz,self.Ny,self.Nx))
        self.field2 = self.field2.reshape((self.Nt,self.Nz,self.Ny,self.Nx))

        for nz in xrange(Nz):
            for ny in xrange(Ny):
                for nx in xrange(Nx):
                    self.results.geomVar[i,j,nz,ny,nx]  = geomVar(  self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )
                    self.results.geomBias[i,j,nz,ny,nx] = geomBias( self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )
                    self.results.KSlog[i,j,nz,ny,nx]    = KSLevels( self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] , self.levelsKS[nz,ny,nx,:] )
                    self.results.PCClog[i,j,nz,ny,nx]   = PCC(      self.field1[:,nz,ny,nx] , self.field2[:,nz,ny,nx] )

        self.field1 = 0
        self.field2 = 0
                                                                                                                                                    
    def performAnalyse(self, printLog=True):
        Nmodels = self.modelList.size
        print('Starting logarithmic space analyse...')
        print('Nmodels = '+str(Nmodels))

        for i in xrange(Nmodels):
            for j in xrange(i):
                if printLog:
                    print('Analysing correlation bewteen model '+str(i)+' and model '+str(j)'.')
                self.performAnalyseOn(i,j)
                
        return self.results
                                                                                    
