###############
# triplotter.py
###############

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plotMatrix(ax, matrix, plotter='imshow', **kwargs):
    if plotter == 'imshow':
        return ax.imshow(matrix, **kwargs)
    elif plotter == 'contour':
        return ax.contour(matrix, **kwargs)
    elif plotter == 'contourf':
        return ax.contourf(matrix, **kwargs)

def triPlotter(figName, XGS, GST, GSNT, Y, plotter='imshow', title='', xLabel='', yLabel='',
               xTicks=[], yTicks=[], mini=None, maxi=None, printIO=False, **kwargs):

    plt.figure()
    plt.clf()

    if mini is None:
        mini = Y.min()
    if maxi is None:
        maxi = Y.max()

    ax = plt.subplot(211)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_yticks(yTicks)
    ax.set_xticks(xTicks)
    kwargs['extent'] = [0.0, 1.0, 0.0, 1.0]
    kwargs['vmin']   = mini
    kwargs['vmax']   = maxi
    im = plotMatrix(ax, Y, plotter, **kwargs)
    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', '10%', pad='5%')
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=mini, vmax=maxi)
    cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation='vertical')
    
    ax = plt.subplot(212)
    ax.plot(XGS, GST, label='with threshold')
    ax.plot(XGS, GSNT, label='without threshold')
    ax.set_ylim([0.,1.])

    plt.legend()
    plt.suptitle(title)
    plt.tight_layout()
 
    plt.savefig(figName)
    plt.close()

    if printIO:
        print('Writing '+figName+' ...')



                                                                                
