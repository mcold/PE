# coding: utf-8

from sqlite3 import connect
from config import *

class Root:

    id_next = 0
    tbl_name = None

    @classmethod
    def __init__(self, id: int = None):
        if id:
            self.id_tmp = id
        else:            
            self.id_tmp = self.id_next
            self.id_next += 1

    @classmethod
    def set_next(self, id: int):
        self.id_next = id

    @classmethod
    def set_tbl_name(self, tbl_name: str):
        self.tbl_name = tbl_name

    @classmethod
    def get_id_next(self):
        if self.tbl_name:
            if self.id_next == 0:
                with connect(db_file) as conn:
                    cur = conn.cursor()
                    cur.execute(f"""select max(id) + 1
                                    from {self.tbl_name}""")
                res = cur.fetchone()
                if res[0]:
                    self.id_next = res[0]
                else:
                    self.id_next = 1
            else:
                self.id_tmp = self.id_next
                # self.id_next += 1
        else:
            self.id_next = 1