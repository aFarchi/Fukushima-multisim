###################
# airColumn.py
###################

from ...processRawData.interpolateRawData import interpolateRawData

class TotalDeposition:

    def __init__(self, funTSelect=None):
        self.name      = 'totalDeposition'
        self.dimension = 2
        self.labels    = [ 'longitude' , 'latitude' ]

        if funTSelect is None:
            def funTSelect(Nt):
                return Nt-1
        self.funTSelect = funTSelect

    def extract(self, rawData):
        t = self.funTSelect(rawData.shape[0])
        return rawData[t,:,:].transpose()

    def extractAllIterations(self, rawData):
        return rawData[:,:,:].transpose((0,2,1))

    def interpolate(self, extractedData, analyseShape):
        return interpolateRawData(extractedData, (analyseShape[3], analyseShape[2]))
