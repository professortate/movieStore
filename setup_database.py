import sqlite3

def setup_database():
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

if __name__ == "__main__":
    setup_database()
    print("Database setup completed successfully.")
