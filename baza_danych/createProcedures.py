import pyodbc
import sys
sys.path.append('../')
from io_kino.bd_connection import connection 
conn = connection()
cursor = conn.cursor()




drop = """
    DROP PROCEDURE IF EXISTS dodaj_film;
    DROP PROCEDURE IF EXISTS dodaj_ocene;
    DROP PROCEDURE IF EXISTS dodaj_film_szczegoly;
    DROP PROCEDURE IF EXISTS dodaj_film_rezyserzy;
    DROP PROCEDURE IF EXISTS dodaj_film_aktorzy;
    DROP PROCEDURE IF EXISTS dodaj_seans;
    DROP PROCEDURE IF EXISTS dodaj_seans_po_id;
    DROP PROCEDURE IF EXISTS dodaj_zamowienie;
    SET IMPLICIT_TRANSACTIONS OFF;
"""
cursor.execute(drop)

proc_dodaj_zamowinie = """
CREATE PROCEDURE dodaj_zamowienie
    @liczba_biletow INT,
    @seans_id INT,
    @imie NVARCHAR(255), 
    @nazwisko NVARCHAR(255), 
    @email NVARCHAR(255), 
    @nr_tel NVARCHAR(255), 
    @plec NVARCHAR(255) 
AS
BEGIN
    IF @@TRANCOUNT = 1
        COMMIT
    BEGIN TRY
        BEGIN TRAN
            SET NOCOUNT ON

            IF EXISTS (SELECT 1 FROM seanse_filmowe WHERE seans_id=@seans_id) 
            BEGIN

                IF @liczba_biletow <= 0
                BEGIN
                    RAISERROR ('LICZBA BILETOW MUSI BYC DODATNIA' ,16,1)
                END
                ELSE
                BEGIN

                    DECLARE @l_woln_miejsc INT
                    EXEC @l_woln_miejsc = wolne_miejsca @seans_id
                    IF @liczba_biletow <= @l_woln_miejsc BEGIN

    
                            INSERT INTO osoba VALUES (
                                @imie,
                                @nazwisko
                            );
                            DECLARE @id_o AS INT = @@IDENTITY;

                            INSERT INTO wlasciciel_adresu_email VALUES(
                                @id_o,
                                @email
                            );
                            INSERT INTO wlasciciel_nr_tel VALUES(
                                @id_o,
                                @nr_tel
                            );

                            IF NOT EXISTS (SELECT plec_id FROM plec WHERE plec=@plec) BEGIN
                                INSERT INTO plec VALUES(@plec);
                            END
                            DECLARE @id_p INT = (SELECT plec_id FROM plec WHERE plec=@plec)

                            INSERT INTO zamowienia VALUES(
                                @seans_id,
                                @id_o,
                                @id_p,
                                @liczba_biletow
                            );

                            COMMIT TRAN
                            IF @@TRANCOUNT = 0
                                SELECT 'ZAMOWIENIE ZOSTALO POMYSLNIE DODANE'
                    END
                    ELSE
                    BEGIN
                        RAISERROR ('NIE MA TYLU WOLNYCH MIEJSC' ,16,1)
                    END
                END
            END
            ELSE BEGIN
                RAISERROR ('SEANS O PODANYM ID NIE ISTNIEJE' ,16,1)
            END
    END TRY
    BEGIN CATCH

        IF @@TRANCOUNT > 0
            ROLLBACK TRAN

        DECLARE @ErrorMessage NVARCHAR(4000);  
        DECLARE @ErrorSeverity INT;  
        DECLARE @ErrorState INT;  

        SELECT   
           @ErrorMessage = ERROR_MESSAGE(),  
           @ErrorSeverity = ERROR_SEVERITY(),  
           @ErrorState = ERROR_STATE();  
        RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);  
    END CATCH
END


"""
cursor.execute(proc_dodaj_zamowinie)

