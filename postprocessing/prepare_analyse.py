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
sessionName   = 'sim-test-2/'
statDir       = outputDir+sessionName+'statistics/'
fileProcesses = outputDir+sessionName+'list_processes.dat'
fileFields    = statDir+'list_fields.dat'
fileLevels    = outputDir+sessionName+'levels.dat'

computeGlobalScaling = True
analyseResolution = (1,1,32,32)
deltaT = 3600.

myrun('mkdir -p '+statDir)
myrun('mkdir -p '+statDir+'scaling/')

prepareGroundLevel     = True
prepareAirColums       = True
prepareTotalDeposition = True

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
namesProcesses = readList.readListOfProcesses(fileProcesses)
for proc in namesProcesses:
    proc = outputDir + sessionName + proc
    myrun('mkdir -p '+proc+'/to_analyse')
    #print(proc)

######################################    
# Prepare fields to analyse
fields = []
dimFields = []

if prepareGroundLevel:    
    ######################################
    # Compute ground level air concentration
    # at a given time
    nameField = 'airGroundLevel'
    dimField  = (2,3)
    (Nta,Nza,Nya,Nxa) = analyseResolution

    def TSelect(Nt):
        return Nt - 1 

    # for gaz
    (Nt,Nz,Ny,Nx) = Ngaz['']
    tSelect = TSelect(Nt)

    if computeGlobalScaling:
        nbrRelevantInfo = 4
        relevantInfo = {}
        for g in Gaz:
            relevantInfo[g] = {}
            for proc in namesProcesses:
                relevantInfo[g][proc] = np.zeros(nbrRelevantInfo)

    for proc in namesProcesses:
        for g in Gaz:
            fileName = proc + '/' + g + '.bin'
            print ('Reading '+fileName+'...')
            data = np.fromfile(fileName, 'f')
            data = data.reshape((Nt,Nz,Ny,Nx))
            data = data[tSelect,:,:,:]
            airGL = data[0,:,:]

            if proc == namesProcesses[0]:
                fields.append(nameField + '_' + g)
                dimFields.append(dimField)
        
            fileName = proc + '/to_analyse/' + nameField + '_' + g + '.npy'
            print ('Writing '+fileName+'...')

            if Ny > Nya:
                airGL = interpolate(airGL,0,Nya)
            if Nx > Nxa:
                airGL = interpolate(airGL,1,Nxa)

            if computeGlobalScaling:
                relevantInfo[g][proc][0] = airGL.mean()**2
                relevantInfo[g][proc][1] = airGL.var()
                relevantInfo[g][proc][2] = airGL.max()
                relevantInfo[g][proc][3] = airGL.min()
        
            np.save(fileName,airGL)

    if computeGlobalScaling:
        for g in Gaz:
            info = np.zeros(5)
            info[1] = 1.
            info[3] = relevantInfo[g][namesProcesses[0]][2]
            info[4] = relevantInfo[g][namesProcesses[0]][3]
            for proc in namesProcesses:
                info[0] += relevantInfo[g][proc][0]
                info[1] *= relevantInfo[g][proc][0]
                info[2] += relevantInfo[g][proc][1]
                info[3]  = np.max( [ info[3], relevantInfo[g][proc][2] ] )
                info[4]  = np.min( [ info[4], relevantInfo[g][proc][3] ] )
            info[0] /= len(namesProcesses)
            info[2] /= len(namesProcesses)
            info[1]  = np.power( info[1] , 1./len(namesProcesses) )

            fileScaling = statDir + 'scaling/' + nameField + '_' + g + '_globalScaling.bin'
            print ('Writing '+fileScaling+'...')
            info.tofile(fileScaling)

    # for aerosols
    if computeGlobalScaling:
        nbrRelevantInfo = 4
        relevantInfo = {}
        for aer in Radios:
            relevantInfo[aer] = {}
            for proc in namesProcesses:
                relevantInfo[aer][proc] = np.zeros(nbrRelevantInfo)                                        

    (Nt,Nz,Ny,Nx) = Nradios['']
    tSelect = TSelect(Nt)
    for proc in namesProcesses:
        for aer in Radios:
            airGLAer = np.zeros(shape=(Ny,Nx))
            weight = 0.
            for rSpe in RadioSpecies[aer]:
                fileName = proc + '/' + rSpe + '.bin'
                print ('Reading '+fileName+'...')
                data = np.fromfile(fileName, 'f')
                data = data.reshape((Nt,Nz,Ny,Nx))
                data = data[tSelect,:,:,:]
                airGLAer += data[0,:,:]
                weight += 1.
            airGLAer /= weight
        
            if proc == namesProcesses[0]:
                fields.append(nameField + '_' + aer)
                dimFields.append(dimField)
                        
            fileName = proc + '/to_analyse/' + nameField + '_' + aer +'.npy'
            print ('Writing '+fileName+'...')

            if Ny > Nya:
                airGLAer = interpolate(airGLAer,0,Nya)
            if Nx > Nxa:
                airGLAer = interpolate(airGLAer,1,Nxa)

            if computeGlobalScaling:
                relevantInfo[aer][proc][0] = airGLAer.mean()**2
                relevantInfo[aer][proc][1] = airGLAer.var()
                relevantInfo[aer][proc][2] = airGLAer.max()
                relevantInfo[aer][proc][3] = airGLAer.min()
                                                                
            np.save(fileName,airGLAer)

    if computeGlobalScaling:
        for aer in Radios:
            info = np.zeros(5)
            info[1] = 1.
            info[3] = relevantInfo[aer][namesProcesses[0]][2]
            info[4] = relevantInfo[aer][namesProcesses[0]][3]
            for proc in namesProcesses:
                info[0] += relevantInfo[aer][proc][0]
                info[1] *= relevantInfo[aer][proc][0]
                info[2] += relevantInfo[aer][proc][1]
                info[3]  = np.max( [ info[3], relevantInfo[aer][proc][2] ] )
                info[4]  = np.min( [ info[4], relevantInfo[aer][proc][3] ] )
            info[0] /= len(namesProcesses)
            info[2] /= len(namesProcesses)
            info[1]  = np.power( info[1] , 1./len(namesProcesses) )

            fileScaling = statDir + 'scaling/' + nameField + '_' + aer + '_globalScaling.bin'
            print ('Writing '+fileScaling+'...')
            info.tofile(fileScaling)

