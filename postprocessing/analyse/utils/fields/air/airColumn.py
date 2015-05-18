###################
# airColumn.py
###################

import numpy as np
from ...io.readLists                      import catchLevelsFromFile
from ...processRawData.interpolateRawData import interpolateRawData

class AirColumn:

    def __init__(self, funTSelect=None, fileLevels=None):
        self.name      = 'airColumn'
        self.dimension = 2
        self.labels    = [ 'longitude' , 'latitude' ]
       
        if funTSelect is None:           
            def funTSelect(Nt):
                return Nt-1
        self.funTSelect = funTSelect

        try:
            levels = catchLevelsFromFile(fileLevels)
            self.weights = np.diff(levels)
        except:
            self.weights = None

    def extract(self, rawData):

        t = self.funTSelect(rawData.shape[0])

        if self.weights is None:
            return np.average(rawData[t,:,:,:],axis=0).transpose()
        else:
            return np.average(rawData[t,:,:,:],axis=0,weights=self.weights).transpose()

    def interpolate(self, extractedData, analyseShape):
        return interpolateRawData(extractedData, (analyseShape[3], analyseShape[2]))
