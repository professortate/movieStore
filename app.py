from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

def get_db_connection():
    conn = sqlite3.connect('movie1.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    movies = conn.execute('''
        SELECT m.Movie_ID, m.Movie_Name, m.Release_Date, d.Director_Name, 
               GROUP_CONCAT(c.Cast_Name, ', ') AS Casts, md.Budget, md.Duration, md.Rating
        FROM Movies m
        LEFT JOIN MovieDetails md ON m.Movie_ID = md.Movie_ID
        LEFT JOIN Directors d ON md.Director_ID = d.id
        LEFT JOIN MovieCasts mc ON m.Movie_ID = mc.Movie_ID
        LEFT JOIN Casts c ON mc.Cast_ID = c.id
        GROUP BY m.Movie_ID
    ''').fetchall()
    conn.close()
    return render_template('index.html', movies=movies)

@app.route('/book_movie', methods=['POST'])
def book_movie():
    movie_name = request.form['movie_name']
    seat_number = request.form['seat_number']
    customer_name = request.form['customer_name']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if seat is already booked
    cursor.execute("SELECT * FROM Bookings WHERE movie_name=? AND seat_number=?", (movie_name, seat_number))
    if cursor.fetchone():
        conn.close()
        flash('Seat already booked. Please choose another seat.', 'error')
        return redirect(url_for('index'))
    
    # If seat is available, book it
    booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO Bookings (movie_name, seat_number, customer_name, booking_date) VALUES (?, ?, ?, ?)",
                   (movie_name, seat_number, customer_name, booking_date))
    conn.commit()
    conn.close()
    
    flash('Seat booked successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/print_booking', methods=['POST'])
def print_booking():
    customer_name = request.form['customer_name']
    
    conn = get_db_connection()
    bookings = conn.execute("SELECT * FROM Bookings WHERE customer_name=?", (customer_name,)).fetchall()
    conn.close()
    
    if bookings:
        return render_template('booking_details.html', bookings=bookings)
    else:
        flash('No bookings found for this customer.', 'info')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
