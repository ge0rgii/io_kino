#!/bin/bash 

python3 $PWD/baza_danych/createTables.py;
python3 $PWD/baza_danych/createProcedures.py;
python3 $PWD/baza_danych/createFunctions.py;
python3 $PWD/baza_danych/createTriggers.py;
python3 $PWD/baza_danych/exampleData.py;

export FLASK_APP=$PWD/app/wyswietl_filmy.py
export FLASK_DEBUG=1
if [ $# ]
then
python3 -m flask run --port $1
else
python3 -m flask run
fi

