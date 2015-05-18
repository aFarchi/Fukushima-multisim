import numpy as np

def extractRawData(procName, AOG, GOR, species, speciesBin, rawShape, deltaT=None, printIO=False):

    if AOG == 'air/':
        for speBin in speciesBin[species]:
            fileName = procName + speBin + '.bin'
            if printIO:
                print ('Reading '+fileName+'...')
            try:
                rawData += np.fromfile(fileName, 'f')
            except:
                rawData  = np.fromfile(fileName, 'f')
        return rawData.reshape(rawShape)

    elif AOG == 'ground/':

        dow = ['dry/','wet/']
        iob = {}
        iob['dry/'] = ['']
        if GOR == 'gaz':
            iob['wet/'] = ['']
        elif GOR == 'radios':
            iob['wet/'] = ['InCloud/', 'BelowCloud/']
        
        for speBin in speciesBin[species]:
            for DOW in dow:
                for IOB in iob[DOW]:
                    fileName = procName + DOW + IOB + speBin + '.bin'
                    if printIO:
                        print ('Reading '+fileName+'...')
                    try:
                        rawData += np.fromfile(fileName, 'f')
                    except:
                        rawData  = np.fromfile(fileName, 'f')
        rawData = rawData.reshape(rawShape)[:,0,:,:]
        return rawData.cumsum(axis=0)*deltaT
