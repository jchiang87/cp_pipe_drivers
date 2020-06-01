import os
import sqlite3
import pandas as pd

__all__ = ['VisitDict']

class VisitDict(dict):
    bot_runs = ['12398', '6935D', '6911D', '6908D', '6905D', '6904D',
                '6903D', '6902D', '6901D', '6900D', '6899D', '6898D',
                '6897D', '6896D', '6895D', '6894D', '6893D', '6892D',
                '6891D', '6890D', '6889D', '6888D', '6887D', '6886D',
                '6885D', '6884D', '6883D', '6882D', '6880D', '6879D',
                '6878D', '6877D', '6876D', '6875D', '6874D', '6874D',
                '6873D', '6872D', '6871D', '6870D', '6869D', '6868D',
                '6867D', '6865D', '6864D', '6863D', '6861D', '6856D',
                '6855D', '6854D', '6853D', '6852D', '6851D', '6850D',
                '6849D', '6848D', '6846D', '6845D', '6844D', '6843D',
                '6841D', '6840D', '6836D', '6835D', '6834D', '6833D',
                '6832D', '6831D', '6829D', '6828D', '6827D', '6826D',
                '6825D', '6819D', '6817D', '6813D', '6812D', '6811D',
                '6810D', '6809D', '6808D', '6807D', '6806D', '6805D',
                '6803D', '6802D', '6801D', '6800D', '6798D', '6797D',
                '6795D', '6794D', '6792D', '6790D', '6787D', '6785D',
                '6784D', '6783D', '6782D', '6781D', '6780D', '6779D',
                '6778D', '6777D', '6774D', '6770D', '6768D', '6755D',
                '6754D', '6753D', '6752D', '6751D', '6750D', '6749D',
                '6748D', '6747D', '6746D', '6745D', '6744D', '6743D',
                '6740D', '6739D', '6738D', '6734D', '6733D', '6732D',
                '6731D', '6729D', '6728D', '6727D', '11882', '11880',
                '11879', '11876', '11875', '11874', '6726D', '6725D']

    def __init__(self, repo, selection=None, BOT_runs=True):
        super(VisitDict, self).__init__()
        registry_file = os.path.join(repo, 'registry.sqlite3')
        assert(os.path.isfile(registry_file))
        query = 'select * from raw'
        if selection is not None:
            query += f' where {selection}'
        with sqlite3.connect(registry_file) as conn:
            self.df = pd.read_sql(query, conn)
        self.runs = dict(zip(self.df['visit'], self.df['run']))
        self.update({(_, self.runs[_]) for _ in set(self.df['visit'])
                     if (not BOT_runs or self.runs[_] in self.bot_runs)})

    def down_select(self, selection, num_ccds=None):
        visits = []
        runs = []
        for visit, run in self.items():
            query = f'visit=={visit}'
            if selection is not None:
                query = ' and '.join((query, f'({selection})'))
            df = self.df.query(query)
            if num_ccds is None or len(df) == num_ccds:
                visits.append(visit)
                runs.append(run)
        return dict(_ for _ in zip(visits, runs))
