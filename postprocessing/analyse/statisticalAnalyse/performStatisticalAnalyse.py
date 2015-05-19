##############################
# performStatisticalAnalyse.py
##############################

import numpy as np
from numpy.linalg import eigh

import statisticalOperators as stats

from ..utils.run.run               import runCommand
from ..utils.io.readLists          import readListOfProcesses
from ..utils.io.readLists          import suffixFileName
from ..utils.absolutePath          import moduleLauncher
from ..utils.species.listOfSpecies import ListOfSpecies
from ..utils.fields.defineFields   import defineFields
from ..utils.scaling.scaling       import arrayToScaling

def saveSymMatrixEig(prefixFileName, matrix):
    n = matrix.shape[0]

    (eigVals,eigVects) = eigh(matrix)

    indexes            = np.argsort(eigVals)
    i                  = np.arange(n)

    sortedEigVals      = eigVals[indexes[n-1-i]]
    sortedEigVects     = eigVects[:, indexes[n-1-i]]

    np.save(prefixFileName+'.npy', matrix)
    np.save(prefixFileName+'_eigVals', sortedEigVals)
    np.save(prefixFileName+'_eigVects', sortedEigVects)

class Analyser:
    def __init__(self, nbrProc, scaling, chooseScaling='mean'):
        self.scaling = scaling
        self.nLevelsAnalyse = len(scaling.scalingFM)
        self.levelsNFM = np.linspace(scaling.mini, scaling.maxi, self.nLevelsAnalyse)
        self.levelsAlpha = np.power(10. , 0.1*np.arange(self.nLevelsAnalyse))

        if chooseScaling == 'geomMean':
            self.scaling.generalScale = self.scaling.geomMeanMeans
        elif chooseScaling == 'var':
            self.scaling.generalScale = self.scaling.meanVars
        else:
            self.scaling.generalScale = self.scaling.meanMeans
                        
        self.MSE     = np.zeros(shape=(nbrProc,nbrProc))
        self.NFMmini = np.zeros(shape=(nbrProc,nbrProc))
        self.bias    = np.zeros(shape=(nbrProc,nbrProc))
        self.BcMSE   = np.zeros(shape=(nbrProc,nbrProc))
        self.TSS     = np.zeros(shape=(nbrProc,nbrProc))
        self.PCC     = np.zeros(shape=(nbrProc,nbrProc))
        self.FOEX    = np.zeros(shape=(nbrProc,nbrProc))
        
        self.NFM     = np.zeros(shape=(nbrProc,nbrProc,self.nLevelsAnalyse))
        self.FAalpha = np.zeros(shape=(nbrProc,nbrProc,self.nLevelsAnalyse))

        self.correctZeroScalings()

    def correctZeroScalings(self):
        if self.scaling.generalScale == 0.0:
            self.scaling.generalScale = 1.0
        if self.scaling.sumMaximum == 0.0:
            self.scaling.sumMaximum = 1.0

        for k in xrange(self.nLevelsAnalyse):
            if self.scaling.scalingFM[k] == 0.0:
                self.scaling.scalingFM[k] = 1.0

    def applyOperators(self, i, j, field0, field1, applyScaling=True):
        if not applyScaling :
            self.MSE[i,j]     = stats.MSE(    field0, field1)
            self.NFMmini[i,j] = stats.NFMmini(field0, field1)
            self.bias[i,j]    = stats.bias(   field0, field1)
            self.BcMSE[i,j]   = stats.BcMSE(  field0, field1)
            self.TSS[i,j]     = stats.TSS(    field0, field1)
            for k in xrange(self.nLevelsAnalyse):
                self.NFM[i,j,k]     = stats.NFM(field0, field1, self.levelsNFM[k])
        else:
            self.MSE[i,j]     = stats.NMSE_corrected(   field0, field1, self.scaling.generalScale)
            self.NFMmini[i,j] = stats.NFMmini_corrected(field0, field1, self.scaling.sumMaximum)
            self.bias[i,j]    = stats.Nbias_corrected(  field0, field1, self.scaling.generalScale)
            self.BcMSE[i,j]   = stats.BcNMSE_corrected( field0, field1, self.scaling.generalScale)
            self.TSS[i,j]     = stats.TSS_corrected(    field0, field1, self.scaling.generalScale)
            for k in xrange(self.nLevelsAnalyse):
                self.NFM[i,j,k]     = stats.NFM_corrected(field0, field1, self.levelsNFM[k], self.scaling.scalingFM[k])

        self.PCC[i,j]     = stats.PCC( field0, field1)
        self.FOEX[i,j]    = stats.FOEX(field0, field1)
        for k in xrange(self.nLevelsAnalyse):
            self.FAalpha[i,j,k] = stats.FA(field0, field1, self.levelsAlpha[k])

    def fill(self):
        for i in xrange(self.MSE.shape[0]):
            for j in xrange(i):
                self.MSE[j,i]     = self.MSE[i,j]
                self.NFMmini[j,i] = self.NFMmini[i,j]
                self.bias[j,i]    = self.bias[i,j]
                self.BcMSE[j,i]   = self.BcMSE[i,j]
                self.TSS[j,i]     = self.TSS[i,j]
                self.PCC[j,i]     = self.PCC[i,j]
                self.FOEX[j,i]    = self.FOEX[i,j]
                for k in xrange(self.nLevelsAnalyse):
                    self.NFM[j,i,k]     = self.NFM[i,j,k]
                for k in xrange(self.nLevelsAnalyse):
                    self.FAalpha[j,i,k] = self.FAalpha[i,j,k]

            self.MSE[i,i]     = 0.0
            self.NFMmini[i,i] = 1.0
            self.bias[i,i]    = 0.0
            self.BcMSE[i,i]   = 0.0
            self.TSS[i,i]     = 1.0
            self.PCC[i,i]     = 1.0
            self.FOEX[i,i]    = 0.0
            for k in xrange(self.nLevelsAnalyse):
                self.NFM[i,i,k]     = 1.0
            for k in xrange(self.nLevelsAnalyse):
                self.FAalpha[i,i,k] = 1.0

    def toFiles(self, directory, printIO):
        if printIO:
            print ('Writing analyse result in ' + directory + ' ...')
        saveSymMatrixEig(directory + 'MSE',     self.MSE)
        saveSymMatrixEig(directory + 'NFMmini', self.NFMmini)
        saveSymMatrixEig(directory + 'bias',    self.bias)
        saveSymMatrixEig(directory + 'BcMSE',   self.BcMSE)
        saveSymMatrixEig(directory + 'TSS',     self.TSS)
        saveSymMatrixEig(directory + 'PCC',     self.PCC)
        saveSymMatrixEig(directory + 'FOEX',    self.FOEX)

        for k in xrange(len(self.levelsNFM)):
            saveSymMatrixEig(directory + 'NFM' + suffixFileName(k,self.nLevelsAnalyse), self.NFM[:,:,k])
        for k in xrange(len(self.levelsAlpha)):
            saveSymMatrixEig(directory + 'FA'  + suffixFileName(k,self.nLevelsAnalyse), self.FAalpha[:,:,k])

