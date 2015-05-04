import os
import sys

import numpy as np
from matplotlib import pyplot as plt

import utils_read_list_of_processes as readList
import utils_plot as plot

######################################
# run command

def myrun(command):
    status = os.system(command)
    print command
    if status != 0:
        sys.exit(status)                

######################################
# Defines directions and file names

outputDir = '/cerea_raid/users/farchia/Fukushima-multisim/output/'
sessionName = 'sim-test-2/'
statDir = outputDir+sessionName+'statistics/'
fileProcesses = outputDir+sessionName+'list_processes.dat'
figDir = outputDir+sessionName+'figures/'

fileFields    = outputDir+sessionName+'list_fields.dat'
analyseResolution = (1,1,32,32)

LinorLog = ['lin','log']

######################################
# Catch name of processes
namesProcesses = readList.readListOfProcesses(fileProcesses)
namesProcesses_corrected = []

for name in namesProcesses:
    print(name)
    namesProcesses_corrected.append(outputDir+sessionName+name)
namesProcesses = namesProcesses_corrected

# determines grid to plot all the results
nbrProcesses = len(namesProcesses)

Nl = int(np.floor(np.sqrt(nbrProcesses)))
Nc = Nl
while Nl*Nc < nbrProcesses:
    Nl += 1

######################################
# Catch name of fields to analyse and
#    corresponding dimensions

namesFields, dimFields = readList.readListOfFields(fileFields)
for i in xrange(len(namesFields)):
    print(namesFields[i])
    #print(dimFields[i])

######################################
# Make directories if necessary

myrun('mkdir -p '+figDir)
for name in namesFields:
    for lol in LinorLog:
        myrun('mkdir -p '+figDir+name+'/'+lol)

######################################
# Map of the results
plotter = 'imshow'

for (field,dim) in zip(namesFields,dimFields):
    if len(dim) == 2:
        for lol in LinorLog:
            fig = plt.figure(1)
            plt.clf()
            fileScaling = statDir+'scaling/'+field+'_globalScaling_'+lol+'.bin'
            scaling = np.fromfile(fileScaling)

            mini = scaling[4]
            maxi = scaling[3]
            
            transpose = False
        
            if dim[0] == 2 or dim[1] == 3:
                tranpose = True

            modelList = []
            for proc in namesProcesses:
                modelList.append(proc+'/to_analyse/'+field+'_'+lol+'.npy')

            j = 1

            for model in modelList:
                ax = plt.subplot(Nl,Nc,j)
                matrix  = np.load(model)

                if transpose:
                    matrix = matrix.transpose()

                im = plot.plotMatrixOnAxes(matrix, ax, plotter, extent=[0.,1.,0.,1.], vmin=mini, vmax=maxi, interpolation='nearest')
                j += 1
                ax.tick_params(
                    axis='x',          
                    which='both',  
                    bottom='off',  
                    top='off',     
                    labelbottom='off')
                ax.tick_params(#does not work -> why ??
                    axis='y',          
                    which='both',  
                    bottom='off',  
                    top='off',     
                    labelbottom='off')

            
            fig.subplots_adjust(right=0.8)
            cbarAx = fig.add_axes([0.85, 0.15, 0.05, 0.7])
            fig.colorbar(im, cax=cbarAx)
            try:
                figname = figDir+field+'/'+lol+'/allmodels_'+lol+'.pdf'
                print(figname)
                plt.savefig(figname)
            except:
                figname = figDir+field+'/'+lol+'/allmodels_'+lol+'.png'
                print(figname)
                plt.savefig(figname)
                                    
