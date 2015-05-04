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
# Greyscale function
def greayscale(matrix, mini, maxi, levels=None, nLevels=32, scale='lin', EPSILON=1.e-50):
    if levels is None:
        if scale == 'lin':
            levels = np.linspace(mini, maxi, nLevels)
        elif scale == 'log':
            mini = np.max([mini,EPSILON])
            levels = np.logspace(np.log10(mini), np.log10(maxi), nLevels)
    else:
        nLevels = len(levels)

    CDF = np.zeros(nLevels+1)

    for i in xrange(nLevels):
        CDF[i+1] = ( matrix < levels[i] ).mean()

    CDF[nLevels] = 1.
    PDF = CDF[1:nLevels+1] - CDF[0:nLevels]
    return PDF

######################################
# Defines directions and file names

outputDir     = '/cerea_raid/users/farchia/Fukushima-multisim/output/'
sessionName   = 'sim-test-2/'
statDir       = outputDir+sessionName+'statistics/'
fileProcesses = outputDir+sessionName+'list_processes.dat'
fileFields    = outputDir+sessionName+'list_fields_greyscale.dat'
fileLevels    = outputDir+sessionName+'config/levels.dat'

analyseResolution = 32
deltaT = 3600.
MINLOGSCALE = 1.e-20

prepareGroundLevel     = False
prepareAirColums       = False
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
NradiosDep=(500,1,120,120)

RadioSpecies = {}
RadioSpecies['Cs137'] = ['Cs137_0','Cs137_1','Cs137_2','Cs137_3','Cs137_4']
Radios = ['Cs137']

Ngaz = {}
Ngaz['']=(83,15,120,120)#83=floor(3000/36)
Ngaz['dry/']=(500,1,120,120)
Ngaz['wet/']=(500,1,120,120)
NgazDep=(500,1,120,120)

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
namesProcesses_corrected = []
for proc in namesProcesses:
    proc = outputDir + sessionName + proc
    namesProcesses_corrected.append(proc)
    #myrun('mkdir -p '+proc+'/to_analyse')
    #print(proc)
namesProcesses = namesProcesses_corrected

######################################    
# Prepare fields to analyse
fields = []

if prepareGroundLevel:    
    ######################################
    # Compute ground level air concentration
    # at a given time
    nameField = 'airGroundLevel'

    def TSelect(Nt):
        return int(np.floor(Nt/2.))

    # for gaz
    (Nt,Nz,Ny,Nx) = Ngaz['']
    tSelect = TSelect(Nt)

    for g in Gaz:
        
        fileScaling = statDir + 'scaling/' + nameField + '_' + g + '_globalScaling.bin'
        scaling = np.fromfile(fileScaling)
        maxi = scaling[3]
        mini = scaling[4]
                                        
        for proc in namesProcesses:

            fileName = proc + '/' + g + '.bin'
            print ('Reading '+fileName+'...')
            data = np.fromfile(fileName, 'f')
            data = data.reshape((Nt,Nz,Ny,Nx))
            data = data[tSelect,:,:,:]
            airGL = data[0,:,:]

            if proc == namesProcesses[0]:
                fields.append(nameField + '_' + g)

            greyScaleLin = greayscale(airGL, mini, maxi, nLevels=analyseResolution, scale='lin')
            greyScaleLOG = greayscale(airGL, mini, maxi, nLevels=analyseResolution, scale='log', EPSILON=MINLOGSCALE)
        
            fileNameLin = proc + '/to_analyse/' + nameField + '_' + g + '_greyscale_lin.npy'
            fileNameLog = proc + '/to_analyse/' + nameField + '_' + g + '_greyscale_log.npy'
            print ('Writing '+fileNameLin+'...')
            print ('Writing '+fileNameLog+'...')

            np.save(fileNameLin,greyScaleLin)
            np.save(fileNameLog,greyScaleLOG)

    # for aerosols
    (Nt,Nz,Ny,Nx) = Nradios['']
    tSelect = TSelect(Nt)

    for aer in Radios:
        fileScaling = statDir + 'scaling/' + nameField + '_' + aer + '_globalScaling.bin'
        scaling = np.fromfile(fileScaling)
        maxi = scaling[3]
        mini = scaling[4]

        for proc in namesProcesses:
    
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

            greyScaleLin = greayscale(airGLAer, mini, maxi, nLevels=analyseResolution, scale='lin')
            greyScaleLOG = greayscale(airGLAer, mini, maxi, nLevels=analyseResolution, scale='log', EPSILON=MINLOGSCALE)
                        
            fileNameLin = proc + '/to_analyse/' + nameField + '_' + aer + '_greyscale_lin.npy'
            fileNameLog = proc + '/to_analyse/' + nameField + '_' + aer + '_greyscale_log.npy'

            print ('Writing '+fileNameLin+'...')
            print ('Writing '+fileNameLog+'...')

            np.save(fileNameLin,greyScaleLin)
            np.save(fileNameLog,greyScaleLOG)
            
