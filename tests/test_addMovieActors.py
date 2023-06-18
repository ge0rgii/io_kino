import sys, pytest
import datetime
sys.path.append('../')
from io_kino.bd_connection import connection
from io_kino.addMovie import addMovie
from io_kino.addMovieActors import addMovieActors

def test_addMovie():
    conn = connection()
    cursor = conn.cursor()

    film1 = (
        "TITANIC",
        "1997-12-19",
        "03:30:00",
    )

    query = 'SELECT film_id FROM filmy WHERE tytul = ? AND premiera = ? AND dlugosc = ?'

    cursor.execute(query, film1)
    row = cursor.fetchall()
    film1_id = row[0][0]

    actor1 = (
        "KATE",
        "WINSLET" 
    )

    actor2 = (
        "BILLY",
        "ZANE"
    )
    
    actor3 = (
        "KATHY",
        "BATES"
    )
    

    query = 'SELECT osoba_id FROM osoba WHERE imie = ? AND nazwisko = ?'

    cursor.execute(query, actor1)
    row = cursor.fetchall()
    actor1_id = row[0][0]

    cursor.execute(query, actor2)
    row = cursor.fetchall()
    actor2_id = row[0][0]

    cursor.execute(query, actor3)
    row = cursor.fetchall()
    actor3_id = row[0][0]

    query = 'SELECT osoba_id FROM filmy_aktorzy WHERE film_id = ? AND osoba_id = ?'

    cursor.execute(query, (film1_id, actor1_id))
    row = cursor.fetchall()
    assert row[0][0] == actor1_id

    cursor.execute(query, (film1_id, actor2_id))
    row = cursor.fetchall()
    assert row[0][0] == actor2_id

    cursor.execute(query, (film1_id, actor3_id))
    row = cursor.fetchall()
    assert row[0][0] == actor3_id

    cursor.close()
    conn.close()