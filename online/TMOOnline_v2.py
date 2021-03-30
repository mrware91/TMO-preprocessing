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
        try:
            retrieveData = (iread % detectors[key]['gatherEveryNthShot'] == 0)
        except KeyError as ke:
            if 'gatherEveryNthShot' in str(ke):
                retrieveData = True
            else:
                raise ke
        if retrieveData:
            detectors[key]['shotData'] = get(detectors[key]['det'])(evt)
            detectors[key]['modified'] = True
        else:
            if 'shotData' not in detectors[key].keys():
                detectors[key][shotData] = None
        
    analysis.update(detectors)
    
    for key in plots.keys():
        plotting.plotElement( iread, key, plots[key], detectors, analysis.data )

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

def shmemReader(exp,run, detectors, analysisDict, plots, nread=1000, loopStyle=defaultLoopStyle):
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
            update(evt, detectors, userAnalysis, plots, iread)
            
            iread += 1
                      
    return None


if __name__ == "__main__":
    print(sys.argv)
    try:
        exp=str(sys.argv[1])
        run=int(sys.argv[2])
        nevt=int(sys.argv[3])
        runType='offline'
    except IndexError as ie:
        print(ie)
        if sys.argv[1] == 'shmem':
            nevt=int(sys.argv[2])
            runType='shmem'
        else:
            print('incorrect input')
            print('provide python TMOOnline.py exp run nevent or ...')
            print('python TMOOnline.py shmem nevent')
            exit
            
    if runType == 'shmem':
        shmemReader(None,None, setup.detectors, setup.analysis, setup.plots, nread=nevt, loopStyle=defaultLoopStyle)
    else:
        shmemReader(exp,run, setup.detectors, setup.analysis, setup.plots, nread=nevt, loopStyle=defaultLoopStyle)
        
        