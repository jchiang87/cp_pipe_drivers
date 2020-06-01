from collections import defaultdict
import numpy as np
import pandas as pd
import lsst.log
import lsst.daf.persistence as dp
import lsst_camera.cp_pipe_drivers as cpd

lsst.log.setLevel('CameraMapper', lsst.log.ERROR)
lsst.log.setLevel('LsstCamMapper', lsst.log.ERROR)
lsst.log.setLevel('LsstCamAssembler', lsst.log.ERROR)

repo = '/lsstdata/offline/teststand/BOT/gen2repo'
butler = dp.Butler(repo)

dataId = dict(run='6813D', imageType='DARK', raftName='R22')

df = cpd.get_raw_amp_stats(butler, dataId)
df.to_pickle('amp_stats_%(imageType)s_%(raftName)s_%(run)s.pkl' % dataId)