if prepareAirColums:
    ######################################
    # Compute columns of air concentration
    # at a given time
    nameField = 'airColumn'
    weights = np.diff(readList.catchLevelsFromFile(fileLevels))

    def TSelect(Nt):
        return int(np.floor(Nt/2.))
    
    # for gaz

    (Nt,Nz,Ny,Nx) = Ngaz['']
    tSelect = TSelect(Nt)

    for g in Gaz:
        fileScaling = statDir + 'scaling/' + nameField + '_' + g + '_globalScaling.bin'
        scaling = np.fromfile(fileScaling)
        maxi = scaling[3]
        mini = scaling[4]
                                    
        for proc in namesProcesses:
        
            fileName = proc + '/' + g + '.bin'
            print ('Reading '+fileName+'...')
            data = np.fromfile(fileName, 'f')
            data = data.reshape((Nt,Nz,Ny,Nx))
            data = data[Nt-1,:,:,:]
            airColumn = np.average(data,axis=0,weights=weights)

            if proc == namesProcesses[0]:
                fields.append(nameField + '_' + g)

            greyScaleLin = greayscale(airColumn, mini, maxi, nLevels=analyseResolution, scale='lin')
            greyScaleLOG = greayscale(airColumn, mini, maxi, nLevels=analyseResolution, scale='log', EPSILON=MINLOGSCALE)

            fileNameLin = proc + '/to_analyse/' + nameField + '_' + g + '_greyscale_lin.npy'
            fileNameLog = proc + '/to_analyse/' + nameField + '_' + g + '_greyscale_log.npy'

            print ('Writing '+fileNameLin+'...')
            print ('Writing '+fileNameLog+'...')

            np.save(fileNameLin,greyScaleLin)
            np.save(fileNameLog,greyScaleLOG)

    # for aerosols

    (Nt,Nz,Ny,Nx) = Nradios['']
    tSelect = TSelect(Nt)
    for aer in Radios:
        fileScaling = statDir + 'scaling/' + nameField + '_' + aer + '_globalScaling.bin'
        scaling = np.fromfile(fileScaling)
        maxi = scaling[3]
        mini = scaling[4]
                                        
        for proc in namesProcesses:

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

            greyScaleLin = greayscale(airColumnAer, mini, maxi, nLevels=analyseResolution, scale='lin')
            greyScaleLOG = greayscale(airColumnAer, mini, maxi, nLevels=analyseResolution, scale='log', EPSILON=MINLOGSCALE)

            fileNameLin = proc + '/to_analyse/' + nameField + '_' + aer + '_greyscale_lin.npy'
            fileNameLog = proc + '/to_analyse/' + nameField + '_' + aer + '_greyscale_log.npy'
            
            print ('Writing '+fileNameLin+'...')
            print ('Writing '+fileNameLog+'...')

            np.save(fileNameLin,greyScaleLin)
            np.save(fileNameLog,greyScaleLOG)

if prepareTotalDeposition:
    ######################################
    # Cumul of the deposition
    nameField = 'totalDeposition'

    # for gaz
    (Ntd,Nzd,Nyd,Nxd) = NgazDep
    for g in Gaz:
        fileScaling = statDir + 'scaling/' + nameField + '_' + g + '_globalScaling.bin'
        scaling = np.fromfile(fileScaling)
        maxi = scaling[3]
        mini = scaling[4]

        for proc in namesProcesses:
            dep = np.zeros(shape=(Nyd,Nxd))
            for DoW in DryorWet:
                (Nt,Nz,Ny,Nx) = Ngaz[DoW]
                fileName = proc + '/' + DoW + g + '.bin'
                print ('Reading '+fileName+'...')
                data = np.fromfile(fileName, 'f')
                data = data.reshape((Nt,Nz,Ny,Nx))
                data = data.cumsum(axis=0)*deltaT
                data = data[Nt-1, 0,:,:]
                #test here if Ny == Nyd and Nx == Nxd
                dep += data

            if proc == namesProcesses[0]:
                fields.append(nameField + '_' + g)
                
            greyScaleLin = greayscale(dep, mini, maxi, nLevels=analyseResolution, scale='lin')
            greyScaleLOG = greayscale(dep, mini, maxi, nLevels=analyseResolution, scale='log', EPSILON=MINLOGSCALE)

            fileNameLin = proc + '/to_analyse/' + nameField + '_' + g + '_greyscale_lin.npy'
            fileNameLog = proc + '/to_analyse/' + nameField + '_' + g + '_greyscale_log.npy'

            print ('Writing '+fileNameLin+'...')
            print ('Writing '+fileNameLog+'...')

            np.save(fileNameLin,greyScaleLin)
            np.save(fileNameLog,greyScaleLOG)
                                                                                    
    # for aerosols
    (Ntd,Nzd,Nyd,Nxd) = NradiosDep
    for aer in Radios:
        fileScaling = statDir + 'scaling/' + nameField + '_' + aer + '_globalScaling.bin'
        scaling = np.fromfile(fileScaling)
        maxi = scaling[3]
        mini = scaling[4]
                                
        for proc in namesProcesses:
            dep = np.zeros(shape=(Nyd,Nxd))
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
                        #test here if Ny == Nyd and Nx == Nxd
                        dep += data
                    
            if proc == namesProcesses[0]:
                fields.append(nameField+'_'+aer)

            greyScaleLin = greayscale(dep, mini, maxi, nLevels=analyseResolution, scale='lin')
            greyScaleLOG = greayscale(dep, mini, maxi, nLevels=analyseResolution, scale='log', EPSILON=MINLOGSCALE)
                        
            fileNameLin = proc + '/to_analyse/' + nameField + '_' + aer + '_greyscale_lin.npy'
            fileNameLog = proc + '/to_analyse/' + nameField + '_' + aer + '_greyscale_log.npy'
            
            print ('Writing '+fileNameLin+'...')
            print ('Writing '+fileNameLog+'...')
            
            np.save(fileNameLin,greyScaleLin)
            np.save(fileNameLog,greyScaleLOG)

######################################
# Writes fields name

f = open(fileFields, 'w')
print ('Writing '+fileFields+'...')

for field in fields:
    f.write(field+'\n')
f.close()
