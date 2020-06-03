from flask import render_template, request, session, redirect


class Numery:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "c":
                return redirect("/numery/create")
            elif form_button[0] == "r":
                session["rid"] = form_button[1:]
                return redirect("/numery/read")
            elif form_button[0] == "u":
                session["rid"] = form_button[1:]
                return redirect("/numery/update")
            elif form_button[0] == "d":
                self.delete(form_button[1:])
            elif form_button[0] == "s":
                pat = request.form["pat"]
                rekordy = self.baza.ask("SELECT numer.id, numer, tytul FROM numer INNER JOIN czasopismo "
                                        "ON id_czasopismo = czasopismo.id "
                                        "AND tytul LIKE '%" + pat + "%' ORDER BY tytul")
                return render_template(self.path, rekordy=rekordy)

        rekordy = self.baza.ask("SELECT numer.id, numer, tytul FROM numer INNER JOIN czasopismo "
                                "ON id_czasopismo = czasopismo.id ORDER BY tytul")
        return render_template(self.path, rekordy=rekordy)

    def render_create(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                numer = request.form["numer"]
                data = request.form["data"]
                id_czasopismo = request.form["czasopisma_wybor"]
                self.create(numer, data, id_czasopismo)
                return redirect("/numery")
            if form_button == "anuluj":
                return redirect("/numery")

        dzisiaj = self.baza.ask("SELECT DATE('now')")[0][0]
        czasopisma = self.baza.ask("SELECT id, tytul FROM czasopismo")
        czasopisma = [[czasopismo[0], czasopismo[1]] for czasopismo in czasopisma]
        return render_template("create_" + self.path, czasopisma=czasopisma, dzisiaj=dzisiaj)

    def render_read(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "wroc":
                return redirect("/numery")

        dane = self.baza.ask("SELECT tytul, numer, data_wydania FROM numer INNER JOIN czasopismo "
                                "ON id_czasopismo = czasopismo.id AND numer.id = " + rid)[0]
        tytul = dane[0]
        numer = dane[1]
        data = dane[2]
        return render_template("read_" + self.path, tytul=tytul, numer=numer, data=data)

    def render_update(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                numer = request.form["numer"]
                data = request.form["data"]
                id_czasopismo = request.form["czasopisma_wybor"]
                self.update(rid, numer, data, id_czasopismo)
                return redirect("/numery")
            if form_button == "anuluj":
                return redirect("/numery")

        stare_dane = self.baza.ask("SELECT numer, data_wydania, id_czasopismo FROM numer WHERE id = " + rid)[0]
        stary_numer = str(stare_dane[0])
        stara_data = stare_dane[1]
        id_czasopismo = str(stare_dane[2])
        stare_czasopismo = self.baza.ask("SELECT id, tytul FROM czasopismo WHERE id = " + id_czasopismo)[0]
        czasopisma = self.baza.ask("SELECT id, tytul FROM czasopismo WHERE id != " + id_czasopismo)
        return render_template("update_" + self.path, stare_czasopismo=stare_czasopismo, czasopisma=czasopisma,
                               stary_numer=stary_numer, stara_data=stara_data)

    def create(self, numer, data, id_czasopismo):
        self.baza.exe("INSERT INTO numer (numer, data_wydania, id_czasopismo) "
                      "VALUES (" + numer + ", '" + data + "', " + id_czasopismo + ")")

    def update(self, rid, numer, data, id_czasopismo):
        self.baza.exe("UPDATE numer SET numer = " + numer + ", data_wydania = '" + data + "', id_czasopismo = "
                      + id_czasopismo + " WHERE id = " + rid)

    def delete(self, rid):
        self.baza.exe("DELETE FROM numer WHERE id = " + rid)
