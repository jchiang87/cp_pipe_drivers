from collections import defaultdict
import subprocess
import lsst_camera.cp_pipe_drivers as cpd

repo = '/lsstdata/offline/teststand/BOT/gen2repo'

run = '6790D'
imageType = 'FLAT'
raftName = 'R22'
selection = (f'imageType=="{imageType}" and run=="{run}" '
             f'and raftName="{raftName}"')

visit_dict = cpd.VisitDict(repo, selection)

visits = sorted(list(visit_dict.keys()))
visit_pairs = defaultdict(list)
for visit in visits:
    my_df = visit_dict.df.query(f'visit=={visit}') 
    if len(my_df) == 9:
        row = my_df.query(f'detectorName=="S00"').iloc[0]
        visit_pairs[(row['filter'], row.expTime)].append(row.visit)

visit_pair_list = []
for items in visit_pairs.values():
    if len(items) != 2:
        continue
    visit_pair_list.append(','.join([str(_) for _ in items]))
visit_pair_list = sorted(visit_pair_list)

visit_list = ' '.join(visit_pair_list[::4])

outdir = 'calib_products'

rerun_folder = 'ptcs'

command = (f'measurePhotonTransferCurve.py {outdir} --rerun {rerun_folder} '
           f'--longlog --id raftName={raftName} '
           f'--visit-pairs {visit_list} '
           '--config isr.doCrosstalk=False --clobber-config --calib CALIB')
print(command)
subprocess.check_call(command, shell=True)
