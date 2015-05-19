###################################
# makeLauncherStatisticalAnalyse.py
###################################

from ..utils.run.run               import runCommand
from ..utils.absolutePath          import moduleLauncher

def makeLauncherAnalyseAllFields(outputDir, sessionName, interpreter='python', printIO=False):
    launcherDir = outputDir + sessionName + 'launchers/statisticalAnalyse/'
    runCommand('mkdir -p '+launcherDir, printIO)

    launcher = launcherDir + 'analyseAllFields.sh'
    f        = open(launcher, 'w')
    f.write('#!/bin/bash\n')
    f.write('\n')
    f.write('outputDir=\''+outputDir+'\'\n')
    f.write('sessionName=\''+sessionName+'\'\n')
    f.write('interpreter=\''+interpreter+'\'\n')
    f.write('launcher=\''+moduleLauncher()+'\'\n')
    f.write('printIO=\''+str(printIO)+'\'\n')
    f.write('function=\'analyseAllFields\'\n')
    f.write('\n')
    f.write('echo \'Starting analyse ...\'\n')
    f.write('echo $interpreter $launcher\' FUNCTION=\'$function\' OUTPUT_DIR=\'$outputDir\' SESSION_NAME=\'$sessionName\' PRINT_IO=\'$printIO\n')
    f.write('$interpreter $launcher FUNCTION=$function OUTPUT_DIR=$outputDir SESSION_NAME=$sessionName PRINT_IO=$printIO\n')
    f.close()
           
    print('Written '+launcher+' ...')
