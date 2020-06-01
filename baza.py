import sqlite3
import pandas as pd
import numpy as np


class Baza:
    def __init__(self, path):
        self.path = path

    def drop(self):
        con = sqlite3.connect(self.path)
        with open("baza_danych/drop.sql", "r", encoding="utf-8") as drop_file:
            drop = drop_file.read().split(";")
        for d in drop:
            con.execute(d)
        con.commit()
        con.close()

    def create(self):
        con = sqlite3.connect(self.path)
        with open("baza_danych/create.sql", "r", encoding="utf-8") as create_file:
            create = create_file.read().split(";")
        for c in create:
            con.execute(c)
        con.commit()
        con.close()

    def insert(self):
        con = sqlite3.connect(self.path)
        with open("baza_danych/insert.sql", "r", encoding="utf-8") as insert_file:
            insert = insert_file.read().split(";")
        for i in insert:
            con.execute(i)
        con.commit()
        con.close()

    def ask(self, sql):
        con = sqlite3.connect(self.path)
        rekordy = pd.read_sql_query(sql, con)
        con.commit()
        con.close()
        return np.array(rekordy)

    def exe(self, sql):
        con = sqlite3.connect(self.path)
        con.execute(sql)
        con.commit()
        con.close()
