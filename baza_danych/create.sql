--ON UPDATE CASCADE s� niepotrzebne poniewa� kluczami s� automatycznie generowane indeksy.
--W zwi�zkach wiele-wiele zapewni� 'conalmniej jeden' tam gdzie jest potrzebne na poziomie aplikacji.

CREATE TABLE Adres(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	nr_budynku INTEGER NOT NULL CHECK(nr_budynku > 0),
	ulica VARCHAR(30) NOT NULL,
	miasto VARCHAR(30) NOT NULL,
	kraj VARCHAR(30) NOT NULL
);

ALTER TABLE Adres
ADD CONSTRAINT niepotarzalny_adres UNIQUE(nr_budynku, ulica, miasto, kraj);

CREATE TABLE Uczelnia(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	nazwa VARCHAR(100) UNIQUE NOT NULL,
	id_adres INTEGER REFERENCES Adres(id) UNIQUE NOT NULL
);

CREATE TABLE Osoba(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	imie VARCHAR(30) NOT NULL,
	nazwisko VARCHAR(30) NOT NULL,
	data_urodzenia DATE CHECK(data_urodzenia < GETDATE()) NOT NULL,
	data_smierci DATE,
	stopien_naukowy CHAR(3) CHECK(stopien_naukowy IN ('mgr', 'drr', 'drh', 'pro')),
	id_uczelnia INTEGER REFERENCES Uczelnia(id)
);

ALTER TABLE Osoba
ADD CONSTRAINT sensowan_smierc CHECK(data_smierci > data_urodzenia AND data_smierci <= GETDATE());

CREATE TABLE Kolekcja(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	nazwa VARCHAR(100) UNIQUE NOT NULL,
	id_adres INTEGER REFERENCES Adres(id) UNIQUE NOT NULL
);

CREATE TABLE Klad(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	nazwa VARCHAR(30),
	opis TEXT,
	ranga VARCHAR(30),
	nisza VARCHAR(30),
	id_nadklad INTEGER REFERENCES Klad(id)
);

ALTER TABLE Klad
ADD CONSTRAINT odpowiednia_ranga
	CHECK(ranga IN (
		'Gatunek',
		'Rodzaj',
		'Rodzina',
		'Rz�d',
		'Gromada',
		'Typ',
		'Kr�lestwo',
		'Domena',
		'Drzewo �ycia'));

ALTER TABLE Klad
ADD CONSTRAINT odpowiednia_nisza
	CHECK(nisza IN (
		'Producent',
		'Reducent',
		'Padlino�erca',
		'Owado�erca',
		'Drapie�nik',
		'Ro�lino�erca'));

ALTER TABLE Klad
ADD CONSTRAINT nisza_dla_gatunku CHECK(nisza IS NULL OR ranga = 'Gatunek');

CREATE TABLE Stanowisko(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	nazwa VARCHAR(100) UNIQUE NOT NULL,
	okres VARCHAR(30),
	opis TEXT
);

CREATE TABLE Okaz(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	identyfikator VARCHAR(30) UNIQUE NOT NULL,
	pseudonim VARCHAR(30),
	data_odkrycia DATE,
	opis TEXT,
	id_klad INTEGER REFERENCES Klad(id) NOT NULL,
	id_kolekcja INTEGER REFERENCES Kolekcja(id),
	id_stanowisko INTEGER REFERENCES Stanowisko(id)
);

CREATE TABLE Odkrywca(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	id_osoba INTEGER REFERENCES Osoba(id) ON DELETE CASCADE NOT NULL,
	id_okaz INTEGER REFERENCES Okaz(id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE Datowanie(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	data_wykonania DATE CHECK(data_wykonania <= GETDATE())NOT NULL,
	technika VARCHAR(30) NOT NULL,
	wiek INTEGER CHECK(wiek > 0) NOT NULL,
	id_okaz INTEGER REFERENCES Okaz(id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE Czasopismo(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	tytul VARCHAR(100) UNIQUE NOT NULL,
	kraj VARCHAR(30) NOT NULL,
	opis TEXT
);

CREATE TABLE Numer(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	numer INTEGER NOT NULL,
	data_wydania DATE CHECK(data_wydania <= GETDATE()) NOT NULL,
	id_czasopismo INTEGER REFERENCES Czasopismo(id) ON DELETE CASCADE NOT NULL
);

ALTER TABLE Numer
ADD CONSTRAINT niepowtarzalny_numer UNIQUE(numer, id_czasopismo);

CREATE TABLE Artykul(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	tytul VARCHAR(100) NOT NULL,
	opis TEXT,
	id_numer INTEGER REFERENCES Numer(id) ON DELETE CASCADE NOT NULL
);

ALTER TABLE Artykul
ADD CONSTRAINT niepowtarzalny_artykul UNIQUE(tytul, id_numer);

CREATE TABLE Autor(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	id_osoba INTEGER REFERENCES Osoba(id) ON DELETE CASCADE  NOT NULL,
	id_artykul INTEGER REFERENCES Artykul(id) ON DELETE CASCADE  NOT NULL
);

CREATE TABLE Wspomina(
	id INTEGER IDENTITY(0, 1) PRIMARY KEY,
	id_artykul INTEGER REFERENCES Artykul(id) ON DELETE CASCADE  NOT NULL,
	id_okaz INTEGER REFERENCES Okaz(id) ON DELETE CASCADE  NOT NULL
);
