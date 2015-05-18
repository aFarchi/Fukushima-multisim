######################
# preprocessRawData.py
######################

import numpy as np

from ..utils.absolutePath                  import modulePath
from ..utils.absolutePath                  import moduleLauncher

from ..utils.run.run                       import runCommand
from ..utils.processRawData.extractRawData import extractRawData
from ..utils.operators.zeroFilter          import ZeroFilter
from ..utils.operators.log10               import Log10Function
from ..utils.scaling.scaling               import computeScaling
from ..utils.scaling.scaling               import computeFMScaling
from ..utils.scaling.scaling               import mergeScalings
from ..utils.scaling.scaling               import addFMScaling
from ..utils.scaling.scaling               import scalingToArray
from ..utils.scaling.greyScale             import computeGreyScale
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
                                 zeroFilter, log10,
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

                gst  = computeGreyScale(data, levels, threshold=True)
                gsnt = computeGreyScale(data, levels, threshold=False)

                fn = proc + 'toAnalyse/' + AOG + field.name + '/' + lol + '/' + species + '_greyScaleThreshold.npy'
                if printIO:
                    print ('Writing ' + fn + ' ...')
                np.save(fn, gst)

                fn = proc + 'toAnalyse/' + AOG + field.name + '/' + lol + '/' + species + '_greyScaleNoThreshold.npy'
                if printIO:
                    print ('Writing ' + fn + ' ...')
                np.save(fn, gsnt)

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
    completeScalingMakeGreyScale(species, AOG, GOR,
                                 fieldList[AOG], procList, lists.speciesBinList[GOR],
                                 lists.rawShapes[GOR][AOG], nLevelsAnalyse, deltaT,
                                 zeroFilter, log10,
                                 scaling, statDir,
                                 printIO)

def prepareAllFields(outputDir, sessionName, funTSelect, analyseShape, nLevelsAnalyse, printIO=False):

    lists = ListOfSpecies(outputDir+sessionName+'config/')

    for AOG in ['air/','ground/']:
        for GOR in ['gaz','radios']:
            for species in lists.speciesList[GOR]:
                prepareSpecies(outputDir, sessionName, funTSelect, analyseShape, nLevelsAnalyse, AOG, GOR, species, printIO)


def makeLancherPrepareAllFields(outputDir, sessionName, xTSelect, analyseShape, nLevelsAnalyse, printIO=False):
    launcherDir = outputDir+sessionName+'launchers/prepareAllFields/'
    runCommand('mkdir -p '+launcherDir, printIO)

    defaultLauncher = modulePath() + 'utils/launchers/defaultLauncher.sh'
    f               = open(defaultLauncher, 'r')
    lines           = f.readlines()
    f.close()
    
    launcher        = launcherDir + 'prepareAllFields.sh'
    f               = open(launcher, 'w')

    for line in lines:
        if '$fileProcesses$' in line:
            f.write(line.replace('$fileProcesses$', launcherDir+'processesPrepareAllFields.dat'))
        elif '$launcher$' in line:
            f.write(line.replace('$launcher$', moduleLauncher()))
        elif '$startString$' in line:
            f.write(line.replace('$startString$', 'Preparing all fields'))
        elif '$logFile$' in line:
            f.write(line.replace('$logFile$', launcherDir+'logPrepareAllFields'))
        elif '$nodesFile$' in line:
            f.write(line.replace('$nodesFile$', launcherDir+'nodes.dat'))
        else:
            f.write(line)
    f.close()

    processes = launcherDir + 'processesPrepareAllFields.dat'
    f         = open(processes, 'w')

    header    = ( 'FUNCTION'     + '\t' +
                  'OUTPUT_DIR'   + '\t' +
                  'SESSION_NAME' + '\t' +
                  'X_TSELECT'    + '\t' +
                  'NT_ANALYSE'   + '\t' +
                  'NZ_ANALYSE'   + '\t' +
                  'NY_ANALYSE'   + '\t' +
                  'NX_ANALYSE'   + '\t' +
                  'N_LEVELS'     + '\t' +
                  'AOG'          + '\t' +
                  'GOR'          + '\t' +
                  'SPECIES'      + '\t' +
                  'PRINT_IO'     + '\n' )
    f.write(header)

    lists = ListOfSpecies(outputDir+sessionName+'config/')
    for AOG in ['air/','ground/']:
        for GOR in ['gaz','radios']:
            for species in lists.speciesList[GOR]:
                line = ( 'prepareSpecies'      + '\t' +
                         outputDir             + '\t' +
                         sessionName           + '\t' +
                         str(xTSelect)         + '\t' +
                         str(analyseShape[0])  + '\t' +
                         str(analyseShape[1])  + '\t' +
                         str(analyseShape[2])  + '\t' +
                         str(analyseShape[3])  + '\t' +
                         str(nLevelsAnalyse)   + '\t' +
                         AOG                   + '\t' +
                         GOR                   + '\t' +
                         species               + '\t' +
                         str(printIO)          + '\n' )
                f.write(line)
    f.close()

    print('Written '+launcher+' ...')
    print('Written '+processes+' ...')
    runCommand('cp '+modulePath()+'utils/launchers/defaultNodes.dat '+launcherDir+'nodes.dat')
    print('Do not forget to specify nodes and log files.')
