from flask import render_template, request, redirect, session


class Kolekcje:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "d":
                self.delete(form_button[1:])
            elif form_button[0] == "u":
                session["rid"] = form_button[1:]
                return redirect("/kolekcje/update")
            elif form_button[0] == "c":
                return redirect("/kolekcje/create")
            elif form_button[0] == "s":
                pat = request.form["pat"]
                rekordy = self.baza.ask("SELECT * FROM kolekcja WHERE nazwa LIKE '%" + pat + "%'")
                return render_template(self.path, rekordy=rekordy)
        rekordy = self.baza.ask("SELECT * FROM kolekcja")
        return render_template(self.path, rekordy=rekordy)

    def render_update(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                nazwa = request.form["nazwa"]
                id_adres = request.form["adresy_wybor"]
                self.update(rid, nazwa, id_adres)
                return redirect("/kolekcje")

        stare_dane = self.baza.ask("SELECT nazwa, id_adres FROM kolekcja WHERE id = " + rid)[0]
        stara_nazwa = stare_dane[0]
        id_adres = str(stare_dane[1])
        stary_adres = self.baza.ask("SELECT * FROM adres WHERE id = " + id_adres)[0]
        stary_adres = [stary_adres[0], str(stary_adres[4] + ", " + stary_adres[3] + ", " + stary_adres[2] + " "
                                           + str(stary_adres[1]))]
        adresy = self.baza.ask("SELECT * FROM adres WHERE id <> " + id_adres)
        adresy = [[adres[0], str(adres[4] + ", " + adres[3] + ", " + adres[2] + " " + str(adres[1]))]
                  for adres in adresy]
        return render_template("update_" + self.path, stary_adres=stary_adres, adresy=adresy, stara_nazwa=stara_nazwa)

    def render_create(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                nazwa = request.form["nazwa"]
                id_adres = request.form["adresy_wybor"]
                self.create(nazwa, id_adres)
                return redirect("/kolekcje")

        adresy = self.baza.ask("SELECT * FROM adres WHERE id NOT IN (SELECT id_adres FROM kolekcja)")
        adresy = [[adres[0], str(adres[4] + ", " + adres[3] + ", " + adres[2] + " " + str(adres[1]))]
                  for adres in adresy]
        return render_template("create_" + self.path, adresy=adresy)

    def update(self, rid, nazwa, id_adres):
        self.baza.exe("UPDATE kolekcja SET nazwa = '" + nazwa + "', id_adres = " + id_adres + " WHERE id = " + rid)

    def create(self, nazwa, id_adres):
        self.baza.exe("INSERT INTO kolekcja (nazwa, id_adres) VALUES ('" + nazwa + "', " + id_adres + ")")

    def delete(self, rid):
        self.baza.exe("DELETE FROM kolekcja WHERE id = " + rid)
