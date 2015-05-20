from analyse.plotting.makeLaunchersPlotting import makeLauncherPlot2dFields
from analyse.plotting.makeLaunchersPlotting import makeLauncherPlotAppliedGS

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

plot2dFields  = True
appliedGS     = True

if plot2dFields:
    makeLauncherPlot2dFields(oDir, sName, nLevelsAnalyse, plotter=plotter, interpolation=interpolation, colors=colors,
                             linestyles=linestyles, linewidths=linewidths, printIO=printIO)

if appliedGS:
    makeLauncherPlotAppliedGS(oDir, sName, plotter=plotter, interpolation=interpolation, colors=colors,
                              linestyles=linestyles, linewidths=linewidths, printIO=printIO)
