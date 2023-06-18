import sys, pytest
import datetime
sys.path.append('../')
from io_kino.bd_connection import connection

def test_addMovieDetails():
    conn = connection()
    cursor = conn.cursor()

    query = 'SELECT film_id FROM filmy WHERE tytul = ? AND premiera = ?'

    cursor.execute(query, ("TITANIC", "1997-12-19" ))
    row = cursor.fetchall()
    film1_id = row[0][0]

    cursor.execute(query, ("Star Wars - The Force Awakens", "2015-12-19" ))
    row = cursor.fetchall()
    film2_id = row[0][0]

    arg1 = (
    film1_id,
    "Rok 1912, brytyjski statek Titanic wyrusza w swój dziewiczy rejs do USA. Na pokładzie emigrant Jack przypadkowo spotyka arystokratke Rose."
    )

    arg2 = (
    film2_id,
    "American epic space opera film produced, co-written, and directed by J. J. Abrams."
    )

    query = 'SELECT film_id FROM filmy_szczegoly WHERE film_id = ? AND opis = ?'

    cursor.execute(query, arg1)
    row = cursor.fetchall()
    assert row[0][0] == film1_id

    cursor.execute(query, arg2)
    row = cursor.fetchall()
    assert row[0][0] == film2_id


    cursor.close()
    conn.close()

