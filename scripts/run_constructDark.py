#!/usr/bin/env python
import os
import subprocess
from lsst_camera.cp_pipe_drivers import VisitSelector

repo = '/lsstdata/offline/teststand/BOT/gen2repo'

imageType = 'DARK'
raftName = 'R22'
expTime = 17
selection = (f'imageType=="{imageType}" and expTime=={expTime} '
             f'and raftName="{raftName}"')

visit_selector = VisitSelector(repo, selection)

visit_list = '^'.join([str(_) for _ in visit_selector(num_ccds=9)][:3])

outdir = 'calib_products'

rerun_folder = 'dark_calibs'

command = (f'constructDark.py {outdir} --rerun {rerun_folder} --longlog --id '
           f'raftName={raftName} visit={visit_list} --batch-type none '
           '--config isr.doCrosstalk=False --clobber-config --calib CALIB')
print(command)
subprocess.check_call(command, shell=True)

rerun_path = os.path.join(outdir, 'rerun', rerun_folder)
file_pattern = os.path.join(rerun_path, 'dark', '*', 'dark-*')
command = (f'ingestCalibs.py {rerun_path} --output CALIB --validity 4000 '
           f'{file_pattern} --mode copy')
print(command)
subprocess.check_call(command, shell=True)
