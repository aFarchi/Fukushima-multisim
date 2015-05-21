############
# applyGS.py
############

import numpy as np
from scipy.interpolate                     import interp1d

from ..utils.run.run                       import runCommand
from ..utils.species.listOfSpecies         import ListOfSpecies
from ..utils.fields.defineFields           import defineFields
from ..utils.io.readLists                  import readListOfProcesses
from ..utils.scaling.scaling               import arrayToScaling

def applyGStoSpecies(outputDir, sessionName, OTGSDir, applyOTGSDir, statDir,
                     AOG, fieldName, lol, TS, species, algoName, printIO):

    fileProcesses   = outputDir + sessionName + 'list_processes.dat'
    procList        = readListOfProcesses(fileProcesses, outputDir + sessionName, '/')
    directory       = OTGSDir + AOG + fieldName + '/' + lol + '/' + TS + '/' + species + '/'
    applydirectory  = applyOTGSDir + AOG + fieldName + '/' + lol + '/' + TS + '/' + species + '/'

    fn    = statDir + 'scaling/' + AOG + fieldName + '/' + lol + '/' + species + '.npy'
    array = np.load(fn)
    scale = arrayToScaling(array)

    def G(x):
        return ( x - scale.mini ) / ( scale.maxi - scale.mini )

    def iG(x):
        return scale.mini + x * ( scale.maxi - scale.mini )

    for p1 in xrange(len(procList)):
        for p2 in xrange(p1):
            
            f0 = np.load(procList[p1] + 'toAnalyse/' + AOG + fieldName + '/' + lol + '/' + species + '.npy')
            f1 = np.load(procList[p2] + 'toAnalyse/' + AOG + fieldName + '/' + lol + '/' + species + '.npy')


            outputDirAlgo  = directory + str(p1) + '-' + str(p2) + '/output_' + algoName + '/'
            outputDirApply = applydirectory + str(p1) + '-' + str(p2) + '/' + algoName + '/'
            fileTmap       = outputDirAlgo + 'Tmap.npy'

            f = open(fileTmap, 'rb')
            X = np.load(f)
            T = np.load(f)
            f.close()

            # make T strictly growing from [0,1] to [0,1]
            NN    = T.size
            error = 0.001
            T[0]  = 0.0
            T     = np.minimum(1.0, T)
            DT    = T[1:] - T[:NN-1]
            DT    = np.maximum(error/NN, DT)
            T[1:] = DT.cumsum()

            T    /= T[NN-1]

            Tmap  = interp1d(X, T)
            iTmap = interp1d(T, X)

            (M, N) = f0.shape
            P = min(M, N) - 1
            GSf0 = np.zeros(shape=(M,N,P+2))
            GSf1 = np.zeros(shape=(M,N,P+2))

            for i in xrange(P+2):
                t = ( float(i) / ( P + 1. ) )
                def iTmapt(x):
                    return t * iTmap(x) + ( 1. - t ) * x
                def Tmapt(x):
                    return t * Tmap(x)  + ( 1. - t ) * x
                GSf0[:,:,i] = iG(iTmapt(G(f0)))
                GSf1[:,:,i] = iG(Tmapt( G(f1)))

            runCommand('mkdir -p '+outputDirApply, printIO)
            outGSf0 = outputDirApply+'GSf0.npy'
            outGSf1 = outputDirApply+'GSf1.npy'
            np.save(outGSf0, GSf0)
            np.save(outGSf1, GSf1)

            if printIO:
                print('Written '+outGSf0+' ...')
                print('Written '+outGSf1+' ...')

def applyGS(outputDir, sessionName, printIO=False):
    OTGSDir        = outputDir + sessionName + 'OTGS/'
    applyOTGSDir   = outputDir + sessionName + 'applyOTGS/'
    statDir        = outputDir + sessionName + 'statistics/'
    fileProcesses  = outputDir + sessionName + 'list_processes.dat'

    lists          = ListOfSpecies()
    procList       = readListOfProcesses(fileProcesses, outputDir+sessionName, '/')
    fieldList      = defineFields()

    listAlgoName = ['pd','anamorph']

    for AOG in ['air/','ground/']:
        for GOR in ['gaz','radios']:
            for species in lists.speciesList[GOR]:
                for field in fieldList[AOG]:
                    for lol in ['lin','log']:
                        for TS in ['Threshold', 'NoThreshold']:
                            for algoName in listAlgoName:
                                applyGStoSpecies(outputDir, sessionName, OTGSDir, applyOTGSDir, statDir,
                                                 AOG, field.name, lol, TS, species, algoName, printIO)
