#################
# defineFields.py
#################

from air.airColumn          import AirColumn
from air.airGroundLevel     import AirGroundLevel
from ground.totalDeposition import TotalDeposition

def defineAirFields(funTSelect=None, fileLevels=None):

    airColumn      = AirColumn(funTSelect, fileLevels)
    airGroundLevel = AirGroundLevel(funTSelect)

    return [ airColumn , airGroundLevel ]

def defineGroundFields(funTSelect=None):

    totalDep = TotalDeposition(funTSelect)

    return [totalDep]

def defineFields(funTSelect=None, fileLevels=None):
    fieldList            = {}
    fieldList['air/']    = defineAirFields(funTSelect, fileLevels)
    fieldList['ground/'] = defineGroundFields(funTSelect)
    return fieldList
