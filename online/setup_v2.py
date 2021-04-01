import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# detectors['sample']={'pskey':'timing', 'get':lambda det: det}

# Analysis is of form {analysisKey: {'function': analysisFunction(), 'detectorKey': 'key', 'analyzeEvery':1}}
# Function element is optional. If not provided, raw data is returned.

###############################################################
### Specify detectors
###############################################################

detectors = {}
analysis = {}
plots = {}
# Fast detectors
# detectors['evrs'] = {'pskey':'timing', 'get':lambda det: det.raw.eventcodes}
# detectors['tmo_atmopal']={'pskey':'tmo_atmopal', 'get':lambda det: det.raw.image, 'gatherEveryNthShot':10}
# detectors['vls']={'pskey':'andor', 'get':lambda det: det.raw.value}
# detectors['gmd']={'pskey':'gmd', 'get':lambda det: det.raw.energy}
# detectors['hsd']={'pskey':'hsd', 'get':lambda det: det.raw.waveforms, 'gatherEveryNthShot':10}
# detectors['photonEnergy']={'pskey':'ebeam', 'get':lambda det: det.raw.ebeamPhotonEnergy}

# # Important Epics
# detectors['vitaraDelay']={'pskey':'las_fs14_target_time', 'get':lambda det: det}

###############################################################
### Evrs Histogram
###############################################################



# detectors['evrs'] = {'pskey':'timing', 'get':lambda det: det.raw.eventcodes}

# def evrsHistogram(dets, data, redfac=.9):
#     if dets['evrs'] is None:
#         return data
        
#     if data is None:
#         data={}
#         data['count'] = 1
#         data['evrsum'] = np.copy(dets['evrs'])
#     else:
#         data['count'] = data['count']*redfac + 1
#         data['evrsum'] = data['evrsum']*redfac + dets['evrs']
        
#     return data
        
# analysis['evrsHistogram'] = {'update': evrsHistogram,'data':None,'updateEveryNthShot':1}

# def xfuncEvrsHistogram(data):
#     NC,NH = data['evrsHistogram_evrsum'].shape
#     return np.arange(NH+1)
    
# def yfuncEvrsHistogram(data):
#     sumHist = np.nansum(data['evrsHistogram_evrsum'],0)
#     sumCount = np.nansum(data['evrsHistogram_count'],0)
#     if sumCount == 0:
#         sumCount = 1
#     return sumHist/sumCount

# plots['evrsHistogram'] = {
#     'type':'Histogram',
#     'dataSource':'analysis',
#     'xfunc': xfuncEvrsHistogram,
#     'yfunc': yfuncEvrsHistogram,
#     'xlabel': 'evr',
#     'ylabel':'counts'
# }

# analysis['photonEnergy'] = {'detectorKey':'photonEnergy'}

###############################################################
### pulseEnergy plots
###############################################################

detectors['gmd']={'pskey':'gmd', 'get':lambda det: det.raw.energy}
detectors['timestamp'] = {'pskey':'timing', 'get': lambda det: lambda evt: evt.timestamp}

def pulseEnergy(dets, data, nsave= int(3600 / (size-3)) ):
    pulseEnergy = dets['gmd']
    timestamp = dets['timestamp']
    if (pulseEnergy is None) | (timestamp is None):
        return data
        
    if data is None:
        data={}
        data['pulseEnergy'] = np.zeros(nsave)*np.nan
        data['num'] = 0
        data['timestamps'] = np.zeros(nsave)*np.nan
    
    data['pulseEnergy'][data['num']%nsave] = pulseEnergy
    data['timestamps'][data['num']%nsave] = timestamp
    
    data['num']+=1
        
    return data

analysis['pulseEnergy'] = {'update': pulseEnergy,'data':None}

def timestampFormat(ts):
    # print(ts.size, np.unique(ts).size)
    # return np.argsort(ts)
    return (ts-np.nanmin(ts))*1e-9

plots['pulseEnergy'] = {
    'type':'XY',
    'xfunc': lambda data: timestampFormat(data['pulseEnergy_timestamps'][:]),
    'yfunc': lambda data: data['pulseEnergy_pulseEnergy'][:],
    'xlabel': 'timestamps',
    'ylabel':'Pulse Energy (mJ)','formats':'.'
}


###############################################################
### hsd plots
###############################################################
# detectors['hsd']={'pskey':'hsd', 'get':lambda det: det.raw.waveforms, 'gatherEveryNthShot':10}

# resample = lambda x, rebin_factor: x.reshape(-1, rebin_factor).mean(1)

# def hsdFunc(dets, data, nsave=int(100/(size-3)), redfac=0.9 ):
#     hsd = dets['hsd']
    
