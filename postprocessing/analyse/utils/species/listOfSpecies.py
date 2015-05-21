##################
# listOfSpecies.py
##################

class ListOfSpecies:

    def __init__(self, configDir=None):
        self.speciesList                    = {}
        self.speciesList['gaz']             = []
        self.speciesList['radios']          = []

        self.speciesBinList                 = {}
        self.speciesBinList['gaz']          = {}
        self.speciesBinList['radios']       = {}

        self.rawShapes                      = {}
        self.rawShapes['gaz']               = {}
        self.rawShapes['gaz']['air/']       = None
        self.rawShapes['gaz']['ground/']    = None
        self.rawShapes['radios']            = {}
        self.rawShapes['radios']['air/']    = None
        self.rawShapes['radios']['ground/'] = None

        self.minValues                      = {}
        self.minValuesGS                    = {}
        self.minValuesLog                   = {}

        try:
            self.initFromFiles(configDir)
        except:
            self.defaultInit()

    def initFromFiles(self, configDir):
        # STILL NEED TO WRITE THIS FUNCTION
        raise ValueError('Not implemented')

    def defaultInit(self):
        self.speciesList['gaz']                = ['I2']
        self.speciesList['radios']             = ['Cs137']
        
        self.speciesBinList['gaz']['I2']       = ['I2']
        self.speciesBinList['radios']['Cs137'] = ['Cs137_0','Cs137_1','Cs137_2','Cs137_3','Cs137_4']
                
        self.rawShapes['gaz']['air/']          = (83,15,120,120)
        self.rawShapes['gaz']['ground/']       = (500,1,120,120)
        self.rawShapes['radios']['air/']       = (500,15,120,120)
        self.rawShapes['radios']['ground/']    = (500,1,120,120)
        
        self.minValues['air/']                 = 1.e-10 # in Bq/m^2
        self.minValues['ground/']              = 1.e-10 # in Bq/m^3
        self.minValuesGS['air/']               = 1.e-11
        self.minValuesGS['ground/']            = 1.e-11
        self.minValuesLog['air/']              = 0.0
        self.minValuesLog['ground/']           = 0.0
        self.deltaT                            = 3600.