proc_dodaj_seans = """
CREATE PROCEDURE dodaj_seans 
    @tytul NVARCHAR(255),
    @premiera DATE,
    @data_rozpoczecia DATETIME, 
    @data_zakonczenia DATETIME, 
    @id_sala INT,
    @cena MONEY
AS
BEGIN
    BEGIN TRY
        SET NOCOUNT ON

        DECLARE @id_f AS INT = (SELECT film_id FROM filmy WHERE tytul=@tytul AND premiera=@premiera)
        IF @id_f IS NULL BEGIN
            RAISERROR ('BLAD - FILM O PODANYM TYTULE I PREMIERZE NIE ISTNIEJE W BAZIE DANYCH' ,16,1)
        END
        ELSE IF (@cena <= 0) BEGIN
            RAISERROR ('BLAD - CENA MUSI BYC DODATNIA' ,16,1)
        END
        ELSE BEGIN
            INSERT INTO seanse_filmowe VALUES (
                @id_f, 
                @data_rozpoczecia, 
                @data_zakonczenia, 
                @id_sala,
                @cena
            )
        END

    END TRY
        BEGIN CATCH
            IF @@TRANCOUNT > 0
                ROLLBACK TRAN

            DECLARE @ErrorMessage NVARCHAR(4000);  
            DECLARE @ErrorSeverity INT;  
            DECLARE @ErrorState INT;  

            SELECT   
               @ErrorMessage = ERROR_MESSAGE(),  
               @ErrorSeverity = ERROR_SEVERITY(),  
               @ErrorState = ERROR_STATE();  
            RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);  
        END CATCH
END
"""
cursor.execute(proc_dodaj_seans)


proc_dodaj_film = """
    CREATE PROCEDURE dodaj_film 
        @tytul NVARCHAR(50), 
        @premiera DATE, 
        @dlugosc time
    AS
    SET NOCOUNT ON
    INSERT INTO filmy VALUES (@tytul, @premiera, @dlugosc);
"""
cursor.execute(proc_dodaj_film)

proc_dodaj_ocene = """
    CREATE PROCEDURE dodaj_ocene
        @film_id INT, 
        @recenzja NVARCHAR(200),
        @ocena INT
    AS
    SET NOCOUNT ON
    INSERT INTO oceny VALUES (@film_id, @recenzja, @ocena);
"""
cursor.execute(proc_dodaj_ocene)

proc_dodaj_film_szczegoly = """
CREATE PROCEDURE dodaj_film_szczegoly 
    @tytul NVARCHAR(50), 
    @premiera DATE,
    @opis NVARCHAR(1000), 
    @recenzje float, 
    @jezyk_oryginalny NVARCHAR(20),
    @jezyk_lektor NVARCHAR(20), 
    @jezyk_napisy NVARCHAR(20), 
    @pg_rating INT
AS
BEGIN
    IF @@TRANCOUNT = 1
        COMMIT
    BEGIN TRY
        BEGIN TRAN
        
            SET NOCOUNT ON

                DECLARE @id_f AS INT = (SELECT film_id FROM filmy WHERE tytul=@tytul AND premiera=@premiera)
                IF @id_f IS NULL 
                BEGIN
                    RAISERROR ('ERROR - FILM O PODANYM TYTULE I PREMIERZE NIE ISTNIEJE W BAZIE DANYCH' ,16,1)
                END
                ELSE IF @recenzje < 0.0 BEGIN
                    RAISERROR ('ERROR - OCENA POWINNA BYC Z ZAKRESU 0-10' ,16,1)
                END
                ELSE IF @recenzje > 10.0 BEGIN
                    RAISERROR ('ERROR - OCENA POWINNA BYC Z ZAKRESU 0-10' ,16,1)
                END
                ELSE IF @pg_rating <= 0 BEGIN
                    RAISERROR ('ERROR - OGRANICZENIE WIEKOWE POWINNO BYC DODATNIE' ,16,1)
                END
                ELSE BEGIN
                    INSERT INTO filmy_szczegoly VALUES
                        (@id_f, @opis, @recenzje, @jezyk_oryginalny, @jezyk_lektor, @jezyk_napisy, @pg_rating)
                    COMMIT TRAN
                    IF @@TRANCOUNT = 0
                        SELECT 'SUKCES'
                END

    END TRY
        BEGIN CATCH
            IF @@TRANCOUNT > 0
                ROLLBACK TRAN

            DECLARE @ErrorMessage NVARCHAR(4000);  
            DECLARE @ErrorSeverity INT;  
            DECLARE @ErrorState INT;  

            SELECT   
               @ErrorMessage = ERROR_MESSAGE(),  
               @ErrorSeverity = ERROR_SEVERITY(),  
               @ErrorState = ERROR_STATE();  
            RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);  
        END CATCH
END
"""
cursor.execute(proc_dodaj_film_szczegoly)




