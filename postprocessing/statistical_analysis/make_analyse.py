import numpy as np
import os
import sys

from utils import utils_read_list_of_processes as readList
from utils import utils_global_analyse as globalAnalyse

######################################
# run command

def myrun(command):
    status = os.system(command)
    print command
    if status != 0:
        sys.exit(status)
                                        
######################################
# Defines directions and file names

outputDir = '/cerea_raid/users/farchia/Fukushima-multisim/output/'
sessionName = 'sim-test/'
statDir = outputDir+sessionName+'statistics/'
fileProcesses = outputDir+sessionName+'list_processes.dat'

fileFields    = statDir+'list_fields.dat'
analyseResolution = (1,1,32,32)

######################################
# Catch name of processes
namesProcesses = readList.readListOfProcesses(fileProcesses)
for name in namesProcesses:
    print(name)

######################################
# Catch name of fields to analyse and
#    corresponding dimensions

namesFields,dimFields = readList.readListOfFields(fileFields)
for name in namesFields:
    print(name)

######################################
# Analyse fields

for i in xrange(len(namesFields)):
    field = namesFields[i]
    dim   = dimFields[i] # useful to test if we want to make space or time analyses
    
    modelList = []
    for proc in namesProcesses:
        modelList.append(proc+'/to_analyse/'+field+'.npy')
    fileScaling = statDir+field+'_globalScaling.bin'

    linGlobAnalyse = GlobalLinearAnalyse(modelList,fileScaling)
    linGlobAnalyse.performAnalyse()
    linGlobAnalyse.results.tofile(statDir+field+'_linGlobalAnalyse.npy')

    # add a filter here for zero data ?
    logGlobAnalyse = GlobalLogAnalyse(modelList)
    logGlobAnalyse.performAnalyse()
    logGlobAnalyse.results.tofile(statDir+field+'_logGlobalAnalyse.npy')

