from flask import render_template, request, redirect, session


class Artykuly:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "c":
                return redirect("/artykuly/create")
            elif form_button[0] == "r":
                session["rid"] = form_button[1:]
                return redirect("/artykuly/read")
            elif form_button[0] == "u":
                session["rid"] = form_button[1:]
                return redirect("/artykuly/update")
            elif form_button[0] == "d":
                self.delete(form_button[1:])
            elif form_button[0] == "s":
                pat = request.form["pat"]
                rekordy = self.baza.ask("SELECT artykul.id, artykul.tytul, czasopismo.tytul FROM artykul "
                                        "INNER JOIN numer ON id_numer = numer.id "
                                        "AND artykul.tytul LIKE '%" + pat + "%' "
                                        "INNER JOIN czasopismo ON id_czasopismo = czasopismo.id "
                                        "ORDER BY czasopismo.tytul, artykul.tytul")
                return render_template(self.path, rekordy=rekordy)
            elif form_button[:3] == "aok":
                session["rid"] = form_button[3:]
                return redirect("/artykuly/okazy")

        rekordy = self.baza.ask("SELECT artykul.id, artykul.tytul, czasopismo.tytul FROM artykul "
                                "INNER JOIN numer ON id_numer = numer.id "
                                "INNER JOIN czasopismo ON id_czasopismo = czasopismo.id "
                                "ORDER BY czasopismo.tytul, artykul.tytul")
        return render_template(self.path, rekordy=rekordy)

    def render_create(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                tytul = request.form["tytul"]
                opis = request.form["opis"]
                id_numer = request.form["numery_wybor"]
                self.create(tytul, opis, id_numer)
                return redirect("/artykuly")
            if form_button == "anuluj":
                return redirect("/artykuly")

        numery = self.baza.ask("SELECT numer.id, tytul, numer FROM numer INNER JOIN czasopismo "
                               "ON id_czasopismo = czasopismo.id ORDER BY tytul")
        numery = [[numer[0], numer[1] + " nr. " + str(numer[2])] for numer in numery]
        return render_template("create_" + self.path, numery=numery)

    def render_read(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "wroc":
                return redirect("/artykuly")

        dane = self.baza.ask("SELECT artykul.tytul, czasopismo.tytul, numer, data_wydania, artykul.opis "
                             "FROM artykul INNER JOIN numer ON id_numer = numer.id "
                             "INNER JOIN czasopismo ON id_czasopismo = czasopismo.id AND artykul.id = " + rid)[0]
        tytul = dane[0]
        czasopismo_numer = dane[1] + " nr. " + str(dane[2])
        data = dane[3]
        opis = dane[4]
        return render_template("read_" + self.path, tytul=tytul, czasopismo_numer=czasopismo_numer, data=data,
                               opis=opis)

    def render_update(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                tytul = request.form["tytul"]
                opis = request.form["opis"]
                id_numer = request.form["numery_wybor"]
                self.update(rid, tytul, opis, id_numer)
                return redirect("/artykuly")
            if form_button == "anuluj":
                return redirect("/artykuly")

        stare_dane = self.baza.ask("SELECT artykul.tytul, artykul.opis, id_numer, czasopismo.tytul, numer "
                                   "FROM artykul INNER JOIN numer ON id_numer = numer.id "
                                   "INNER JOIN czasopismo ON id_czasopismo = czasopismo.id AND artykul.id = " + rid)[0]
        stary_tytul = stare_dane[0]
        stary_opis = stare_dane[1]
        stary_numer = [stare_dane[2], stare_dane[3] + " nr. " + str(stare_dane[4])]
        numery = self.baza.ask("SELECT numer.id, tytul, numer FROM numer INNER JOIN czasopismo "
                               "ON id_czasopismo = czasopismo.id "
                               "AND numer.id != " + str(stare_dane[2]) + " ORDER BY tytul")
        numery = [[numer[0], numer[1] + " nr. " + str(numer[2])] for numer in numery]
        return render_template("update_" + self.path, stary_tytul=stary_tytul, stary_opis=stary_opis,
                               stary_numer=stary_numer, numery=numery)

    def create(self, tytul, opis, id_numer):
        if opis != "None":
            self.baza.exe("INSERT INTO artykul (tytul, opis, id_numer) "
                          "VALUES ('" + tytul + "', '" + opis + "', " + id_numer + ")")
        else:
            self.baza.exe("INSERT INTO artykul (tytul, opis, id_numer) "
                          "VALUES ('" + tytul + "', NULL, " + id_numer + ")")

    def update(self, rid, tytul, opis, id_numer):
        if opis != "None":
            self.baza.exe("UPDATE artykul "
                          "SET tytul = '" + tytul + "', opis = '" + opis +
                          "', id_numer = " + id_numer + " WHERE id = " + rid)
        else:
            self.baza.exe("UPDATE artykul "
                          "SET tytul = '" + tytul + "', opis = NULL, id_numer = " + id_numer + " WHERE id = " + rid)

    def delete(self, rid):
        self.baza.exe("DELETE FROM artykul WHERE id = " + rid)

    def render_okazy(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "c":
                return redirect("/artykuly/okazy/add")
            elif form_button[0] == "d":
                self.delete_okaz(form_button[1:])

        rekordy = self.baza.ask("SELECT wspomina.id, identyfikator, nazwa "
                                "FROM wspomina INNER JOIN okaz ON id_okaz = okaz.id "
                                "LEFT JOIN kolekcja ON id_kolekcja = kolekcja.id "
                                "WHERE id_artykul = " + rid + " ORDER BY nazwa")
        return render_template("artykuly_okazy.html", rekordy=rekordy)

    def render_okazy_add(self):
        rid = session["rid"]
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button == "zatwierdz":
                id_okaz = request.form["okazy_wybor"]
                self.create_okaz(rid, id_okaz)
                return redirect("/artykuly/okazy")
            if form_button == "anuluj":
                return redirect("/artykuly/okazy")

        okazy = self.baza.ask("SELECT okaz.id, identyfikator || ' w: ' || nazwa "
                              "FROM okaz LEFT JOIN kolekcja ON id_kolekcja = kolekcja.id "
                              "WHERE okaz.id NOT IN "
                              "(SELECT id_okaz FROM wspomina WHERE id_artykul = " + rid + ") ORDER BY nazwa")
        return render_template("add_artykuly_okazy.html", okazy=okazy)

    def create_okaz(self, rid, id_okaz):
        self.baza.exe("INSERT INTO wspomina (id_artykul, id_okaz) VALUES (" + rid + ", " + id_okaz + ")")

    def delete_okaz(self, sid):
        self.baza.exe("DELETE FROM wspomina WHERE id = " + sid)
