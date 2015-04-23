#import os
#import sys
import numpy as np
from matplotlib import pyplot as plt

import utils_read_list_of_processes as readList
import utils_plot.py as plot

######################################
# run command

#def myrun(command):
#    status = os.system(command)
#    print command
#    if status != 0:
#        sys.exit(status)

######################################
# Defines directions and file names

outputDir = '/cerea_raid/users/farchia/Fukushima-multisim/output/'
sessionName = 'sim-test/'
statDir = outputDir+sessionName+'statistics/'
fileProcesses = outputDir+sessionName+'list_processes.dat'

fileFields    = statDir+'list_fields.dat'
analyseResolution = (1,1,32,32)

######################################
# Catch name of processes
namesProcesses = readList.readListOfProcesses(fileProcesses)
for name in namesProcesses:
    print(name)

# determines grid to plot all the results
nbrProcesses = len(namesProcesses)
divisors = []
for i in (1 + np.arange(nbrProcesses)):
    if np.mod(nbrProcesses,i) == 0:
        divisors.append(i)

divisors = np.array(divisors)
best = divisors[ np.argmin(np.abs(divisors-np.sqrt(nbrProcesses))) ]
best = np.max([ best, nbrProcesses/best ])
grid = (best, nbrProcesses/best)

######################################
# Catch name of fields to analyse and
#    corresponding dimensions

namesFields,dimFields = readList.readListOfFields(fileFields)
for name in namesFields:
    print(name)
                                        
######################################
# Map of the results
plotter = 'contourf'

for i in xrange(len(namesFields)):
    field = namesFields[i]
    dim   = dimFields[i]
    fileScaling = statDir+field+'_globalScaling.bin'
    
    if len(dim) == 2:
        ax = plot.openFigSubfig(figNbr=2,subFigNbr=111,clear=True)
        plot.correctAxesExtend(ax,0.,grid[0],0.,grid[1])

        scaling = np.fromfile(fileScaling)
        mini = scaling[4]
        maxi = scaling[3]
        transpose = False
        
        if dim[0] == 2 or dim[1] == 3:
            tranpose = True

        modelList = []
        for proc in namesProcesses:
            modelList.append(proc+'/to_analyse/'+field+'.npy')

        for X in xrange(grid[0]):
            for Y in xrange(grid[1]):
                matrix  = np.load(modelList[grid[0]*Y+X])
                figname = statDir+field+'_model'+str(grid[0]*Y+X) 
                if transpose:
                    matrix = matrix.transpose()

                if plotter == 'imshow':
                    plot.plotMatrixOnAxes(matrix, ax, origin='lower', extent=[X,X+1.,Y,Y+1.], vmin=mini, vmax=maxi,
                                          cmap=None, norm=None, aspect=None, interpolation=None, alpha=None, shape=None,
                                          filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None)
                    try:
                        figname += '.pdf'
                        saveMatrix(matrix, figname, clbar=True,
                                   origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                                   grid=False, title='', xlabel='', ylabel='',
                                   cmap=None, norm=None, aspect=None, interpolation=None, alpha=None, shape=None,
                                   filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None)
                    except:
                        figname += '.png'
                        saveMatrix(matrix, figname, clbar=True,
                                   origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                                   grid=False, title='', xlabel='', ylabel='',
                                   cmap=None, norm=None, aspect=None, interpolation=None, alpha=None, shape=None,
                                   filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None)

                elif plotter == 'contour':
                    plot.contourMatrixOnAxes(matrix, ax, levels=None, vmin=mini, vmax=maxi, origin='lower', extent=[X,X+1.,Y,Y+1.], extend='neither',
                                             colors=,None, linewidths=None, linestyles=None, locator=None, alpha=None, cmap=None, norm=None, antialiased=True)

                    try:
                        figname += '.pdf'
                        saveMatrixContour(matrix, figname, clbar=True, fill=True,
                                          origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                                          grid=False, title='', xlabel='', ylabel='',
                                          cmap=None, norm=None, alpha=None,
                                          levels=None, extend='neither',
                                          colors=None, linewidths=None, linestyles=None, locator=None, antialiased=True)
                    except:
                         figname += '.png'
                         saveMatrixContour(matrix, figname, clbar=True, fill=True,
                                           origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                                           grid=False, title='', xlabel='', ylabel='',
                                           cmap=None, norm=None, alpha=None,
                                           levels=None, extend='neither',
                                           colors=None, linewidths=None, linestyles=None, locator=None, antialiased=True)
                                                                     
                elif plotter == 'contourf':
                    plot.contourfMatrixOnAxes(matrix, ax, levels=None, vmin=mini, vmax=maxi, origin='lower', extent=[X,X+1.,Y,Y+1.], extend='neither',
                                              colors=None, linewidths=None, linestyles=None, locator=None, alpha=None, cmap=None, norm=None, antialiased=True)

                    try:
                        figname += '.pdf'
                        saveMatrixContour(matrix, figname, clbar=True, fill=True,
                                          origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                                          grid=False, title='', xlabel='', ylabel='',
                                          cmap=None, norm=None, alpha=None,
                                          levels=None, extend='neither',
                                          colors=None, linewidths=None, linestyles=None, locator=None, antialiased=True)
                    except:
                        figname += '.png'
                        saveMatrixContour(matrix, figname, clbar=True, fill=True,
                                          origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                                          grid=False, title='', xlabel='', ylabel='',
                                          cmap=None, norm=None, alpha=None,
                                          levels=None, extend='neither',
                                          colors=None, linewidths=None, linestyles=None, locator=None, antialiased=True)

        plt.figure(2)
        # add vertical and horizontal lines to distinguish the small matrices
        for X in xrange(grid[0]):
            ax.plot([X,X],[0.,grid[1]],'k-',linewidth=5)
        for Y in xrange(grid[1]):
            ax.plot([X,X],[0.,grid[1]],'k-',linewidth=5))
        
        addLabelsTitleGrid(grid=False,title=field,xlabel='',ylabel='')
        try:
            plt.savefig(statDir+field+'_allmodels.pdf')
        except:
            plt.savefig(statDir+field+'_allmodels.png')
