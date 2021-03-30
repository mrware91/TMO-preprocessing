import numpy as np
import psmon.plots
import psmon.publish

def plotImage(nevt, plotName, plotTitle, im,aspect_ratio=1,**kwargs):
    print('?')
    aplot = psmon.plots.Image(nevt, plotTitle, im, aspect_ratio=aspect_ratio)
    psmon.publish.send(plotName, aplot)
    return None

def plotXY(nevt, plotName, x,y, plotTitle='', xlabel='x',ylabel='y',formats='-',**kwargs):
    print('?')
    x=np.array(x).astype(float)
    y=np.array(y).astype(float)
    idx = (~np.isnan(x))&(~np.isnan(y))
    aplot = psmon.plots.XYPlot(nevt, plotTitle,
                               x[idx], y[idx],
                               xlabel=xlabel,
                               ylabel=ylabel,
                               formats=formats)
    psmon.publish.send(plotName, aplot)
    
def plotHist(nevt, plotName, x,y, plotTitle='',xlabel='x',ylabel='y',formats='-',fills=True,**kwargs):
    aplot = psmon.plots.Hist(nevt, plotTitle,
                               x, y,
                               xlabel=xlabel,
                               ylabel=ylabel,
                               formats=formats,fills=fills)
    psmon.publish.send(plotName, aplot)

def plotElement( nevent, name, plotDictionary, detectors, analysis ):
    plotTitle = name
    if plotDictionary['dataSource'] == 'detectors':
        dataSource = detectors
    else:
        dataSource = analysis
        
    
    if plotDictionary['type'] == 'XY':
        print(dataSource.keys())
        x = plotDictionary['xfunc'](dataSource)
        y = plotDictionary['yfunc'](dataSource)
        plotXY( nevent, name, x, y, plotTitle=name, **plotDictionary )
    elif plotDictionary['type'] == 'Image':
        im = plotDictionary['imageFunc'](dataSource)
        modified = plotDictionary['modifiedFunc'](dataSource)
        if not modified:
            return
        plotImage( nevent, name, name, im, **plotDictionary )
        
    elif plotDictionary['type'] == 'Histogram':
        x = plotDictionary['xfunc'](dataSource)
        y = plotDictionary['yfunc'](dataSource)
        plotHist( nevent, name, x,y, plotTitle = name, **plotDictionary )