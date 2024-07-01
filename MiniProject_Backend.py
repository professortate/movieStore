import sqlite3

def MovieData():
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            Movie_ID text,
            Movie_Name text,
            Release_Date text,
            Director text,
            Cast text,
            Budget text,
            Duration text,
            Rating text
        )
    """)
    conn.commit()
    conn.close()

def AddMovieRec(Movie_ID, Movie_Name, Release_Date, Director, Cast, Budget, Duration, Rating):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO book VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
                (Movie_ID, Movie_Name, Release_Date, Director, Cast, Budget, Duration, Rating))
    conn.commit()
    conn.close()

def ViewMovieData():
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows

def DeleteMovieRec(id):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE id=?", (id,))
    conn.commit()
    conn.close()

def SearchMovieData(Movie_ID="", Movie_Name="", Release_Date="", Director="", Cast="", Budget="", Duration="", Rating=""):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM book WHERE Movie_ID=? OR Movie_Name=? OR Release_Date=? OR Director=? OR Cast=? OR Budget=? OR Duration=? OR Rating=?
    """, (Movie_ID, Movie_Name, Release_Date, Director, Cast, Budget, Duration, Rating))
    rows = cur.fetchall()
    conn.close()
    return rows

def UpdateMovieData(id, Movie_ID="", Movie_Name="", Release_Date="", Director="", Cast="", Budget="", Duration="", Rating=""):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE book SET Movie_ID=?, Movie_Name=?, Release_Date=?, Director=?, Cast=?, Budget=?, Duration=?, Rating=? WHERE id=?
    """, (Movie_ID, Movie_Name, Release_Date, Director, Cast, Budget, Duration, Rating, id))
    conn.commit()
    conn.close()

def SearchMovieByName(Movie_Name=""):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book WHERE Movie_Name=?", (Movie_Name,))
    rows = cur.fetchall()
    conn.close()
    return rows
