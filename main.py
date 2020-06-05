from baza import Baza
from menu import Menu
from osoby import Osoby
from okazy import Okazy
from adresy import Adresy
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
path_adresy = "adresy.html"
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
adresy_handler = Adresy(baza, path_adresy)
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


@app.route('/osoby', methods=['GET', 'POST'])
def osoby():
    return osoby_handler.render()


@app.route('/osoby/create', methods=['GET', 'POST'])
def create_osoby():
    return osoby_handler.render_create()


@app.route('/osoby/read', methods=['GET', 'POST'])
def read_osoby():
    return osoby_handler.render_read()


@app.route('/osoby/update', methods=['GET', 'POST'])
def update_osoby():
    return osoby_handler.render_update()


@app.route('/okazy', methods=['GET', 'POST'])
def okazy():
    return okazy_handler.render()


@app.route('/okazy/create', methods=['GET', 'POST'])
def create_okazy():
    return okazy_handler.render_create()


@app.route('/okazy/read', methods=['GET', 'POST'])
def read_okazy():
    return okazy_handler.render_read()


@app.route('/okazy/update', methods=['GET', 'POST'])
def update_okazy():
    return okazy_handler.render_update()


@app.route('/okazy/datowania', methods=['GET', 'POST'])
def datowania_okazy():
    return okazy_handler.render_datowania()


@app.route('/okazy/datowania/create', methods=['GET', 'POST'])
def create_datowania_okazy():
    return okazy_handler.render_datowania_create()


@app.route('/okazy/artykuly', methods=['GET', 'POST'])
def artykuly_okazy():
    return okazy_handler.render_artykuly()


@app.route('/okazy/artykuly/add', methods=['GET', 'POST'])
def add_artykuly_okazy():
    return okazy_handler.render_artykuly_add()


@app.route('/adresy', methods=['GET', 'POST'])
def adresy():
    return adresy_handler.render()


@app.route('/adresy/create', methods=['GET', 'POST'])
def create_adresy():
    return adresy_handler.render_create()


@app.route('/adresy/read', methods=['GET', 'POST'])
def read_adresy():
    return adresy_handler.render_read()


@app.route('/adresy/update', methods=['GET', 'POST'])
def update_adresy():
    return adresy_handler.render_update()


@app.route('/klady', methods=['GET', 'POST'])
def klady():
    return klady_handler.render()


@app.route('/klady/create', methods=['GET', 'POST'])
def create_klady():
    return klady_handler.render_create()


@app.route('/klady/read', methods=['GET', 'POST'])
def read_klady():
    return klady_handler.render_read()


@app.route('/klady/update', methods=['GET', 'POST'])
def update_klady():
    return klady_handler.render_update()


@app.route('/uczelnie', methods=['GET', 'POST'])
def uczelnie():
    return uczelnie_handler.render()


@app.route('/uczelnie/create', methods=['GET', 'POST'])
def create_uczelnie():
    return uczelnie_handler.render_create()


@app.route('/uczelnie/read', methods=['GET', 'POST'])
def read_uczelnie():
    return uczelnie_handler.render_read()


@app.route('/uczelnie/update', methods=['GET', 'POST'])
def update_uczelnie():
    return uczelnie_handler.render_update()


@app.route('/artykuly', methods=['GET', 'POST'])
def artykuly():
    return artykuly_handler.render()


@app.route('/artykuly/create', methods=['GET', 'POST'])
def create_artykuly():
    return artykuly_handler.render_create()


@app.route('/artykuly/read', methods=['GET', 'POST'])
def read_artykuly():
    return artykuly_handler.render_read()


@app.route('/artykuly/update', methods=['GET', 'POST'])
def update_artykuly():
    return artykuly_handler.render_update()


@app.route('/numery', methods=['GET', 'POST'])
def numery():
    return numery_handler.render()


@app.route('/numery/create', methods=['GET', 'POST'])
def create_numery():
    return numery_handler.render_create()


@app.route('/numery/read', methods=['GET', 'POST'])
def read_numery():
    return numery_handler.render_read()


@app.route('/numery/update', methods=['GET', 'POST'])
def update_numery():
    return numery_handler.render_update()


@app.route('/czasopisma', methods=['GET', 'POST'])
def czasopisma():
    return czasopisma_handler.render()


@app.route('/czasopisma/create', methods=['GET', 'POST'])
def create_czasopisma():
    return czasopisma_handler.render_create()


@app.route('/czasopisma/read', methods=['GET', 'POST'])
def read_czasopisma():
    return czasopisma_handler.render_read()


@app.route('/czasopisma/update', methods=['GET', 'POST'])
def update_czasopisma():
    return czasopisma_handler.render_update()


@app.route('/kolekcje', methods=['GET', 'POST'])
def kolekcje():
    return kolekcje_handler.render()


@app.route('/kolekcje/create', methods=['GET', 'POST'])
def create_kolekcje():
    return kolekcje_handler.render_create()


@app.route('/kolekcje/read', methods=['GET', 'POST'])
def read_kolekcje():
    return kolekcje_handler.render_read()


@app.route('/kolekcje/update', methods=['GET', 'POST'])
def update_kolekcje():
    return kolekcje_handler.render_update()


@app.route('/stanowiska', methods=['GET', 'POST'])
def stanowiska():
    return stanowiska_handler.render()


@app.route('/stanowiska/create', methods=['GET', 'POST'])
def create_stanowiska():
    return stanowiska_handler.render_create()


@app.route('/stanowiska/read', methods=['GET', 'POST'])
def read_stanowiska():
    return stanowiska_handler.render_read()


@app.route('/stanowiska/update', methods=['GET', 'POST'])
def update_stanowiska():
    return stanowiska_handler.render_update()


if __name__ == "__main__":
    app.run(debug=True)
