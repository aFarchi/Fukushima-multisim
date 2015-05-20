#!/usr/bin/env python

from analyse.preprocessRawData.makeLauncherPreprocess          import makeLauncherPreprocessRawDataForAllSpecies
from analyse.statisticalAnalyse.makeLauncherStatisticalAnalyse import makeLauncherAnalyseAllFields 
from analyse.greyScaleAnalyse.makeLaunchersOTGSAnalyse         import makeLaunchersOTGSAnalyse
from analyse.greyScaleAnalyse.makeLauncherApplyGS              import makeLauncherApplyGS

oDir           = '/cerea_raid/users/farchia/Fukushima-multisim/output/'
sName          = 'sim-test-2/'

analyseShape   = (1,1,32,32)
nLevelsAnalyse = 30
printIO        = True

xTSelect       = 1.0

plotter        = 'imshow'
interpolation  = 'nearest'
colors         = 'k'
linestyles     = 'solid'
linewidths     = 1.5

prepareAllFieds    = False
statisticalAnalyse = False
OTGSAnalyse        = True
applyGS            = False

if prepareAllFieds:
    makeLauncherPreprocessRawDataForAllSpecies(oDir, sName, xTSelect, analyseShape, nLevelsAnalyse, printIO)

if statisticalAnalyse:
    makeLauncherAnalyseAllFields(oDir, sName, printIO=printIO)

if OTGSAnalyse:
    makeLaunchersOTGSAnalyse(oDir, sName, nLevelsAnalyse, printIO)

if applyGS:
    makeLauncherApplyGS(oDir, sName, printIO)


