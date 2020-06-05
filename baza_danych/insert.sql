INSERT INTO Adres(nr_budynku, ulica, miasto, kraj)
VALUES
	(1, 'Fiołkowa', 'Wałbrzych', 'Polska'),
	(14, 'Rossenstrasse', 'Berlin', 'Niemcy'),
	(37, 'Independence streat', 'Nowy Jork', 'USA'),
	(12, 'Marszałkowska', 'Warszawa', 'Polska'),
	(82, 'Seals streat', 'Shefield', 'Wielka Brytania'),
	(47, 'Warszawska', 'Kraków', 'Polska'),
	(6, 'Krakowska', 'Warszawa', 'Polska'),
	(4, 'Bydgoska', 'Gdańsk', 'Polska'),
	(35, 'Ho Chi Minh', 'Ho Chi Minh', 'Wietnam'),
	(64, 'Żółkiewskiego', 'Zamość', 'Polska');

INSERT INTO Uczelnia(nazwa, id_adres)
VALUES
	('Uniwersytet Zamoyski', 10),
	('Uniwersytet Ho Chi Minha w Ho Chi Minh', 9),
	('Brytyjska Akademia Górniczo-Morska', 5),
	('Wyższa Szkoła Paleontologiczna', 1),
	('Warszawska Akademia Krakowska', 7),
	('Krakowska Akademia Warszawska', 6);

INSERT INTO Osoba(imie, nazwisko, data_urodzenia, data_smierci, stopien_naukowy, id_uczelnia)
VALUES
	('Jacek', 'Placek', '2001-01-29', NULL, NULL, NULL),
	('Władysław', 'Pechowiec', '1988-03-10', '2019-11-14', 'drr', 1),
	('Stanisław', 'Szczeżuja', '1914-05-23', '1985-07-04', 'pro', 1),
	('Dobrmiła', 'Winnicka', '1997-06-18', NULL, 'mgr', 6),
	('Thren', 'Hao Ma', '1967-02-02', NULL, 'drh', 2),
	('John', 'Brown', '1945-04-13', '1999-12-20', 'drr', 3),
	('Alexander', 'Helmborn', '1975-10-04', NULL, 'drr', 3),
	('Hugo', 'Shwartzhafen', '1980-09-25', NULL, 'drh', NULL),
	('Jerzy', 'Koniecpolski', '1978-02-11', NULL, 'drr', NULL),
	('Xi', 'Xiao Min', '1967-02-18', NULL, 'pro', 5);

INSERT INTO Kolekcja(nazwa, id_adres)
VALUES
	('Kolekcja Skamieniałości Uniwerystetu Zamoyskiego', 10),
	('Zbiory Johna Thuma', 3),
	('Berlińskie Muzeum Paleontologiczne', 2),
	('Muzeum Historii Naturalnej w Gdańsku', 8),
	('Warszawskie Muzeum Paleontologiczne', 4),
	('Kolekcja Skamieniałości Organizmów Morskich Brytyjskiej Akademii Górniczo-Morskiej', 5);

INSERT INTO Klad(nazwa, opis, ranga, nisza, id_nadklad)
VALUES
	('ziemskie życie', 'Jedyne znane drzewo życia.', 'Drzewo Życia', NULL, NULL),
	('potomkowie LUCA', 'Wszystkie obecnie żyjące organizmy.', NULL, NULL, 1),
	('bakterie', NULL, 'Domena', NULL, 2),
	('archonty', NULL, 'Domena', NULL, 2),
	('eukarionty', NULL, 'Domena', NULL, 4),
	('zwierzęta', NULL, 'Królestwo', NULL, 5),
	('rośliny', NULL, 'Królestwo', NULL, 5),
	('grzyby', NULL, 'Królestwo', NULL, 5),
	('Prototaxitaceae', NULL, 'Rodzina', NULL, 8),
	('Prototaxites', NULL, 'Rodzaj', NULL, 9),
	('wtórouste', NULL, NULL, NULL, 6),
	('szkarłupnie', NULL, 'Typ', NULL, 11),
	('strunowce', NULL, 'Typ', NULL, 11),
	('kręgowce', NULL, NULL, NULL, 13),
	('czworonogi', NULL, NULL, NULL, 14),
	('owodniowce', NULL, NULL, NULL, 15),
	('synapsydy', NULL, 'Gromada', NULL, 16),
	('pelycosauria', NULL, 'Rząd', NULL, 17),
	('Cotylorchynchus', NULL, 'Rodzaj', NULL, 18),
	('Cotylorchynchus romeri', NULL, 'Gatunek', 'Roślinożerca', 19),
	('Cotylorchynchus hancocki', NULL, 'Gatunek', 'Roślinożerca', 19),
	('Cotylorchynchus bransoni', NULL, 'Gatunek', 'Roślinożerca', 19);

INSERT INTO Stanowisko(nazwa, okres, opis)
VALUES
	('Osówisko skalne w Chrząszczyżewąszycach', 'Perm', 'biedny doktor Pechowiec...'),
	('Plac budowy centrum handlowego w Płocku', 'Perm', 'nic specjalnego');

INSERT INTO Okaz(identyfikator, pseudonim, data_odkrycia, opis, id_klad, id_kolekcja, id_stanowisko)
VALUES
	('dsnfejfq12', 'Lary', NULL, NULL, 20, 1, 1),
	('dsnfejfq13', NULL, NULL, NULL, 20, 1, 1),
	('dsnfejfq14', NULL, NULL, NULL, 21, 1, 1),
	('dsnfejfq15', NULL, NULL, NULL, 21, 2, 2),
	('dsnfejfq16', NULL, NULL, NULL, 21, 3, 2),
	('dsnfejfq17', NULL, NULL, NULL, 22, 4, 1);

INSERT INTO Datowanie(data_wykonania, technika, wiek, id_okaz)
VALUES
	('2019-12-20', 'Argon', 275000000, 2),
	('2012-11-23', 'Argon', 274000000, 2),
	('2000-05-02', 'Argon', 273000000, 6);

INSERT INTO Czasopismo(tytul, kraj, opis)
VALUES
	('Polskie czasopismo paleontologiczne', 'Polska', NULL),
	('British Journal of Mining and Ocean', 'Wielka Brytania', NULL);

INSERT INTO Numer(numer, data_wydania, id_czasopismo)
VALUES
	(1, '2001-11-04', 1),
	(2, '2008-12-09', 1),
	(1, '2020-03-15', 2);

INSERT INTO Artykul(tytul, opis, id_numer)
VALUES
	('Śmierć pechowego doktora ujawnia skamielinę.', NULL, 1),
	('Cotylorhynchusy są fajne.', NULL, 1),
	('I like to swim and mine.', NULL, 3);

INSERT INTO Autor(id_osoba, id_artykul)
VALUES
	(3, 1),
	(4, 1),
	(3, 2),
	(7, 3);

INSERT INTO Odkrywca(id_osoba, id_okaz)
VALUES
	(2, 1);

INSERT INTO Wspomina(id_artykul, id_okaz)
VALUES
	(1, 1),
	(2, 3),
	(2, 4),
	(2, 6);