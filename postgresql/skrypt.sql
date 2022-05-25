CREATE TABLE Blokady 
    ( 
     Id_blokady SERIAL NOT NULL,
     Data_rozpoczecia DATE  NOT NULL , 
     Data_zakonczenia DATE  NOT NULL , 
     Powod TEXT  NOT NULL , 
     Uzytkownicy_Id_uzytkownika INTEGER  NOT NULL 
    ) 
;


CREATE INDEX Relation_3 ON Blokady 
    ( 
     Uzytkownicy_Id_uzytkownika ASC 
    ) 
;


CREATE TABLE Komentarze 
    ( 
     Id_komentarza SERIAL  NOT NULL  , 
     Tresc TEXT  NOT NULL , 
     Data_dodania DATE  NOT NULL , 
     Uzytkownicy_Id_uzytkownika INTEGER  NOT NULL , 
     Memy_Id_mema INTEGER  NOT NULL , 
     Komentarze_Id_komentarza INTEGER 
    ) 
;


CREATE INDEX Relation_11 ON Komentarze 
    ( 
     Komentarze_Id_komentarza ASC 
    ) 
;
CREATE INDEX Relation_13 ON Komentarze 
    ( 
     Memy_Id_mema ASC 
    ) 
;
CREATE INDEX Relation_2 ON Komentarze 
    ( 
     Uzytkownicy_Id_uzytkownika ASC 
    ) 
;

ALTER TABLE Komentarze 
    ADD CONSTRAINT Komentarze_PK PRIMARY KEY ( Id_komentarza ) ;


CREATE TABLE Memy 
    ( 
     Id_mema SERIAL  NOT NULL , 
     Nazwa_pliku TEXT  NOT NULL , 
     Data_dodania DATE  NOT NULL , 
     Uzytkownicy_Id_uzytkownika INTEGER  NOT NULL,
     Tytul TEXT  NOT NULL,
     Opis TEXT  NOT NULL,
     Kategoria TEXT  NOT NULL
    ) 
;


CREATE INDEX Relation_1 ON Memy 
    ( 
     Uzytkownicy_Id_uzytkownika ASC 
    ) 
;

ALTER TABLE Memy 
    ADD CONSTRAINT Memy_PK PRIMARY KEY ( Id_mema ) ;


CREATE TABLE Oceny_komentarzy 
    ( 
     Jaka_ocena SMALLINT  NOT NULL , 
     Uzytkownicy_Id_uzytkownika INTEGER  NOT NULL , 
     Komentarze_Id_komentarza INTEGER  NOT NULL 
    ) 
;


CREATE INDEX Relation_8 ON Oceny_komentarzy 
    ( 
     Uzytkownicy_Id_uzytkownika ASC 
    ) 
;
CREATE INDEX Relation_9 ON Oceny_komentarzy 
    ( 
     Komentarze_Id_komentarza ASC 
    ) 
;


CREATE TABLE Oceny_memow 
    ( 
     Jaka_ocena SMALLINT  NOT NULL , 
     Uzytkownicy_Id_uzytkownika INTEGER  NOT NULL , 
     Memy_Id_mema INTEGER  NOT NULL 
    ) 
;


CREATE INDEX Relation_5 ON Oceny_memow 
    ( 
     Uzytkownicy_Id_uzytkownika ASC 
    ) 
;
CREATE INDEX Relation_6 ON Oceny_memow 
    ( 
     Memy_Id_mema ASC 
    ) 
;


CREATE TABLE Uzytkownicy 
    ( 
     Id_uzytkownika SERIAL  NOT NULL , 
     Login TEXT  NOT NULL , 
     Haslo TEXT  NOT NULL ,
     Email TEXT  NOT NULL,
     Typ_uzytkownika SMALLINT  NOT NULL , 
     Data_dolaczenia DATE  NOT NULL 
    ) 
;



ALTER TABLE Uzytkownicy 
    ADD CONSTRAINT Uzytkownicy_PK PRIMARY KEY ( Id_uzytkownika ) ;


CREATE TABLE Zgloszenia_komentarzy 
    ( 
     Id_zgloszenia SERIAL  NOT NULL , 
     Tresc TEXT  NOT NULL , 
     Czy_rozpatrzony BOOLEAN  NOT NULL , 
     Komentarze_Id_komentarza INTEGER  NOT NULL , 
     Uzytkownicy_Id_uzytkownika INTEGER  NOT NULL 
    ) 
;


CREATE INDEX Relation_18 ON Zgloszenia_komentarzy 
    ( 
     Komentarze_Id_komentarza ASC 
    ) 
;
CREATE INDEX Relation_20 ON Zgloszenia_komentarzy 
    ( 
     Uzytkownicy_Id_uzytkownika ASC 
    ) 
;

ALTER TABLE Zgloszenia_komentarzy 
    ADD CONSTRAINT Id_komentarzy_PK PRIMARY KEY ( Id_zgloszenia ) ;


CREATE TABLE Zgloszenia_memow 
    ( 
     Id_zgloszenia SERIAL  NOT NULL , 
     Tresc TEXT  NOT NULL , 
     Czy_rozpatrzony BOOLEAN  NOT NULL , 
     Memy_Id_mema INTEGER  NOT NULL , 
     Uzytkownicy_Id_uzytkownika INTEGER  NOT NULL 
    ) 
;


CREATE INDEX Relation_17 ON Zgloszenia_memow 
    ( 
     Memy_Id_mema ASC 
    ) 
;
CREATE INDEX Relation_19 ON Zgloszenia_memow 
    ( 
     Uzytkownicy_Id_uzytkownika ASC 
    ) 
;

ALTER TABLE Zgloszenia_memow 
    ADD CONSTRAINT Zgloszenia_PK PRIMARY KEY ( Id_zgloszenia ) ;

ALTER TABLE Blokady 
    ADD CONSTRAINT Blokady_PK PRIMARY KEY ( Id_blokady ) ;