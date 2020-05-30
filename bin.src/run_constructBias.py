#!/usr/bin/env python
import subprocess
from lsst_camera.cp_pipe_drivers import VisitSelector, setup_output_dir

repo = '/lsstdata/offline/teststand/BOT/gen2repo'

imageType = 'BIAS'
run = '6790D'
raftName = 'R22'
selection = (f'imageType=="{imageType}" and run=="{run}" '
             f'and raftName="{raftName}"')

visit_selector = VisitSelector(repo, selection)

visit_list = '^'.join([str(_) for _ in visit_selector(num_ccds=9)][:20])

outdir = 'calib_products'
try:
    setup_output_dir(repo, outdir)
except OSError:
    pass

command = (f'constructBias.py {outdir} --rerun bias --longlog --id '
           f'raftName={raftName} visit={visit_list} --batch-type none '
           '--config isr.doCrosstalk=False --clobber-config')
print(command)
subprocess.check_call(command, shell=True)
