import sys, pytest
import datetime
sys.path.append('../')
from io_kino.bd_connection import connection

def test_addMovieScreening():
    conn = connection()
    cursor = conn.cursor()

    query = 'SELECT film_id FROM filmy WHERE tytul = ? AND premiera = ?'

    cursor.execute(query, ("Star Wars - The Force Awakens", "2015-12-19" ))
    row = cursor.fetchall()
    film1_id = row[0][0]

    cursor.execute(query, ("Spider-Man: No Way Home", "2021-10-17" ))
    row = cursor.fetchall()
    film2_id = row[0][0]

    arg1 = (
        film1_id,
        "2024-02-12 11:20:00",
        "2024-02-12 13:50:00",
        "1",
        "17"
    )

    arg2 = (
    film2_id,
    "2024-02-12 11:20:00",
    "2024-02-12 13:05:00",
    "2",
    "41"
    )

    query = 'SELECT seans_id FROM seanse_filmowe WHERE film_id = ? AND data_rozpoczecia = ? AND data_zakonczenia = ? AND sala_id = ? AND cena = ?'

    cursor.execute(query, arg1)
    row = cursor.fetchall()
    assert len(row) != 0

    cursor.execute(query, arg2)
    row = cursor.fetchall()
    assert len(row) != 0

    cursor.close()
    conn.close()




    


