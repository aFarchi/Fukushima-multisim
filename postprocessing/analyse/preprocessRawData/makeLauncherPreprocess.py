###########################
# makeLauncherPreprocess.py
###########################

import numpy as np

from ..utils.absolutePath                  import modulePath
from ..utils.absolutePath                  import moduleLauncher

from ..utils.run.run                       import runCommand
from ..utils.species.listOfSpecies         import ListOfSpecies

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
