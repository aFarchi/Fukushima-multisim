#!/usr/bin/env python
import os
import sys

from analyse.preprocessRawData.preprocessRawData          import preprocessRawDataForSpecies


from analyse.statisticalAnalyse.performStatisticalAnalyse import analyseAllFields
from analyse.greyScaleAnalyse.mergeOTGSResults            import mergeOTGSResults
from analyse.greyScaleAnalyse.applyGS                     import applyGStoSpecies

# Read the list of parameters

sys.argv.pop(0)
arguments=dict()
for arg in sys.argv:
    members=arg.split('=')
    arguments[members[0]]=members[1]

# launch the correct function

if arguments['FUNCTION'] == 'preprocessRawDataForSpecies':
    outputDir    = arguments['OUTPUT_DIR']
    sessionName  = arguments['SESSION_NAME']
    xTSelect     = float(arguments['X_TSELECT'])
    ntAnalyse    = int(arguments['NT_ANALYSE'])
    nzAnalyse    = int(arguments['NZ_ANALYSE'])
    nyAnalyse    = int(arguments['NY_ANALYSE'])
    nxAnalyse    = int(arguments['NX_ANALYSE'])
    nLevels      = int(arguments['N_LEVELS'])
    AOG          = arguments['AOG']
    GOR          = arguments['GOR']
    species      = arguments['SPECIES']
    printIO      = ( arguments['PRINT_IO'] == 'True' )
    analyseShape = (ntAnalyse,nzAnalyse,nyAnalyse,nxAnalyse)

    preprocessRawDataForSpecies(outputDir, sessionName, xTSelect, analyseShape, nLevels, AOG, GOR, species, printIO)

if arguments['FUNCTION'] == 'analyseAllFields':
    outputDir   = arguments['OUTPUT_DIR']
    sessionName = arguments['SESSION_NAME']
    printIO     = ( arguments['PRINT_IO'] == 'True' )

    analyseAllFields(outputDir, sessionName, printIO)

if arguments['FUNCTION'] == 'mergeOTGSResults':
    nbrProc   = int(arguments['NBR_PROC'])
    directory = arguments['DIR']
    algoName  = arguments['ALGO']
    printIO   = ( arguments['PRINT_IO'] == 'True' )

    mergeOTGSResults(nbrProc, directory, algoName, printIO)

if arguments['FUNCTION'] == 'applyGStoSpecies':
    outputDir    = arguments['OUTPUT_DIR']
    sessionName  = arguments['SESSION_NAME']
    OTGSDir      = arguments['OTGS_DIR']
    applyOTGSDir = arguments['APPLYOTGS_DIR']
    statDir      = arguments['STAT_DIR']
    AOG          = arguments['AOG']
    fieldName    = arguments['FIELD_NAME']
    lol          = arguments['LOL']
    TS           = arguments['TS']
    species      = arguments['SPECIES']
    algoName     = arguments['ALGO_NAME']
    printIO      = ( arguments['PRINT_IO'] == 'True' )

    applyGStoSpecies(outputDir, sessionName, OTGSDir, applyOTGSDir, statDir,
                     AOG, fieldName, lol, TS, species, algoName, printIO)
