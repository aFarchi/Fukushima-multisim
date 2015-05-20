######################
# preprocessRawData.py
######################

import numpy as np

from ..utils.run.run                       import runCommand
from ..utils.processRawData.extractRawData import extractRawData
from ..utils.operators.zeroFilter          import ZeroFilter
from ..utils.operators.log10               import Log10Function
from ..utils.scaling.scaling               import computeScaling
from ..utils.scaling.scaling               import computeFMScaling
from ..utils.scaling.scaling               import mergeScalings
from ..utils.scaling.scaling               import addFMScaling
from ..utils.scaling.scaling               import scalingToArray
from ..utils.scaling.greyScale             import GreyScaleMaker
from ..utils.species.listOfSpecies         import ListOfSpecies
from ..utils.io.readLists                  import readListOfProcesses
from ..utils.fields.defineFields           import defineFields

def createDirectories(AOG, fieldList, procList, statDir, printIO=False):

    for field in fieldList:
        for lol in ['/lin','/log']:
            runCommand('mkdir -p '+statDir+'scaling/'+AOG+field.name+lol, printIO)
            for proc in procList:
                runCommand('mkdir -p '+proc+'toAnalyse/'+AOG+field.name+lol, printIO)

def preprocessSpeciesRawData(species, AOG, GOR, 
                             fieldList, procList, speciesBinList, 
                             rawShape, analyseShape, deltaT, 
                             zeroFilter, log10, 
                             printIO=False):

    scaling   = {}
    maximum   = {}
    for lol in ['lin','log']:
        scaling[lol]   = {}
        maximum[lol]   = {}
        for field in fieldList:
            scaling[lol][field]   = {}

    for proc in procList:
        rawData = extractRawData(proc, AOG, GOR, species, speciesBinList, rawShape, deltaT, printIO)
        rawData = zeroFilter(rawData, AOG)
            
        for field in fieldList:
            for lol in ['lin','log']:
                if lol == 'log':
                    data = field.extract(log10(rawData, AOG))
                else:
                    data = field.extract(rawData)
                        
                try:
                    maximum[lol][field] = np.maximum( maximum[lol][field] , data )
                except:
                    maximum[lol][field] = data

                scaling[lol][field][proc] = computeScaling(data)
                data                      = field.interpolate(data, analyseShape)

                fn = proc + 'toAnalyse/' + AOG + field.name + '/' + lol + '/' + species + '.npy'
                if printIO:
                    print ('Writing ' + fn + ' ...')
                np.save(fn, data)

    return mergeScalings(scaling, maximum, fieldList, procList)

def completeScalingMakeGreyScale(species, AOG, GOR,
                                 fieldList, procList, speciesBinList,
                                 rawShape, nLevelsAnalyse, deltaT,
                                 zeroFilter, log10, gsMakers,
                                 scaling, statDir,
                                 printIO=False):

    scalingFM = {}
    for lol in ['lin','log']:
        scalingFM[lol] = {}
        for field in fieldList:
            scalingFM[lol][field] = {}

    for proc in procList:
        rawData = extractRawData(proc, AOG, GOR, species, speciesBinList, rawShape, deltaT, printIO)
        rawData = zeroFilter(rawData, AOG)

        for field in fieldList:
            for lol in ['lin','log']:
                if lol == 'log':
                    data = field.extract(log10(rawData,AOG))
                else:
                    data = field.extract(rawData)

                mini   = scaling[field][lol].mini
                maxi   = scaling[field][lol].maxi
                levels = np.linspace(mini, maxi, nLevelsAnalyse)

                scalingFM[lol][field][proc] = computeFMScaling(data, levels)

                for TS in ['Threshold', 'NoThreshold']:
                    gs = gsMakers[lol][TS](data, AOG, levels)
                    fn = proc + 'toAnalyse/' + AOG + field.name + '/' + lol + '/' + species + '_greyScale' + TS + '.npy'
                    np.save(fn, gs)
                    if printIO:
                        print ('Writing ' + fn + ' ...')

    scaling = addFMScaling(scaling, scalingFM, fieldList, procList)

    for field in fieldList:
        for lol in ['lin','log']:
            
            fn = statDir + 'scaling/' + AOG + field.name + '/' + lol + '/' + species + '.npy'
            if printIO:
                print ('Writing ' + fn + ' ...')
            array = scalingToArray(scaling[field][lol])
            np.save(fn, array)

def prepareSpecies(outputDir, sessionName, funTSelect, analyseShape, nLevelsAnalyse, AOG, GOR, species, printIO=False):
    statDir              = outputDir + sessionName + 'statistics/'
    fileProcesses        = outputDir + sessionName + 'list_processes.dat'
    fileLevels           = outputDir + sessionName + 'config/levels.dat'

    # zeroFilter and log10 filter with default values
    minValues            = {}
    minValues['air/']    = 1.e-10 # in Bq/m^2
    minValues['ground/'] = 1.e-10 # in Bq/m^3

    log10                = Log10Function(minValues)
    zeroFilter           = ZeroFilter(minValues)
    # deltaT should be catched from config file ...
    deltaT               = 3600.

    # List of species
    lists                = ListOfSpecies(outputDir+sessionName+'config/')

    # Name of processes
    procList             = readListOfProcesses(fileProcesses, outputDir + sessionName, '/')

    # Fields
    fieldList            = defineFields(funTSelect, fileLevels)

    createDirectories(AOG, fieldList[AOG], procList, statDir, printIO)
    scaling = preprocessSpeciesRawData(species, AOG, GOR, fieldList[AOG], procList, lists.speciesBinList[GOR],
                                       lists.rawShapes[GOR][AOG], analyseShape, deltaT,
                                       zeroFilter, log10,
                                       printIO)

    minValuesGS             = {}
    minValuesGS['air/']     = 1.e-11
    minValuesGS['ground/']  = 1.e-11
    zeroFilterGS            = ZeroFilter(minValuesGS)

    minValuesLog            = {}
    minValuesLog['air/']    = 0.0
    minValuesLog['ground/'] = 0.0

    gsMakers                       = {}
    gsMakers['lin']                = {}
    gsMakers['lin']['Threshold']   = GreyScaleMaker(minValues, True)
    gsMakers['lin']['NoThreshold'] = GreyScaleMaker(minValues, False)
    gsMakers['log']                = {}
    gsMakers['log']['Threshold']   = GreyScaleMaker(minValues, True)
    gsMakers['log']['NoThreshold'] = GreyScaleMaker(minValues, False)
    
    completeScalingMakeGreyScale(species, AOG, GOR,
                                 fieldList[AOG], procList, lists.speciesBinList[GOR],
                                 lists.rawShapes[GOR][AOG], nLevelsAnalyse, deltaT,
                                 zeroFilterGS, log10, gsMakers, 
                                 scaling, statDir,
                                 printIO)

def prepareAllFields(outputDir, sessionName, funTSelect, analyseShape, nLevelsAnalyse, printIO=False):

    lists = ListOfSpecies(outputDir+sessionName+'config/')

    for AOG in ['air/','ground/']:
        for GOR in ['gaz','radios']:
            for species in lists.speciesList[GOR]:
                prepareSpecies(outputDir, sessionName, funTSelect, analyseShape, nLevelsAnalyse, AOG, GOR, species, printIO)
