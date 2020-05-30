import os

__all__ = ['setup_output_dir']

def setup_output_dir(root_repo, output_dir):
    with open(os.path.join(root_repo, '_mapper')) as fd:
        mapper = fd.readline().strip()

    os.makedirs(output_dir, exist_ok=False)

    repository_cfg = os.path.join(output_dir, 'repositoryCfg.yaml')
    with open(repository_cfg, 'w') as output:
        output.write(f'''!RepositoryCfg_v1
_mapper: &id001 !!python/name:{mapper} ''
_mapperArgs: {}
_parents:
- !RepositoryCfg_v1
  _mapper: *id001
  _mapperArgs: {}
  _parents: []
  _policy: null
  _root: {root_repo}
  dirty: true
_policy: null
_root: null
dirty: true
''')
