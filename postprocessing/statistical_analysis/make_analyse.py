import numpy as np
import os
import sys

from utils_read_list_of_processes import *
from utils_global_analyse import *


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

myrun('mkdir -p '+statDir)

######################################
# Defines species

AirorDryorWet = ['','dry/','wet/']
InorBelow = {}
InorBelow['wet/'] = ['InCloud/', 'BelowCloud/', '']
InorBelow['dry/'] = ['']
InorBelow[''] = ['']

Nradios = {}
Nradios['']=(500,15,120,120)
Nradios['dry/']=(500,1,120,120)
Nradios['wet/']=(500,1,120,120)
Nradios['wet/InCloud/']=(500,1,120,120)
Nradios['wet/BelowCloud/']=(500,1,120,120)
RadioSpecies = {}
RadioSpecies['Cs137'] = ['Cs137_0','Cs137_1','Cs137_2','Cs137_3','Cs137_4']
Radios = ['Cs137']

Ngaz = {}
Ngaz['']=(83,15,120,120)#83=floor(3000/36)
Ngaz['dry/']=(500,1,120,120)
Ngaz['wet/']=(500,1,120,120)
Gaz = ['I2']

######################################
# List of species

Species = []
# add gaz species
for g in Gaz:
    for AoDoW in AirorDryorWet:
        speName = AoDoW + g + '.bin'
        N = Ngaz[AoDoW]
        Species.append((speName,N))

# add aerosol species
for aer in Radios:
    for rSpe in RadioSpecies[aer]:
        for AoDoW in AirorDryorWet:
            for IoB in InorBelow[AoDoW]:
                speName = AoDoW + IoB + rSpe + '.bin'
                N = Nradios[AoDoW + IoB]
                Species.append((speName,N))

# print list of species
for (name,n) in Species:
    nt,nz,ny,nx = n
    sizeOfFile = 4*nt*nz*ny*nx
    #print(name+':'+str(nt)+'x'+str(nz)+'x'+str(ny)+'x'+str(nx)+'\n'+str(sizeOfFile))    
    #print(name)
    
######################################
# Catch name of processes
namesProcesses = readListOfProcesses(fileProcesses)
for name in namesProcesses:
    print(name)

######################################
# add here some function to coarse / filter the data ?

######################################
# Analyse Cs137_0_coarsed
modelList = []
for proc in namesProcesses:
    modelList.append(proc+'/Cs137_0_coarsed.bin')

linGlobAnalyse = GlobalLinearAnalyse(modelList)
linGlobAnalyse.performAnalyse()
linGlobAnalyse.results.tofile(statDir+'Cs137_0_coarsed_lin_global_analyse.dat')

# Should add a filter here for zero data
logGlobAnalyse = GlobalLogAnalyse(modelList)
logGlobAnalyse.performAnalyse()
logGlobAnalyse.results.tofile(statDir+'Cs137_0_coarsed_log_global_analyse.dat')
