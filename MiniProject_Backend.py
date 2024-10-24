import sqlite3
from datetime import datetime

def initialize_db():
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Movies (
            id INTEGER PRIMARY KEY,
            Movie_ID TEXT UNIQUE,
            Movie_Name TEXT,
            Release_Date TEXT
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Directors (
            id INTEGER PRIMARY KEY,
            Director_Name TEXT UNIQUE
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Casts (
            id INTEGER PRIMARY KEY,
            Cast_Name TEXT UNIQUE
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS MovieDetails (
            id INTEGER PRIMARY KEY,
            Movie_ID TEXT,
            Director_ID INTEGER,
            Budget TEXT,
            Duration TEXT,
            Rating TEXT,
            FOREIGN KEY (Movie_ID) REFERENCES Movies (Movie_ID),
            FOREIGN KEY (Director_ID) REFERENCES Directors (id)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS MovieCasts (
            id INTEGER PRIMARY KEY,
            Movie_ID TEXT,
            Cast_ID INTEGER,
            FOREIGN KEY (Movie_ID) REFERENCES Movies (Movie_ID),
            FOREIGN KEY (Cast_ID) REFERENCES Casts (id)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Bookings (
            id INTEGER PRIMARY KEY,
            movie_name TEXT,
            seat_number INTEGER,
            customer_name TEXT,
            booking_date TEXT
        )
    """)
    
    conn.commit()
    conn.close()

initialize_db()

def AddMovieRec(Movie_ID, Movie_Name, Release_Date, Director, Cast, Budget, Duration, Rating):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO Movies (Movie_ID, Movie_Name, Release_Date) VALUES (?, ?, ?)",
                (Movie_ID, Movie_Name, Release_Date))

    cur.execute("INSERT OR IGNORE INTO Directors (Director_Name) VALUES (?)", (Director,))
    cur.execute("SELECT id FROM Directors WHERE Director_Name=?", (Director,))
    Director_ID = cur.fetchone()[0]

    cur.execute("INSERT INTO MovieDetails (Movie_ID, Director_ID, Budget, Duration, Rating) VALUES (?, ?, ?, ?, ?)",
                (Movie_ID, Director_ID, Budget, Duration, Rating))

    for actor in Cast.split(','):
        cur.execute("INSERT OR IGNORE INTO Casts (Cast_Name) VALUES (?)", (actor.strip(),))
        cur.execute("SELECT id FROM Casts WHERE Cast_Name=?", (actor.strip(),))
        Cast_ID = cur.fetchone()[0]
        cur.execute("INSERT INTO MovieCasts (Movie_ID, Cast_ID) VALUES (?, ?)", (Movie_ID, Cast_ID))

    conn.commit()
    conn.close()

def ViewMovieData():
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT m.Movie_ID, m.Movie_Name, m.Release_Date, d.Director_Name, 
               GROUP_CONCAT(c.Cast_Name, ', ') AS Casts, md.Budget, md.Duration, md.Rating
        FROM Movies m
        LEFT JOIN MovieDetails md ON m.Movie_ID = md.Movie_ID
        LEFT JOIN Directors d ON md.Director_ID = d.id
        LEFT JOIN MovieCasts mc ON m.Movie_ID = mc.Movie_ID
        LEFT JOIN Casts c ON mc.Cast_ID = c.id
        GROUP BY m.Movie_ID
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

def DeleteMovieRec(Movie_ID):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM Movies WHERE Movie_ID=?", (Movie_ID,))
    cur.execute("DELETE FROM MovieDetails WHERE Movie_ID=?", (Movie_ID,))
    cur.execute("DELETE FROM MovieCasts WHERE Movie_ID=?", (Movie_ID,))

    conn.commit()
    conn.close()

def SearchMovieData(Movie_ID="", Movie_Name=""):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()

    query = """
        SELECT m.Movie_ID, m.Movie_Name, m.Release_Date, d.Director_Name, 
               GROUP_CONCAT(c.Cast_Name, ', ') AS Casts, md.Budget, md.Duration, md.Rating
        FROM Movies m
        LEFT JOIN MovieDetails md ON m.Movie_ID = md.Movie_ID
        LEFT JOIN Directors d ON md.Director_ID = d.id
        LEFT JOIN MovieCasts mc ON m.Movie_ID = mc.Movie_ID
        LEFT JOIN Casts c ON mc.Cast_ID = c.id
        WHERE m.Movie_ID LIKE ? OR m.Movie_Name LIKE ?
        GROUP BY m.Movie_ID
    """

    cur.execute(query, ('%' + Movie_ID + '%', '%' + Movie_Name + '%'))

    rows = cur.fetchall()
    conn.close()
    return rows

def UpdateMovieData(id, Movie_ID="", Movie_Name="", Release_Date="", Director="", Cast="", Budget="", Duration="", Rating=""):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()

    cur.execute("UPDATE Movies SET Movie_Name=?, Release_Date=? WHERE Movie_ID=?", 
                (Movie_Name, Release_Date, Movie_ID))

    cur.execute("INSERT OR IGNORE INTO Directors (Director_Name) VALUES (?)", (Director,))
    cur.execute("SELECT id FROM Directors WHERE Director_Name=?", (Director,))
    Director_ID = cur.fetchone()[0]

    cur.execute("UPDATE MovieDetails SET Director_ID=?, Budget=?, Duration=?, Rating=? WHERE Movie_ID=?", 
                (Director_ID, Budget, Duration, Rating, Movie_ID))

    cur.execute("DELETE FROM MovieCasts WHERE Movie_ID=?", (Movie_ID,))
    for actor in Cast.split(','):
        cur.execute("INSERT OR IGNORE INTO Casts (Cast_Name) VALUES (?)", (actor.strip(),))
        cur.execute("SELECT id FROM Casts WHERE Cast_Name=?", (actor.strip(),))
        Cast_ID = cur.fetchone()[0]
        cur.execute("INSERT INTO MovieCasts (Movie_ID, Cast_ID) VALUES (?, ?)", (Movie_ID, Cast_ID))

    conn.commit()
    conn.close()

def book_seat(movie_name, seat_number, customer_name):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    
    # Check if seat is already booked
    cur.execute("SELECT * FROM Bookings WHERE movie_name=? AND seat_number=?", (movie_name, seat_number))
    if cur.fetchone():
        conn.close()
        return False
    
    # If seat is available, book it
    booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO Bookings (movie_name, seat_number, customer_name, booking_date) VALUES (?, ?, ?, ?)",
                (movie_name, seat_number, customer_name, booking_date))
    
    conn.commit()
    conn.close()
    return True

def get_booking_details(customer_name):
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM Bookings WHERE customer_name=?", (customer_name,))
    bookings = cur.fetchall()
    
    conn.close()
    return bookings

def get_all_bookings():
    conn = sqlite3.connect("movie1.db")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM Bookings")
    bookings = cur.fetchall()
    
    conn.close()
    return bookings
