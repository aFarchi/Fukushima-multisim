###############
# plotFields.py
###############

import numpy as np

from ..utils.absolutePath                  import modulePath
from ..utils.absolutePath                  import moduleLauncher

from ..utils.run.run                       import runCommand
from ..utils.species.listOfSpecies         import ListOfSpecies
from ..utils.fields.defineFields           import defineFields
from ..utils.io.readLists                  import readListOfProcesses
from ..utils.io.readLists                  import suffixFileName
from ..utils.scaling.scaling               import arrayToScaling

def makeLauncherPlot2dFields(outputDir, sessionName, nLevelsAnalyse, plotter='imshow', printIO=False):

    figDir        = outputDir + sessionName + 'figures/'
    statDir       = outputDir + sessionName + 'statistics/'
    fileProcesses = outputDir + sessionName + 'list_processes.dat'

    launcherDir   = outputDir + sessionName + 'launchers/plotting/plot2dFields/'
    runCommand('mkdir -p '+launcherDir)

    lists         = ListOfSpecies()
    procList      = readListOfProcesses(fileProcesses, outputDir+sessionName, '/')
    fieldList     = defineFields()

    launcher      = launcherDir + 'plot2dFields.sh'
    f             = open(modulePath() + 'utils/launchers/defaultLauncher.sh', 'r')
    lines         = f.readlines()
    f.close()

    f = open(launcher, 'w')
    for line in lines:
        if '$fileProcesses$' in line:
            f.write(line.replace('$fileProcesses$', launcherDir+'processesPlot2dFields.dat'))
        elif '$launcher$' in line:
            f.write(line.replace('$launcher$', moduleLauncher()))
        elif '$startString$' in line:
            f.write(line.replace('$startString$', 'Plotting 2d fields'))
        elif '$logFile$' in line:
            f.write(line.replace('$logFile$', launcherDir+'logPlot2dFields'))
        elif '$nodesFile$' in line:
            f.write(line.replace('$nodesFile$', launcherDir+'nodesPlot2dFields.dat'))
        else:
            f.write(line)
    f.close()

    fileNameProcesses = launcherDir + 'processesPlot2dFields.dat'
    fileProcesses     = open(fileNameProcesses, 'w')
    fileProcesses.write('FUNCTION'     + '\t' +
                        'OUTPUT_DIR'   + '\t' +
                        'SESSION_NAME' + '\t' +
                        'STAT_DIR'     + '\t' +
                        'FIG_DIR'      + '\t' +
                        'N_LEVELS'     + '\t' +
                        'AOG'          + '\t' +
                        'FIELD_NAME'   + '\t' +
                        'LOL'          + '\t' +
                        'SPECIES'      + '\t' +
                        'XLABEL'       + '\t' +
                        'YLABEL'       + '\t' +
                        'PLOTTER'      + '\t' +
                        'PRINT_IO'     + '\n' )

    for AOG in ['air/','ground/']:
        for GOR in ['gaz','radios']:
            for species in lists.speciesList[GOR]:
                for field in fieldList[AOG]:
                    labels = field.labels
                    for lol in ['lin','log']:
                        fileProcesses.write('plot2dFields'      + '\t' +
                                            outputDir           + '\t' +
                                            sessionName         + '\t' +
                                            statDir             + '\t' +
                                            figDir              + '\t' +
                                            str(nLevelsAnalyse) + '\t' +
                                            AOG                 + '\t' +
                                            field.name          + '\t' +
                                            lol                 + '\t' +
                                            species             + '\t' +
                                            labels[0]           + '\t' +
                                            labels[1]           + '\t' +
                                            plotter             + '\t' +
                                            str(printIO)        + '\n' )

    print('Written '+launcher+' ...')
    print('Written '+fileNameProcesses+' ...')
    runCommand('cp '+modulePath()+'utils/launchers/defaultNodes.dat '+launcherDir+'nodesPlot2dFields.dat')    
    print('Do not forget to specify nodes and log files.')
