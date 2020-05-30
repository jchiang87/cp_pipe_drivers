import os
import sqlite3
import pandas as pd

__all__ = ['VisitSelector']

class VisitSelector:
    def __init__(self, repo, selection=None):
        registry_file = os.path.join(repo, 'registry.sqlite3')
        assert(os.path.isfile(registry_file))
        query = 'select * from raw'
        if selection is not None:
            query += f' where {selection}'
        with sqlite3.connect(registry_file) as conn:
            self.df = pd.read_sql(query, conn)

    def __call__(self, num_ccds=None, selection=None):
        if num_ccds is None:
            return sorted(list(set(self.df['visit'])))
        visits = []
        for visit in set(self.df['visit']):
            query = f'visit=={visit}'
            if selection is not None:
                query = ' and '.join((query, f'({selection})'))
            if len(self.df.query(query) == num_ccds):
                visits.append(visit)
        return sorted(visits)
