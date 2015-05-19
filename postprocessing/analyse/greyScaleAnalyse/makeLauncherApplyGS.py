########################
# makeLauncherApplyGS.py
########################

from ..utils.absolutePath                  import modulePath
from ..utils.absolutePath                  import moduleLauncher

from ..utils.run.run                       import runCommand
from ..utils.species.listOfSpecies         import ListOfSpecies
from ..utils.fields.defineFields           import defineFields
from ..utils.io.readLists                  import readListOfProcesses
 
def makeLauncherApplyGS(outputDir, sessionName, printIO=False):
    OTGSDir        = outputDir + sessionName + 'OTGS/'
    applyOTGSDir   = outputDir + sessionName + 'applyOTGS/'
    statDir        = outputDir + sessionName + 'statistics/'
    fileProcesses  = outputDir + sessionName + 'list_processes.dat'

    launcherDir    = outputDir + sessionName + 'launchers/applyGS/'
    runCommand('mkdir -p '+launcherDir)

    lists          = ListOfSpecies()
    procList       = readListOfProcesses(fileProcesses, outputDir+sessionName, '/')
    fieldList      = defineFields()

    listAlgoName = ['pd','anamorph']


    launcher = launcherDir + 'applyGS.sh'
    f        = open(modulePath() + 'utils/launchers/defaultLauncher.sh', 'r')
    lines    = f.readlines()
    f.close()

    f = open(launcher, 'w')
    for line in lines:
        if '$fileProcesses$' in line:
            f.write(line.replace('$fileProcesses$', launcherDir+'processesApplyGS.dat'))
        elif '$launcher$' in line:
            f.write(line.replace('$launcher$', moduleLauncher()))
        elif '$startString$' in line:
            f.write(line.replace('$startString$', 'Applying greyScale to fields'))
        elif '$logFile$' in line:
            f.write(line.replace('$logFile$', launcherDir+'logApplyGS'))
        elif '$nodesFile$' in line:
            f.write(line.replace('$nodesFile$', launcherDir+'nodesApplyGS.dat'))
        else:
            f.write(line)
    f.close()

    fileNameProcesses = launcherDir + 'processesApplyGS.dat'
    fileProcesses     = open(fileNameProcesses, 'w')
    fileProcesses.write('FUNCTION'      + '\t' +
                        'OUTPUT_DIR'    + '\t' +
                        'SESSION_NAME'  + '\t' +
                        'OTGS_DIR'      + '\t' +
                        'APPLYOTGS_DIR' + '\t' +
                        'STAT_DIR'      + '\t' +
                        'AOG'           + '\t' +
                        'FIELD_NAME'    + '\t' +
                        'LOL'           + '\t' +
                        'TS'            + '\t' +
                        'SPECIES'       + '\t' +
                        'ALGO_NAME'     + '\t' +
                        'PRINT_IO'      + '\n' )

    for AOG in ['air/','ground/']:
        for GOR in ['gaz','radios']:
            for species in lists.speciesList[GOR]:
                for field in fieldList[AOG]:
                    for lol in ['lin','log']:
                        for TS in ['Threshold', 'NoThreshold']:
                            for algoName in listAlgoName:
                                fileProcesses.write('applyGStoSpecies' + '\t' +
                                                    outputDir          + '\t' +
                                                    sessionName        + '\t' +
                                                    OTGSDir            + '\t' +
                                                    applyOTGSDir       + '\t' +
                                                    statDir            + '\t' +
                                                    AOG                + '\t' +
                                                    field.name         + '\t' +
                                                    lol                + '\t' +
                                                    TS                 + '\t' +
                                                    species            + '\t' +
                                                    algoName           + '\t' +
                                                    str(printIO)       + '\n' )

    print('Written '+launcher+' ...')
    print('Written '+fileNameProcesses+' ...')
    runCommand('cp '+modulePath()+'utils/launchers/defaultNodes.dat '+launcherDir+'nodesApplyGS.dat')    
    print('Do not forget to specify nodes and log files.')
