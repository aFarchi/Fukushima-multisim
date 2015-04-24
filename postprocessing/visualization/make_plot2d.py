import numpy as np
from matplotlib import pyplot as plt

import utils_read_list_of_processes as readList
import utils_plot as plot

######################################
# Defines directions and file names

outputDir = '/cerea_raid/users/farchia/Fukushima-multisim/output/'
sessionName = 'sim-test/'
statDir = outputDir+sessionName+'statistics/'
fileProcesses = outputDir+sessionName+'list_processes.dat'

fileFields    = statDir+'list_fields.dat'
analyseResolution = (1,1,32,32)
scale = 'lin'

LOGSCALEMIN = 1.e-30
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

print(grid)

######################################
# Catch name of fields to analyse and
#    corresponding dimensions

namesFields, dimFields = readList.readListOfFields(fileFields)
for i in xrange(len(namesFields)):
    print(namesFields[i])
    print(dimFields[i])

######################################
# Log filter

def log10Filter(matrix):
    return  np.log10( np.maximum(matrix, LOGSCALEMIN) )

######################################
# Map of the results
plotter = 'imshow'

for i in xrange(len(namesFields)):
    field = namesFields[i]
    dim   = dimFields[i]
    fileScaling = statDir+field+'_globalScaling.bin'
    
    if len(dim) == 2:
        ax = plot.openFigSubfig(figNbr=2,subFigNbr=111,clear=True)
        plot.correctAxesExtend(ax,0.,grid[0],0.,grid[1])

        scaling = np.fromfile(fileScaling)
        if scale == 'lin':
            mini = scaling[4]
            maxi = scaling[3]
        elif scale == 'log':
            mini = log10Filter(scaling[4])
            maxi = log10Filter(scaling[3])
            
        transpose = False
        
        if dim[0] == 2 or dim[1] == 3:
            tranpose = True
            dim = ( dim[1] , dim[0] )

        Xlabel = '$x$'
        Ylabel = '$y$'

        if dim[0] == 0:
            Xlabel = '$t$'
        elif dim[0] == 1:
            Xlabel = '$z$'

        if dim[1] == 0:
            Ylabel = '$t$'
        elif dim[1] == 1:
            Ylabel = '$z$'

        modelList = []
        for proc in namesProcesses:
            modelList.append(proc+'/to_analyse/'+field+'.npy')

        for X in xrange(grid[0]):
            for Y in xrange(grid[1]):
                matrix  = np.load(modelList[grid[0]*Y+X])
                if scale == 'log':
                    matrix = log10Filter(matrix)
                
                figname = statDir+field+'_model'+str(grid[0]*Y+X)
                title   = field+'\nmodel : '+str(grid[0]*Y+X)
                if transpose:
                    matrix = matrix.transpose()

                im = plot.plotMatrixOnAxes(matrix, ax, plotter, extent=[X,X+1.,Y,Y+1.], vmin=mini, vmax=maxi, interpolation='nearest')
                plot.trySaveMatrixPDF(matrix, figname, plotter, title=title, xlabel=Xlabel, ylabel=Ylabel, interpolation='nearest')

        plt.figure(2)
        # add vertical and horizontal lines to distinguish the small matrices
        for X in xrange(grid[0]+1):
            ax.plot([X,X],[0.,grid[1]],'k-',linewidth=5)
        for Y in xrange(grid[1]+1):
            ax.plot([0,grid[0]],[Y,Y],'k-',linewidth=5)

        plot.addLabelsTitleGrid(grid=False,title=field,xlabel=Xlabel,ylabel=Ylabel)
        plt.colorbar(im)
        
        try:
            figname = statDir+field+'_allmodels.pdf'
            print(figname)
            plt.savefig(figname)
        except:
            figname = statDir+field+'_allmodels.png'
            print(figname)
            plt.savefig(figname)
                                    
