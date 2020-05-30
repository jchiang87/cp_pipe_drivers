#!/usr/bin/env python
import os
import subprocess
from lsst_camera.cp_pipe_drivers import VisitSelector, setup_output_dir

repo = '/lsstdata/offline/teststand/BOT/gen2repo'

imageType = 'BIAS'
raftName = 'R22'
run = '6790D'
selection = (f'imageType=="{imageType}" and run=="{run}" '
             f'and raftName="{raftName}"')

visit_selector = VisitSelector(repo, selection)

visit_list = '^'.join([str(_) for _ in visit_selector(num_ccds=9)][:3])

outdir = 'calib_products'
try:
    setup_output_dir(repo, outdir)
except OSError:
    pass

rerun_folder = 'bias_calibs'

command = (f'constructBias.py {outdir} --rerun {rerun_folder} --longlog --id '
           f'raftName={raftName} visit={visit_list} --batch-type none '
           '--config isr.doCrosstalk=False --clobber-config')
print(command)
subprocess.check_call(command, shell=True)

rerun_path = os.path.join(outdir, 'rerun', rerun_folder)
file_pattern = os.path.join(rerun_path, 'bias', '*', 'bias-*')
command = (f'ingestCalibs.py {rerun_path} --output CALIB --validity 4000 '
           f'{file_pattern} --mode copy')
print(command)
subprocess.check_call(command, shell=True)
