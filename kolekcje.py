from flask import render_template, request, redirect, session


class Kolekcje:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            acc = session["acc"]
            form_button = request.form["button"]
            if form_button[0] == "c" and acc == "3":
                return redirect("/kolekcje/create")
            elif form_button[0] == "r" and acc in ["2", "3"]:
                session["rid"] = form_button[1:]
                return redirect("/kolekcje/read")
            elif form_button[0] == "u" and acc == "3":
                session["rid"] = form_button[1:]
                return redirect("/kolekcje/update")
            elif form_button[0] == "d" and acc == "3":
                self.delete(form_button[1:])
            elif form_button[0] == "s":
                pat = request.form["pat"]
                rekordy = self.baza.ask("SELECT kolekcja.id, nazwa, kraj FROM kolekcja INNER JOIN adres "
                                        "ON id_adres = adres.id AND nazwa LIKE '%" + pat + "%' ORDER BY kraj")
                return render_template(self.path, rekordy=rekordy)

        rekordy = self.baza.ask("SELECT kolekcja.id, nazwa, kraj FROM kolekcja INNER JOIN adres "
                                "ON id_adres = adres.id ORDER BY kraj")
        return render_template(self.path, rekordy=rekordy)

    def render_create(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                nazwa = request.form["nazwa"]
                id_adres = request.form["adresy_wybor"]
                self.create(nazwa, id_adres)
                return redirect("/kolekcje")
            if form_button == "anuluj":
                return redirect("/kolekcje")

        adresy = self.baza.ask("SELECT * FROM adres WHERE id NOT IN (SELECT id_adres FROM kolekcja)")
        adresy = [[adres[0], str(adres[4] + ", " + adres[3] + ", " + adres[2] + " " + str(adres[1]))]
                  for adres in adresy]
        return render_template("create_" + self.path, adresy=adresy)

    def render_read(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "wroc":
                return redirect("/kolekcje")

        dane = self.baza.ask("SELECT nazwa, id_adres FROM kolekcja WHERE id = " + rid)[0]
        nazwa = dane[0]
        id_adres = str(dane[1])
        adres = self.baza.ask("SELECT * FROM adres WHERE id = " + id_adres)[0]
        adres = str(adres[4] + ", " + adres[3] + ", " + adres[2] + " " + str(adres[1]))
        return render_template("read_" + self.path, adres=adres, nazwa=nazwa)

    def render_update(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                nazwa = request.form["nazwa"]
                id_adres = request.form["adresy_wybor"]
                self.update(rid, nazwa, id_adres)
                return redirect("/kolekcje")
            if form_button == "anuluj":
                return redirect("/kolekcje")

        stare_dane = self.baza.ask("SELECT nazwa, id_adres FROM kolekcja WHERE id = " + rid)[0]
        stara_nazwa = stare_dane[0]
        id_adres = str(stare_dane[1])
        stary_adres = self.baza.ask("SELECT * FROM adres WHERE id = " + id_adres)[0]
        stary_adres = [stary_adres[0], str(stary_adres[4] + ", " + stary_adres[3] + ", " + stary_adres[2] + " "
                                           + str(stary_adres[1]))]
        adresy = self.baza.ask("SELECT * FROM adres WHERE id NOT IN (SELECT id_adres FROM kolekcja)")
        adresy = [[adres[0], str(adres[4] + ", " + adres[3] + ", " + adres[2] + " " + str(adres[1]))]
                  for adres in adresy]
        return render_template("update_" + self.path, stary_adres=stary_adres, adresy=adresy, stara_nazwa=stara_nazwa)

    def create(self, nazwa, id_adres):
        self.baza.exe("INSERT INTO kolekcja (nazwa, id_adres) VALUES ('" + nazwa + "', " + id_adres + ")")

    def update(self, rid, nazwa, id_adres):
        self.baza.exe("UPDATE kolekcja SET nazwa = '" + nazwa + "', id_adres = " + id_adres + " WHERE id = " + rid)

    def delete(self, rid):
        self.baza.exe("DELETE FROM kolekcja WHERE id = " + rid)
