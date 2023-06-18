import pyodbc
import sys
sys.path.append('../')
from io_kino.bd_connection import connection 
conn = connection()
cursor = conn.cursor()




drop = """
    DROP FUNCTION IF EXISTS wyswietl_szczegoly_filmu;
    DROP FUNCTION IF EXISTS wyswietl_szczegoly_filmu_po_id;
    DROP FUNCTION IF EXISTS wyswietl_recenzje_filmu_po_id;
    DROP FUNCTION IF EXISTS wyswietl_aktorow_filmu;
    DROP FUNCTION IF EXISTS wyswietl_seanse_po_id;
    DROP FUNCTION IF EXISTS wyswietl_sale_po_id;
    DROP FUNCTION IF EXISTS wyswietl_aktorow_filmu_po_id;
    DROP FUNCTION IF EXISTS wyswietl_seans_po_id;
    DROP FUNCTION IF EXISTS wyswietl_seanse_historia_po_id;
    DROP FUNCTION IF EXISTS wyswietl_rezyserow_filmu_po_id;
    DROP FUNCTION IF EXISTS l_sprz_bilet_na_seans;
    DROP FUNCTION IF EXISTS wolne_miejsca;
    DROP VIEW IF EXISTS raport_sprzedazy;
    DROP VIEW IF EXISTS wyswietl_sale_kinowe;
    DROP VIEW IF EXISTS wyswietl_filmy;
    DROP VIEW IF EXISTS wyswietl_oceny;
    DROP VIEW IF EXISTS wyswietl_filmy_popularne;
    SET IMPLICIT_TRANSACTIONS OFF;
"""
cursor.execute(drop)

bilety = """
    CREATE FUNCTION l_sprz_bilet_na_seans (@id_seans INT)
    RETURNS INT
    AS
    BEGIN
        DECLARE @l_sprz_bilet INT
        SELECT @l_sprz_bilet = SUM(liczba_biletow)  
        FROM zamowienia WHERE seans_id=@id_seans
        RETURN @l_sprz_bilet
    END
"""
cursor.execute(bilety)



wolne_miejsca = """
    CREATE FUNCTION wolne_miejsca (@id_seans INT)
    RETURNS INT
    AS
    BEGIN
        DECLARE @l_sprz_bilet INT;
        EXEC @l_sprz_bilet = l_sprz_bilet_na_seans @id_seans
        DECLARE @limit_miejsc INT

        SELECT @limit_miejsc = limit_miejsc 
        FROM sale_kinowe 
        JOIN seanse_filmowe ON seanse_filmowe.sala_id = sale_kinowe.sala_id
        WHERE seans_id=@id_seans

        DECLARE @l_wolnych_miejsc INT
        IF @l_sprz_bilet IS NULL
            SET @l_wolnych_miejsc = @limit_miejsc
        ELSE
            SET @l_wolnych_miejsc = @limit_miejsc - @l_sprz_bilet

        RETURN @l_wolnych_miejsc
    END
"""
cursor.execute(wolne_miejsca)






wyswietl_szczegoly_filmu_po_id = """
    CREATE FUNCTION wyswietl_szczegoly_filmu_po_id (@id_F INT)
    RETURNS TABLE
    AS
    RETURN( 
        SELECT 
            filmy.tytul, 
            filmy.premiera, 
            filmy.dlugosc, 
            FS.opis, 
            FS.recenzje, 
            FS.jezyk_oryginalny, 
            FS.jezyk_lektor, 
            FS.jezyk_napisy, 
            FS.pg_rating 
        FROM filmy 
        LEFT JOIN   
            filmy_szczegoly AS FS ON FS.film_id = filmy.film_id
        WHERE filmy.film_id = @id_F
    )
"""
cursor.execute(wyswietl_szczegoly_filmu_po_id)

wyswietl_recenzje_filmu_po_id = """
    CREATE FUNCTION wyswietl_recenzje_filmu_po_id (@id_F INT)
    RETURNS TABLE
    AS
    RETURN( 
        SELECT 
            filmy.tytul, 
            oceny.recenzja, 
            oceny.ocena
        FROM filmy 
         JOIN   
            oceny ON oceny.film_id = filmy.film_id
        WHERE filmy.film_id = @id_F
    )
"""
cursor.execute(wyswietl_recenzje_filmu_po_id)


wyswietl_aktorow_filmu_po_id = """
    CREATE FUNCTION wyswietl_aktorow_filmu_po_id (@id_f INT)
    RETURNS TABLE
    AS
    RETURN ( 
        SELECT 
            filmy.tytul, 
            filmy.premiera, 
            filmy.dlugosc, 
            o.imie, 
            o.nazwisko, 
            p.plec,
            'W ROLI' AS j, 
            r_o.imie AS rola_imie, 
            r_o.nazwisko AS rola_nazwisko, 
            r_p.plec as rola_plec
        FROM filmy 
        JOIN 
            filmy_aktorzy AS FA ON FA.film_id = filmy.film_id
        JOIN 
            osoba AS o ON o.osoba_id = FA.osoba_id
        JOIN 
            osoba AS r_o ON r_o.osoba_id = FA.rola_osoba_id
        JOIN 
            plec AS p ON p.plec_id = FA.plec_id
        JOIN 
            plec AS r_p ON r_p.plec_id = FA.rola_plec_id
        WHERE filmy.film_id = @id_f
    )
"""
cursor.execute(wyswietl_aktorow_filmu_po_id)



