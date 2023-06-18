from flask import Flask, render_template, request, redirect, g
from werkzeug.exceptions import HTTPException
import pyodbc

from bd_connection import connection
from addMovie import addMovie
from addMovieDetails import addMovieDetails
from addMovieActors import addMovieActors
from addMovieScreening import addMovieScreening
from addRate import addRate
from bookTicket import bookTicket 

wyswietl_filmy = Flask(__name__)


@wyswietl_filmy.errorhandler(Exception)
def handle_exception(e):
    # HTTP errors
    if isinstance(e, HTTPException):
        return e

    # non-HTTP exceptions
    e_msg_data = str(e).split("[SQL Server]")[1]
    e_msg = e_msg_data.split("(")[0]
    return render_template("error.html", e=e_msg), 500


@wyswietl_filmy.before_request
def before_request():
    """
    function establishing connection to database before each other function starts
    
    records connection to g.conn
    records connection cursor to g.cursor
    """
    
    g.conn = connection()
    g.cursor = g.conn.cursor()

@wyswietl_filmy.teardown_request
def teardown_request(exception):
    """function closing connection to database after each other function ends"""
    
    if hasattr(g, 'cursor'):
        g.cursor.close()
    if hasattr(g, 'conn'):
        g.conn.close()


@wyswietl_filmy.route("/")
def main():
    """function generating main page view"""
    
    filmy = []
    g.cursor.execute("SELECT * FROM wyswietl_filmy")
    for row in g.cursor.fetchall():
        filmy.append( {
                "id":       row[0], 
                "tytul":    row[1], 
                "premiera": row[2], 
                "dlugosc":  row[3],
                "ocena":  row[4]
            })
    return render_template("wyswietl_filmy.html", filmy = filmy)


@wyswietl_filmy.route("/popularne")
def popularne():
    """function views most popular movies"""
    
    filmy = []
    g.cursor.execute("SELECT * FROM wyswietl_filmy_popularne")
    for row in g.cursor.fetchall():
        filmy.append( {
                "id":       row[0], 
                "tytul":    row[1], 
                "premiera": row[2], 
                "dlugosc":  row[3]
            })
    return render_template("wyswietl_filmy_popularne.html", filmy = filmy)


@wyswietl_filmy.route("/a_wyswietl_filmy")
def a_wyswietl_filmy():
    """function generating main page view for admin"""
    
    filmy = []
    g.cursor.execute("SELECT * FROM wyswietl_filmy")
    for row in g.cursor.fetchall():
        filmy.append({
            "id":       row[0], 
            "tytul":    row[1], 
            "premiera": row[2], 
            "dlugosc":  row[3],
            "ocena":  row[4]
            })
    return render_template("a_wyswietl_filmy.html", filmy = filmy)

@wyswietl_filmy.route('/recenzje/<int:id>')
def recenzje(id):
    """function generating opinions view"""
    
    filmy = []
    g.cursor.execute("SELECT * FROM wyswietl_recenzje_filmu_po_id(?)", id)
    for row in g.cursor.fetchall():
        filmy.append({
            "tytul":            row[0], 
            "recenzja":         row[1], 
            "ocena":          row[2]
            })
    return render_template("wyswietl_filmy_recenzje.html", filmy = filmy, film_id = id)

@wyswietl_filmy.route("/dodaj_film", methods = ['GET','POST'])
def dodaj_film():
    """function generating adding film view and allowing to add new film for admin"""
    
    if request.method == 'GET':
        return render_template("dodaj_film.html", film = {})
    if request.method == 'POST':
        arg = (
            str(request.form["tytul"]),
            str(request.form["premiera"]),
            str(request.form["dlugosc"])
        )
        addMovie(arg, g.cursor)

        wyniki=[]
        for row in g.cursor.fetchall():
          wyniki.append({"w": row[0]})

        g.conn.commit()
        return render_template("wynik_dodania.html", wyniki = wyniki)

@wyswietl_filmy.route("/dodaj_recenzje/<int:id>", methods = ['GET','POST'])
def dodaj_recenzje(id):
    """function generating adding opinion view and allowing to add new opinion"""
    
    if request.method == 'GET':
        return render_template("dodaj_recenzje.html", film = {})
    if request.method == 'POST':
        arg = (
            str(id),
            str(request.form["recenzja"]),
            str(request.form["ocena"])
        )
        addRate(arg, g.cursor)

        wyniki=[]
        for row in g.cursor.fetchall():
          wyniki.append({"w": row[0]})

        g.conn.commit()
        return render_template("wynik_dodania.html", wyniki = wyniki)
        
