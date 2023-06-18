import sys
sys.path.append('../')
from io_kino.bd_connection import connection 
conn = connection()
cursor = conn.cursor()

from io_kino.addMovie import addMovie
from io_kino.addMovieDetails import addMovieDetails
from io_kino.bookTicket import bookTicket
from io_kino.addMovieDirectors import addMovieDirectors
from io_kino.addMovieActors import addMovieActors
from io_kino.addMovieScreening import addMovieScreening

# data example for tests
arg1 = (
    "Star Wars - The Force Awakens",
    "2015-12-19",
    "2:30:00",
);addMovie(arg1, cursor)

arg = (
    "Star Wars - The Force Awakens",
    "2015-12-19",
    "American epic space opera film produced, co-written, and directed by J. J. Abrams.",
    8.3,
    "angielski",
    "polski",
    "polski",
    6,
);addMovieDetails(arg, cursor)




arg2 = (
    "Spider-Man: No Way Home",
    "2021-10-17",
    "1:45:00",
);addMovie(arg2, cursor)


arg = (
    "Spider-Man: No Way Home",
    "2021-10-17",
    " American superhero film based on the Marvel Comics character Spider-Man, co-produced by Columbia Pictures and Marvel Studios and distributed by Sony Pictures Releasing.",
    5.9,
    "polski",
    "polski",
    "polski",
    5,
);addMovieDetails(arg, cursor)


arg = (
    "Spider-Man: No Way Home", "2021-10-17", 
    "Willem", "Dafoe", "mezczyzna", 
    "Green", "Goblin", "mezczyzna",
); addMovieActors(arg, cursor)



arg3 = (
    "TITANIC",
    "1997-12-19",
    "03:30:00",
);addMovie(arg3, cursor)


arg = (
    "TITANIC",
    "1997-12-19",
    "Rok 1912, brytyjski statek Titanic wyrusza w swój dziewiczy rejs do USA. Na pokładzie emigrant Jack przypadkowo spotyka arystokratke Rose.",
    7.3,
    "angielski",
    "angielski",
    "polski",
    13,
);addMovieDetails(arg, cursor)


arg = (
    "TITANIC", "1997-12-19", 
    "KATE", "WINSLET", "kobieta", 
    "ROSE", "BUKATER", "kobieta",
); addMovieActors(arg, cursor)
arg = (
    "TITANIC", "1997-12-19", 
    "BILLY", "ZANE", "mezczyzna", 
    "CALEDON", "HOCKLEY", "mezczyzna",
); addMovieActors(arg, cursor)
arg = (
    "TITANIC", "1997-12-19", 
    "KATHY", "BATES", "kobieta",
    "MOLLY", "BROWN", "kobieta", 
); addMovieActors(arg, cursor)




arg = """
    SET IMPLICIT_TRANSACTIONS OFF;
    INSERT INTO stanowiska VALUES
    ('kasjer'),
    ('osoba_sprzatajaca'),
    ('manager'),
    ('konserwator'),
    ('recepcjonista'),
    ('asystent'),
    ('ksiegowy'),
    ('radca_prawny'),
    ('informatyk'),
    ('kinooperator');

    INSERT INTO osoba VALUES('Jan', 'Kowalski');
    INSERT INTO plec VALUES('mezczyzna');
    INSERT INTO pracownicy VALUES(0, 0, '2010-01-01', 3000, 0);
    INSERT INTO osoba VALUES('Adam', 'Nowak');
    INSERT INTO pracownicy VALUES(1, 1, '2012-11-03', 3200, 0);
    INSERT INTO osoba VALUES('Adam', 'Kowalski');
    INSERT INTO pracownicy VALUES(2, 1, '2013-11-03', 3200, 0);

    INSERT INTO sale_kinowe VALUES
    (1,120,0,0),
    (2,90,0,0),
    (3,120,0,1),
    (4,180,0,2),
    (5,150,0,1);
"""
cursor.execute(arg)




arg = (
    "TITANIC",
    "1997-12-19",
    "2024-02-11 13:20:00",
    "2024-02-11 17:30:00",
    "1",
    "7"
);addMovieScreening(arg, cursor)




arg = (
    "Star Wars - The Force Awakens",
    "2015-12-19",
    "2024-02-12 11:20:00",
    "2024-02-12 13:50:00",
    "1",
    "17"
);addMovieScreening(arg, cursor)


arg = (
    "Spider-Man: No Way Home",
    "2021-10-17",
    "2024-02-12 11:20:00",
    "2024-02-12 13:05:00",
    "2",
    "41"
);addMovieScreening(arg, cursor)




arg = (
    "2",
    "1",
    "Gocha",
    "kolek",
    "Gocha.kolek@gmail.com",
    "565790555",
    "kobieta"
);bookTicket(arg, cursor)


arg = (
    "1",
    "2",
    "Martyna",
    "Nowak",
    "martyna.nowak@gmail.com",
    "565790555",
    "kobieta"
);bookTicket(arg, cursor)


arg = (
    "3",
    "0",
    "lokim",
    "turest",
    "lokim.turest@gmail.com",
    "565790555",
    "kobieta"
);bookTicket(arg, cursor)


cursor.commit()
cursor.close()
conn.close()