wyswietl_seans_po_id = """
    CREATE FUNCTION wyswietl_seans_po_id (@id_s INT)
    RETURNS TABLE
    AS
    RETURN( 
        SELECT  
            filmy.tytul, 
            filmy.premiera,
            filmy.dlugosc,
            S.data_rozpoczecia,
            S.data_zakonczenia,
            S.sala_id,
            S.seans_id,
            CAST(ISNULL(S.cena,0) AS DECIMAL (19,2)) cena
        FROM filmy 
        LEFT JOIN 
            seanse_filmowe AS S ON S.film_id = filmy.film_id
        WHERE S.seans_id = @id_s
    )
"""
cursor.execute(wyswietl_seans_po_id)



wyswietl_seanse_filmu_po_id = """
    CREATE FUNCTION wyswietl_seanse_po_id (@id_f INT)
    RETURNS TABLE
    AS
    RETURN( 
        SELECT  
            filmy.tytul, 
            filmy.premiera,
            filmy.dlugosc,
            S.data_rozpoczecia,
            S.data_zakonczenia,
            S.sala_id,
            S.seans_id,
            CAST(ISNULL(S.cena,0) AS DECIMAL (19,2)) cena
        FROM filmy 
        JOIN 
            seanse_filmowe AS S ON S.film_id = filmy.film_id
        WHERE filmy.film_id = @id_f AND S.data_zakonczenia >= GETDATE()
    )
"""
cursor.execute(wyswietl_seanse_filmu_po_id)


wyswietl_seanse_historia_po_id = """
    CREATE FUNCTION wyswietl_seanse_historia_po_id (@id_f INT)
    RETURNS TABLE
    AS
    RETURN( 
        SELECT  
            filmy.tytul, 
            filmy.premiera,
            filmy.dlugosc,
            S.data_rozpoczecia,
            S.data_zakonczenia,
            S.sala_id,
            S.seans_id,
            CAST(ISNULL(S.cena,0) AS DECIMAL (19,2)) cena
        FROM filmy 
        JOIN 
            seanse_filmowe AS S ON S.film_id = filmy.film_id
        WHERE filmy.film_id = @id_f AND S.data_zakonczenia < GETDATE()
    )
"""
cursor.execute(wyswietl_seanse_historia_po_id)



wyswietl_sale_po_id = """
    CREATE FUNCTION wyswietl_sale_po_id (@sala_id INT)
    RETURNS TABLE
    AS
    RETURN( 
        SELECT  
            sala_id,
            limit_miejsc,
            wejscie_dla_niepelnosprawnych
        FROM 
            sale_kinowe
        WHERE 
            sala_id = @sala_id
    )
"""
cursor.execute(wyswietl_sale_po_id)


wyswietl_sprzedaz = """
    CREATE VIEW raport_sprzedazy
    AS
        SELECT  
            s.film_id, 
            COUNT(z.seans_id) l_seans,
            CAST(ISNULL(AVG(s.cena),0) AS DECIMAL (19,2)) srednia_cena_za_bilet,
            ISNULL(SUM(z.liczba_biletow),0) l_sprz_biletow,
            CAST(ISNULL(SUM(s.cena * z.liczba_biletow),0) AS DECIMAL (19,2)) laczny_przychod
        FROM 
            seanse_filmowe s
        LEFT JOIN 
            zamowienia z ON s.seans_id = z.seans_id
        GROUP BY 
            s.film_id
"""
cursor.execute(wyswietl_sprzedaz)

arg = """
    CREATE VIEW wyswietl_filmy_popularne
    AS
        SELECT
            TOP 5
            f.film_id,
            tytul,
            premiera,
            dlugosc
        FROM
            filmy f
        LEFT JOIN 
            seanse_filmowe AS S ON S.film_id = f.film_id
        LEFT JOIN 
            zamowienia z ON S.seans_id = z.seans_id
        GROUP BY f.film_id, tytul, premiera, dlugosc
        ORDER BY SUM(z.liczba_biletow) DESC
"""
cursor.execute(arg)


sale = """
    CREATE VIEW wyswietl_sale_kinowe
    AS
        SELECT  
            s.sala_id,
            s.limit_miejsc,
            s.wejscie_dla_niepelnosprawnych,
            s.pracownik_id
        FROM 
            sale_kinowe s
"""
cursor.execute(sale)

wyswietl_oceny= """
    CREATE VIEW wyswietl_oceny
    AS
        SELECT
            film_id,
            AVG(ocena) as ocena
        FROM oceny 
        GROUP BY film_id
"""
cursor.execute(wyswietl_oceny)

wyswietl_filmy = """
    CREATE VIEW wyswietl_filmy
    AS
        SELECT
            filmy.film_id,
            tytul,
            premiera,
            dlugosc,
            CASE WHEN ocena IS NULL THEN 'brak' ELSE CAST(ocena AS VARCHAR(10)) END AS ocena
        FROM
            filmy LEFT JOIN wyswietl_oceny ON filmy.film_id = wyswietl_oceny.film_id
"""
cursor.execute(wyswietl_filmy)








cursor.commit()
cursor.close()
conn.close()