def analyseField(AOG, GS, field, lol, procList, statDir, speciesList, printIO):

    for species in speciesList:
        speDir = statDir + 'result/' + AOG + field.name + '/' + lol + '/' + species + GS + '/'
        runCommand('mkdir -p ' + speDir, printIO)
        fn     = statDir + 'scaling/' + AOG + field.name + '/' + lol + '/' + species + '.npy'
        array  = np.load(fn)
        scale  = arrayToScaling(array)

        if 'greyScale' in GS:
            scale.mini = 0.
            scale.maxi = 1.

        result = Analyser(len(procList), scale, chooseScaling='mean')

        for i in xrange(len(procList)):
            for j in xrange(i):

                fnI   = procList[i] + 'toAnalyse/' + AOG + field.name + '/' + lol + '/' + species + GS + '.npy'
                dataI = np.load(fnI)

                fnJ   = procList[j] + 'toAnalyse/' + AOG + field.name + '/' + lol + '/' + species + GS + '.npy'
                dataJ = np.load(fnJ)

                applyScaling = ( lol == 'lin' ) and not ( 'greyScale' in GS )
                
                result.applyOperators(i, j, dataI, dataJ, applyScaling)

        result.fill()
        result.toFiles(speDir, printIO)

def analyseAllFields(outputDir, sessionName, printIO):

    statDir       = outputDir + sessionName + 'statistics/'
    fileProcesses = outputDir + sessionName + 'list_processes.dat'

    lists = ListOfSpecies()

    # Name of processes
    procList = readListOfProcesses(fileProcesses, outputDir + sessionName, '/')

    # Fields
    fieldList = defineFields()

    for AOG in ['air/','ground/']:
        for GOR in ['gaz','radios']:
            for field in fieldList[AOG]:
                for lol in ['lin','log']:
                    for GS in ['', '_greyScaleThreshold', '_greyScaleNoThreshold']:
                        analyseField(AOG, GS, field, lol, procList, statDir, lists.speciesList[GOR], printIO)
