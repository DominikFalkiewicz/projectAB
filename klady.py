from flask import render_template, redirect, request, session


class Klady:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "c":
                return redirect("/klady/create")
            elif form_button[0] == "r":
                session["rid"] = form_button[1:]
                return redirect("/klady/read")
            elif form_button[0] == "u":
                session["rid"] = form_button[1:]
                return redirect("/klady/update")
            elif form_button[0] == "d":
                self.delete(form_button[1:])
            elif form_button[0] == "s":
                pat = request.form["pat"]
                rekordy = self.baza.ask("SELECT klad.id, klad.ranga, klad.nazwa, nadklad.nazwa FROM klad "
                                        "LEFT JOIN klad AS nadklad ON klad.id_nadklad = nadklad.id "
                                        "WHERE klad.nazwa LIKE '%" + pat + "%' ORDER BY klad.ranga")
                return render_template(self.path, rekordy=rekordy)

        rekordy = self.baza.ask("SELECT klad.id, klad.ranga, klad.nazwa, nadklad.nazwa FROM klad "
                                "LEFT JOIN klad AS nadklad ON klad.id_nadklad = nadklad.id ORDER BY klad.ranga")
        return render_template(self.path, rekordy=rekordy)

    def render_create(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                nazwa = request.form["nazwa"]
                ranga = request.form["ranga"]
                opis = request.form["opis"]
                nisza = request.form["nisza"]
                id_nadklad = request.form["nadklady_wybor"]
                self.create(nazwa, ranga, opis, nisza, id_nadklad)
                return redirect("/klady")
            if form_button == "anuluj":
                return redirect("/klady")

        nadklady = self.baza.ask("SELECT id, nazwa FROM klad WHERE ranga != 'Gatunek'")
        return render_template("create_" + self.path, nadklady=nadklady)

    def render_read(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "wroc":
                return redirect("/klady")

        dane = self.baza.ask("SELECT nazwa, ranga, opis, nisza, id_nadklad FROM klad WHERE id = " + rid)[0]
        nazwa = dane[0]
        ranga = dane[1]
        opis = dane[2]
        nisza = dane[3]
        id_nadklad = str(dane[4])
        nadklad = self.baza.ask("SELECT nazwa FROM klad WHERE id = " + id_nadklad)[0][0]
        return render_template("read_" + self.path, nazwa=nazwa, nadklad=nadklad, ranga=ranga, nisza=nisza, opis=opis)

    def render_update(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                nazwa = request.form["nazwa"]
                ranga = request.form["ranga"]
                opis = request.form["opis"]
                nisza = request.form["nisza"]
                id_nadklad = request.form["nadklady_wybor"]
                self.update(rid, nazwa, ranga, opis, nisza, id_nadklad)
                return redirect("/klady")
            if form_button == "anuluj":
                return redirect("/klady")

        dane = self.baza.ask("SELECT nazwa, ranga, opis, nisza, id_nadklad FROM klad WHERE id = " + rid)[0]
        stara_nazwa = dane[0]
        stara_ranga = dane[1]
        stary_opis = dane[2]
        stara_nisza = dane[3]
        id_nadklad = str(dane[4])
        if id_nadklad == "None":
            stary_nadklad = ["NULL", "-brak-"]
            nadklady = self.baza.ask("SELECT id, nazwa FROM klad "
                                     "WHERE ranga != 'Gatunek' AND id != " + rid)
        else:
            stary_nadklad = self.baza.ask("SELECT id, nazwa FROM klad WHERE id = " + id_nadklad)[0]
            nadklady = self.baza.ask("SELECT id, nazwa FROM klad "
                                     "WHERE ranga != 'Gatunek' AND id NOT IN (" + rid + ", " + id_nadklad + ")")
            nadklady = [[nadklad[0], nadklad[1]] for nadklad in nadklady]
            nadklady.append(["NULL", "-brak-"])
        return render_template("update_" + self.path, nadklady=nadklady, stary_nadklad=stary_nadklad,
                               stara_nazwa=stara_nazwa, stara_ranga=stara_ranga, stara_nisza=stara_nisza,
                               stary_opis=stary_opis)

    def create(self, nazwa, ranga_p, opis_p, nisza_p, id_nadklad):
        if ranga_p == "None":
            ranga = "NULL"
        else:
            ranga = "'" + ranga_p + "'"

        if opis_p == "None":
            opis = "NULL"
        else:
            opis = "'" + opis_p + "'"

        if nisza_p == "None":
            nisza = "NULL"
        else:
            nisza = "'" + nisza_p + "'"

        self.baza.exe("INSERT INTO klad (nazwa, ranga, opis, nisza, id_nadklad) "
                      "VALUES ('" + nazwa + "', " + ranga + ", " + opis + ", " + nisza + ", " + id_nadklad + ")")

    def update(self, rid, nazwa, ranga_p, opis_p, nisza_p, id_nadklad):
        if ranga_p == "None":
            ranga = "NULL"
        else:
            ranga = "'" + ranga_p + "'"

        if opis_p == "None":
            opis = "NULL"
        else:
            opis = "'" + opis_p + "'"

        if nisza_p == "None":
            nisza = "NULL"
        else:
            nisza = "'" + nisza_p + "'"

        self.baza.exe("UPDATE klad SET nazwa = '" + nazwa + "', ranga = " + ranga + ", opis = " + opis + ", nisza = " +
                      nisza + ", id_nadklad = " + id_nadklad + " WHERE id = " + rid)

    def delete(self, rid):
        podklady = self.baza.ask("SELECT id FROM klad WHERE id_nadklad = " + rid)

        for pid in podklady:
            self.delete(str(pid[0]))

        self.baza.exe("DELETE FROM klad WHERE id = " + rid)
