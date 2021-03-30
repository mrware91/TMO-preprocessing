import numpy as np

###############################################################
### Specify detectors
###############################################################

detectors = {}
# Fast detectors
# detectors['sample']={'pskey':'timing', 'get':lambda det: det}
detectors['evrs'] = {'pskey':'timing', 'get':lambda det: det.raw.eventcodes}
detectors['tmo_atmopal']={'pskey':'tmo_atmopal', 'get':lambda det: det.raw.image, 'gatherEveryNthShot':10}
detectors['vls']={'pskey':'andor', 'get':lambda det: det.raw.value}
detectors['gmd']={'pskey':'gmd', 'get':lambda det: det.raw.energy}
detectors['hsd']={'pskey':'hsd', 'get':lambda det: det.raw.waveforms, 'gatherEveryNthShot':10}
detectors['photonEnergy']={'pskey':'ebeam', 'get':lambda det: det.raw.ebeamPhotonEnergy}

# Important Epics
detectors['vitaraDelay']={'pskey':'las_fs14_target_time', 'get':lambda det: det}

###############################################################
### Specify analyses to perform and write to small data
###############################################################

# Analysis is of form {analysisKey: {'function': analysisFunction(), 'detectorKey': 'key', 'analyzeEvery':1}}
# Function element is optional. If not provided, raw data is returned.
analysis = {}
analysis['evrs'] = {'detectorKey':'evrs'}
analysis['pulseEnergy'] = {'detectorKey':'gmd'}
analysis['photonEnergy'] = {'detectorKey':'photonEnergy'}

###############################################################
### Specify plots to display
###############################################################
plots = {}
plots['pulseEnergyVlabtime'] = {
    'type':'XY',
    'dataSource':'analysis',
    'xfunc': lambda data: np.arange(data['pulseEnergy'].size),
    'yfunc': lambda data: data['pulseEnergy'],
    'xlabel': 'idx',
    'ylabel':'pulse energy (mJ)'
}
                                
plots['timetool'] = {
    'type':'Image',
    'dataSource':'detectors',
    'modifiedFunc': lambda data: data['tmo_atmopal']['modified'],
    'imageFunc': lambda data: data['tmo_atmopal']['shotData']
}