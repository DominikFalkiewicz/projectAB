from flask import render_template


class Stats:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        rekordy1 = []

        lo = self.baza.ask("SELECT COUNT(*) FROM osoba")[0][0]
        rekordy1.append(["Liczba Osób", lo])

        ln = self.baza.ask("SELECT COUNT(*) FROM osoba WHERE id_uczelnia IS NOT NULL")[0][0]
        rekordy1.append(["Liczba Naukowców", ln])

        sw = self.baza.ask("SELECT "
                           "AVG(strftime('%Y', COALESCE(data_smierci, DATE('now'))) - strftime('%Y', data_urodzenia)) "
                           "FROM osoba")[0][0]
        rekordy1.append(["Średni Wiek", sw])

        na = self.baza.ask("SELECT imie, nazwisko, stopien_naukowy, COUNT(*) as l "
                           "FROM osoba INNER JOIN autor ON id_osoba = osoba.id "
                           "GROUP BY osoba.id, imie, nazwisko, stopien_naukowy ORDER BY l DESC LIMIT 1")[0]
        if na[0] is None:
            na = na[0] + " " + na[1] + ", " + str(na[3]) + " artykułów"
        else:
            na = na[2] + ". " + na[0] + " " + na[1] + ", " + str(na[3]) + " artykułów"
        rekordy1.append(["Najlepszy autor", na])

        no = self.baza.ask("SELECT imie, nazwisko, stopien_naukowy, COUNT(*) as l "
                           "FROM osoba INNER JOIN odkrywca ON id_osoba = osoba.id "
                           "GROUP BY osoba.id, imie, nazwisko, stopien_naukowy ORDER BY l DESC LIMIT 1")[0]
        if na[0] is None:
            no = no[0] + " " + no[1] + ", " + str(no[3]) + " skamielin"
        else:
            no = no[2] + ". " + no[0] + " " + no[1] + ", " + str(no[3]) + " skamielin"
        rekordy1.append(["Najlepszy odkrywca", no])

        rekordy1.append(["", ""])

        nr = self.baza.ask("SELECT nadklad.nazwa, COUNT(*) AS l FROM klad AS nadklad "
                           "INNER JOIN klad ON nadklad.id = klad.id_nadklad GROUP BY nadklad.id, nadklad.nazwa "
                           "ORDER BY l DESC LIMIT 1")[0]
        rekordy1.append(["Najbardziej rozgałęziony klad", nr[0] + ", " + str(nr[1]) + " podkladów"])
        ns = self.baza.ask("SELECT nazwa, COUNT(*) AS l FROM okaz INNER JOIN klad ON id_klad = klad.id "
                           "WHERE ranga = 'Gatunek' GROUP BY klad.id, nazwa ORDER BY l DESC LIMIT 1")[0]
        rekordy1.append(["Najczęstszy gatunek", ns[0] + ", " + str(ns[1]) + " okazów"])

        rekordy1.append(["", ""])

        nu = self.baza.ask("SELECT nazwa, COUNT(*) AS l FROM uczelnia INNER JOIN osoba ON id_uczelnia = uczelnia.id "
                           "GROUP BY uczelnia.id, nazwa ORDER BY l DESC LIMIT 1")[0]
        rekordy1.append(["Najpopularniejsza uczelnia", nu[0] + ", " + str(nu[1]) + " pracowników"])

        rekordy1.append(["", ""])

        nk = self.baza.ask("SELECT nazwa, COUNT(*) AS l FROM kolekcja INNER JOIN okaz ON id_kolekcja = kolekcja.id "
                           "GROUP BY kolekcja.id, nazwa ORDER BY l DESC LIMIT 1")[0]
        rekordy1.append(["Największa kolekcja", nk[0] + ", " + str(nk[1]) + " okazów"])

        rekordy1.append(["", ""])

        ns = self.baza.ask("SELECT nazwa, COUNT(*) AS l FROM stanowisko "
                           "INNER JOIN okaz ON id_stanowisko = stanowisko.id "
                           "GROUP BY stanowisko.id, nazwa ORDER BY l DESC LIMIT 1")[0]
        rekordy1.append(["Najzasobniejsze zbiorowisko", ns[0] + ", " + str(ns[1]) + " okazów"])

        rekordy1.append(["", ""])

        nc = self.baza.ask("SELECT czasopismo.tytul, COUNT(*) AS l FROM czasopismo "
                           "INNER JOIN numer ON id_czasopismo = czasopismo.id "
                           "INNER JOIN artykul ON id_numer = numer.id "
                           "GROUP BY czasopismo.id, czasopismo.tytul ORDER BY l DESC LIMIT 1")[0]
        rekordy1.append(["Najpopularniejsze czasopismo", nc[0] + ", " + str(nc[1]) + " artykułów"])

        return render_template(self.path, rekordy1=rekordy1)