if prepareAirColums:
    ######################################
    # Compute columns of air concentration
    # at a given time
    nameField = 'airColumn'
    dimField  = (2,3)
    (Nta,Nza,Nya,Nxa) = analyseResolution
    weights = np.diff(readList.catchLevelsFromFile(fileLevels))

    def TSelect(Nt):
        return Nt - 1
    
    # for gaz
    if computeGlobalScaling:
        nbrRelevantInfo = 4
        relevantInfo = {}
        for g in Gaz:
            relevantInfo[g] = {}
            for proc in namesProcesses:
                relevantInfo[g][proc] = np.zeros(nbrRelevantInfo)

    (Nt,Nz,Ny,Nx) = Ngaz['']
    tSelect = TSelect(Nt)
    for proc in namesProcesses:
        for g in Gaz:
            fileName = proc + '/' + g + '.bin'
            print ('Reading '+fileName+'...')
            data = np.fromfile(fileName, 'f')
            data = data.reshape((Nt,Nz,Ny,Nx))
            data = data[Nt-1,:,:,:]
            airColumn = np.average(data,axis=0,weights=weights)

            if proc == namesProcesses[0]:
                fields.append(nameField + '_' + g)
                dimFields.append(dimField)
        
            fileName = proc + '/to_analyse/' + nameField + '_' + g + '.npy'
            print ('Writing '+fileName+'...')

            if Ny > Nya:
                airColumn = interpolate(airColumn,0,Nya)
            if Nx > Nxa:
                airColumn = interpolate(airColumn,1,Nxa)

            if computeGlobalScaling:
                relevantInfo[g][proc][0] = airColumn.mean()**2
                relevantInfo[g][proc][1] = airColumn.var()
                relevantInfo[g][proc][2] = airColumn.max()
                relevantInfo[g][proc][3] = airColumn.min()
        
            np.save(fileName,airColumn)

    if computeGlobalScaling:
        for g in Gaz:
            info = np.zeros(5)
            info[1] = 1.
            info[3] = relevantInfo[g][namesProcesses[0]][2]
            info[4] = relevantInfo[g][namesProcesses[0]][3]
            for proc in namesProcesses:
                info[0] += relevantInfo[g][proc][0]
                info[1] *= relevantInfo[g][proc][0]
                info[2] += relevantInfo[g][proc][1]
                info[3]  = np.max( [ info[3], relevantInfo[g][proc][2] ] )
                info[4]  = np.min( [ info[4], relevantInfo[g][proc][3] ] )
            info[0] /= len(namesProcesses)
            info[2] /= len(namesProcesses)
            info[1]  = np.power( info[1] , 1./len(namesProcesses) )

            fileScaling = statDir + 'scaling/' + nameField + '_' + g + '_globalScaling.bin'
            print ('Writing '+fileScaling+'...')
            info.tofile(fileScaling)

    # for aerosols
    if computeGlobalScaling:
        nbrRelevantInfo = 4
        relevantInfo = {}
        for aer in Radios:
            relevantInfo[aer] = {}
            for proc in namesProcesses:
                relevantInfo[aer][proc] = np.zeros(nbrRelevantInfo)                                        

    (Nt,Nz,Ny,Nx) = Nradios['']
    tSelect = TSelect(Nt)
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
                airColumnAer += np.average(data,axis=0,weights=weights)
                weight += 1.
            airColumnAer /= weight
        
            if proc == namesProcesses[0]:
                fields.append(nameField + '_' + aer)
                dimFields.append(dimField)
                
            fileName = proc + '/to_analyse/' + nameField + '_' + aer +'.npy'
            print ('Writing '+fileName+'...')

            if Ny > Nya:
                airColumnAer = interpolate(airColumnAer,0,Nya)
            if Nx > Nxa:
                airColumnAer = interpolate(airColumnAer,1,Nxa)

            if computeGlobalScaling:
                relevantInfo[aer][proc][0] = airColumnAer.mean()**2
                relevantInfo[aer][proc][1] = airColumnAer.var()
                relevantInfo[aer][proc][2] = airColumnAer.max()
                relevantInfo[aer][proc][3] = airColumnAer.min()
                                                                
            np.save(fileName,airColumnAer)

    if computeGlobalScaling:
        for aer in Radios:
            info = np.zeros(5)
            info[1] = 1.
            info[3] = relevantInfo[aer][namesProcesses[0]][2]
            info[4] = relevantInfo[aer][namesProcesses[0]][3]
            for proc in namesProcesses:
                info[0] += relevantInfo[aer][proc][0]
                info[1] *= relevantInfo[aer][proc][0]
                info[2] += relevantInfo[aer][proc][1]
                info[3]  = np.max( [ info[3], relevantInfo[aer][proc][2] ] )
                info[4]  = np.min( [ info[4], relevantInfo[aer][proc][3] ] )
            info[0] /= len(namesProcesses)
            info[2] /= len(namesProcesses)
            info[1]  = np.power( info[1] , 1./len(namesProcesses) )

            fileScaling = statDir + 'scaling/' + nameField + '_' + aer + '_globalScaling.bin'
            print ('Writing '+fileScaling+'...')
            info.tofile(fileScaling)

