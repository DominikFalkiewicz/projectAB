from flask import render_template, request, redirect, session


class Osoby:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "c":
                return redirect("/osoby/create")
            elif form_button[0] == "r":
                session["rid"] = form_button[1:]
                return redirect("/osoby/read")
            elif form_button[0] == "u":
                session["rid"] = form_button[1:]
                return redirect("/osoby/update")
            elif form_button[0] == "d":
                self.delete(form_button[1:])
            elif form_button[0] == "s":
                pat = request.form["pat"]
                rekordy = self.baza.ask("SELECT osoba.id, imie, nazwisko, stopien_naukowy, nazwa FROM osoba "
                                        "LEFT JOIN uczelnia ON id_uczelnia = uczelnia.id "
                                        "WHERE imie LIKE '%" + pat + "%' OR nazwisko LIKE '%" + pat + "%' "
                                        "ORDER BY nazwisko")
                return render_template(self.path, rekordy=rekordy)

        rekordy = self.baza.ask("SELECT osoba.id, imie, nazwisko, stopien_naukowy, nazwa "
                                "FROM osoba LEFT JOIN uczelnia ON id_uczelnia = uczelnia.id ORDER BY nazwisko")
        return render_template(self.path, rekordy=rekordy)

    def render_create(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                imie = request.form["imie"]
                nazwisko = request.form["nazwisko"]
                data_urodzenia = request.form["data_urodzenia"]
                data_smierci = request.form["data_smierci"]
                stopien_naukowy = request.form["stopien_naukowy"]
                id_uczelnia = request.form["uczelnie_wybor"]
                self.create(imie, nazwisko, data_urodzenia, data_smierci, stopien_naukowy, id_uczelnia)
                return redirect("/osoby")
            if form_button == "anuluj":
                return redirect("/osoby")

        uczelnie = self.baza.ask("SELECT id, nazwa FROM uczelnia")
        return render_template("create_" + self.path, uczelnie=uczelnie)

    def render_read(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "wroc":
                return redirect("/osoby")

        dane = self.baza.ask("SELECT imie, nazwisko, data_urodzenia, data_smierci, stopien_naukowy, nazwa "
                             "FROM osoba LEFT JOIN uczelnia ON id_uczelnia = uczelnia.id WHERE osoba.id = " + rid)[0]
        imie = dane[0]
        nazwisko = dane[1]
        data_urodzenia = dane[2]
        data_smierci = dane[3]
        stopien_naukowy = dane[4]
        uczelnia = dane[5]
        return render_template("read_" + self.path, imie=imie, nazwisko=nazwisko, data_urodzenia=data_urodzenia,
                               data_smierci=data_smierci, stopien_naukowy=stopien_naukowy, uczelnia=uczelnia)

    def render_update(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                imie = request.form["imie"]
                nazwisko = request.form["nazwisko"]
                data_urodzenia = request.form["data_urodzenia"]
                data_smierci = request.form["data_smierci"]
                stopien_naukowy = request.form["stopien_naukowy"]
                id_uczelnia = request.form["uczelnie_wybor"]
                self.update(rid, imie, nazwisko, data_urodzenia, data_smierci, stopien_naukowy, id_uczelnia)
                return redirect("/osoby")
            if form_button == "anuluj":
                return redirect("/osoby")

        stare_dane = self.baza.ask("SELECT imie, nazwisko, data_urodzenia, data_smierci, stopien_naukowy, id_uczelnia "
                                   "FROM osoba WHERE id = " + rid)[0]
        stare_imie = stare_dane[0]
        stare_nazwisko = stare_dane[1]
        stare_urodzenie = stare_dane[2]
        stara_smierc = stare_dane[3]
        stary_stopien = stare_dane[4]
        id_uczelnia = stare_dane[5]

        if id_uczelnia is None:
            stara_uczelnia = ["NULL", "-brak-"]
            uczelnie = self.baza.ask("SELECT id, nazwa FROM uczelnia")
        else:
            stara_uczelnia = self.baza.ask("SELECT id, nazwa FROM uczelnia WHERE id != " + str(id_uczelnia))[0]
            uczelnie = self.baza.ask("SELECT id, nazwa FROM uczelnia WHERE id != " + str(id_uczelnia))
            uczelnie = [[uczelnia[0], uczelnia[1]] for uczelnia in uczelnie]
            uczelnie.append(["NULL", "-brak-"])

        return render_template("update_" + self.path, stare_imie=stare_imie, stare_nazwisko=stare_nazwisko,
                               stare_urodzenie=stare_urodzenie, stara_smierc=stara_smierc, stary_stopien=stary_stopien,
                               stara_uczelnia=stara_uczelnia, uczelnie=uczelnie)

    def create(self, imie, nazwisko, data_urodzenia, data_smierci_p, stopien_naukowy_p, id_uczelnia_p):

        if data_smierci_p == "None":
            data_smierci = "NULL"
        else:
            data_smierci = "'" + data_smierci_p + "'"

        if stopien_naukowy_p == "None":
            stopien_naukowy = "NULL"
        else:
            stopien_naukowy = "'" + stopien_naukowy_p + "'"

        id_uczelnia = id_uczelnia_p
        if id_uczelnia_p == "None":
            id_uczelnia = "NULL"

        self.baza.exe("INSERT INTO "
                      "osoba (imie, nazwisko, data_urodzenia, data_smierci, stopien_naukowy, id_uczelnia) "
                      "VALUES ('" + imie + "', '" + nazwisko + "', '" + data_urodzenia + "', " + data_smierci + ", " +
                      stopien_naukowy + ", " + id_uczelnia + ")")

    def update(self, rid, imie, nazwisko, data_urodzenia, data_smierci_p, stopien_naukowy_p, id_uczelnia_p):

        if data_smierci_p == "None":
            data_smierci = "NULL"
        else:
            data_smierci = "'" + data_smierci_p + "'"

        if stopien_naukowy_p == "None":
            stopien_naukowy = "NULL"
        else:
            stopien_naukowy = "'" + stopien_naukowy_p + "'"

        id_uczelnia = id_uczelnia_p
        if id_uczelnia_p == "None":
            id_uczelnia = "NULL"

        self.baza.exe("UPDATE osoba SET imie = '" + imie + "', nazwisko = '" + nazwisko + "', data_urodzenia = '" +
                      data_urodzenia + "', data_smierci = " + data_smierci + ", stopien_naukowy = " + stopien_naukowy +
                      ", id_uczelnia = " + id_uczelnia + " WHERE id = " + rid)

    def delete(self, rid):
        self.baza.exe("DELETE FROM osoba WHERE id = " + rid)
