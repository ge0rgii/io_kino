import pyodbc
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
from io_kino.addRate import addRate





q = """
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
cursor.execute(q)

arg1 = (
    "TITANIC",
    "1997-12-19",
    "03:30:00",
);addMovie(arg1, cursor)

arg = (
    "TITANIC",
    "1997-12-19",
    "2024-02-11 13:20:00",
    "2024-02-11 17:30:00",
    "1",
    "22"
);addMovieScreening(arg, cursor)
arg = (
    "1",
    "0",
    "Michal",
    "Nowak",
    "michal.nowak@gmail.com",
    "655690555",
    "mezczyzna"
);bookTicket(arg, cursor)

arg = (
    "2",
    "0",
    "Karol",
    "Kowalski",
    "karol.kowalski@gmail.com",
    "755790555",
    "mezczyzna"
);bookTicket(arg, cursor)
arg = (
    "2",
    "0",
    "Martyna",
    "Nowak",
    "martyna.nowak@gmail.com",
    "565790555",
    "kobieta"
);bookTicket(arg, cursor)
arg = (
    "TITANIC",
    "1997-12-19",
    "2024-02-12 11:00:00",
    "2024-02-12 14:50:00",
    "2",
    "24"
);addMovieScreening(arg, cursor)
arg = (
    "1",
    "0",
    "Martyn",
    "Nowak",
    "martyn.nowak@wp.com",
    "544790555",
    "mezczyzna"
);bookTicket(arg, cursor)
arg = (
    "1",
    "0",
    "Agnieszka",
    "Nowak",
    "agnieszka.nowak@gmail.com",
    "562790555",
    "kobieta"
);bookTicket(arg, cursor)
arg = (
    "TITANIC",
    "1997-12-19",
    "2023-02-14 19:10:00",
    "2023-02-14 23:05:00",
    "1",
    "28"
);addMovieScreening(arg, cursor)
arg = (
    "2",
    "0",
    "Adam",
    "Adamczyk",
    "adam.adamczyk@gmail.com",
    "562110555",
    "mezczyzna"
);bookTicket(arg, cursor)

arg2 = (
    "TITANIC",
    "1997-12-19",
    "Rok 1912, brytyjski statek Titanic wyrusza w swój dziewiczy rejs do USA. Na pokładzie emigrant Jack przypadkowo spotyka arystokratke Rose.",
    7.3,
    "angielski",
    "angielski",
    "polski",
    13,
);addMovieDetails(arg2, cursor)

arg3 = (
    "TITANIC",
    "1997-12-19",
    "James",
    "Cameron",
    "mezczyzna",
    8.5
); addMovieDirectors(arg3, cursor)






addMovieActors( 
    (
        "TITANIC", "1997-12-19", 
        "LEONARDO", "DICAPRIO", "mezczyzna", 
        "JACK", "DAWSON", "mezczyzna"
    ), cursor)

arg4 = (
    "TITANIC", "1997-12-19", 
    "KATE", "WINSLET", "kobieta", 
    "ROSE", "BUKATER", "kobieta",
); addMovieActors(arg4, cursor)
arg4 = (
    "TITANIC", "1997-12-19", 
    "BILLY", "ZANE", "mezczyzna", 
    "CALEDON", "HOCKLEY", "mezczyzna",
); addMovieActors(arg4, cursor)
arg4 = (
    "TITANIC", "1997-12-19", 
    "KATHY", "BATES", "kobieta",
    "MOLLY", "BROWN", "kobieta", 
); addMovieActors(arg4, cursor)


arg1 = (
    "ZIELONA MILA", 
    "2000-03-24", 
    "03:09:00", 
)#;dodaj_film(arg1)
addMovie(arg1, cursor)

arg = (
    "ZIELONA MILA",
    "2000-03-24",
    "2023-02-18 13:05:00",
    "2023-02-18 17:10:00",
    "1",
    "17"
);addMovieScreening(arg, cursor)
arg = (
    "2",
    "3",
    "Jakub",
    "Adamczyk",
    "jakub.adamczyk@gmail.com",
    "562114455",
    "mezczyzna"
);bookTicket(arg, cursor)
arg = (
    "1",
    "3",
    "Bartek",
    "Adamczyk",
    "bartek.adamczyk@gmail.com",
    "619114455",
    "mezczyzna"
);bookTicket(arg, cursor)
arg = (
    "1",
    "3",
    "Korad",
    "Adamczyk",
    "konrat.adamczyk@gmail.com",
    "619154451",
    "mezczyzna"
);bookTicket(arg, cursor)
arg = (
    "ZIELONA MILA",
    "2000-03-24",
    "2023-02-18 15:45:00",
    "2023-02-18 18:25:00",
    "2",
    "18"
);addMovieScreening(arg, cursor)
arg = (
    "1",
    "3",
    "Bartlomiej",
    "Adamczyk",
    "bartlomiej.adamczyk@gmail.com",
    "619454452",
    "mezczyzna"
);bookTicket(arg, cursor)
arg = (
    "ZIELONA MILA",
    "2000-03-24",
    "2023-02-19 12:10:00",
    "2023-02-19 15:05:00",
    "2",
    "16"
);addMovieScreening(arg, cursor)
arg = (
    "1",
    "4",
    "Bartlomiej",
    "Nowak",
    "bartlomiej.nowak@gmail.com",
    "619454052",
    "mezczyzna"
);#bookTicket(arg, cursor)
arg = (
    "1",
    "3",
    "Bartlomiej",
    "Kowalski",
    "bartlomiej.kowalski@gmail.com",
    "619054052",
    "mezczyzna"
);bookTicket(arg, cursor)
arg = (
    "2",
    "3",
    "Karolina",
    "Kowalska",
    "karolina.kowalska@gmail.com",
    "619054952",
    "kobieta"
);bookTicket(arg, cursor)
arg = (
    "ZIELONA MILA",
    "2000-03-24",
    "2023-02-19 14:00:00",
    "2023-02-19 17:20:00",
    "1",
    "19"
);addMovieScreening(arg, cursor)
arg = (
    "ZIELONA MILA",
    "2000-03-24",
    "2023-02-19 19:05:00",
    "2023-02-19 23:15:00",
    "1",
    "22"
);addMovieScreening(arg, cursor)
arg = (
    "2",
    "4",
    "Karolina",
    "Karolska",
    "karolina.karolska@gmail.com",
    "610154952",
    "kobieta"
);bookTicket(arg, cursor)
arg2 = (
    "ZIELONA MILA", 
    "2000-03-24", 
    "Emerytowany strażnik więzienny opowiada przyjaciółce o niezwykłym mężczyźnie, którego skazano na śmierć za zabójstwo dwóch 9-letnich dziewczynek.",
    8.6,
    "angielski",
    "angielski",
    "polski",
    13,
); addMovieDetails(arg2, cursor)
arg3 = (
    "ZIELONA MILA", 
    "2000-03-24", 
    "Frank",
    "Darabont",
    "mezczyzna",
    8.6
); addMovieDirectors(arg3, cursor)



arg4 = (
    "ZIELONA MILA", "2000-03-24", 
    "TOM", "HANKS", "mezczyzna",
    "PAUL", "EDGECOMB", "mezczyzna", 
); addMovieActors(arg4, cursor)
arg4 = (
    "ZIELONA MILA", "2000-03-24", 
    "MICHAEL", "DUNCAN", "mezczyzna",
    "JOHN", "COFFEY", "mezczyzna", 
); addMovieActors(arg4, cursor)







arg1 = (
    "SKAZANI NA SHAWSHANK", 
    "1995-04-16", 
    "02:22:00", 
); addMovie(arg1, cursor)
arg4 = (
    "SKAZANI NA SHAWSHANK", "1995-04-16", 
    "TIM", "ROBBINS", "mezczyzna",
    "ANDY", "DUFRESNE", "mezczyzna", 
); addMovieActors(arg4, cursor)
arg4 = (
    "SKAZANI NA SHAWSHANK", "1995-04-16", 
    "MORGAN", "FREEMAN", "mezczyzna",
    "ELLIS", "REDDING", "mezczyzna", 
); addMovieActors(arg4, cursor)
arg4 = (
    "SKAZANI NA SHAWSHANK", "1995-04-16", 
    "BOB", "GUNTON", "mezczyzna",
    "NACZELNIK", "NORTON", "mezczyzna", 
); addMovieActors(arg4, cursor)
arg = (
    "SKAZANI NA SHAWSHANK",
    "1995-04-16",
    "2023-03-01 12:05:00",
    "2023-03-01 14:30:00",
    "1",
    "17.50"
);addMovieScreening(arg, cursor)
arg = (
    "SKAZANI NA SHAWSHANK",
    "1995-04-16",
    "2023-03-01 19:20:00",
    "2023-03-01 23:30:00",
    "1",
    "25.70"
);addMovieScreening(arg, cursor)
arg = (
    "SKAZANI NA SHAWSHANK",
    "1995-04-16",
    "2023-03-01 18:15:00",
    "2023-03-01 21:00:00",
    "2",
    "21.10"
);addMovieScreening(arg, cursor)
arg2 = (
    "SKAZANI NA SHAWSHANK", 
    "1995-04-16", 
    "Adaptacja opowiadania Stephena Kinga. Niesłusznie skazany na dożywocie bankier, stara się przetrwać w brutalnym, więziennym świecie.",
    8.8,
    "angielski",
    "polski",
    "polski",
    13,
); addMovieDetails(arg2, cursor)
arg3 = (
    "SKAZANI NA SHAWSHANK", 
    "1995-04-16", 
    "Frank",
    "Darabont",
    "mezczyzna",
    8.6
); addMovieDirectors(arg3, cursor)
arg = (
    "2",
    "7",
    "Agata",
    "Karolska",
    "agata.karolska@gmail.com",
    "610134052",
    "kobieta"
);bookTicket(arg, cursor)



arg = (
    "2",
    "8",
    "Anna",
    "Karolska",
    "anna.karolska@gmail.com",
    "610111052",
    "kobieta"
);bookTicket(arg, cursor)

arg1 = (
    "FORREST GUMP", 
    "1994-11-4", 
    "02:22:00", 
); addMovie(arg1, cursor)
arg = (
    "FORREST GUMP",
    "1994-11-4",
    "2023-03-02 12:15:00",
    "2023-03-02 14:00:00",
    "1",
    "19.45"
);addMovieScreening(arg, cursor)
arg = (
    "FORREST GUMP",
    "1994-11-4",
    "2023-03-02 18:15:00",
    "2023-03-02 21:00:00",
    "3",
    "21.10"
);addMovieScreening(arg, cursor)
arg2 = (
    "FORREST GUMP", 
    "1994-11-4", 
    "Historia życia Forresta, chłopca o niskim ilorazie inteligencji z niedowładem kończyn, który staje się miliarderem i bohaterem wojny w Wietnamie.",
    8.5,
    "angielski",
    "angielski",
    "polski",
    13,
); addMovieDetails(arg2, cursor)
arg3 = (
    "FORREST GUMP", 
    "1994-11-4", 
    "Robert",
    "Zemeckis",
    "mezczyzna",
    8.1
);addMovieDirectors(arg3, cursor)

arg4 = (
    "FORREST GUMP", "1994-11-4", 
    "TOM", "HANKS", "mezczyzna",
    "FORREST", "GUMP", "mezczyzna", 
); addMovieActors(arg4, cursor)



arg1 = (
    "LEON ZAWODOWIEC", 
    "1995-05-26", 
    "01:50:00", 
); addMovie(arg1, cursor)
arg2 = (
    "LEON ZAWODOWIEC", 
    "1995-05-26", 
    "Płatny morderca ratuje dwunastoletnią dziewczynkę, której rodzina została zabita przez skorumpowanych policjantów.",
    8.1,
    "francuski",
    "angielski",
    "polski",
    16,
); addMovieDetails(arg2, cursor)
arg3 = (
    "LEON ZAWODOWIEC", 
    "1995-05-26", 
    "Luc",
    "Besson",
    "mezczyzna",
    7.2
); addMovieDirectors(arg3, cursor)
arg4 = (
    "LEON ZAWODOWIEC", "1995-05-26", 
    "JEAN", "RENO", "mezczyzna",
    "LEON","", "mezczyzna", 
    )
addMovieActors(arg4, cursor)
arg = (
    "LEON ZAWODOWIEC",
    "1995-05-26",
    "2023-03-02 18:15:00",
    "2023-03-02 21:00:00",
    "4",
    "23.10"
);addMovieScreening(arg, cursor)



arg1 = (
    "MATRIX", 
    "1999-08-13", 
    "02:16:00", 
); addMovie(arg1, cursor)
arg2 = (
    "MATRIX", 
    "1999-08-13", 
    "Haker komputerowy Neo dowiaduje się od tajemniczych rebeliantów, że świat, w którym żyje, jest tylko obrazem przesyłanym do jego mózgu przez roboty.",
    7.6,
    "angielski",
    "angielski",
    "polski",
    15,
); addMovieDetails(arg2, cursor)
arg3 = (
    "MATRIX", 
    "1999-08-13", 
    "Lilly",
    "Wachowski",
    "kobieta",
    7.2
);addMovieDirectors(arg3, cursor)

arg3 = (
    "MATRIX", 
    "1999-08-13", 
    "Lana",
    "Wachowski",
    "kobieta",
    7.5
);addMovieDirectors(arg3, cursor)
arg = (
    "2",
    "8",
    "Dawid",
    "Nisko",
    "dawid.niski@gmail.com",
    "599921059",
    "mezczyzna"
);bookTicket(arg, cursor)
arg = (
    "2",
    "9",
    "Dawid",
    "Wysoki",
    "dawid.wysoki@gmail.com",
    "501821059",
    "mezczyzna"
);bookTicket(arg, cursor)
arg = (
    "1",
    "9",
    "Sebastian",
    "Dawid",
    "sebastian.dawid@gmail.com",
    "593121059",
    "mezczyzna"
);bookTicket(arg, cursor)


for i in range(6):
    argRate = (
        str(i),
        "niezly",
        "0"
    );addRate(argRate, cursor)

cursor.commit()
cursor.close()
conn.close()
