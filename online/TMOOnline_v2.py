# Standard Python imports
import psana
import numpy as np
import time
import sys

import os
import time

import analyses
import loop
import setup_v2 as setup
import plotting_v2 as plotting


def update(evt, detectors, analysis, plots, iread):
    for key in detectors.keys():
        detectors[key]['modified'] = False
        get = detectors[key]['get']
        if evt % detector['gatherEveryNthShot'] == 0:
            detectors[key]['shotData'] = get(detectors[key]['det'])(evt)
            detectors[key]['modified'] = True
        else:
            if 'shotData' not in detectors[key].keys():
                detectors[key][shotData] = None
        
    analysis.update(detectors)
    
    for key in plots.keys():
        plotting.plotElement( iread, key, plots[key], detectors, analysis )

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

def shmemReader(exp,run, detectors, analysisDict, nread=1000, loopStyle=defaultLoopStyle):
    if (exp is None) & (run is None):
        ds = psana.DataSource(shmem='tmo')
    else:
        ds=psana.DataSource(exp=exp, run=run) #psdm
    
    ########################################################################
    # loop over runs
    ########################################################################
    for run in ds.runs():
        detectorSetup(run, detectors)
        
        userAnalysis = analyses.analyses( analysisDict, nread )
        
        iread = 0
        for nevt, evt in enumerate(loopStyle(run.events())): #loop over events
            update(evt, detectors, userAnalysis, iread)
            
            iread += 1
            if iread >= nread:
                break
                      
    return None
