###############
# plotFields.py
###############

import numpy as np

from ..utils.run.run                       import runCommand
from ..utils.species.listOfSpecies         import ListOfSpecies
from ..utils.fields.defineFields           import defineFields
from ..utils.io.readLists                  import readListOfProcesses
from ..utils.io.readLists                  import suffixFileName
from ..utils.scaling.scaling               import arrayToScaling

from plotter2d import plotMatrix

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import animation as anim
from mpl_toolkits.axes_grid1 import make_axes_locatable


def customTransparency(t):
        return max(t,0.25)

def plotAppliedGStoSpecies(outputDir, sessionName, OTGSDir, applyOTGSDir, statDir, figDir,
                           AOG, fieldName, lol, TS, species, algoName,
                           xLabel, yLabel, plotter='imshow', printIO=False, **kwargs):

    fileProcesses   = outputDir + sessionName + 'list_processes.dat'
    procList        = readListOfProcesses(fileProcesses, outputDir + sessionName, '/')
    dir             = AOG + fieldName + '/' + lol + '/' + TS + '/' + species + '/'
    directory       = OTGSDir + dir
    applydirectory  = applyOTGSDir + dir
    figdirectory    = figDir + 'applyGS/' + dir

    fn    = statDir + 'scaling/' + AOG + fieldName + '/' + lol + '/' + species + '.npy'
    array = np.load(fn)
    scale = arrayToScaling(array)
    mini  = scale.mini
    maxi  = scale.maxi

    transpFun = customTransparency

    kwargsCurrent = kwargs
    if not kwargsCurrent.has_key('origin'):
        kwargsCurrent['origin'] = 'lower'
    if not kwargsCurrent.has_key('extent'):
        kwargsCurrent['extent'] = [0.,1.,0.,1.]
    if not kwargsCurrent.has_key('vmin'):
        kwargsCurrent['vmin'] = scale.mini
    if not kwargsCurrent.has_key('vmax'):
        kwargsCurrent['vmax'] = scale.maxi
    if not kwargsCurrent.has_key('interpolation'):
        kwargsCurrent['interpolation'] = 'nearest'

    kwargsInit                = {}
    kwargsInit['origin']      = 'lower'
    kwargsInit['extent']      = [0.,1.,0.,1.]
    kwargsInit['vmin']        = mini
    kwargsInit['vmax']        = maxi
    kwargsInit['colors']      = 'k'
    kwargsInit['linestyles']  = 'solid'
    kwargsInit['linewidths']  = 1.5

    kwargsFinal               = {}
    kwargsFinal['origin']     = 'lower'
    kwargsFinal['extent']     = [0.,1.,0.,1.]
    kwargsFinal['vmin']       = mini
    kwargsFinal['vmax']       = maxi
    kwargsFinal['colors']     = 'k'
    kwargsFinal['linestyles'] = 'dashed'
    kwargsFinal['linewidths'] = 1.5

    xTxt  = 0.01
    yTxt  = -0.05
    yPbar = -0.05

    for p1 in xrange(len(procList)):
        for p2 in xrange(p1):

            f0 = np.load(procList[p1] + 'toAnalyse/' + AOG + fieldName + '/' + lol + '/' + species + '.npy')
            f1 = np.load(procList[p2] + 'toAnalyse/' + AOG + fieldName + '/' + lol + '/' + species + '.npy')

            outputDirApply = applydirectory + str(p1) + '-' + str(p2) + '/' + algoName + '/'
            outputDirFig   = figdirectory   + str(p1) + '-' + str(p2) + '/' + algoName + '/'
            
            outGSf0 = outputDirApply+'GSf0.npy'
            outGSf1 = outputDirApply+'GSf1.npy'

            GSf0 = np.load(outGSf0)
            GSf1 = np.load(outGSf1)

            runCommand('mkdir -p '+outputDirFig, printIO)

            Tmax = GSf0.shape[2]

            for (matrix,mInit,mFinal,prefix) in zip([GSf0, GSf1],[f0,f1],[f1,f0],['GSf0','GSf1']):
                for t in xrange(Tmax):

                    kwargsInit['alpha']  = transpFun(1.-float(t)/(Tmax-1.))
                    kwargsFinal['alpha'] = transpFun(float(t)/(Tmax-1.))
                    
                    plt.figure()
                    plt.clf()
                    ax = plt.subplot(111)
                    
                    timeText     = ax.text(xTxt, yTxt, suffixFileName(t,Tmax)+' / '+str(Tmax-1))
                    if t < Tmax-1:
                        lineBkgPbar, = ax.plot([float((0.+t)/(Tmax))*0.6+0.2,0.8],[yPbar,yPbar], 'k-', linewidth=5)
                    if t > 0:
                        linePbar,    = ax.plot([0.2,float((0.+t)/(Tmax))*0.6+0.2],[yPbar,yPbar], 'g-', linewidth=5)
                
                    im = plotMatrix(ax, matrix[:,:,t], plotter, **kwargsCurrent)
                    plotMatrix(ax, mInit, 'contour', **kwargsInit)
                    plotMatrix(ax, mFinal, 'contour', **kwargsFinal)
                    
                    ax.set_xlabel(xLabel)
                    ax.set_ylabel(yLabel)
                
                    ax.set_xlim(-0.1,1.1)
                    ax.set_ylim(-0.1,1.1)
                
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes('right', '10%', pad='5%')

                    cmap = mpl.cm.jet
                    norm = mpl.colors.Normalize(vmin=mini, vmax=maxi)
                    cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation='vertical')
                
                    ax.set_title(prefix+'\nt = ' + suffixFileName(t,Tmax) + ' / '+str(Tmax-1))
                    plt.tight_layout()
                
                    figName = outputDirFig + prefix + suffixFileName(t,Tmax) + '.pdf'
                    print('Writing '+figName+' ...')
                    plt.savefig(figName)
                    plt.close()
                                                                                
def plotAppliedGS(outputDir, sessionName, plotter='imshow', printIO=False, **kwargs):
    OTGSDir        = outputDir + sessionName + 'OTGS/'
    applyOTGSDir   = outputDir + sessionName + 'applyOTGS/'
    statDir        = outputDir + sessionName + 'statistics/'
    fileProcesses  = outputDir + sessionName + 'list_processes.dat'
    figDir         = outputDir + sessionName + 'figures/'
    
    lists          = ListOfSpecies()
    procList       = readListOfProcesses(fileProcesses, outputDir+sessionName, '/')
    fieldList      = defineFields()
    
    listAlgoName = ['pd','anamorph']
    
    for AOG in ['air/','ground/']:
        for GOR in ['gaz','radios']:
            for species in lists.speciesList[GOR]:
                for field in fieldList[AOG]:
                    xLabel = field.labels[0]
                    yLabel = field.labels[1]
                    for lol in ['lin','log']:
                        for TS in ['Threshold', 'NoThreshold']:
                            for algoName in listAlgoName:
                                plotAppliedGStoSpecies(outputDir, sessionName, OTGSDir, applyOTGSDir, statDir, figDir,
                                                       AOG, field.name, lol, TS, species, algoName,
                                                       xLabel, yLabel, plotter, printIO, **kwargs)
                                
