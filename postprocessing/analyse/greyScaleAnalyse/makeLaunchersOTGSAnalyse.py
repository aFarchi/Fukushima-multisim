#############################
# makeLaunchersOTGSAnalyse.py
#############################

from ..utils.absolutePath                  import modulePath
from ..utils.absolutePath                  import OTPath
from ..utils.absolutePath                  import moduleLauncher

from ..utils.run.run                       import runCommand
from ..utils.species.listOfSpecies         import ListOfSpecies
from ..utils.fields.defineFields           import defineFields
from ..utils.io.readLists                  import readListOfProcesses

def makeLaunchersOTGSAnalyse(outputDir, sessionName, nLevelsAnalyse, printIO=False):

    fileProcesses      = outputDir + sessionName + 'list_processes.dat'
    OTGSDir            = outputDir + sessionName + 'OTGS/'
    configOTtoComplete = modulePath() + 'utils/configOT/OTGS.cfg'
    launcherDir        = outputDir + sessionName + 'launchers/OTGSAnalyse/'
    figDir             = outputDir + sessionName + 'figures/OTGSAnalyse/'

    for subdir in ['performOTGS/', 'mergeOTGS/', 'plotOTGS/', 'animOTGS/']:
        runCommand('mkdir -p '+launcherDir+subdir, printIO)
    runCommand('mkdir -p '+OTGSDir, printIO)

    procList  = readListOfProcesses(fileProcesses, outputDir+sessionName, '/')
    fieldList = defineFields()
    lists     = ListOfSpecies()

    listAlgoName     = ['pd','anamorph']

    # Launcher OTGS
    
    launcherPerform = launcherDir + 'performOTGS/performOTGSAnalyse.sh'
    f               = open(modulePath() + 'utils/launchers/defaultLauncher.sh', 'r')
    lines           = f.readlines()
    f.close()

    f = open(launcherPerform, 'w')
    for line in lines:
        if '$fileProcesses$' in line:
            f.write(line.replace('$fileProcesses$', launcherDir+'performOTGS/processesPerformOTGSAnalyse.dat'))
        elif '$launcher$' in line:
            f.write(line.replace('$launcher$', OTPath()+'launchSimulation1D.py'))
        elif '$startString$' in line:
            f.write(line.replace('$startString$', 'Starting OT greyScale'))
        elif '$logFile$' in line:
            f.write(line.replace('$logFile$', launcherDir+'performOTGS/logPerformOTGSAnalyse'))
        elif '$nodesFile$' in line:
            f.write(line.replace('$nodesFile$', launcherDir+'performOTGS/nodesPerformOTGSAnalyse.dat'))
        else:
            f.write(line)
    f.close()

    # Launcher Merge Result

    launcherMerge = launcherDir + 'mergeOTGS/mergeOTGSResults.sh'
    f             = open(modulePath() + 'utils/launchers/defaultLauncher.sh', 'r')
    lines         = f.readlines()
    f.close()

    f = open(launcherMerge, 'w')
    for line in lines:
        if '$fileProcesses$' in line:
            f.write(line.replace('$fileProcesses$', launcherDir+'mergeOTGS/processesMergeOTGSResults.dat'))
        elif '$launcher$' in line:
            f.write(line.replace('$launcher$', moduleLauncher()))
        elif '$startString$' in line:
            f.write(line.replace('$startString$', 'Merging OT greyScale results'))
        elif '$logFile$' in line:
            f.write(line.replace('$logFile$', launcherDir+'mergeOTGS/logMergeOTGSResults'))
        elif '$nodesFile$' in line:
            f.write(line.replace('$nodesFile$', launcherDir+'mergeOTGS/nodesMergeOTGSResults.dat'))
        else:
            f.write(line)
    f.close()

    # Launcher Plot Results

    launcherPlot = launcherDir + 'plotOTGS/plotOTGSResults.sh'
    f            = open(modulePath() + 'utils/launchers/defaultLauncher.sh', 'r')
    lines        = f.readlines()
    f.close()

    f = open(launcherPlot, 'w')
    for line in lines:
        if '$fileProcesses$' in line:
            f.write(line.replace('$fileProcesses$', launcherDir+'plotOTGS/processesPlotOTGSResults.dat'))
        elif '$launcher$' in line:
            f.write(line.replace('$launcher$', OTPath()+'plotDirectory1D.py'))
        elif '$startString$' in line:
            f.write(line.replace('$startString$', 'Plotting OT greyScale results'))
        elif '$logFile$' in line:
            f.write(line.replace('$logFile$', launcherDir+'plotOTGS/logPlotOTGSResults'))
        elif '$nodesFile$' in line:
            f.write(line.replace('$nodesFile$', launcherDir+'plotOTGS/nodesPlotOTGSResults.dat'))
        else:
            f.write(line)
    f.close()

    # Launcher Anim Results

    launcherAnim = launcherDir + 'animOTGS/animOTGSResults.sh'
    f            = open(modulePath() + 'utils/launchers/defaultLauncher.sh', 'r')
    lines        = f.readlines()
    f.close()

    f = open(launcherAnim, 'w')
    for line in lines:
        if '$fileProcesses$' in line:
            f.write(line.replace('$fileProcesses$', launcherDir+'animOTGS/processesAnimOTGSResults.dat'))
        elif '$launcher$' in line:
            f.write(line.replace('$launcher$', OTPath()+'animDirectory1D.py'))
        elif '$startString$' in line:
            f.write(line.replace('$startString$', 'Animating OT greyScale results'))
        elif '$logFile$' in line:
            f.write(line.replace('$logFile$', launcherDir+'animOTGS/logAnimOTGSResults'))
        elif '$nodesFile$' in line:
            f.write(line.replace('$nodesFile$', launcherDir+'animOTGS/nodesAnimOTGSResults.dat'))
        else:
            f.write(line)
    f.close()

    # Processes

    processesPerform     = launcherDir + 'performOTGS/processesPerformOTGSAnalyse.dat'
    fileProcessesPerform = open(processesPerform, 'w')
    fileProcessesPerform.write('CONFIG_FILE\tPRINT_IO\n')

    processesMerge       = launcherDir + 'mergeOTGS/processesMergeOTGSResults.dat'
    fileProcessesMerge   = open(processesMerge, 'w')
    fileProcessesMerge.write('FUNCTION\tNBR_PROC\tDIR\tALGO\tPRINT_IO\n')

    processesPlot        = launcherDir + 'plotOTGS/processesPlotOTGSResults.dat'
    fileProcessesPlot    = open(processesPlot, 'w')
    fileProcessesPlot.write('CONFIG_FILE\tFIG_DIR\tPRINT_IO\n')

    processesAnim        = launcherDir + 'animOTGS/processesAnimOTGSResults.dat'
    fileProcessesAnim    = open(processesAnim, 'w')
    fileProcessesAnim.write('CONFIG_FILE\tFIG_DIR\tPRINT_IO\n')


    sLauncherPlot     = launcherDir + 'plotOTGS/plotOTGSResults-1proc.sh'
    sLauncherAnim     = launcherDir + 'animOTGS/animOTGSResults-1proc.sh'
    fileSLauncherPlot = open(sLauncherPlot, 'w')
    fileSLauncherAnim = open(sLauncherAnim, 'w')
    fileSLauncherPlot.write('#!/bin/bash\n')
    fileSLauncherAnim.write('#!/bin/bash\n')


    for AOG in ['air/','ground/']:
        for GOR in ['gaz','radios']:
            for species in lists.speciesList[GOR]:
                for field in fieldList[AOG]:
                    for lol in ['lin','log']:
                        for TS in ['Threshold', 'NoThreshold']:
                            directory = OTGSDir + AOG + field.name + '/' + lol + '/' + TS + '/' + species + '/'

                            for p1 in xrange(len(procList)):
                                for p2 in xrange(p1):

                                    oDir   = directory + str(p1) + '-' + str(p2) + '/'
                                    fDir   = figDir + AOG + field.name + '/' + lol + '/' + TS + '/' + species + '/' + str(p1) + '-' + str(p2) + '/'
                                    runCommand('mkdir -p '+oDir, printIO)

                                    filef0 = procList[p1] + 'toAnalyse/' + AOG + field.name + '/' + lol + '/' + species + '_greyScale' + TS + '.npy'
                                    filef1 = procList[p2] + 'toAnalyse/' + AOG + field.name + '/' + lol + '/' + species + '_greyScale' + TS + '.npy'
                                 
                                    for algoName in listAlgoName:
                                        f     = open(configOTtoComplete,'r')
                                        lines = f.readlines()
                                        f.close()

                                        f = open(oDir + 'OTGS_'+algoName+'.cfg','w')
                                        for line in lines:
                                            if '$outputDir$' in line:
                                                f.write(line.replace('$outputDir$', oDir+'output_'+algoName+'/'))
                                            elif '$nLevelsAnalyse$' in line:
                                                f.write(line.replace('$nLevelsAnalyse$',str(nLevelsAnalyse-1)))
                                            elif '$algoName$' in line:
                                                f.write(line.replace('$algoName$',algoName))
                                            elif '$fileF0$' in line:
                                                f.write(line.replace('$fileF0$',filef0))
                                            elif '$fileF1$' in line:
                                                f.write(line.replace('$fileF1$',filef1))
                                            else:
                                                f.write(line)
                                        f.close()
                                        fileProcessesPerform.write(oDir+'OTGS_'+algoName+'.cfg\t' +
                                                                   str(printIO)+'\n')
                                        fileProcessesPlot.write(oDir+'OTGS_'+algoName+'.cfg\t' + 
                                                                fDir+'output_'+algoName+'/\t' + 
                                                                str(printIO)+'\n')
                                        fileProcessesAnim.write(oDir+'OTGS_'+algoName+'.cfg\t' + 
                                                                fDir+'output_'+algoName+'/\t' +
                                                                str(printIO)+'\n')

                                        fileSLauncherPlot.write(OTPath()+'plotDirectory1D.py' +
                                                                ' CONFIG_FILE=' + oDir + 'OTGS_' + algoName + '.cfg' +
                                                                ' FIG_DIR='     + fDir + 'output_' + algoName + '/' + 
                                                                ' PRINT_IO='    + str(printIO) + '\n')
                                        fileSLauncherAnim.write(OTPath()+'animDirectory1D.py' +
                                                                ' CONFIG_FILE=' + oDir + 'OTGS_' + algoName + '.cfg' +
                                                                ' FIG_DIR='     + fDir + 'output_' + algoName + '/' + 
                                                                ' PRINT_IO='    + str(printIO) + '\n')

                            for algoName in listAlgoName:
                                fileProcessesMerge.write('mergeOTGSResults\t'+str(len(procList))+'\t'+directory+'\t'+algoName+'\t'+str(printIO)+'\n')

    fileProcessesPerform.close()
    fileProcessesMerge.close()
    fileProcessesPlot.close()
    fileProcessesAnim.close()
    fileSLauncherPlot.close()
    fileSLauncherAnim.close()
    
    print('Written '+launcherPerform+' ...')
    print('Written '+launcherMerge+' ...')
    print('Written '+launcherPlot+' ...')
    print('Written '+launcherAnim+' ...')
    print('Written '+processesPerform+' ...')
    print('Written '+processesMerge+' ...')
    print('Written '+processesPlot+' ...')
    print('Written '+processesAnim+' ...')

    runCommand('cp '+modulePath()+'utils/launchers/defaultNodes.dat '+launcherDir+'performOTGS/nodesPerformOTGSAnalyse.dat', printIO)
    runCommand('cp '+modulePath()+'utils/launchers/defaultNodes.dat '+launcherDir+'mergeOTGS/nodesMergeOTGSResults.dat', printIO)
    runCommand('cp '+modulePath()+'utils/launchers/defaultNodes.dat '+launcherDir+'plotOTGS/nodesPlotOTGSResults.dat', printIO)
    runCommand('cp '+modulePath()+'utils/launchers/defaultNodes.dat '+launcherDir+'animOTGS/nodesAnimOTGSResults.dat', printIO)

    print('Do not forget to specify nodes and log files.')
