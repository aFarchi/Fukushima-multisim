##############
# plotter1d.py
##############

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec

def plotter1d(figName, X, Y, opt=None, ylims=None, title='', xLabel='', yLabel='', grid=False, printIO=False):

    plt.figure()
    plt.clf()
    ax = plt.subplot(111)

    if not opt is None:
        ax.plot(X, Y, opt)
    else:
        ax.plot(X, Y)

    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)

    if not ylims is None:
        ax.set_ylim(ylims)

    if grid:
        ax.grid()
        
    ax.set_title(title)
    plt.tight_layout()
    if printIO:
        print('Writing '+figName+' ...')
    plt.savefig(figName)
    plt.close()
    
def multiPlotter1d(figName, X, arrayNameList, ylims=None, titleList=None, supTitle='', grid=False, printIO=False):

    nbr = len(arrayNameList)
    
    if titleList is None:
        titleList = []
        for i in xrange(nbr):
            titleList.append('sim '+str(i))

    Nc = int(np.floor(np.sqrt(nbr)))
    Nl = Nc
    while Nc*Nl < nbr:
        Nl += 1

    figure = plt.figure()
    plt.clf()
    gs = gridspec.GridSpec(Nl, Nc)
    j = 0

    for (arrayName, title) in zip(arrayNameList, titleList):
        nc = int(np.mod(j,Nc))
        nl = int((j-nc)/Nc)
        
        ax = plt.subplot(gs[nl,nc])
        Y = np.load(arrayName)
        ax.plot(X,Y)
        
        if not ylims is None:
            ax.set_ylim(ylims)

        if grid:
            ax.grid()
        ax.set_title(title)
        j += 1

    gs.tight_layout(figure,rect=[0.,0.,1.,1.])
    plt.suptitle(supTitle)
    if printIO:
        print('Writing '+figName+' ...')
    plt.savefig(figName)
    plt.close()
    