#     if (hsd is None):
#         return data
        
#     try:
#         hsd.keys()
#     except AttributeError as ae:
#         if 'float' in str(ae):
#             return data
#         else:
#             raise ae
        
#     itofWaveform = resample(hsd[0][0],10)
#     diodeWaveform = resample(hsd[9][0][:5000],10)
        
#     if data is None:
#         data={}
#         data['diodeTime'] = resample(hsd[9]['times'][:5000],10)
#         data['itofTime'] = resample(hsd[0]['times'],10)
#         data['num'] = 0
        
#         idims = np.shape(itofWaveform)
#         ddims = np.shape(diodeWaveform)
#         data['itofSS'] = np.zeros((*idims))
#         data['diodeSS'] = np.zeros((*ddims))
#         data['itofAvg'] = np.zeros((*idims))
#         data['diodeAvg'] = np.zeros((*ddims))
#         # data['itofWaveforms'] = np.zeros((nsave,*idims))*np.nan
#         # data['diodeWaveforms'] = np.zeros((nsave,*ddims))*np.nan
    
#     # data['itofWaveforms'][data['num']%nsave,] = itofWaveform
#     # data['diodeWaveforms'][data['num']%nsave,] = diodeWaveform
    
    
#     data['itofSS'] = itofWaveform
#     data['diodeSS'] = diodeWaveform
#     data['itofAvg'] = itofWaveform + redfac * data['itofAvg']
#     data['diodeAvg'] = diodeWaveform + redfac * data['diodeAvg']
    
#     data['num'] = 1 + redfac*data['num']
        
#     return data

# analysis['hsd'] = {'update': hsdFunc,'data':None}

# plots['diodeSS'] = {
#     'type':'XY',
#     'xfunc': lambda data: data['hsd_diodeTime'][0,:],
#     'yfunc': lambda data: data['hsd_diodeSS'][0,:],
#     'xlabel': 'Time (us)',
#     'ylabel':'Waveform (arb)','formats':'-'
# }

# plots['diodeAvg'] = {
#     'type':'XY',
#     'xfunc': lambda data: data['hsd_diodeTime'][0,:],
#     'yfunc': lambda data: np.nansum(data['hsd_diodeAvg'],0)/np.nansum(data['hsd_num'],0),
#     'xlabel': 'Time (us)',
#     'ylabel':'Waveform (arb)','formats':'-'
# }

# plots['itofSS'] = {
#     'type':'XY',
#     'xfunc': lambda data: data['hsd_itofTime'][0,:],
#     'yfunc': lambda data: data['hsd_itofSS'][0,:],
#     'xlabel': 'Time (us)',
#     'ylabel':'Waveform (arb)','formats':'-'
# }

# plots['itofAvg'] = {
#     'type':'XY',
#     'xfunc': lambda data: data['hsd_itofTime'][0,:],
#     'yfunc': lambda data: np.nansum(data['hsd_itofAvg'],0)/np.nansum(data['hsd_num'],0),
#     'xlabel': 'Time (us)',
#     'ylabel':'Waveform (arb)','formats':'-'
# }



###############################################################
### timetool 2D plots
###############################################################
# detectors['tmo_atmopal']={'pskey':'tmo_atmopal', 'get':lambda det: det.raw.image, 'gatherEveryNthShot':1}
# detectors['evrs'] = {'pskey':'timing', 'get':lambda det: det.raw.eventcodes}
# def ttFunc(dets, data, redfac=0.9 ):
#     evrs = dets['evrs']
#     ttimg = dets['tmo_atmopal']
    
#     if (ttimg is None) | (evrs is None):
#         return data
        
#     if data is None:
#         data={}
#         data['num'] = 0
        
#         ddims = np.shape(ttimg)
#         data['SS'] = np.zeros_like(ttimg)
#         data['Avg'] = np.zeros_like(ttimg)
    
    
#     data['SS'] = ttimg
#     data['Avg'] = ttimg + redfac * data['Avg']
    
#     data['num'] = 1 + redfac*data['num']
        
#     return data

# analysis['tt'] = {'update': ttFunc,'data':None, 'post2MasterEveryNthShot':100}

# plots['ttSS'] = {
#     'type':'Image',
#     'imageFunc': lambda data: data['tt_SS'][0,:],
#     'plotEveryNthSec':1
# }

# plots['ttAvg'] = {
#     'type':'Image',
#     'imageFunc': lambda data: np.nansum(data['tt_Avg'],0)/np.nansum(data['tt_num'],0),
#     'plotEveryNthSec':1
# }


