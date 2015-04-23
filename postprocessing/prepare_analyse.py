import numpy as np
import os
import sys
from scipy.interpolate import interp1d

from utils_read_list_of_processes import *

######################################
# run command

def myrun(command):
    status = os.system(command)
    print command
    if status != 0:
        sys.exit(status)

######################################
# Interpolation function

def interpolate(array, axis, newN):
    shape = array.shape
    oldN = shape[axis]
    oldX = ( np.arange(oldN) + 0.5 ) / oldN
    newX = ( np.arange(newN) + 0.5 ) / newN
    function = interp1d(oldX, array, axis=axis, bounds_error=False, fill_value=0.)
    return function(newX)

######################################
# Defines directions and file names

outputDir     = '/cerea_raid/users/farchia/Fukushima-multisim/output/'
sessionName   = 'sim-test/'
statDir       = outputDir+sessionName+'statistics/'
fileProcesses = outputDir+sessionName+'list_processes.dat'
fileFields    = statDir+'list_fields.dat'

analyseResolution = (1,1,32,32)
deltaT = 3600.

######################################
# Defines species

AirorDryorWet = ['','dry/','wet/']
DryorWet      = ['dry/','wet/']

InorBelow = {}
InorBelow['wet/'] = ['InCloud/', 'BelowCloud/', '']
InorBelow['dry/'] = ['']
InorBelow[''] = ['']
InorBelow_DoW = {}
InorBelow_DoW['wet/'] = ['InCloud/', 'BelowCloud/']
InorBelow_DoW['dry/'] = ['']

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
for proc in namesProcesses:
    proc = outputDir + sessionName + proc
    myrun('mkdir -p '+proc+'/to_analyse')
    #print(proc)

######################################    
# Prepare fields to analyse
fields = []

######################################
# Compute columns of air concentration
# at the end of the simulation 

(Nta,Nza,Nya,Nxa) = analyseResolution
(Nt,Nz,Ny,Nx) = Ngaz['']
for proc in namesProcesses:
    for g in Gaz:
        fileName = proc + '/' + g + '.bin'
        print ('Reading '+fileName+'...')
        data = np.fromfile(fileName, 'f')
        data = data.reshape((Nt,Nz,Ny,Nx))
        data = data[Nt-1,:,:,:]
        airColumn = data.mean(axis=0)

        nameField = 'airColumn_' + g
        if proc == namesProcesses[0]:
            fields.append(nameField)
        
        fileName = proc + '/to_analyse/' + nameField + '.npy'
        print ('Writing '+fileName+'...')

        if Ny > Nya:
            airColumn = interpolate(airColumn,0,Nya)
        if Nx > Nxa:
            airColumn = interpolate(airColumn,1,Nxa)
        
        np.save(fileName,airColumn)

(Nt,Nz,Ny,Nx) = Nradios['']
for proc in namesProcesses:
    for aer in Radios:
        airColumnAer = np.zeros(shape=(Ny,Nx))
        weight = 0.
        for rSpe in RadioSpecies[aer]:
            fileName = proc + '/' + rSpe + '.bin'
            print ('Reading '+fileName+'...')
            data = np.fromfile(fileName, 'f')
            data = data.reshape((Nt,Nz,Ny,Nx))
            data = data[Nt-1,:,:,:]
            airColumnAer += data.mean(axis=0)
            weight += 1.
        airColumnAer /= weight
        
        nameField = 'airColumn_' + aer
        if proc == namesProcesses[0]:
            fields.append(nameField)
                        
        fileName = proc + '/to_analyse/' + nameField + '.npy'
        print ('Writing '+fileName+'...')

        if Ny > Nya:
            airColumnAer = interpolate(airColumn,0,Nya)
        if Nx > Nxa:
            airColumnAer = interpolate(airColumn,1,Nxa)
                                
        np.save(fileName,airColumnAer)

######################################
# Cumul of the deposition

(Nta,Nza,Nya,Nxa) = analyseResolution

for proc in namesProcesses:
    for g in Gaz:
        dep = np.zeros(shape=(Nya,Nxa))
        for DoW in DryorWet:
            (Nt,Nz,Ny,Nx) = Ngaz[DoW]
            fileName = proc + '/' + DoW + g + '.bin'
            print ('Reading '+fileName+'...')
            data = np.fromfile(fileName, 'f')
            data = data.reshape((Nt,Nz,Ny,Nx))
            data = data.cumsum(axis=0)*deltaT
            data = data[Nt-1, 0,:,:]
            if Ny > Nya:
                data = interpolate(data,0,Nya)
            if Nx > Nxa:
                data = interpolate(data,1,Nxa)
            dep += data

        nameField = 'totalDeposition_' + g
        if proc == namesProcesses[0]:
            fields.append(nameField)
        fileName = proc + '/to_analyse/' + nameField + '.npy'
        print ('Writing '+fileName+'...')
        np.save(fileName,dep)
                             

for proc in namesProcesses:
    for aer in Radios:
        dep = np.zeros(shape=(Nya,Nxa))

        for rSpe in RadioSpecies[aer]:
            for DoW in DryorWet:
                for IoB in InorBelow_DoW[DoW]:
                    (Nt,Nz,Ny,Nx) = Nradios[DoW+IoB]
                    fileName = proc + '/' + DoW + IoB + rSpe + '.bin'
                    print ('Reading '+fileName+'...')
                    data = np.fromfile(fileName, 'f')
                    data = data.reshape((Nt,Nz,Ny,Nx))
                    data = data.cumsum(axis=0)*deltaT
                    data = data[Nt-1, 0,:,:]

                    if Ny > Nya:
                        data = interpolate(data,0,Nya)
                    if Nx > Nxa:
                        data = interpolate(data,1,Nxa)
                    dep += data
                    
        nameField = 'totalDeposition_' + aer
        if proc == namesProcesses[0]:
            fields.append(nameField)
        fileName = proc + '/to_analyse/' + nameField + '.npy'
        print ('Writing '+fileName+'...')
        np.save(fileName,dep)
                                                        
######################################
# Writes fields name

f = open(fileFields, 'w')
for field in fields:
    f.write(field+'\n')
f.close()
