#!/usr/bin/env python
import os
import subprocess
import lsst_camera.cp_pipe_drivers as cpd

repo = '/lsstdata/offline/teststand/BOT/gen2repo'

imageType = 'BIAS'
raftName = 'R22'
run = '6813D'
selection = (f'imageType=="{imageType}" and run=="{run}" '
             f'and raftName="{raftName}"')

visit_dict = cpd.VisitDict(repo, selection)

visits = sorted(list(visit_dict.keys()))
visit_list = '^'.join([str(_) for _ in (visits[11:20] + visits[33:42]
                                        + visits[53:62])])

outdir = 'calib_products'
try:
    cpd.setup_output_dir(repo, outdir)
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
