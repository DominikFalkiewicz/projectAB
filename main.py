from baza import Baza

path = "baza.db"


baza = Baza(path)

baza.create()
baza.insert()
baza.drop()