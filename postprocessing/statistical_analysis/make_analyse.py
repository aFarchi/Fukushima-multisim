import numpy as np
import os
import sys
import pickle

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
fileFieldsGS  = outputDir+sessionName+'list_fields_greyscale.dat'

analyseResolution = (1,1,32,32)

LinorLog = ['lin','log']

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
# Analyse linear fields 

for (field,dim) in zip(namesFields,dimFields)
    # dim is a useful test if we want to make space or time analyses
    
    modelList = []
    for proc in namesProcesses:
        modelList.append(proc+'/to_analyse/'+field+'_lin.npy')
    fileScaling = statDir+field+'_globalScaling_lin.bin'

    linGlobAnalyse = GlobalLinearAnalyse(modelList,fileScaling)
    res = linGlobAnalyse.performAnalyse()
    f = open(statDir+field+'_linGlobalAnalyse_lin.bin','wb')
    p = pickle.Pickler(f)
    p.dump(res)
    f.close()

    # add a filter here for zero data ?
    logGlobAnalyse = GlobalLogAnalyse(modelList)
    res = logGlobAnalyse.performAnalyse()
    f = open(statDir+field+'_logGlobalAnalyse_lin.bin','wb')
    p = pickle.Pickler(f)
    p.dump(res)
    f.close()

######################################
# Analyse log fields 

for (field,dim) in zip(namesFields,dimFields)
    
    modelList = []
    for proc in namesProcesses:
        modelList.append(proc+'/to_analyse/'+field+'_log.npy')
    fileScaling = statDir+field+'_globalScaling_log.bin'

    linGlobAnalyse = GlobalLinearAnalyse(modelList,fileScaling)
    res = linGlobAnalyse.performAnalyse()
    f = open(statDir+field+'_linGlobalAnalyse_log.npy','wb')
    p = pickle.Pickler(f)
    p.dump(res)
    f.close()

######################################
# Catch name of GS fields to analyse

f = open(fileFieldsGS,'r')
lines = f.readlines()
f.close()

nameFields = []
for line in lines:
    nameFields.append(line.replace('\n',''))

fileScaling = statDir + 'GS_scling.temp.bin'
infos = np.ones(5)
infos[4] = 0.
infos.tofile(fileScaling)

for lol in LinorLog:
    for field in namesFields:
        modelList = []
        for proc in namesProcesses:
            modelList.append(proc+'/to_analyse/'+field+'_greyscale_'+lol+'.npy')

        linGlobAnalyse = GlobalLinearAnalyse(modelList,fileScaling)
        res = linGlobAnalyse.performAnalyse()
        f = open(statDir+field+'_linGlobalAnalyse_greyscale_'+lol'.npy','wb')
        p = pickle.Pickler(f)
        p.dump(res)
        f.close()

myrun('rm '+fileScaling)
