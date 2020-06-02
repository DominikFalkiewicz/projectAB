from flask import render_template, request, redirect, session


class Czasopisma:
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
                return redirect("/czasopisma/update")
            elif form_button[0] == "c":
                return redirect("/czasopisma/create")
            elif form_button[0] == "s":
                pat = request.form["pat"]
                rekordy = self.baza.ask("SELECT * FROM czasopismo WHERE tytul LIKE '%" + pat + "%'")
                return render_template(self.path, rekordy=rekordy)
        rekordy = self.baza.ask("SELECT * FROM czasopismo")
        return render_template(self.path, rekordy=rekordy)

    def render_create(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                tytul = request.form["tytul"]
                kraj = request.form["kraj"]
                opis = request.form["opis"]
                self.create(tytul, kraj, opis)
                return redirect("/czasopisma")

        return render_template("create_" + self.path)

    def render_update(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                tytul = request.form["tytul"]
                kraj = request.form["kraj"]
                opis = request.form["opis"]
                self.update(rid, tytul, kraj, opis)
                return redirect("/czasopisma")

        stare_dane = self.baza.ask("SELECT tytul, kraj, opis FROM czasopismo WHERE id = " + rid)[0]
        stary_tytul = stare_dane[0]
        stary_kraj = stare_dane[1]
        stary_opis = stare_dane[2]
        return render_template("update_" + self.path, stary_tytul=stary_tytul, stary_kraj=stary_kraj,
                               stary_opis=stary_opis)

    def delete(self, rid):
        self.baza.exe("DELETE FROM czasopismo WHERE id = " + rid)

    def create(self, tytul, kraj, opis):
        self.baza.exe("INSERT INTO czasopismo (tytul, kraj, opis) "
                      "VALUES ('" + tytul + "', '" + kraj + "', '" + opis + "')")

    def update(self, rid, tytul, kraj, opis):
        self.baza.exe("UPDATE czasopismo "
                      "SET tytul = '" + tytul + "', kraj = '" + kraj + "', opis = '" + opis + "' WHERE id = " + rid)
