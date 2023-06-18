import sys, pytest
import datetime
sys.path.append('../')
from io_kino.bd_connection import connection

def test_raport():
    conn = connection()
    cursor = conn.cursor()

    query = 'SELECT SUM(cena * liczba_biletow) FROM zamowienia LEFT JOIN seanse_filmowe ON zamowienia.seans_id = seanse_filmowe.seans_id'

    cursor.execute(query)
    row = cursor.fetchall()
    assert row[0][0] == 96


    cursor.close()
    conn.close()