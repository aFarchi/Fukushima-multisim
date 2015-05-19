###############
# plotFields.py
###############

import numpy as np

from ..utils.run.run                       import runCommand
from ..utils.species.listOfSpecies         import ListOfSpecies
from ..utils.fields.defineFields           import defineFields
from ..utils.io.readLists                  import readListOfProcesses
from ..utils.io.readLists                  import suffixFileName
from ..utils.scaling.scaling               import arrayToScaling

from plotter1d                             import plotter1d
from plotter1d                             import multiPlotter1d
from plotter2d                             import plotter2d
from plotter2d                             import multiPlotter2d
from triplotter                            import triPlotter

def plot2dProcessedRawDataSpecies(outputDir, sessionName, statDir, figDir, nLevelsAnalyse,
                                  AOG, fieldName, lol, species, xLabel, yLabel, plotter='imshow', printIO=False, **kwargs):
        
    fileProcesses   = outputDir + sessionName + 'list_processes.dat'
    procList        = readListOfProcesses(fileProcesses, outputDir + sessionName, '/')

    directory       = figDir + AOG + fieldName + '/' + lol + '/' + species + '/'

    fn    = statDir + 'scaling/' + AOG + fieldName + '/' + lol + '/' + species + '.npy'
    array = np.load(fn)
    scale = arrayToScaling(array)

    runCommand('mkdir -p '+directory, printIO)

    if not kwargs.has_key('extent'):
        kwargs['extent'] = [0.0, 1.0, 0.0, 1.0]
    if not kwargs.has_key('interpolation'):
        kwargs['interpolation'] = 'nearest'
    if not kwargs.has_key('colors'):
        kwargs['colors'] = 'k'
    if not kwargs.has_key('linestyles'):
        kwargs['linestyles'] = 'solid'
    if not kwargs.has_key('linewidths'):
        kwargs['linewidths'] = 1.5

    for GS in ['', '_greyScaleThreshold', '_greyScaleNoThreshold']:

        for i in xrange(len(procList)):

            fileName = procList[i] + 'toAnalyse/' + AOG + fieldName + '/' + lol + '/' + species + GS + '.npy'
            Y        = np.load(fileName)
            figName  = directory + species + GS + '_' + suffixFileName(i, len(procList)) + '.pdf'

            if 'greyScale' in GS:
                X = np.linspace(scale.mini, scale.maxi, nLevelsAnalyse)
                plotter1d(figName, X, Y, ylims=[0.0 ,1.0], title=fieldName+'\n grey scale', grid=True, printIO=printIO)
            else:
                plotter2d(figName, Y, scale.mini, scale.maxi, plotter=plotter, title=fieldName, xLabel=xLabel, yLabel=yLabel, printIO=printIO, **kwargs)

        fileNames = []
        for proc in procList:
            fileNames.append(proc + 'toAnalyse/' + AOG + fieldName + '/' + lol + '/' + species + GS + '.npy')
        figName = directory + species + GS + '_allSim.pdf'

        if 'greyScale' in GS:
            X = np.linspace(scale.mini, scale.maxi, nLevelsAnalyse)
            multiPlotter1d(figName, X, fileNames, ylims=[0.0 ,1.0], supTitle=fieldName+'\n grey scale', grid=True, printIO=printIO)
        elif len(Y.shape) == 2:
            multiPlotter2d(figName, fileNames, scale.mini, scale.maxi, plotter=plotter, supTitle=fieldName, printIO=printIO, **kwargs)

    for i in xrange(len(procList)):
        prefixFn = fileName = procList[i] + 'toAnalyse/' + AOG + fieldName + '/' + lol + '/' + species
        Y    = np.load(prefixFn+'.npy')
        GST  = np.load(prefixFn+'_greyScaleThreshold.npy')
        GSNT = np.load(prefixFn+'_greyScaleNoThreshold.npy')
        XGS  = np.linspace(scale.mini, scale.maxi, nLevelsAnalyse)

        figName  = directory + species + '_triPlot_' + suffixFileName(i, len(procList)) + '.pdf'
        triPlotter(figName, XGS, GST, GSNT, Y, plotter=plotter, title=fieldName, xLabel=xLabel, yLabel=yLabel,
                   mini=scale.mini, maxi=scale.maxi, printIO=printIO)

def plot2dFields(outputDir, sessionName, nLevelsAnalyse, plotter='imshow', printIO=False, **kwargs):

    figDir        = outputDir + sessionName + 'figures/'
    fileProcesses = outputDir + sessionName + 'list_processes.dat'
    statDir       = outputDir + sessionName + 'statistics/'
    
    lists         = ListOfSpecies()
    procList      = readListOfProcesses(fileProcesses, outputDir+sessionName, '/')
    fieldList     = defineFields()

    for AOG in ['air/','ground/']:
        for GOR in ['gaz','radios']:
            for species in lists.speciesList[GOR]:
                for field in fieldList[AOG]:
                    labels = field.labels
                    for lol in ['lin','log']:
                        plot2dProcessedRawDataSpecies(outputDir, sessionName, statDir, figDir, nLevelsAnalyse,
                                                      AOG, field.name, lol, species, labels[0], labels[1], plotter, printIO, **kwargs)
