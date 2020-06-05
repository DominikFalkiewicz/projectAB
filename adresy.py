from flask import render_template, request, redirect, session


class Adresy:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            acc = session["acc"]
            form_button = request.form["button"]
            if form_button[0] == "c" and acc == "3":
                return redirect("/adresy/create")
            elif form_button[0] == "r" and acc in ["2", "3"]:
                session["rid"] = form_button[1:]
                return redirect("/adresy/read")
            elif form_button[0] == "u" and acc == "3":
                session["rid"] = form_button[1:]
                return redirect("/adresy/update")
            elif form_button[0] == "d" and acc == "3":
                self.delete(form_button[1:])
            elif form_button[0] == "s":
                pat = request.form["pat"]
                rekordy = self.baza.ask("SELECT * FROM adres WHERE kraj LIKE '%" + pat + "%' OR miasto LIKE '%" + pat +
                                        "%' OR ulica LIKE '%" + pat + "%' ORDER BY kraj")
                return render_template(self.path, rekordy=rekordy)

        rekordy = self.baza.ask("SELECT * FROM adres ORDER BY kraj")
        return render_template(self.path, rekordy=rekordy)

    def render_create(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                kraj = request.form["kraj"]
                miasto = request.form["miasto"]
                ulica = request.form["ulica"]
                nr_budynku = request.form["nr_budynku"]
                self.create(kraj, miasto, ulica, nr_budynku)
                return redirect("/adresy")
            if form_button == "anuluj":
                return redirect("/adresy")

        return render_template("create_" + self.path)

    def render_read(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "wroc":
                return redirect("/adresy")

        dane = self.baza.ask("SELECT kraj, miasto, ulica, nr_budynku FROM adres WHERE id = " + rid)[0]
        if dane[2] is None:
            adres = dane[0] + ", " + dane[1] + " " + str(dane[3])
        else:
            adres = dane[0] + ", " + dane[1] + ", " + dane[2] + " " + str(dane[3])
        return render_template("read_" + self.path, adres=adres)

    def render_update(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                kraj = request.form["kraj"]
                miasto = request.form["miasto"]
                ulica = request.form["ulica"]
                nr_budynku = request.form["nr_budynku"]
                self.update(rid, kraj, miasto, ulica, nr_budynku)
                return redirect("/adresy")
            if form_button == "anuluj":
                return redirect("/adresy")

        stare_dane = self.baza.ask("SELECT kraj, miasto, ulica, nr_budynku FROM adres WHERE id = " + rid)[0]
        stary_kraj = stare_dane[0]
        stare_miasto = stare_dane[1]
        stara_ulica = stare_dane[2]
        stary_numer = stare_dane[3]
        return render_template("update_" + self.path, stary_kraj=stary_kraj, stare_miasto=stare_miasto,
                               stara_ulica=stara_ulica, stary_numer=stary_numer)

    def create(self, kraj, miasto, ulica, nr_budynku):
        if ulica != "None":
            self.baza.exe("INSERT INTO adres (kraj, miasto, ulica, nr_budynku) "
                          "VALUES ('" + kraj + "', '" + miasto + "', '" + ulica + "', " + nr_budynku + ")")
        else:
            self.baza.exe("INSERT INTO adres (kraj, miasto, ulica, nr_budynku) "
                          "VALUES ('" + kraj + "', '" + miasto + "', NULL, " + nr_budynku + ")")

    def update(self, rid, kraj, miasto, ulica, nr_budynku):
        if ulica != "None":
            self.baza.exe("UPDATE adres SET kraj = '" + kraj + "', miasto = '" + miasto + "', ulica = '" + ulica +
                          "', nr_budynku = " + nr_budynku + " WHERE id = " + rid)
        else:
            self.baza.exe("UPDATE adres SET kraj = '" + kraj + "', miasto = '" + miasto +
                          "', ulica = NULL, nr_budynku = " + nr_budynku + " WHERE id = " + rid)

    def delete(self, rid):
        self.baza.exe("DELETE FROM adres WHERE id = " + rid)
