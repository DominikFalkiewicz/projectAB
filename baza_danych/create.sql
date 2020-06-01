--ON UPDATE CASCADE s� niepotrzebne poniewa� kluczami s� automatycznie generowane indeksy.
--W zwi�zkach wiele-wiele zapewni� 'conalmniej jeden' tam gdzie jest potrzebne na poziomie aplikacji.

CREATE TABLE Adres(
	id INTEGER PRIMARY KEY,
	nr_budynku INTEGER CHECK(nr_budynku > 0) NOT NULL,
	ulica VARCHAR(30) CHECK(LENGTH(ulica) > 0),
	miasto VARCHAR(30) CHECK(LENGTH(miasto) > 0) NOT NULL,
	kraj VARCHAR(30) CHECK(LENGTH(kraj) > 0) NOT NULL,
	UNIQUE(nr_budynku, ulica, miasto, kraj)
);

CREATE TABLE Uczelnia(
	id INTEGER PRIMARY KEY,
	nazwa VARCHAR(100) CHECK(LENGTH(nazwa) > 0) UNIQUE NOT NULL,
	id_adres INTEGER REFERENCES Adres(id) UNIQUE NOT NULL
);

CREATE TABLE Osoba(
	id INTEGER PRIMARY KEY,
	imie VARCHAR(30) CHECK(LENGTH(imie) > 0) NOT NULL,
	nazwisko VARCHAR(30) CHECK(LENGTH(nazwisko) > 0) NOT NULL,
	data_urodzenia DATE CHECK(data_urodzenia < DATE('now')) NOT NULL,
	data_smierci DATE CHECK(data_smierci <= DATE('now')),
	stopien_naukowy CHAR(3) CHECK(stopien_naukowy IN ('mgr', 'drr', 'drh', 'pro')),
	id_uczelnia INTEGER REFERENCES Uczelnia(id),
	CHECK(data_smierci > data_urodzenia AND data_smierci <= DATE('now'))
);

CREATE TABLE Kolekcja(
	id INTEGER PRIMARY KEY,
	nazwa VARCHAR(100) CHECK(LENGTH(nazwa) > 0) UNIQUE NOT NULL,
	id_adres INTEGER REFERENCES Adres(id) UNIQUE NOT NULL
);

CREATE TABLE Klad(
	id INTEGER PRIMARY KEY,
	nazwa VARCHAR(30) CHECK(LENGTH(nazwa) > 0),
	opis TEXT,
	ranga VARCHAR(30),
	nisza VARCHAR(30),
	id_nadklad INTEGER REFERENCES Klad(id),
	CHECK(ranga IN (NULL, 'Gatunek', 'Rodzaj', 'Rodzina', 'Rz�d', 'Gromada', 'Typ', 'Kr�lestwo', 'Domena',
	'Drzewo �ycia')),
	CHECK(nisza IN (NULL, 'Producent', 'Reducent', 'Padlino�erca', 'Owado�erca', 'Drapie�nik', 'Ro�lino�erca')),
	CHECK(nisza IS NULL OR ranga = 'Gatunek')
);

CREATE TABLE Stanowisko(
	id INTEGER PRIMARY KEY,
	nazwa VARCHAR(100) CHECK(LENGTH(nazwa) > 0) UNIQUE NOT NULL,
	okres VARCHAR(30) CHECK(LENGTH(okres) > 0),
	opis TEXT
);

CREATE TABLE Okaz(
	id INTEGER PRIMARY KEY,
	identyfikator VARCHAR(30) CHECK(LENGTH(identyfikator) > 0) UNIQUE NOT NULL,
	pseudonim VARCHAR(30) CHECK(LENGTH(pseudonim) > 0),
	data_odkrycia DATE CHECK(data_odkrycia <= DATE('now')),
	opis TEXT,
	id_klad INTEGER REFERENCES Klad(id) NOT NULL,
	id_kolekcja INTEGER REFERENCES Kolekcja(id) ON DELETE SET NULL,
	id_stanowisko INTEGER REFERENCES Stanowisko(id) ON DELETE SET NULL
);

CREATE TABLE Odkrywca(
	id INTEGER PRIMARY KEY,
	id_osoba INTEGER REFERENCES Osoba(id) ON DELETE CASCADE NOT NULL,
	id_okaz INTEGER REFERENCES Okaz(id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE Datowanie(
	id INTEGER PRIMARY KEY,
	data_wykonania DATE CHECK(data_wykonania <= DATE('now'))NOT NULL,
	technika VARCHAR(30) CHECK(LENGTH(technika) > 0) NOT NULL,
	wiek INTEGER CHECK(wiek > 0) NOT NULL,
	id_okaz INTEGER REFERENCES Okaz(id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE Czasopismo(
	id INTEGER PRIMARY KEY,
	tytul VARCHAR(100) CHECK(LENGTH(tytul) > 0) UNIQUE NOT NULL,
	kraj VARCHAR(30) CHECK(LENGTH(kraj) > 0) NOT NULL,
	opis TEXT
);

CREATE TABLE Numer(
	id INTEGER PRIMARY KEY,
	numer INTEGER CHECK(numer > 0) NOT NULL,
	data_wydania DATE CHECK(data_wydania <= DATE('now')) NOT NULL,
	id_czasopismo INTEGER REFERENCES Czasopismo(id) ON DELETE CASCADE NOT NULL,
	UNIQUE(numer, id_czasopismo)
);

CREATE TABLE Artykul(
	id INTEGER PRIMARY KEY,
	tytul VARCHAR(100) CHECK(LENGTH(tytul) > 0) NOT NULL,
	opis TEXT,
	id_numer INTEGER REFERENCES Numer(id) ON DELETE CASCADE NOT NULL,
	UNIQUE(tytul, id_numer)
);

CREATE TABLE Autor(
	id INTEGER PRIMARY KEY,
	id_osoba INTEGER REFERENCES Osoba(id) ON DELETE CASCADE  NOT NULL,
	id_artykul INTEGER REFERENCES Artykul(id) ON DELETE CASCADE  NOT NULL
);

CREATE TABLE Wspomina(
	id INTEGER PRIMARY KEY,
	id_artykul INTEGER REFERENCES Artykul(id) ON DELETE CASCADE  NOT NULL,
	id_okaz INTEGER REFERENCES Okaz(id) ON DELETE CASCADE  NOT NULL
);
