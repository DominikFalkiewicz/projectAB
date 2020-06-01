import sqlite3


class Baza:
    def __init__(self, path):
        self.path = path
        self.con = sqlite3.connect(path)

    def drop(self):
        with open("baza_danych/drop.sql") as drop_file:
            drop = drop_file.read().split(";")
        for d in drop:
            self.con.execute(d)
        self.con.commit()

    def create(self):
        with open("baza_danych/create.sql") as create_file:
            create = create_file.read().split(";")
        for c in create:
            self.con.execute(c)
        self.con.commit()

    def insert(self):
        with open("baza_danych/insert.sql") as insert_file:
            insert = insert_file.read().split(";")
        for i in insert:
            self.con.execute(i)
        self.con.commit()