@wyswietl_filmy.route("/a_wyswietl_filmy/rezerwacje", methods = ['GET','POST'])
def wyswietl_rezerwacje():
    """function generating searching booking view and allowing to search booking with phone number"""
    
    if request.method == 'GET':
        return render_template("rezerwacje.html")
    if request.method == 'POST':
        numer = str(request.form["numer"])
        
        rezerwacje = []
        g.cursor.execute("SELECT imie, nazwisko, email, data_rozpoczecia, tytul, liczba_biletow FROM wlasciciel_adresu_email AS e JOIN osoba AS o ON e.osoba_id = o.osoba_id JOIN wlasciciel_nr_tel AS w ON o.osoba_id = w.osoba_id JOIN zamowienia AS z ON w.osoba_id = z.osoba_id JOIN seanse_filmowe AS s ON z.seans_id = s.seans_id JOIN filmy AS f ON s.film_id = f.film_id WHERE nr_tel = " + numer)
        for row in g.cursor.fetchall():
            rezerwacje.append( {
                    "imie":    row[0],
                    "nazwisko": row[1],
                    "mail": row[2],
                    "data":    row[3],
                    "tytul": row[4],
                    "liczba":  row[5]
                })
        return render_template("rezerwacje_osoby.html", rezerwacje = rezerwacje, numer = numer)

@wyswietl_filmy.route("/a_wyswietl_filmy/sprzedaz")
def sprzedaz():
    """function generating sale raport view for admin"""
    
    sprzedaz = []
    g.cursor.execute("SELECT * FROM raport_sprzedazy")
    for row in g.cursor.fetchall():
        sprzedaz.append({
                        "id":                    row[0], 
                        "l_seans":               row[1], 
                        "srednia_cena_za_bilet": row[2], 
                        "l_sprz_biletow":        row[3], 
                        "laczny_przychod":       row[4]
                        })

    return render_template("a_sprzedaz.html", sprzedaz = sprzedaz)


@wyswietl_filmy.route("/a_wyswietl_filmy/sale_lista")
def sale_lista():
    """function generating cinema rooms list view for admin"""
    
    sale = []
    g.cursor.execute("SELECT * FROM wyswietl_sale_kinowe")
    for row in g.cursor.fetchall():
        sale.append({
            "sala_id":                       row[0], 
            "limit_miejsc":                  row[1], 
            "wejscie_dla_niepelnosprawnych": row[2], 
            "pracownik_id":                  row[3]
            })
    return render_template("a_sale.html", sale = sale)
    
@wyswietl_filmy.route("/dodaj_seans", methods = ['GET','POST'])
def dodaj_seans():
    """function generating adding screening view and allowing to add new film for admin"""
    
    if request.method == 'GET':
        return render_template("dodaj_seans.html", seans = {})
    if request.method == 'POST':
        arg = (
            str(request.form["tytul"]),
            str(request.form["premiera"]),
            str(request.form["data_rozpoczecia"]),
            str(request.form["data_zakonczenia"]),
            str(request.form["id_s"]),
            str(request.form["cena"])
        )
        addMovieScreening(arg, g.cursor)

        wyniki=[]
        for row in g.cursor.fetchall():
          wyniki.append({"w": row[0]})

        g.conn.commit()
        return render_template("wynik_dodania.html",wyniki = wyniki)


@wyswietl_filmy.route("/dodaj_aktorow", methods = ['GET','POST'])
def dodaj_aktorow():
    """function generating adding actor view and allowing to add new actor for admin"""
    
    if request.method == 'GET':
        return render_template("dodaj_aktorow.html", film = {})
    if request.method == 'POST':
        arg = [
            str(request.form["tytul"]),
            str(request.form["premiera"]),
            str(request.form["imie"]),
            str(request.form["nazwisko"]),
            str(request.form["plec"]),
            str(request.form["imie_roli"]),
            str(request.form["nazwisko_roli"]),
            str(request.form["plec_roli"])
        ]
        addMovieActors(arg, g.cursor)

        wyniki=[]
        for row in g.cursor.fetchall():
          wyniki.append({"w": row[0]})

        g.conn.commit()
        return render_template("wynik_dodania.html",wyniki = wyniki)








@wyswietl_filmy.route("/dodaj_film_szczegoly", methods = ['GET','POST'])
def dodaj_film_szczegoly():
    """function generating adding film details view and allowing to add film details for admin"""
    
    if request.method == 'GET':
        return render_template("dodaj_film_szczegoly.html", film = {})
    if request.method == 'POST':
        arg = [
            str(request.form["tytul"]),
            str(request.form["premiera"]),
            str(request.form["opis"]),
            str(request.form["recenzje"]),
            str(request.form["jezyk_oryginalny"]),
            str(request.form["jezyk_lektor"]),
            str(request.form["jezyk_napisy"]),
            str(request.form["pg_rating"])
        ]

        addMovieDetails(arg, g.cursor)

        wyniki=[]
        for row in g.cursor.fetchall():
          wyniki.append({"w": row[0]})

        g.conn.commit()
        return render_template("wynik_dodania.html",wyniki = wyniki)



