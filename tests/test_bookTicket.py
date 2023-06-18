import sys, pytest
import datetime
sys.path.append('../')
from io_kino.bd_connection import connection

def test_bookTicket():
    conn = connection()
    cursor = conn.cursor()

    arg1 = (
    "1",
    "2",
    "Martyna",
    "Nowak"
    )

    query = 'SELECT osoba_id FROM osoba WHERE osoba.imie = ? AND osoba.nazwisko = ?'
    cursor.execute(query, (arg1[2], arg1[3]) )
    row = cursor.fetchall()
    osoba1_id = row[0][0]

    query = 'SELECT osoba.imie, osoba.nazwisko FROM zamowienia LEFT JOIN osoba ON zamowienia.osoba_id = osoba.osoba_id WHERE zamowienia.seans_id = ? AND zamowienia.osoba_id = ?'

    cursor.execute(query, (arg1[1], osoba1_id) )
    row = cursor.fetchall()
    assert row[0][0] == arg1[2] and row[0][1] == arg1[3]

    cursor.close()
    conn.close()