###############################################################
### timetool 1D plots
###############################################################
# detectors['tmo_atmopal']={'pskey':'tmo_atmopal', 'get':lambda det: det.raw.image, 'gatherEveryNthShot':1}
# detectors['evrs'] = {'pskey':'timing', 'get':lambda det: det.raw.eventcodes}
# def tt1dFunc(dets, data, redfac=0.9 ):
#     evrs = np.array(dets['evrs'],dtype=bool)
#     ttimg = dets['tmo_atmopal']
    
#     if (ttimg is None) | (evrs is None) | (np.nanmedian(ttimg[:]) < -40):
#         return data
        
#     xrayOff= evrs[161]
#     tt1d = np.sum(ttimg[360:500,:],0)
#     if data is None:
#         data={}
#         data['num'] = 0
        
#         ddims = np.shape(ttimg)
#         data['SS'] = np.zeros_like(tt1d)*np.nan
#         data['AvgBG'] = np.zeros_like(tt1d)*np.nan
    
#     if ~xrayOff:
#         data['SS'] = tt1d
    
#     else:
#         if data['num'] == 0:
#             data['AvgBG'] = tt1d
#         else:
#             data['AvgBG'] = tt1d + redfac * data['AvgBG']
#         data['num'] = 1 + redfac*data['num']
        
#     return data

# analysis['tt1d'] = {'update': tt1dFunc,'data':None, 'post2MasterEveryNthShot':1}

# def yfuncttSSdiv(data):
#     if np.nansum(data['tt1d_num'],0) <= 0:
#         return np.zeros_like(data['tt1d_SS'][0,:])
#     else:
#         y=data['tt1d_SS'][0,:]/(np.nansum(data['tt1d_AvgBG'],0)/np.nansum(data['tt1d_num'],0))
#         return y/y[0]

# plots['ttSSdiv'] = {
#     'type':'XY',
#     'xfunc': lambda data: np.arange(data['tt1d_SS'][0,:].size),
#     'yfunc': yfuncttSSdiv,
#     'plotEveryNthSec':.5
# }

# def yfuncttavgBG(data):
#     if np.nansum(data['tt1d_num'],0) <= 0:
#         return np.zeros_like(data['tt1d_SS'][0,:])
#     else:
#         return np.nansum(data['tt1d_AvgBG'],0)/np.nansum(data['tt1d_num'],0)

# plots['ttAvgBG'] = {
#     'type':'XY',
#     'xfunc': lambda data: np.arange(data['tt1d_SS'][0,:].size),
#     'yfunc': yfuncttavgBG,
#     'plotEveryNthSec':.5
# }




###############################################################
### hsd plots
###############################################################
detectors['hsd']={'pskey':'hsd', 'get':lambda det: det.raw.waveforms, 'gatherEveryNthShot':10}

resample = lambda x, rebin_factor: x.reshape(-1, rebin_factor).mean(1)

def hsdFunc(dets, data, nsave=int(100/(size-3)), redfac=0.9 ):
    hsd = dets['hsd']
    
    if (hsd is None):
        return data
        
    try:
        hsd.keys()
    except AttributeError as ae:
        if 'float' in str(ae):
            return data
        else:
            raise ae
        
    tofWaveform = resample(hsd[0][0],10)
        
    if data is None:
        data={}
        data['tofTime'] = resample(hsd[0]['times'],10)
        data['num'] = 0
        
        idims = np.shape(tofWaveform)
        data['tofSS'] = np.zeros((*idims))
        data['tofAvg'] = np.zeros((*idims))
        # data['itofWaveforms'] = np.zeros((nsave,*idims))*np.nan
        # data['diodeWaveforms'] = np.zeros((nsave,*ddims))*np.nan
    
    # data['itofWaveforms'][data['num']%nsave,] = itofWaveform
    # data['diodeWaveforms'][data['num']%nsave,] = diodeWaveform
    
    
    data['tofSS'] = tofWaveform
    data['tofAvg'] = tofWaveform + redfac * data['tofAvg']
    
    data['num'] = 1 + redfac*data['num']
        
    return data

analysis['hsd'] = {'update': hsdFunc,'data':None}

plots['tofSS'] = {
    'type':'XY',
    'xfunc': lambda data: data['hsd_tofTime'][0,:],
    'yfunc': lambda data: data['hsd_tofSS'][0,:],
    'xlabel': 'Time (us)',
    'ylabel':'Waveform (arb)','formats':'-'
}

plots['tofAvg'] = {
    'type':'XY',
    'xfunc': lambda data: data['hsd_tofTime'][0,:],
    'yfunc': lambda data: np.nansum(data['hsd_tofAvg'],0)/np.nansum(data['hsd_num'],0),
    'xlabel': 'Time (us)',
    'ylabel':'Waveform (arb)','formats':'-'
}
