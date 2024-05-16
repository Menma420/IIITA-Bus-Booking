from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="28042023",
    database="test"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book_seat', methods=['POST'])
def book_seat():
    seat_number = request.form['seat']
    try:
        # Check if the seat is already booked
        cursor.execute("SELECT * FROM seat_table WHERE seatno = %s", (seat_number,))
        seat = cursor.fetchone()
        if seat:
            if seat[1] == 1:
                return f"Seat {seat_number} is already booked."
        else:
            # Insert the booking information into the database
            cursor.execute("UPDATE seat_table SET status=1 where seatno={}".format(seat_number))
            db.commit()
            return f"Seat {seat_number} booked successfully!"
    except mysql.connector.Error as err:
        return f"An error occurred: {err}"
    finally:
        cursor.close()

@app.route('/get_seat_status')
def get_seat_status():
    try:
        cursor.execute("SELECT * FROM seat_table")
        seats = [{'seatno': seat[0], 'status': seat[1]} for seat in cursor.fetchall()]
        return jsonify(seats)
    except mysql.connector.Error as err:
        return f"An error occurred: {err}"
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
