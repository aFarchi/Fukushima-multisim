import numpy as np
import os
import sys
from scipy.interpolate import interp1d

from statistical_analysis.utils import utils_read_list_of_processes as readList

######################################
# run command

def myrun(command):
    status = os.system(command)
    print command
    if status != 0:
        sys.exit(status)

######################################
# Defines directions and file names

outputDir     = '/cerea_raid/users/farchia/Fukushima-multisim/output/'
sessionName   = 'sim-test-2/'

GSDir         = outputDir+sessionName+'OT-greyscale/'
fileFields    = outputDir+sessionName+'list_fields_greyscale.dat'

defaultConfig = '/cerea_raid/users/farchia/Fukushima-multisim/postprocessing/optimal_transport/config-greyscale.txt'
defaultMerger = '/cerea_raid/users/farchia/Fukushima-multisim/postprocessing/optimal_transport/merge_results.py'

OTDir         = '/profils_cerea/farchia/OT/Optimal-Transport/OT1D/'
OTlauncher    = 'launchSimulation.py'
statDir       = outputDir+sessionName+'statistics/'
fileProcesses = outputDir+sessionName+'list_processes.dat'

fileLevels    = outputDir+sessionName+'config/levels.dat'

analyseResolution = 32
deltaT = 3600.
MINLOGSCALE = 1.e-20

prepareGroundLevel     = False
prepareAirColums       = False
prepareTotalDeposition = True
algoName = 'pd'

LinorLog = ['lin','log']

######################################

myrun('mkdir -p '+GSDir)

    
######################################
# Catch name of processes and names of fields
namesProcesses = readList.readListOfProcesses(fileProcesses)
namesProcesses_corrected = []
for proc in namesProcesses:
    proc = outputDir + sessionName + proc
    namesProcesses_corrected.append(proc)
namesProcesses = namesProcesses_corrected

f = open(fileFieldsGS,'r')
lines = f.readlines()
f.close()

nameFields = []
for line in lines:
    nameFields.append(line.replace('\n',''))

f = open(defaultConfig,'r')
lines = f.readlines()
f.close()

for nameField in nameFields:
    for lol in LinorLog:
        myrun('mkdir -p '+ GSDir + nameField + lol)
        launcher = GSDir + nameField + lol + '/launcher.sh'
        fileLauncher = open(launcher,'w')
        fileLauncher.write('#!/bin/bash\n')
        fileLauncher.write('cd ' + OTDir + '\n')
        
        for i1 in xrange(len(namesProcesses)):
            for i2 in xrange(i1):
                repOut = GSDir + nameField + lol + '/fields/' + str(i1) + '-' + str(i2) + '/'
                repFigs = GSDir + nameField + lol + '/figures/' + str(i1) + '-' + str(i2) + '/'
                myrun('mkdir -p '+repOut)
                myrun('mkdir -p '+repFigs)

                filef0 = namesProcesses[i1] + '_greyscale_' + lol + '.npy'
                filef1 = namesProcesses[i2] + '_greyscale_' + lol + '.npy'

                m = np.zeros(analyseResolution)
                np.save(m,repOut+'m0.npy')
                np.save(m,repOut+'m1.npy')

                f = open(repOut + 'config.txt', 'w')
                for line in lines:
                    if '$outputDir$' in line:
                        f.write(line.replace('$outputDir$',repOut))
                    elif '$analyseResolution$' in line:
                        f.write(line.replace('$analyseResolution$',str(analyseResolution-1)))
                    elif '$algoName$' in line:
                        f.write(line.replace('$algoName$',algoName))
                    elif '$fileF0$' in line:
                        f.write(line.replace('$fileF0$',filef0))
                    elif '$fileF1$' in line:
                        f.write(line.replace('$fileF1$',filef1))
                    elif '$fileM0$' in line:
                        f.write(line.replace('$fileM0$',repOut+'m0.npy'))
                    elif '$fileM1$' in line:
                        f.write(line.replace('$fileM1$',repOut+'m1.npy'))
                    else:
                        f.write(line)
                f.close()
                fileLauncher.write('python '+OTlauncher+' '+repOut+'config.txt '+repFigs+'\n')

        fileLauncher.write('cd ' + GSDir + nameField + lol)
        fileLauncher.write('python merge_results.py')
        fileLauncher.close()

        fileMerger = open(defaultMerger,'r')
        linesMerger = fileMerger.readlines()
        fileMerger.close()
        fileMerger = open(GSDir+nameField+lol+'/merge_results.py','w')

        for line in linesMerger:
            if '$nbrProc$' in line:
                fileMerger.write(line.replace('$nbrProc$',str(len(namesProcesses))))
            elif '$rep$' in line:
                fileMerger.write(line.replace('$rep$',GSDir + nameField + lol))
            else:
                fileMerger.write(line)
        fileMerger.close()
        