if prepareTotalDeposition:
    ######################################
    # Cumul of the deposition
    nameField = 'totalDeposition'
    dimField  = (2,3)
    (Nta,Nza,Nya,Nxa) = analyseResolution

    # for gaz
    if computeGlobalScaling:
        nbrRelevantInfo = 4
        relevantInfo = {}
        for g in Gaz:
            relevantInfo[g] = {}
            for proc in namesProcesses:
                relevantInfo[g][proc] = np.zeros(nbrRelevantInfo)

    for proc in namesProcesses:
        for g in Gaz:
            dep = np.zeros(shape=(Ny,Nx))
            for DoW in DryorWet:
                (Nt,Nz,Ny,Nx) = Ngaz[DoW]
                fileName = proc + '/' + DoW + g + '.bin'
                print ('Reading '+fileName+'...')
                data = np.fromfile(fileName, 'f')
                data = data.reshape((Nt,Nz,Ny,Nx))
                data = data.cumsum(axis=0)*deltaT
                data = data[Nt-1, 0,:,:]
                dep += data

            if proc == namesProcesses[0]:
                fields.append(nameField + '_' + g)
                dimFields.append(dimField)
            
            fileName = proc + '/to_analyse/' + nameField + '_' + g + '.npy'
            print ('Writing '+fileName+'...')

            if Ny > Nya:
                dep = interpolate(dep,0,Nya)
            if Nx > Nxa:
                dep = interpolate(dep,1,Nxa)

            if computeGlobalScaling:
                relevantInfo[g][proc][0] = dep.mean()**2
                relevantInfo[g][proc][1] = dep.var()
                relevantInfo[g][proc][2] = dep.max()
                relevantInfo[g][proc][3] = dep.min()                                                

            np.save(fileName,dep)
                             
    if computeGlobalScaling:
        for g in Gaz:
            info = np.zeros(5)
            info[1] = 1.
            info[3] = relevantInfo[g][namesProcesses[0]][2]
            info[4] = relevantInfo[g][namesProcesses[0]][3]
            for proc in namesProcesses:
                info[0] += relevantInfo[g][proc][0]
                info[1] *= relevantInfo[g][proc][0]
                info[2] += relevantInfo[g][proc][1]
                info[3]  = np.max( [ info[3], relevantInfo[g][proc][2] ] )
                info[4]  = np.min( [ info[4], relevantInfo[g][proc][3] ] )
            info[0] /= len(namesProcesses)
            info[2] /= len(namesProcesses)
            info[1]  = np.power( info[1] , 1./len(namesProcesses) )
        
            fileScaling = statDir + 'scaling/' + nameField + '_' + g + '_globalScaling.bin'
            print ('Writing '+fileScaling+'...')
            info.tofile(fileScaling)

    # for aerosols
    if computeGlobalScaling:
        nbrRelevantInfo = 4
        relevantInfo = {}
        for aer in Radios:
            relevantInfo[aer] = {}
            for proc in namesProcesses:
                relevantInfo[aer][proc] = np.zeros(nbrRelevantInfo)                            

    for proc in namesProcesses:
        for aer in Radios:
            dep = np.zeros(shape=(Ny,Nx))

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
                        dep += data
                    
            if proc == namesProcesses[0]:
                fields.append(nameField+'_'+aer)
                dimFields.append(dimField)
            
            fileName = proc + '/to_analyse/' + nameField + '_' + aer + '.npy'
            print ('Writing '+fileName+'...')
            
            if Ny > Nya:
                dep = interpolate(dep,0,Nya)
            if Nx > Nxa:
                dep = interpolate(dep,1,Nxa)

            if computeGlobalScaling:
                relevantInfo[aer][proc][0] = dep.mean()**2
                relevantInfo[aer][proc][1] = dep.var()
                relevantInfo[aer][proc][2] = dep.max()
                relevantInfo[aer][proc][3] = dep.min()                                                
        
            np.save(fileName,dep)

    if computeGlobalScaling:
        for aer in Radios:
            info = np.zeros(5)
            info[1] = 1.
            info[3] = relevantInfo[aer][namesProcesses[0]][2]
            info[4] = relevantInfo[aer][namesProcesses[0]][3]
            for proc in namesProcesses:
                info[0] += relevantInfo[aer][proc][0]
                info[1] *= relevantInfo[aer][proc][0]
                info[2] += relevantInfo[aer][proc][1]
                info[3]  = np.max( [ info[3], relevantInfo[aer][proc][2] ] )
                info[4]  = np.min( [ info[4], relevantInfo[aer][proc][3] ] )
            info[0] /= len(namesProcesses)
            info[2] /= len(namesProcesses)
            info[1]  = np.power( info[1] , 1./len(namesProcesses) )
            
            fileScaling = statDir + 'scaling/' + nameField + '_' + aer + '_globalScaling.bin'
            print ('Writing '+fileScaling+'...')
            info.tofile(fileScaling)
        
######################################
# Writes fields name and dimensions

f = open(fileFields, 'w')
print ('Writing '+fileFields+'...')

for (field,dim) in zip(fields,dims):
    f.write(field+':')
    for dim in dims:
        f.write(str(dim)+',')
    f.write('\n')

f.close()
