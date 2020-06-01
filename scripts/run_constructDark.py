#!/usr/bin/env python
import os
import subprocess
import lsst_camera.cp_pipe_drivers as cpd

repo = '/lsstdata/offline/teststand/BOT/gen2repo'

imageType = 'DARK'
raftName = 'R22'
run = '6813D'
selection = (f'imageType=="{imageType}" and run=="{run}" '
             f'and raftName="{raftName}"')

visit_dict = cpd.VisitDict(repo, selection)

visit_list = '^'.join([str(_) for _ in sorted(list(visit_dict.keys()))])

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
