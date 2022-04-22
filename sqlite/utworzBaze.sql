CREATE TABLE blokady (
    data_rozpoczecia           DATE NOT NULL,
    data_zakonczenia           DATE NOT NULL,
    powod                      TEXT NOT NULL,
    uzytkownicy_id_uzytkownika INTEGER NOT NULL,
	CONSTRAINT relation_3 FOREIGN KEY ( uzytkownicy_id_uzytkownika )
        REFERENCES uzytkownicy ( id_uzytkownika )
);

CREATE TABLE komentarze (
    id_komentarza              INTEGER PRIMARY KEY NOT NULL,
    tresc                      TEXT NOT NULL,
    data_dodania               DATE NOT NULL,
    uzytkownicy_id_uzytkownika INTEGER NOT NULL,
    memy_id_mema               INTEGER NOT NULL,
    komentarze_id_komentarza   INTEGER,
	CONSTRAINT relation_11 FOREIGN KEY ( komentarze_id_komentarza )
        REFERENCES komentarze ( id_komentarza ),
		CONSTRAINT relation_13 FOREIGN KEY ( memy_id_mema )
        REFERENCES memy ( id_mema ),
		CONSTRAINT relation_2 FOREIGN KEY ( uzytkownicy_id_uzytkownika )
        REFERENCES uzytkownicy ( id_uzytkownika )
);


CREATE TABLE memy (
    id_mema                    INTEGER PRIMARY KEY NOT NULL,
    nazwa_pliku                TEXT NOT NULL,
    data_dodania               DATE NOT NULL,
    uzytkownicy_id_uzytkownika INTEGER NOT NULL,
	CONSTRAINT relation_1 FOREIGN KEY ( uzytkownicy_id_uzytkownika )
        REFERENCES uzytkownicy ( id_uzytkownika )
);


CREATE TABLE oceny_komentarzy (
    jaka_ocena                 SMALLINT NOT NULL,
    uzytkownicy_id_uzytkownika INTEGER NOT NULL,
    komentarze_id_komentarza   INTEGER NOT NULL,
	CONSTRAINT relation_8 FOREIGN KEY ( uzytkownicy_id_uzytkownika )
        REFERENCES uzytkownicy ( id_uzytkownika ),
		CONSTRAINT relation_9 FOREIGN KEY ( komentarze_id_komentarza )
        REFERENCES komentarze ( id_komentarza )
);

CREATE TABLE oceny_memow (
    jaka_ocena                 SMALLINT NOT NULL,
    uzytkownicy_id_uzytkownika INTEGER NOT NULL,
    memy_id_mema               INTEGER NOT NULL,
	CONSTRAINT relation_5 FOREIGN KEY ( uzytkownicy_id_uzytkownika )
        REFERENCES uzytkownicy ( id_uzytkownika ),
		CONSTRAINT relation_6 FOREIGN KEY ( memy_id_mema )
        REFERENCES memy ( id_mema )
);

CREATE TABLE uzytkownicy (
    id_uzytkownika  INTEGER PRIMARY KEY NOT NULL,
    login           TEXT NOT NULL,
    haslo           TEXT NOT NULL,
    typ_uzytkownika SMALLINT NOT NULL,
    data_dolaczenia DATE NOT NULL
);


CREATE TABLE zgloszenia_komentarzy (
    id_zgloszenia              INTEGER NOT NULL,
    tresc                      TEXT NOT NULL,
    czy_rozpatrzony            CHAR(1) NOT NULL,
    komentarze_id_komentarza   INTEGER NOT NULL,
    uzytkownicy_id_uzytkownika INTEGER NOT NULL,
	CONSTRAINT id_komentarzy_pk PRIMARY KEY ( id_zgloszenia ),
	CONSTRAINT relation_18 FOREIGN KEY ( komentarze_id_komentarza )
        REFERENCES komentarze ( id_komentarza ),
		CONSTRAINT relation_20 FOREIGN KEY ( uzytkownicy_id_uzytkownika )
        REFERENCES uzytkownicy ( id_uzytkownika )

);


CREATE TABLE zgloszenia_memow (
    id_zgloszenia              INTEGER NOT NULL,
    tresc                      TEXT NOT NULL,
    czy_rozpatrzony            CHAR(1) NOT NULL,
    memy_id_mema               INTEGER NOT NULL,
    uzytkownicy_id_uzytkownika INTEGER NOT NULL,
	CONSTRAINT zgloszenia_pk PRIMARY KEY ( id_zgloszenia ),
	CONSTRAINT relation_17 FOREIGN KEY ( memy_id_mema )
        REFERENCES memy ( id_mema ),
		CONSTRAINT relation_19 FOREIGN KEY ( uzytkownicy_id_uzytkownika )
        REFERENCES uzytkownicy ( id_uzytkownika )
);

