##############
# plotter2d.py
##############

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import gridspec

def plotMatrix(ax, matrix, plotter='imshow', **kwargs):
    if plotter == 'imshow':
        return ax.imshow(matrix, **kwargs)
    elif plotter == 'contour':
        return ax.contour(matrix, **kwargs)
    elif plotter == 'contourf':
        return ax.contourf(matrix, **kwargs)

def plotter2d(figName, Y, mini=None, maxi=None, plotter='imshow', title='', xLabel='', yLabel='', xticks=[], yticks=[], printIO=False, **kwargs):
    
    plt.figure()
    plt.clf()
    ax = plt.subplot(111)

    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)

    try:
        extent = kwargs['extent']
        ax.set_xlim(extent[0],extent[1])
        ax.set_ylim(extent[2],extent[3])
    except:
        kwargs['extent'] = [0.0, 1.0, 0.0, 1.0]
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)

    if mini is None:
        mini = Y.min()
    if maxi is None:
        maxi = Y.max()

    ax.set_yticks(yticks)
    ax.set_xticks(xticks)

    kwargs['vmin'] = mini
    kwargs['vmax'] = maxi

    im = plotMatrix(ax, Y, plotter, **kwargs)
    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', '10%', pad='5%')

    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=mini, vmax=maxi)
    cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation='vertical')

    ax.set_title(title)
    plt.tight_layout()
    if printIO:
        print('Writing '+figName+' ...')
    plt.savefig(figName)
    plt.close()


def multiPlotter2d(figName, arrayNameList, mini, maxi, plotter='imshow', titleList=None, supTitle='', printIO=False, **kwargs):

    nbr = len(arrayNameList)
    
    if titleList is None:
        titleList = []
        for i in xrange(nbr):
            titleList.append('sim '+str(i))

    kwargs['vmin'] = mini
    kwargs['vmax'] = maxi
    
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
        
        try:
            extent = kwargs['extent']
            ax.set_xlim(extent[0],extent[1])
            ax.set_ylim(extent[2],extent[3])
        except:
            kwargs['extent'] = [0.0, 1.0, 0.0, 1.0]
            ax.set_xlim(0.0, 1.0)
            ax.set_ylim(0.0, 1.0)

        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_title(title)        
        im = plotMatrix(ax, Y, plotter, **kwargs)
        j += 1


    gs.tight_layout(figure,rect=[0.,0.,0.85,1.])
    gs2 = gridspec.GridSpec(1,1)
    gs2.update(left=0.87,right=0.93)

    cax = plt.subplot(gs2[0,0],frameon=False)
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=mini, vmax=maxi)
    cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation='vertical')

    plt.suptitle(supTitle)

    if printIO:
        print('Writing '+figName+' ...')
    plt.savefig(figName)
    plt.close()
                                                                                
