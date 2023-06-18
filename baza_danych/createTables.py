import pyodbc
import sys
sys.path.append('../')
from io_kino.bd_connection import connection 
conn = connection()
cursor = conn.cursor()





drop_tables = """
    IF OBJECT_ID('zamowienia',N'U') IS NOT NULL DROP TABLE zamowienia
    IF OBJECT_ID('pracownicy_szczegoly',N'U') IS NOT NULL DROP TABLE pracownicy_szczegoly 
    IF OBJECT_ID('filmy_szczegoly',N'U') IS NOT NULL DROP TABLE filmy_szczegoly
    IF OBJECT_ID('filmy_aktorzy',N'U') IS NOT NULL DROP TABLE filmy_aktorzy
    IF OBJECT_ID('filmy_pomocnicy',N'U') IS NOT NULL DROP TABLE filmy_pomocnicy
    IF OBJECT_ID('filmy_rezyserzy',N'U') IS NOT NULL DROP TABLE filmy_rezyserzy


    IF OBJECT_ID('seanse_filmowe',N'U') IS NOT NULL DROP TABLE seanse_filmowe 
    IF OBJECT_ID('sale_kinowe',N'U') IS NOT NULL DROP TABLE sale_kinowe 
    
    IF OBJECT_ID('oceny',N'U') IS NOT NULL DROP TABLE oceny 
    IF OBJECT_ID('filmy',N'U') IS NOT NULL DROP TABLE filmy 

    IF OBJECT_ID('stanowiska',N'U') IS NOT NULL DROP TABLE stanowiska 
    IF OBJECT_ID('pracownicy',N'U') IS NOT NULL DROP TABLE pracownicy 

    IF OBJECT_ID('wlasciciel_nr_tel',N'U') IS NOT NULL DROP TABLE wlasciciel_nr_tel 
    IF OBJECT_ID('wlasciciel_adresu_email',N'U') IS NOT NULL DROP TABLE wlasciciel_adresu_email
    IF OBJECT_ID('osoba_adres',N'U') IS NOT NULL DROP TABLE osoba_adres
    IF OBJECT_ID('osoba',N'U') IS NOT NULL DROP TABLE osoba 
    IF OBJECT_ID('plec',N'U') IS NOT NULL DROP TABLE plec 
    DROP PROCEDURE IF EXISTS UzupelnijDaneFilmow;
"""
cursor.execute(drop_tables)




osoba = """
    CREATE TABLE osoba (
        osoba_id INT IDENTITY(0,1) PRIMARY KEY,
        imie NVARCHAR(50),
        nazwisko NVARCHAR(50),
    );
    CREATE TABLE plec (
        plec_id INT IDENTITY(0,1) PRIMARY KEY,
        plec NVARCHAR(50),
    );
    -- jedna osoba moze miec kilka numerow tel
    CREATE TABLE wlasciciel_nr_tel (
        osoba_id INT FOREIGN KEY REFERENCES osoba(osoba_id),
        nr_tel NVARCHAR(9),
    );
    CREATE TABLE wlasciciel_adresu_email (
        osoba_id INT FOREIGN KEY REFERENCES osoba(osoba_id),
        email NVARCHAR(255),
    );
    CREATE TABLE osoba_adres (
        osoba_id INT FOREIGN KEY REFERENCES osoba(osoba_id),
        kraj_zamieszkania NVARCHAR(50),
        miasto_zamieszkania NVARCHAR(50),
        kod_pocztowy NVARCHAR(15),
        ulica NVARCHAR(30),
        nr_budynku NVARCHAR(8),
    );
"""
cursor.execute(osoba)




pracownicy = """
    CREATE TABLE stanowiska (
        stanowisko_id INT IDENTITY(0,1) PRIMARY KEY,
        nazwa_stanowiska NVARCHAR(50),
    );

    CREATE TABLE pracownicy (
        pracownik_id INT IDENTITY(0,1) PRIMARY KEY,
        osoba_id INT FOREIGN KEY REFERENCES osoba(osoba_id),
        stanowisko_id INT FOREIGN KEY REFERENCES osoba(osoba_id),
        data_zatrudnienia DATE,
        wynagrodzenie MONEY,
        plec_id INT FOREIGN KEY REFERENCES plec(plec_id)
    );
"""
cursor.execute(pracownicy)




sale_kinowe = """
    IF OBJECT_ID('sale_kinowe',N'U') IS NOT NULL DROP TABLE sale_kinowe 
    CREATE TABLE sale_kinowe(
        sala_id INT PRIMARY KEY,
        limit_miejsc INT NOT NULL,
        wejscie_dla_niepelnosprawnych BIT,
        pracownik_id int FOREIGN KEY REFERENCES pracownicy(pracownik_id)
    );
"""
cursor.execute(sale_kinowe)


filmy = """
    CREATE TABLE filmy (
        film_id INT IDENTITY(0,1) PRIMARY KEY,
        tytul NVARCHAR(50),
        premiera DATE,
        dlugosc time
    );
    CREATE TABLE oceny (
        id INT IDENTITY(0,1) PRIMARY KEY,
        film_id INT FOREIGN KEY REFERENCES filmy(film_id),
        recenzja NVARCHAR(200),
        ocena INT
    );
    CREATE TABLE filmy_szczegoly (
        film_id INT FOREIGN KEY REFERENCES filmy(film_id),
        opis NVARCHAR(1000),
        recenzje float CHECK (recenzje >= 0.0), CHECK (recenzje <= 10),
        jezyk_oryginalny NVARCHAR(20),
        jezyk_lektor NVARCHAR(20),
        jezyk_napisy NVARCHAR(20),
        pg_rating INT CHECK (pg_rating > 0)
    );
    CREATE TABLE filmy_rezyserzy (
        film_id INT FOREIGN KEY REFERENCES filmy(film_id),
        osoba_id INT FOREIGN KEY REFERENCES osoba(osoba_id),
        plec_id INT FOREIGN KEY REFERENCES plec(plec_id),
        ocena_rezysera float CHECK (ocena_rezysera > 0.0)
    );
    CREATE TABLE filmy_aktorzy (
        film_id INT FOREIGN KEY REFERENCES filmy(film_id),
        osoba_id INT FOREIGN KEY REFERENCES osoba(osoba_id),
        plec_id INT FOREIGN KEY REFERENCES plec(plec_id),
        rola_osoba_id INT FOREIGN KEY REFERENCES osoba(osoba_id),
        rola_plec_id INT FOREIGN KEY REFERENCES plec(plec_id),
    );
"""
cursor.execute(filmy)


seanse_filmowe = """
    IF OBJECT_ID('seanse_filmowe',N'U') IS NOT NULL DROP TABLE seanse_filmowe 
    CREATE TABLE seanse_filmowe (
        seans_id INT IDENTITY(0,1) PRIMARY KEY,
        film_id INT FOREIGN KEY REFERENCES filmy(film_id),
        data_rozpoczecia DATETIME,
        data_zakonczenia DATETIME,
        sala_id int FOREIGN KEY REFERENCES sale_kinowe(sala_id),
        cena MONEY CHECK (cena > 0)
    );
"""
cursor.execute(seanse_filmowe)

zamowienia = """
    CREATE TABLE zamowienia (
        seans_id INT FOREIGN KEY REFERENCES seanse_filmowe(seans_id),
        osoba_id INT FOREIGN KEY REFERENCES osoba(osoba_id),
        plec_id INT FOREIGN KEY REFERENCES plec(plec_id),
        liczba_biletow INT
    );
"""
cursor.execute(zamowienia)

cursor.commit()
cursor.close()
conn.close()
