from flask import render_template, request, redirect, session


class Okazy:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "c":
                return redirect("/okazy/create")
            elif form_button[0] == "r":
                session["rid"] = form_button[1:]
                return redirect("/okazy/read")
            elif form_button[0] == "u":
                session["rid"] = form_button[1:]
                return redirect("/okazy/update")
            elif form_button[0] == "d":
                self.delete(form_button[1:])
            elif form_button[0] == "s":
                pat = request.form["pat"]
                rekordy = self.baza.ask("SELECT okaz.id, identyfikator, pseudonim, klad.nazwa, kolekcja.nazwa "
                                        "FROM okaz LEFT JOIN kolekcja ON id_kolekcja = kolekcja.id "
                                        "LEFT JOIN klad ON id_klad = klad.id "
                                        "WHERE identyfikator LIKE '%" + pat + "%' OR pseudonim LIKE '%" + pat + "%' "
                                        "OR klad.nazwa LIKE '%" + pat + "%' OR kolekcja.nazwa LIKE '%" + pat + "%' "
                                        "ORDER BY klad.nazwa")
                return render_template(self.path, rekordy=rekordy)
            elif form_button[:3] == "adt":
                session["rid"] = form_button[3:]
                return redirect("/okazy/datowania")
            elif form_button[:3] == "aar":
                session["rid"] = form_button[3:]
                return redirect("/okazy/artykuly")
            elif form_button[:3] == "aos":
                session["rid"] = form_button[3:]
                return redirect("/okazy/osoby")

        rekordy = self.baza.ask("SELECT okaz.id, identyfikator, pseudonim, klad.nazwa, kolekcja.nazwa "
                                "FROM okaz LEFT JOIN kolekcja ON id_kolekcja = kolekcja.id "
                                "LEFT JOIN klad ON id_klad = klad.id ORDER BY klad.nazwa")
        return render_template(self.path, rekordy=rekordy)

    def render_create(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                identyfikator = request.form["identyfikator"]
                pseudonim = request.form["pseudonim"]
                data_odkrycia = request.form["data"]
                opis = request.form["opis"]
                id_klad = request.form["klady_wybor"]
                id_kolekcja = request.form["kolekcje_wybor"]
                id_stanowisko = request.form["stanowiska_wybor"]
                self.create(identyfikator, pseudonim, data_odkrycia, opis, id_klad, id_kolekcja, id_stanowisko)
                return redirect("/okazy")
            if form_button == "anuluj":
                return redirect("/okazy")

        klady = self.baza.ask("SELECT id, nazwa FROM klad")
        kolekcje = self.baza.ask("SELECT id, nazwa FROM kolekcja")
        stanowiska = self.baza.ask("SELECT id, nazwa FROM stanowisko")
        return render_template("create_" + self.path, klady=klady, kolekcje=kolekcje, stanowiska=stanowiska)

    def render_read(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "wroc":
                return redirect("/okazy")

        dane = self.baza.ask("SELECT identyfikator, pseudonim, data_odkrycia, okaz.opis, klad.nazwa, kolekcja.nazwa, "
                             "stanowisko.nazwa FROM okaz LEFT JOIN klad ON id_klad = klad.id "
                             "LEFT JOIN kolekcja ON id_kolekcja = kolekcja.id "
                             "LEFT JOIN stanowisko ON id_stanowisko = stanowisko.id "
                             "WHERE okaz.id = " + rid)[0]
        identyfikator = dane[0]
        pseudonim = dane[1]
        data = dane[2]
        opis = dane[3]
        klad = dane[4]
        kolekcja = dane[5]
        stanowisko = dane[6]
        return render_template("read_" + self.path, identyfikator=identyfikator, pseudonim=pseudonim, data=data,
                               opis=opis, klad=klad, kolekcja=kolekcja, stanowisko=stanowisko)

    def render_update(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                identyfikator = request.form["identyfikator"]
                pseudonim = request.form["pseudonim"]
                data_odkrycia = request.form["data"]
                opis = request.form["opis"]
                id_klad = request.form["klady_wybor"]
                id_kolekcja = request.form["kolekcje_wybor"]
                id_stanowisko = request.form["stanowiska_wybor"]
                self.update(rid, identyfikator, pseudonim, data_odkrycia, opis, id_klad, id_kolekcja, id_stanowisko)
                return redirect("/okazy")
            if form_button == "anuluj":
                return redirect("/okazy")

        stare_dane = self.baza.ask("SELECT identyfikator, pseudonim, data_odkrycia, opis, id_klad, id_kolekcja, "
                                   "id_stanowisko FROM okaz WHERE okaz.id = " + rid)[0]
        stary_identyfikator = stare_dane[0]
        stary_pseudonim = stare_dane[1]
        stara_data = stare_dane[2]
        stary_opis = stare_dane[3]
        id_klad = stare_dane[4]
        id_kolekcja = stare_dane[5]
        id_stanowisko = stare_dane[6]

        stary_klad = self.baza.ask("SELECT id, nazwa FROM klad WHERE id = " + str(id_klad))[0]
        klady = self.baza.ask("SELECT id, nazwa FROM klad WHERE id != " + str(id_klad))

        if id_kolekcja is not None:
            stara_kolekcja = self.baza.ask("SELECT id, nazwa FROM kolekcja WHERE id = " + str(id_kolekcja))[0]
            kolekcje = self.baza.ask("SELECT id, nazwa FROM kolekcja WHERE id != " + str(id_kolekcja))
            kolekcje = [[kolekcja[0], kolekcja[1]] for kolekcja in kolekcje]
            kolekcje.append(["NULL", "-brak-"])
        else:
            stara_kolekcja = ["NULL", "-brak-"]
            kolekcje = self.baza.ask("SELECT id, nazwa FROM kolekcja")

        if id_stanowisko is not None:
            stare_stanowisko = self.baza.ask("SELECT id, nazwa FROM stanowisko WHERE id = " + str(id_stanowisko))[0]
            stanowiska = self.baza.ask("SELECT id, nazwa FROM stanowisko WHERE id != " + str(id_stanowisko))
            stanowiska = [[stanowisko[0], stanowisko[1]] for stanowisko in stanowiska]
            stanowiska.append(["NULL", "-brak-"])
        else:
            stare_stanowisko = ["NULL", "-brak-"]
            stanowiska = self.baza.ask("SELECT id, nazwa FROM stanowisko")

        return render_template("update_" + self.path, stary_identyfikator=stary_identyfikator,
                               stary_pseudonim=stary_pseudonim, stara_data=stara_data, stary_opis=stary_opis,
                               stary_klad=stary_klad, stara_kolekcja=stara_kolekcja, stare_stanowisko=stare_stanowisko,
                               klady=klady, kolekcje=kolekcje, stanowiska=stanowiska)

    def create(self, identyfikator, pseudonim_p, data_odkrycia_p, opis_p, id_klad, id_kolekcja_p, id_stanowisko_p):
        if pseudonim_p == "None":
            pseudonim = "NULL"
        else:
            pseudonim = "'" + pseudonim_p + "'"

        if data_odkrycia_p == "None":
            data_odkrycia = "NULL"
        else:
            data_odkrycia = "'" + data_odkrycia_p + "'"

        if opis_p == "None":
            opis = "NULL"
        else:
            opis = "'" + opis_p + "'"

        id_kolekcja = id_kolekcja_p
        if id_kolekcja_p == "None":
            id_kolekcja = "NULL"

        id_stanowisko = id_stanowisko_p
        if id_stanowisko_p == "None":
            id_stanowisko = "NULL"

        self.baza.exe("INSERT INTO "
                      "okaz (identyfikator, pseudonim, data_odkrycia, opis, id_klad, id_kolekcja, id_stanowisko) "
                      "VALUES ('" + identyfikator + "', " + pseudonim + ", " + data_odkrycia + ", " + opis + ", " +
                      id_klad + ", " + id_kolekcja + ", " + id_stanowisko + ")")

    def update(self, rid, identyfikator, pseudonim_p, data_odkrycia_p, opis_p, id_klad, id_kolekcja_p, id_stanowisko_p):
        if pseudonim_p == "None":
            pseudonim = "NULL"
        else:
            pseudonim = "'" + pseudonim_p + "'"

        if data_odkrycia_p == "None":
            data_odkrycia = "NULL"
        else:
            data_odkrycia = "'" + data_odkrycia_p + "'"

        if opis_p == "None":
            opis = "NULL"
        else:
            opis = "'" + opis_p + "'"

        id_kolekcja = id_kolekcja_p
        if id_kolekcja_p == "None":
            id_kolekcja = "NULL"

        id_stanowisko = id_stanowisko_p
        if id_stanowisko_p == "None":
            id_stanowisko = "NULL"

        self.baza.exe("UPDATE okaz SET identyfikator = '" + identyfikator + "', pseudonim = " + pseudonim +
                      ", data_odkrycia = " + data_odkrycia + ", opis = " + opis + ", id_klad = " + id_klad +
                      ", id_kolekcja = " + id_kolekcja + ", id_stanowisko = " + id_stanowisko + " WHERE id = " + rid)

    def delete(self, rid):
        self.baza.exe("DELETE FROM okaz WHERE id = " + rid)

    def render_datowania(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "c":
                return redirect("/okazy/datowania/create")
            elif form_button[0] == "d":
                self.delete_datowanie(form_button[1:])

        rekordy = self.baza.ask("SELECT id, data_wykonania, technika, wiek FROM datowanie "
                                "WHERE id_okaz = " + rid + " ORDER BY data_wykonania DESC")
        return render_template("datowania.html", rekordy=rekordy)

    def render_datowania_create(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                data_wykonania = request.form["data"]
                technika = request.form["technika"]
                wiek = request.form["wiek"]
                self.create_datowanie(rid, data_wykonania, technika, wiek)
                return redirect("/okazy/datowania")
            if form_button == "anuluj":
                return redirect("/okazy/datowania")

        return render_template("add_datowanie.html")

    def create_datowanie(self, rid, data_wykonania, technika, wiek):
        self.baza.exe("INSERT INTO datowanie (data_wykonania, technika, wiek, id_okaz) "
                      "VALUES ('" + data_wykonania + "', '" + technika + "', " + wiek + ", " + rid + ")")

    def delete_datowanie(self, sid):
        self.baza.exe("DELETE FROM datowanie WHERE id = " + sid)

    def render_artykuly(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "c":
                return redirect("/okazy/artykuly/add")
            elif form_button[0] == "d":
                self.delete_artykul(form_button[1:])

        rekordy = self.baza.ask("SELECT wspomina.id, artykul.tytul, czasopismo.tytul || ' nr. ' || numer "
                                "FROM wspomina INNER JOIN artykul ON id_artykul = artykul.id "
                                "INNER JOIN numer ON id_numer = numer.id "
                                "INNER JOIN czasopismo ON id_czasopismo = czasopismo.id "
                                "WHERE id_okaz = " + rid + " ORDER BY czasopismo.tytul")
        return render_template("okazy_artykuly.html", rekordy=rekordy)

    def render_artykuly_add(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                id_artykul = request.form["artykuly_wybor"]
                self.create_artykul(rid, id_artykul)
                return redirect("/okazy/artykuly")
            if form_button == "anuluj":
                return redirect("/okazy/artykuly")

        artykuly = self.baza.ask("SELECT artykul.id, artykul.tytul || ' w: ' || czasopismo.tytul || ' nr. ' || numer "
                                 "FROM artykul INNER JOIN numer ON id_numer = numer.id "
                                 "INNER JOIN czasopismo ON id_czasopismo = czasopismo.id "
                                 "WHERE artykul.id NOT IN "
                                 "(SELECT id_artykul FROM wspomina WHERE id_okaz = " + rid + ")")
        return render_template("add_okazy_artykuly.html", artykuly=artykuly)

    def create_artykul(self, rid, id_artykul):
        self.baza.exe("INSERT INTO wspomina (id_okaz, id_artykul) VALUES (" + rid + ", " + id_artykul + ")")

    def delete_artykul(self, sid):
        self.baza.exe("DELETE FROM wspomina WHERE id = " + sid)

    def render_osoby(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "c":
                return redirect("/okazy/osoby/add")
            elif form_button[0] == "d":
                self.delete_osoba(form_button[1:])

        rekordy = self.baza.ask("SELECT odkrywca.id, imie, nazwisko, stopien_naukowy FROM odkrywca "
                                "INNER JOIN osoba ON id_osoba = osoba.id WHERE id_okaz = " + rid + " ORDER BY nazwisko")
        return render_template("okazy_osoby.html", rekordy=rekordy)

    def render_osoby_add(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                id_osoba = request.form["osoby_wybor"]
                self.create_osoba(rid, id_osoba)
                return redirect("/okazy/osoby")
            if form_button == "anuluj":
                return redirect("/okazy/osoby")

        osoby = self.baza.ask("SELECT id, COALESCE(stopien_naukowy || '. ', '') || imie || ' ' || nazwisko FROM osoba "
                              "WHERE id NOT IN (SELECT id_osoba FROM odkrywca WHERE id_okaz = " + rid + ")")
        print(osoby)
        return render_template("add_okazy_osoby.html", osoby=osoby)

    def create_osoba(self, rid, id_osoba):
        self.baza.exe("INSERT INTO odkrywca (id_okaz, id_osoba) VALUES (" + rid + ", " + id_osoba + ")")

    def delete_osoba(self, sid):
        self.baza.exe("DELETE FROM odkrywca WHERE id = " + sid)

