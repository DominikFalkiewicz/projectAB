from baza import Baza
from menu import Menu
from osoby import Osoby
from okazy import Okazy
from klady import Klady
from uczelnie import Uczelnie
from artykuly import Artykuly
from numery import Numery
from czasopisma import Czasopisma
from stanowiska import Stanowiska
from kolekcje import Kolekcje
from flask import Flask

path_db = "baza.db"
path_menu = "menu.html"
path_osoby = "osoby.html"
path_okazy = "okazy.html"
path_klady = "klady.html"
path_uczelnie = "uczelnie.html"
path_artykuly = "artykuly.html"
path_numery = "numery.html"
path_czasopisma = "czasopisma.html"
path_stanowiska = "stanowiska.html"
path_kolekcje = "kolekcje.html"

baza = Baza(path_db)

baza.drop()
baza.create()
baza.insert()

menu_handler = Menu(baza, path_menu)
osoby_handler = Osoby(baza, path_osoby)
okazy_handler = Okazy(baza, path_okazy)
klady_handler = Klady(baza, path_klady)
uczelnie_handler = Uczelnie(baza, path_uczelnie)
artykuly_handler = Artykuly(baza, path_artykuly)
numery_handler = Numery(baza, path_numery)
czasopisma_handler = Czasopisma(baza, path_czasopisma)
stanowiska_handler = Stanowiska(baza, path_stanowiska)
kolekcje_handler = Kolekcje(baza, path_kolekcje)

app = Flask(__name__)
app.secret_key = '1234567890'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def menu():
    return menu_handler.render()


@app.route('/osoby')
def osoby():
    return osoby_handler.render()


@app.route('/okazy')
def okazy():
    return okazy_handler.render()


@app.route('/klady')
def klady():
    return klady_handler.render()


@app.route('/uczelnie')
def uczelnie():
    return uczelnie_handler.render()


@app.route('/artykuly')
def artykuly():
    return artykuly_handler.render()


@app.route('/numery')
def numery():
    return numery_handler.render()


@app.route('/czasopisma', methods=['GET', 'POST'])
def czasopisma():
    return czasopisma_handler.render()

@app.route('/czasopisma/update', methods=['GET', 'POST'])
def update_czasopisma():
    return czasopisma_handler.render_update()

@app.route('/czasopisma/create', methods=['GET', 'POST'])
def create_czasopisma():
    return czasopisma_handler.render_create()


@app.route('/kolekcje', methods=['GET', 'POST'])
def kolekcje():
    return kolekcje_handler.render()


@app.route('/kolekcje/update', methods=['GET', 'POST'])
def update_kolekcje():
    return kolekcje_handler.render_update()


@app.route('/kolekcje/create', methods=['GET', 'POST'])
def create_kolekcje():
    return kolekcje_handler.render_create()


@app.route('/stanowiska')
def stanowiska():
    return stanowiska_handler.render()


if __name__ == "__main__":
    app.run(debug=True)

