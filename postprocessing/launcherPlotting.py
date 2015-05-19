#!/usr/bin/env python
import os
import sys

from analyse.plotting.plotFields                          import plot2dProcessedRawDataSpecies

# Read the list of parameters

sys.argv.pop(0)
arguments=dict()
for arg in sys.argv:
    members=arg.split('=')
    arguments[members[0]]=members[1]

# launch the correct function

if arguments['FUNCTION'] == 'plot2dFields':
    outputDir   = arguments['OUTPUT_DIR']
    sessionName = arguments['SESSION_NAME']
    statDir     = arguments['STAT_DIR']
    figDir      = arguments['FIG_DIR']
    nLevels     = int(arguments['N_LEVELS'])
    AOG         = arguments['AOG']
    fieldName   = arguments['FIELD_NAME']
    lol         = arguments['LOL']
    species     = arguments['SPECIES']
    xLabel      = arguments['XLABEL']
    yLabel      = arguments['YLABEL']
    plotter     = arguments['PLOTTER']
    printIO     = ( arguments['PRINT_IO'] == 'True' )

    plot2dProcessedRawDataSpecies(outputDir, sessionName, statDir, figDir, nLevels,
                                  AOG, fieldName, lol, species, xLabel, yLabel, plotter, printIO)