proc_dodaj_film_aktorzy = """
CREATE PROCEDURE dodaj_film_aktorzy 
    @tytul NVARCHAR(50), 
    @premiera DATE,
    @imie_aktora NVARCHAR(50), 
    @nazwisko_aktora NVARCHAR(50), 
    @plec_aktora NVARCHAR(50),
    @imie_rola_aktora NVARCHAR(50), 
    @nazwisko_rola_aktora NVARCHAR(50), 
    @plec_rola_aktora NVARCHAR(50)
AS
BEGIN
    IF @@TRANCOUNT = 1
        COMMIT

    BEGIN TRY
        BEGIN TRAN

            SET NOCOUNT ON

            DECLARE @id_f AS INT = (SELECT film_id FROM filmy WHERE tytul=@tytul AND premiera=@premiera)

            IF @id_f IS NULL 
            BEGIN
                RAISERROR ('PODANY FILM NIE ISTNIEJE W BAZIE DANYCH' ,16,1)
            END
            ELSE 
            BEGIN

                DECLARE @id_o INT
                IF NOT EXISTS (SELECT 1 FROM osoba WHERE imie=@imie_aktora AND nazwisko=@nazwisko_aktora)
                BEGIN
                    INSERT INTO osoba VALUES (@imie_aktora, @nazwisko_aktora);
                    SET @id_o = @@IDENTITY
                END
                ELSE
                    SELECT @id_o = osoba_id FROM osoba WHERE imie=@imie_aktora AND nazwisko=@nazwisko_aktora


                DECLARE @id_rola_o INT
                IF NOT EXISTS (SELECT 1 FROM osoba WHERE imie=@imie_rola_aktora AND nazwisko=@nazwisko_rola_aktora)
                BEGIN
                    INSERT INTO osoba VALUES (@imie_rola_aktora, @nazwisko_rola_aktora);
                    SET @id_rola_o = @@IDENTITY
                END
                ELSE
                    SELECT @id_rola_o = osoba_id FROM osoba WHERE imie=@imie_rola_aktora AND nazwisko=@nazwisko_rola_aktora


                DECLARE @id_p INT
                IF NOT EXISTS (SELECT 1 FROM plec WHERE plec=@plec_aktora)
                BEGIN
                    INSERT INTO plec VALUES (@plec_aktora);
                    SET @id_p = @@IDENTITY
                END
                ELSE
                    SELECT @id_p = plec_id FROM plec WHERE plec=@plec_aktora


                DECLARE @id_rola_p INT
                IF NOT EXISTS (SELECT 1 FROM plec WHERE plec=@plec_rola_aktora)
                BEGIN
                    INSERT INTO plec VALUES (@plec_rola_aktora);
                    SET @id_rola_p = @@IDENTITY
                END
                ELSE
                    SELECT @id_rola_p = plec_id FROM plec WHERE plec=@plec_rola_aktora


                IF EXISTS(
                        SELECT 
                            1 
                        FROM 
                            filmy_aktorzy 
                        WHERE 
                            film_id=@id_f AND 
                            osoba_id=@id_o AND 
                            plec_id=@id_p AND 
                            rola_osoba_id=@id_rola_o AND 
                            rola_plec_id=@id_rola_p) 
                BEGIN
                    RAISERROR ('JUZ ISTNIEJE' ,16,1)
                END
                ELSE BEGIN
                    INSERT INTO 
                        filmy_aktorzy 
                    VALUES
                        (@id_f, @id_o, @id_p, @id_rola_o, @id_rola_p);


                    COMMIT TRAN
                    IF @@TRANCOUNT = 0
                        SELECT
                            'AKTOR FILMU ZOSTAL DODANY PRAWIDLOWO'

                END
            END
    END TRY
        BEGIN CATCH

            IF @@TRANCOUNT > 0
                ROLLBACK TRAN

            DECLARE @ErrorMessage NVARCHAR(4000);  
            DECLARE @ErrorSeverity INT;  
            DECLARE @ErrorState INT;  

            SELECT   
               @ErrorMessage = ERROR_MESSAGE(),  
               @ErrorSeverity = ERROR_SEVERITY(),  
               @ErrorState = ERROR_STATE();  
            RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);  
        END CATCH
END

"""
cursor.execute(proc_dodaj_film_aktorzy)






