def addRate(arg, cursor):
    sql_procedura_dodaj_ocene = """ EXEC dodaj_ocene 
        @film_id=?, 
        @recenzja=?,
        @ocena=?
    """
    cursor.execute(sql_procedura_dodaj_ocene, arg)
    return cursor