@wyswietl_filmy.route('/szczegoly/<int:id>')
def szczegoly(id):
    """function generating film details view"""
    
    filmy = []
    g.cursor.execute("SELECT * FROM wyswietl_szczegoly_filmu_po_id(?)", id)
    for row in g.cursor.fetchall():
        filmy.append({
            "tytul":            row[0], 
            "premiera":         row[1], 
            "dlugosc":          row[2], 
            "opis":             row[3], 
            "recenzje":         row[4], 
            "jezyk_oryginalny": row[5], 
            "jezyk_lektor":     row[6], 
            "jezyk_napisy":     row[7], 
            "pg_rating":        row[8]
            })
    return render_template("wyswietl_filmy_szczegoly.html", filmy = filmy)


@wyswietl_filmy.route('/aktorzy/<int:id>')
def aktorzy(id):
    """function generating film actors view"""
    
    filmy = []
    g.cursor.execute("SELECT * FROM wyswietl_aktorow_filmu_po_id(?)", id)
    for row in g.cursor.fetchall():
        filmy.append({
            "tytul":        row[0], 
            "premiera":     row[1], 
            "dlugosc":      row[2], 
            "o_imie":       row[3], 
            "o_nazwisko":   row[4], 
            "o_plec":       row[5], 
            "w_roli":       row[6], 
            "r_o_imie":     row[7], 
            "r_o_nazwisko": row[8], 
            "r_o_plec":     row[9]
            })
    return render_template("wyswietl_aktorow.html", filmy = filmy)


@wyswietl_filmy.route('/seans/<int:id>')
def seans(id):
    """function generating screenings view"""
    
    seanse = []
    g.cursor.execute("SELECT * FROM wyswietl_seanse_po_id(?)", id)
    for row in g.cursor.fetchall():
        seanse.append({
            "tytul":            row[0], 
            "premiera":         row[1], 
            "dlugosc":          row[2], 
            "data_rozpoczecia": row[3], 
            "data_zakonczenia": row[4], 
            "sala_id":          row[5], 
            "seans_id":         row[6], 
            "cena":             row[7]
            })
    return render_template("wyswietl_seans.html", seanse = seanse, id = id)


@wyswietl_filmy.route('/seans/<int:id>/history')
def history(id):
    """function generating screenings view"""
    
    seanse = []
    g.cursor.execute("SELECT * FROM wyswietl_seanse_historia_po_id(?)", id)
    for row in g.cursor.fetchall():
        seanse.append({
            "tytul":            row[0], 
            "premiera":         row[1], 
            "dlugosc":          row[2], 
            "data_rozpoczecia": row[3], 
            "data_zakonczenia": row[4], 
            "sala_id":          row[5], 
            "seans_id":         row[6], 
            "cena":             row[7]
            })
    return render_template("wyswietl_seans_history.html", seanse = seanse, id = id)



@wyswietl_filmy.route('/seans/sale/<int:id>')
def sale(id):
    """function generating room view"""
    
    sale = []
    g.cursor.execute("SELECT * FROM wyswietl_sale_po_id(?)", id)
    for row in g.cursor.fetchall():
        sale.append({
            "sala_id":                       row[0], 
            "limit_miejsc":                  row[1], 
            "wejscie_dla_niepelnosprawnych": row[2]
            })
    return render_template("wyswietl_sale.html", sale = sale)



@wyswietl_filmy.route('/seans/bilety/<int:id>', methods = ['GET','POST'])
def bilety(id):
    """function generating ordering tickets view and allowing to order ticket"""
    
    if request.method == 'GET':
        seans = []
        g.cursor.execute("SELECT * FROM wyswietl_seans_po_id(?)", id)
        for row in g.cursor.fetchall():
            seans.append({
                "tytul":            row[0], 
                "premiera":         row[1], 
                "dlugosc":          row[2], 
                "data_rozpoczecia": row[3], 
                "data_zakonczenia": row[4], 
                "sala_id":          row[5], 
                "seans_id":         row[6], 
                "cena":             row[7]
                })

        g.cursor.execute("SELECT dbo.wolne_miejsca(?)", id)
        for row in g.cursor.fetchall():
            seans.append({"l": row[0]})
        return render_template("kup_bilet.html", bilet = {}, seans = seans)

    if request.method == 'POST':
        arg = [
            str(request.form["liczba_biletow"]),
            str(id),
            str(request.form["imie"]),
            str(request.form["nazwisko"]),
            str(request.form["email"]),
            str(request.form["nr_tel"]),
            str(request.form["plec"])
        ]
        bookTicket(arg, g.cursor)

        wyniki=[]
        for row in g.cursor.fetchall():
          wyniki.append({"w": row[0],})

        g.conn.commit()
        return render_template("wynik_dodania.html",wyniki = wyniki)





if(__name__ == "__main__"):
    wyswietl_filmy.run()