proc_dodaj_film_rezyserzy = """
CREATE PROCEDURE dodaj_film_rezyserzy 
    @tytul NVARCHAR(50), 
    @premiera DATE,
    @imie_rezysera NVARCHAR(50), 
    @nazwisko_rezysera NVARCHAR(50), 
    @plec_rezysera NVARCHAR(50),
    @ocena_rezysera float
AS
BEGIN
    IF @@TRANCOUNT = 1
        COMMIT
    SET NOCOUNT ON

    DECLARE @id_f AS INT = (SELECT film_id FROM filmy WHERE tytul=@tytul AND premiera=@premiera);

    IF @id_f IS NOT NULL 
    BEGIN

        BEGIN TRY
            BEGIN TRAN  

            DECLARE @id_o INT
            IF NOT EXISTS (SELECT 1 FROM osoba WHERE imie=@imie_rezysera AND nazwisko=@nazwisko_rezysera)
            BEGIN
                INSERT INTO osoba VALUES (@imie_rezysera, @nazwisko_rezysera);
                SET @id_o = @@IDENTITY
            END
            ELSE
                SELECT @id_o = osoba_id FROM osoba WHERE imie=@imie_rezysera AND nazwisko=@nazwisko_rezysera

            DECLARE @id_p INT
            IF NOT EXISTS (SELECT 1 FROM plec WHERE plec=@plec_rezysera)
            BEGIN
                INSERT INTO plec VALUES (@plec_rezysera);
                SET @id_p = @@IDENTITY
            END
            ELSE
                SELECT @id_p = plec_id FROM plec WHERE plec=@plec_rezysera

            IF NOT EXISTS(
                SELECT 
                    1 
                FROM 
                    filmy_rezyserzy 
                WHERE 
                    film_id=@id_f AND 
                    osoba_id=@id_o AND 
                    plec_id=@id_p AND 
                    ocena_rezysera=@ocena_rezysera) 
            BEGIN
                INSERT INTO filmy_rezyserzy VALUES
                    (@id_f, @id_o, @id_p, @ocena_rezysera);
                SELECT 'REZYSER FILMU ZOSTAL DODANY PRAWIDLOWO'
                COMMIT TRAN
            END
            ELSE
                SELECT 'JUZ ISTNIEJE'

        END TRY
            BEGIN CATCH

                IF @@TRANCOUNT > 0
                    ROLLBACK TRAN

                DECLARE @ErrorMessage NVARCHAR(4000);  
                DECLARE @ErrorSeverity INT;  
                DECLARE @ErrorState INT;  

                SELECT   
                   @ErrorMessage = ERROR_MESSAGE(),  
                   @ErrorSeverity = ERROR_SEVERITY(),  
                   @ErrorState = ERROR_STATE();  
                RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);  
            END CATCH
        
    END
    ELSE
        SELECT 'PODANY FILM NIE ISTNIEJE W BAZIE DANYCH'
END

"""
cursor.execute(proc_dodaj_film_rezyserzy)





cursor.commit()
cursor.close()
conn.close()

