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

def saveMatrixImshow(matrix, figname, clbar=True, 
                     origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                     grid=False, title='', xlabel='', ylabel='',
                     cmap=None, norm=None, aspect=None, interpolation=None, alpha=1., shape=None,
                     filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None):
    plt.figure(1)
    plt.clf()
    #if interpolation == None:
    #    interpolation = 'none'
    im1=plt.imshow(matrix, cmap=cmap, norm=norm, aspect=aspect, alpha=alpha, interpolation=interpolation,
                   vmin=vmin, vmax=vmax, origin=origin, extent=extent, shape=shape, filternorm=filternorm, filterrad=filterrad, imlim=imlim,
                   resample=resample)#, url=url)
    
    if clbar:
        plt.colorbar(im1)

    addLabelsTitleGrid(grid,title,xlabel,ylabel)
    plt.savefig(figname)
    print figname
    return 0

def saveMatrixContour(matrix, figname, clbar=True, fill=True, 
                      origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                      grid=False, title='', xlabel='', ylabel='',
                      cmap=None, norm=None, alpha=1.,
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

    addLabelsTitleGrid(grid,title,xlabel,ylabel)
    plt.savefig(figname)
    print figname
    return 0

def imshowMatrix(matrix, origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                 cmap=None, norm=None, aspect=None, interpolation=None, alpha=1., shape=None,
                 filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None):
    
    if interpolation == None:
        interpolation = 'none'
    im1=plt.imshow(matrix, cmap=cmap, norm=norm, aspect=aspect, interpolation=interpolation, alpha=alpha,
                   vmin=vmin, vmax=vmax, origin=origin, extent=extent, shape=shape, filternorm=filternorm, filterrad=filterrad, imlim=imlim,
                   resample=resample)#, url=url)
    return im1

def contourMatrix(matrix, levels=None, vmin=None, vmax=None, origin='lower', extent=[0.,1.,0.,1.], extend='neither',
                  colors=None, linewidths=None, linestyles=None, locator=None, alpha=1., cmap=None, norm=None, antialiased=True):
    return plt.contour(matrix, levels=levels, vmin=vmin, vmax=vmax, origin=origin, extent=extent, extend=extend,
                       colors=colors, linewidths=linewidths, linestyles=linestyles, locator=locator, alpha=alpha,
                       cmap=cmap, norm=norm, antialiased=antialiased)

def contourfMatrix(matrix, levels=None, vmin=None, vmax=None, origin='lower', extent=[0.,1.,0.,1.], extend='neither',
                   colors=None, linewidths=None, linestyles=None, locator=None, alpha=1., cmap=None, norm=None, antialiased=True):
    return plt.contourf(matrix, levels=levels, vmin=vmin, vmax=vmax, origin=origin, extent=extent, extend=extend,
                        colors=colors, linewidths=linewidths, linestyles=linestyles, locator=locator, alpha=alpha,
                        cmap=cmap, norm=norm, antialiased=antialiased)

def imshowMatrixOnAxes(matrix, ax, origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None,
                       cmap=None, norm=None, aspect=None, interpolation=None, alpha=1., shape=None,
                       filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None):
    
    #if interpolation == None:
    #    interpolation = 'none'
    return ax.imshow(matrix, cmap=cmap, norm=norm, aspect=aspect, interpolation=interpolation, alpha=alpha,
                     vmin=vmin, vmax=vmax, origin=origin, extent=extent, shape=shape, filternorm=filternorm, filterrad=filterrad, imlim=imlim,
                     resample=resample)#, url=url)


def contourMatrixOnAxes(matrix, ax, levels=None, vmin=None, vmax=None, origin='lower', extent=[0.,1.,0.,1.], extend='neither',
                        colors=None, linewidths=None, linestyles=None, locator=None, alpha=1., cmap=None, norm=None, antialiased=True):
    return ax.contour(matrix, levels=levels, vmin=vmin, vmax=vmax, origin=origin, extent=extent, extend=extend,
                      colors=colors, linewidths=linewidths, linestyles=linestyles, locator=locator, alpha=alpha,
                      cmap=cmap, norm=norm, antialiased=antialiased)

def contourfMatrixOnAxes(matrix, ax, levels=None, vmin=None, vmax=None, origin='lower', extent=[0.,1.,0.,1.], extend='neither',
                         colors=None, linewidths=None, linestyles=None, locator=None, alpha=1., cmap=None, norm=None, antialiased=True):
    return ax.contourf(matrix, levels=levels, vmin=vmin, vmax=vmax, origin=origin, extent=extent, extend=extend,
                        colors=colors, linewidths=linewidths, linestyles=linestyles, locator=locator, alpha=alpha,
                        cmap=cmap, norm=norm, antialiased=antialiased)

                  
def plotMatrixOnAxes(matrix, ax, plotter='imshow', origin='lower', extent=[0.,1.,0.,1.], vmin=None, vmax=None, interpolation='nearest'):
    if plotter == 'imshow':
        return imshowMatrixOnAxes(matrix, ax, origin=origin, extent=extent, vmin=vmin, vmax=vmax, interpolation=interpolation)
    elif plotter == 'contour':
        return contourMatrixOnAxes(matrix, ax, vmin=vmin, vmax=vmax, origin=origin, extent=extent)
    elif plotter == 'contourf':
        return contourfMatrixOnAxes(matrix, ax, vmin=vmin, vmax=vmax, origin=origin, extent=extent)

def trySaveMatrixPDF(matrix, figname, plotter='imshow', title='', xlabel='', ylabel='', interpolation='nearest'):
    if plotter == 'imshow':
        try:
            return saveMatrixImshow(matrix, figname+'.pdf', title=title, xlabel=xlabel, ylabel=ylabel, interpolation=interpolation)
        except:
            return saveMatrixImshow(matrix, figname+'.png', title=title, xlabel=xlabel, ylabel=ylabel, interpolation=interpolation)
    elif plotter == 'contour':
        try:
            return saveMatrixContour(matrix, figname+'.pdf', fill=False, title=title, xlabel=xlabel, ylabel=ylabel)
        except:
            return saveMatrixContour(matrix, figname+'.png', fill=False, title=title, xlabel=xlabel, ylabel=ylabel)

    elif plotter == 'contourf':
        try:
            return saveMatrixContour(matrix, figname+'.pdf', title=title, xlabel=xlabel, ylabel=ylabel)
        except:
            return saveMatrixContour(matrix, figname+'.png', title=title, xlabel=xlabel, ylabel=ylabel)
