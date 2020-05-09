INSERT INTO Adres(nr_budynku, ulica, miasto, kraj)
VALUES
	(1, 'Fio³kowa', 'Wa³brzych', 'Polska'),
	(14, 'Rossenstrasse', 'Berlin', 'Niemcy'),
	(37, 'Independence streat', 'Nowy Jork', 'USA'),
	(12, 'Marsza³kowska', 'Warszawa', 'Polska'),
	(82, 'Seals streat', 'Shefield', 'Wielka Brytania'),
	(47, 'Warszawska', 'Kraków', 'Polska'),
	(6, 'Krakowska', 'Warszawa', 'Polska'),
	(4, 'Bydgoska', 'Gdañsk', 'Polska'),
	(35, 'Ho Chi Minh', 'Ho Chi Minh', 'Wietnam'),
	(64, '¯ó³kiewskiego', 'Zamoœæ', 'Polska');

INSERT INTO Uczelnia(nazwa, id_adres)
VALUES
	('Uniwersytet Zamoyski', 9),
	('Uniwersytet Ho Chi Minha w Ho Chi Minh', 8),
	('Brytyjska Akademia Górniczo-Morska', 4),
	('Wy¿sza Szko³a Paleontologiczna', 0),
	('Warszawska Akademia Krakowska', 6),
	('Krakowska Akademia Warszawska', 5);

INSERT INTO Osoba(imie, nazwisko, data_urodzenia, data_smierci, stopien_naukowy, id_uczelnia)
VALUES
	('Jacek', 'Placek', '2001-01-29', NULL, NULL, NULL),
	('W³adys³aw', 'Pechowiec', '1988-03-10', '2019-11-14', 'drr', 0),
	('Stanis³aw', 'Szcze¿uja', '1914-05-23', '1985-07-04', 'pro', 0),
	('Dobrmi³a', 'Winnicka', '1997-06-18', NULL, 'mgr', 5),
	('Thren', 'Hao Ma', '1967-02-02', NULL, 'drh', 1),
	('John', 'Brown', '1945-04-13', '1999-12-20', 'drr', 2),
	('Alexander', 'Helmborn', '1975-10-04', NULL, 'drr', 2),
	('Hugo', 'Shwartzhafen', '1980-09-25', NULL, 'drh', NULL),
	('Jerzy', 'Koniecpolski', '1978-02-11', NULL, 'drr', NULL),
	('Xi', 'Xiao Min', '1967-02-18', NULL, 'pro', 4);

INSERT INTO Kolekcja(nazwa, id_adres)
VALUES
	('Kolekcja Skamienia³oœci Uniwerystetu Zamoyskiego', 9),
	('Zbiory Johna Thuma', 2),
	('Berliñskie Muzeum Paleontologiczne', 1),
	('Muzeum Historii Naturalnej w Gdañsku', 7),
	('Warszawskie Muzeum Paleontologiczne', 3),
	('Kolekcja Skamienia³oœci Organizmów Morskich Brytyjskiej Akademii Górniczo-Morskiej', 4);

INSERT INTO Klad(nazwa, opis, ranga, nisza, id_nadklad)
VALUES
	('ziemskie ¿ycie', 'Jedyne znane drzewo ¿ycia.', 'Drzewo ¯ycia', NULL, NULL),
	('potomkowie LUCA', 'Wszystkie obecnie ¿yj¹ce organizmy.', NULL, NULL, 0),
	('bakterie', NULL, 'Domena', NULL, 1),
	('archonty', NULL, 'Domena', NULL, 1),
	('eukarionty', NULL, 'Domena', NULL, 3),
	('zwierzêta', NULL, 'Królestwo', NULL, 4),
	('roœliny', NULL, 'Królestwo', NULL, 4),
	('grzyby', NULL, 'Królestwo', NULL, 4),
	('Prototaxitaceae', NULL, 'Rodzina', NULL, 7),
	('Prototaxites', NULL, 'Rodzaj', NULL, 8),
	('wtórouste', NULL, NULL, NULL, 5),
	('szkar³upnie', NULL, 'Typ', NULL, 10),
	('strunowce', NULL, 'Typ', NULL, 10),
	('krêgowce', NULL, NULL, NULL, 12),
	('czworonogi', NULL, NULL, NULL, 13),
	('owodniowce', NULL, NULL, NULL, 14),
	('synapsydy', NULL, 'Gromada', NULL, 15),
	('pelycosauria', NULL, 'Rz¹d', NULL, 16),
	('Cotylorchynchus', NULL, 'Rodzaj', NULL, 17),
	('Cotylorchynchus romeri', NULL, 'Gatunek', 'Roœlino¿erca', 18),
	('Cotylorchynchus hancocki', NULL, 'Gatunek', 'Roœlino¿erca', 18),
	('Cotylorchynchus bransoni', NULL, 'Gatunek', 'Roœlino¿erca', 18);

INSERT INTO Stanowisko(nazwa, okres, opis)
VALUES
	('Osówisko skalne w Chrz¹szczy¿ew¹szycach', 'Perm', 'biedny doktor Pechowiec...'),
	('Plac budowy centrum handlowego w P³ocku', 'Perm', 'nic specjalnego');

INSERT INTO Okaz(identyfikator, pseudonim, data_odkrycia, opis, id_klad, id_kolekcja, id_stanowisko)
VALUES
	('dsnfejfq12', 'Lary', NULL, NULL, 19, 0, 0),
	('dsnfejfq13', NULL, NULL, NULL, 19, 0, 0),
	('dsnfejfq14', NULL, NULL, NULL, 20, 0, 0),
	('dsnfejfq15', NULL, NULL, NULL, 20, 1, 0),
	('dsnfejfq16', NULL, NULL, NULL, 20, 2, 0),
	('dsnfejfq17', NULL, NULL, NULL, 21, 3, 0);

INSERT INTO Datowanie(data_wykonania, technika, wiek, id_okaz)
VALUES
	('2019-12-20', 'Argon', 275000000, 1),
	('2012-11-23', 'Argon', 274000000, 1),
	('2000-05-02', 'Argon', 273000000, 5);

INSERT INTO Czasopismo(tytul, kraj, opis)
VALUES
	('Polskie czasopismo paleontologiczne', 'Polska', NULL),
	('British Journal of Mining and Ocean', 'Wielka Brytania', NULL);

INSERT INTO Numer(numer, data_wydania, id_czasopismo)
VALUES
	(1, '2001-11-04', 0),
	(2, '2008-12-09', 0),
	(1, '2020-03-15', 1);

INSERT INTO Artykul(tytul, opis, id_numer)
VALUES
	('Œmieræ pechowego doktora ujawnia skamielinê.', NULL, 0),
	('Cotylorhynchusy s¹ fajne.', NULL, 0),
	('I like to swim and mine.', NULL, 2);

INSERT INTO Autor(id_osoba, id_artykul)
VALUES
	(2, 0),
	(3, 0),
	(2, 1),
	(6, 2);

INSERT INTO Odkrywca(id_osoba, id_okaz)
VALUES
	(1, 0);

INSERT INTO Wspomina(id_artykul, id_okaz)
VALUES
	(0, 0),
	(1, 2),
	(1, 3),
	(1, 5);