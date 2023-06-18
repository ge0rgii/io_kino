import sys, pytest
import datetime
sys.path.append('../')
from io_kino.bd_connection import connection

def test_addMovie():
    conn = connection()
    cursor = conn.cursor()

    arg1 = (
        "Star Wars - The Force Awakens",
        "2015-12-19",
        "2:30:00",
        )
    
    arg2 = (
        "Spider-Man: No Way Home",
        "2021-10-17",
        "1:45:00",
    )

    arg3 = (
        "TITANIC",
        "1997-12-19",
        "03:30:00",
    )
    
    query = 'SELECT tytul, premiera FROM filmy WHERE tytul = ? AND premiera = ? AND dlugosc = ?'

    cursor.execute(query, arg1)
    row = cursor.fetchall()
    assert row[0][0] == arg1[0] and row[0][1].strftime('%Y-%m-%d') == arg1[1]

    cursor.execute(query, arg2)
    row = cursor.fetchall()
    assert row[0][0] == arg2[0] and row[0][1].strftime('%Y-%m-%d') == arg2[1]

    cursor.execute(query, arg3)
    row = cursor.fetchall()
    assert row[0][0] == arg3[0] and row[0][1].strftime('%Y-%m-%d') == arg3[1]

    query = 'SELECT film_id FROM filmy WHERE film_id = 3'
    row = cursor.fetchall()
    assert len(row) == 0
     
    cursor.close()
    conn.close()