# Standard Python imports
import psana
import numpy as np
import time
import sys

import analyses
import loop

def getEpics(run):
    epicsNames = []
    for key in run.epicsinfo:
        epicsNames.append( key[0] )
    return epicsNames

def makeEpicsDetectorDictionary(run):
    epicsNames = getEpics(run)
    detectors = {}
    for name in epicsNames:
        detectors[name] = {'pskey':name, 'get':lambda det: det}
    return detectors

def makeEpicsAnalysisDictionary(run):
    epicsNames = getEpics(run)
    analysis = {}
    for name in epicsNames:
        analysis[name] = {'function':lambda x: x, 'detectorKey':name}
    return analysis

def update(evt, detectors, analysis):
    for key in detectors.keys():
        get = detectors[key]['get']
        detectors[key]['shotData'] = get(detectors[key]['det'])(evt)

    analysis.update(detectors)

def detectorSetup(run, detectors):
    pskeys = set([detectors[key]['pskey'] for key in detectors.keys()])
    psDetectors = {}
    for pskey in pskeys:
        try:
            psDetectors[pskey] = run.Detector(pskey)
        except psana.psexp.run.DetectorNameError as de:
            print('%s is not implemented, dropping' % pskey)
            psDetectors[pskey] = None

    for key in detectors.keys():
        if psDetectors[detectors[key]['pskey']] is not None:
            detectors[key]['det'] = psDetectors[detectors[key]['pskey']]
        else:
            detectors[key]['get'] = lambda x: lambda y: 0
            detectors[key]['det'] = None


defaultLoopStyle = lambda iterator: loop.timeIt(iterator, printEverySec=10)

def XTCReader(exp,run, detectors, analysisDict, nread=1000, loopStyle=defaultLoopStyle):
    ds=psana.DataSource(exp=exp, run=run) #psdm
    
    ########################################################################
    # loop over runs
    ########################################################################
    for run in ds.runs():
        detectorSetup(run, detectors)
        theAnalysis = analyses.analyses( analysisDict, nread )
    
        epics = makeEpicsDetectorDictionary(run)
        epicsAnalysisDict = makeEpicsAnalysisDictionary(run)
        epicsAnalysis = analyses.analyses( epicsAnalysisDict, nread, printMode='quiet' )
        detectorSetup(run, epics)
        
        iread = 0
        for nevt, evt in enumerate(loopStyle(run.events())): #loop over events
            update(evt, detectors, theAnalysis)
            update(evt, epics, epicsAnalysis)
            
            iread += 1
            if iread >= nread:
                break
                      
    return theAnalysis.data, epicsAnalysis.data
