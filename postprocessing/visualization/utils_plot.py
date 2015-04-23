import numpy as np
from matplotlib import pyplot as plt

def openFigSubfig(xscale='linear',yscale='linear',figNbr=1,subFigNbr=111,clear=True):
    fig = plt.figure(figNbr)
    if clear:
        plt.clf()
    ax = fig.add_subplot(subFigNbr)
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    return ax

def addLabelsTitleGrid(grid=False,title='',xlabel='',ylabel=''):
    if grid:
        plt.grid()
    if not title == '':
        plt.title(title)
    if not xlabel == '':
        plt.xlabel(xlabel)
    if not ylabel == '':
        plt.ylabel(ylabel)
    return 0

def plotOnAxes(ax,X,Y,opt='',legend=''):
    if opt == '':
        if legend == '':
            ax.plot(X,Y)
        else:
            ax.plot(X,Y,label=legend)
    else:
        if legend == '':
            ax.plot(X,Y,opt)
        else:
            ax.plot(X,Y,opt,label=legend)
    return 0

def correctAxesExtend(ax,xmin='None',xmax='None',ymin='None',ymax='None'):
    if not xmin == 'None':
        ax.set_xlim(left=xmin)
    if not xmax == 'None':
        ax.set_xlim(right=xmax)
    if not ymin == 'None':
        ax.set_ylim(bottom=ymin)
    if not ymax == 'None':
        ax.set_ylim(top=ymax)
    return 0

def addLegend(legend=True):
    if legend:
        plt.legend(prop=dict(size=10),bbox_to_anchor=(0, 0, 1, 1), bbox_transform=plt.gcf().transFigure)

def saveMatrix(matrix, figname, clbar=True, 
               origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
               grid=False, title='', xlabel='', ylabel='',
               cmap=None, norm=None, aspect=None, interpolation=None, alpha=None, shape=None,
               filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None):
    plt.figure(1)
    plt.clf()
    if interpolation == None:
        interpolation = 'none'
    im1=plt.imshow(matrix, cmap=cmap, norm=norm, aspect=aspect, alpha=alpha, interpolation=interpolation,
                   vmin=vmin, vmax=vmax, origin=origin, extent=extent, shape=shape, filternorm=filternorm, filterrad=filterrad, imlim=imlim,
                   resample=resample, url=url)
    
    if clbar:
        plt.colorbar(im1)

    add_labels_title_grid(grid,title,xlabel,ylabel)
    plt.savefig(figname)
    print figname
    return 0

def saveMatrixContour(matrix, figname, clbar=True, fill=True, 
                      origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                      grid=False, title='', xlabel='', ylabel='',
                      cmap=None, norm=None, alpha=None,
                      levels=None, extend='neither',
                      colors=None, linewidths=None, linestyles=None, locator=None, antialiased=True):

    plt.figure(1)
    plt.clf()
    
    if fill:
        im = plt.contourf(matrix, levels=levels, vmin=vmin, vmax=vmax, origin=origin, extent=extent, extend=extend,
                          colors=colors, linewidths=linewidths, linestyles=linestyles, locator=locator, alpha=alpha,
                          cmap=cmap, norm=norm, antialiased=antialiased)
    else:
        im = plt.contour(matrix, levels=levels, vmin=vmin, vmax=vmax, origin=origin, extent=extent, extend=extend,
                         colors=colors, linewidths=linewidths, linestyles=linestyles, locator=locator, alpha=alpha,
                         cmap=cmap, norm=norm, antialiased=antialiased)

    if clbar:
        plt.colorbar(im)

    add_labels_title_grid(grid,title,xlabel,ylabel)
    plt.savefig(figname)
    print figname
    return 0

def plotMatrix(matrix, origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
               cmap=None, norm=None, aspect=None, interpolation=None, alpha=None, shape=None,
               filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None):
    
    if interpolation == None:
        interpolation = 'none'
    im1=plt.imshow(matrix, cmap=cmap, norm=norm, aspect=aspect, interpolation=interpolation, alpha=alpha,
                   vmin=vmin, vmax=vmax, origin=origin, extent=extent, shape=shape, filternorm=filternorm, filterrad=filterrad, imlim=imlim,
                   resample=resample, url=url)
    return im1

def contourMatrix(matrix, levels=None, vmin=None, vmax=None, origin='lower', extent=[0.,1.,0.,1.], extend='neither',
                  colors=None, linewidths=None, linestyles=None, locator=None, alpha=None, cmap=None, norm=None, antialiased=True):
    return plt.contour(matrix, levels=levels, vmin=vmin, vmax=vmax, origin=origin, extent=extent, extend=extend,
                       colors=colors, linewidths=linewidths, linestyles=linestyles, locator=locator, alpha=alpha,
                       cmap=cmap, norm=norm, antialiased=antialiased)

def contourfMatrix(matrix, levels=None, vmin=None, vmax=None, origin='lower', extent=[0.,1.,0.,1.], extend='neither',
                   colors=None, linewidths=None, linestyles=None, locator=None, alpha=None, cmap=None, norm=None, antialiased=True):
    return plt.contourf(matrix, levels=levels, vmin=vmin, vmax=vmax, origin=origin, extent=extent, extend=extend,
                        colors=colors, linewidths=linewidths, linestyles=linestyles, locator=locator, alpha=alpha,
                        cmap=cmap, norm=norm, antialiased=antialiased)

def plotMatrixOnAxes(matrix, ax, origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                     cmap=None, norm=None, aspect=None, interpolation=None, alpha=None, shape=None,
                     filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None):
    
    if interpolation == None:
        interpolation = 'none'
    return ax.imshow(matrix, cmap=cmap, norm=norm, aspect=aspect, interpolation=interpolation, alpha=alpha,
                     vmin=vmin, vmax=vmax, origin=origin, extent=extent, shape=shape, filternorm=filternorm, filterrad=filterrad, imlim=imlim,
                     resample=resample, url=url)


def contourMatrixOnAxes(matrix, ax, levels=None, vmin=None, vmax=None, origin='lower', extent=[0.,1.,0.,1.], extend='neither',
                        colors=None, linewidths=None, linestyles=None, locator=None, alpha=None, cmap=None, norm=None, antialiased=True):
    return ax.contour(matrix, levels=levels, vmin=vmin, vmax=vmax, origin=origin, extent=extent, extend=extend,
                      colors=colors, linewidths=linewidths, linestyles=linestyles, locator=locator, alpha=alpha,
                      cmap=cmap, norm=norm, antialiased=antialiased)

def contourfMatrixOnAxes(matrix, ax, levels=None, vmin=None, vmax=None, origin='lower', extent=[0.,1.,0.,1.], extend='neither',
                         colors=None, linewidths=None, linestyles=None, locator=None, alpha=None, cmap=None, norm=None, antialiased=True):
    return ax.contourf(matrix, levels=levels, vmin=vmin, vmax=vmax, origin=origin, extent=extent, extend=extend,
                        colors=colors, linewidths=linewidths, linestyles=linestyles, locator=locator, alpha=alpha,
                        cmap=cmap, norm=norm, antialiased=antialiased)

                  
