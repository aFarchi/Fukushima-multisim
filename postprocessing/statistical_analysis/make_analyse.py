import numpy as np

from utils_read_list_of_processes import *

######################################
# Defines directions and file names

outputDir = './'
statDir = output_dir+'statistics/'

fileProcesses = outputDir + 'list_processes.dat'

######################################
# Defines species

AirorDryorwet = ['./','dry/','wet/']
InorBelow = {}
InorBelow['wet/'] = ['InCloud/', 'BelowCloud/', '']
InorBelow['dry/'] = ['']
InorBelow['./'] = ['']

Nradios = {}
Nradios['./']=(500,15,120,120)
Nradios['dry/']=(500,1,120,120)
Nradios['wet/']=(500,1,120,120)
Nradios['wet/InCloud/']=(500,1,120,120)
Nradios['wet/BelowCloud/']=(500,1,120,120)
RadioSpecies = {}
RadioSpecies['Cs137'] = ['Cs137_0','Cs137_1','Cs137_2','Cs137_3','Cs137_4']
Radios = ['Cs137']

Ngaz = {}
Ngaz['./']=(83,15,120,120)
Ngaz['dry/']=(500,1,120,120)
Ngaz['wet/']=(500,1,120,120)
Gaz = ['I2']

######################################
# List of species

Species = []
# add gaz species
for g in Gaz:
    for AoDoW in AirorDryorwet:
        


######################################
# Catch name of processes

namesProcesses = readListOfProcesses(fileName)
