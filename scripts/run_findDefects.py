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

rerun_folder = 'defects'

command = (f'findDefects.py {outdir} --rerun {rerun_folder} --longlog '
           f'--id raftName={raftName} '
           f'--visitList {visit_list} '
           '--clobber-config --calib CALIB')
print(command)
subprocess.check_call(command, shell=True)
