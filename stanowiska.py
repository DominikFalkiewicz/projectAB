from flask import render_template, request, redirect, session


class Stanowiska:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "c":
                return redirect("/stanowiska/create")
            elif form_button[0] == "r":
                session["rid"] = form_button[1:]
                return redirect("/stanowiska/read")
            elif form_button[0] == "u":
                session["rid"] = form_button[1:]
                return redirect("/stanowiska/update")
            elif form_button[0] == "d":
                self.delete(form_button[1:])
            elif form_button[0] == "s":
                pat = request.form["pat"]
                rekordy = self.baza.ask("SELECT id, nazwa, okres FROM stanowisko "
                                        "WHERE nazwa LIKE '%" + pat + "%'ORDER BY okres")
                return render_template(self.path, rekordy=rekordy)

        rekordy = self.baza.ask("SELECT id, nazwa, okres FROM stanowisko ORDER BY okres")
        return render_template(self.path, rekordy=rekordy)

    def render_create(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                nazwa = request.form["nazwa"]
                okres = request.form["okres"]
                self.create(nazwa, okres)
                return redirect("/stanowiska")
            if form_button == "anuluj":
                return redirect("/stanowiska")

        return render_template("create_" + self.path)

    def render_read(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "wroc":
                return redirect("/stanowiska")

        dane = self.baza.ask("SELECT nazwa, okres FROM stanowisko WHERE id = " + rid)[0]
        nazwa = dane[0]
        okres = dane[1]
        return render_template("read_" + self.path, nazwa=nazwa, okres=okres)

    def render_update(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                nazwa = request.form["nazwa"]
                okres = request.form["okres"]
                self.update(rid, nazwa, okres)
                return redirect("/stanowiska")
            if form_button == "anuluj":
                return redirect("/stanowiska")

        stare_dane = self.baza.ask("SELECT nazwa, okres FROM stanowisko WHERE id = " + rid)[0]
        stara_nazwa = stare_dane[0]
        stary_okres = stare_dane[1]
        return render_template("update_" + self.path, stara_nazwa=stara_nazwa, stary_okres=stary_okres)

    def create(self, nazwa, okres):
        self.baza.exe("INSERT INTO stanowisko (nazwa, okres) VALUES ('" + nazwa + "', '" + okres + "')")

    def update(self, rid, nazwa, okres):
        self.baza.exe("UPDATE stanowisko SET nazwa = '" + nazwa + "', okres = '" + okres + "' WHERE id = " + rid)

    def delete(self, rid):
        self.baza.exe("DELETE FROM stanowisko WHERE id = " + rid)
