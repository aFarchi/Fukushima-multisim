##############
# readLists.py
##############

import numpy as np

def suffixFileName(i,iMaxP1):
    nDigit = np.ceil(np.log10(iMaxP1))
    s = str(int(i))
    while len(s) < nDigit:
        s = '0'+s
    return s

def suffixOfShifts(dx,dy,dz,dt):
    s = 'shift_'
    s += dx + '_'
    s += dy + '_'
    s += dz + '_'
    s += dt
    return s
                                                
def catchLevelsFromFile(fileName):
    f = open(fileName, 'r')
    lines = f.readlines()
    levels = np.zeros(len(lines))
    for i in xrange(len(lines)):
        levels[i] = float(lines[i])
    return levels
                            
def readListOfProcesses(fileName, prefixProcName=None, suffixProcName=None):
    f = open(fileName, 'r')
    lines = f.readlines()

    parameters = lines[0].split('\t')
    parameters[len(parameters)-1] = parameters[len(parameters)-1].replace('\n','')

    for i in xrange(len(parameters)):
        if parameters[i] == 'BCS':
            BCS_num = i
        elif parameters[i] == 'BCSunder':
            BCSunder_num = i
        elif parameters[i] == 'ICS':
            ICS_num = i
        elif parameters[i] == 'ICSunder':
            ICSunder_num = i
        elif parameters[i] == 'DRY_DEP':
            DRY_DEP_num = i
        elif parameters[i] == 'RESOLUTION':
            RESOLUTION_num = i
        elif parameters[i] == 'SOURCE':
            SOURCE_num = i
        elif parameters[i] == 'PSD_SOURCE':
            PSD_SOURCE_num = i
        elif parameters[i] == 'METEO':
            METEO_num = i
        elif parameters[i] == 'KZ':
            KZ_num = i
        elif parameters[i] == 'RAIN':
            RAIN_num = i
        elif parameters[i] == 'DX':
            DX_num = i
        elif parameters[i] == 'DY':
            DY_num = i
        elif parameters[i] == 'DZ':
            DZ_num = i
        elif parameters[i] == 'DT':
            DT_num = i
            
    names = []
    for i in (1+np.arange(len(lines)-1)):
        parameters = lines[i].split('\t')
        parameters[len(parameters)-1] = parameters[len(parameters)-1].replace('\n','')

        BCS        = parameters[BCS_num]
        BCSunder   = parameters[BCSunder_num]
        ICS        = parameters[ICS_num]
        ICSunder   = parameters[ICSunder_num]
        DryDep     = parameters[DRY_DEP_num]
        Reso       = parameters[RESOLUTION_num]
        Source     = parameters[SOURCE_num]
        PSD_Source = parameters[PSD_SOURCE_num]
        Met        = parameters[METEO_num]
        Kz         = parameters[KZ_num]
        Rain       = parameters[RAIN_num]
        dx         = parameters[DX_num]
        dy         = parameters[DY_num]
        dz         = parameters[DZ_num]
        dt         = parameters[DT_num]

        suffix = suffixOfShifts(dx,dy,dz,dt)
        name = ( Reso + '-' +
                 Source + '_' + PSD_Source + '-' +
                 Met + '-' +
                 Kz + '-' +
                 Rain + '-' +
                 DryDep + '-' +
                 ICS + '-' + ICSunder + '-' +
                 BCS + '-' + BCSunder + '-' +
                 suffix )
        names.append(name)


    if not prefixProcName is None:
        result = []
        for name in names:
            result.append(prefixProcName + name)
        names = result

    if not suffixProcName is None:
        result = []
        for name in names:
            result.append(name + suffixProcName)
        names = result

    return names
