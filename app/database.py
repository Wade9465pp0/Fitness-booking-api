import sqlite3
from datetime import datetime
import pytz


DB_NAME = "studio.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS classes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            datetime TEXT,
                            instructor TEXT,
                            slots INTEGER
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            class_id INTEGER,
                            client_name TEXT,
                            client_email TEXT,
                            FOREIGN KEY(class_id) REFERENCES classes(id)
                          )''')
        conn.commit()
    from app.seed_data import seed_classes
    seed_classes()

def get_classes():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes")
        rows = cursor.fetchall()
        return [dict(zip(["id", "name", "datetime", "instructor", "slots"], row)) for row in rows]

def book_class(data):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT slots FROM classes WHERE id = ?", (data.class_id,))
        result = cursor.fetchone()
        if not result:
            raise ValueError("Class not found.")
        slots = result[0]
        if slots <= 0:
            raise ValueError("No slots available.")
        cursor.execute("INSERT INTO bookings (class_id, client_name, client_email) VALUES (?, ?, ?)",
                       (data.class_id, data.client_name, data.client_email))
        cursor.execute("UPDATE classes SET slots = slots - 1 WHERE id = ?", (data.class_id,))
        conn.commit()
    return {"message": "Booking successful."}

def get_bookings_by_email(email):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT c.name, c.datetime, c.instructor FROM bookings b
                          JOIN classes c ON b.class_id = c.id
                          WHERE b.client_email = ?''', (email,))
        rows = cursor.fetchall()
        return [{"class_name": row[0], "datetime": row[1], "instructor": row[2]} for row in rows]
# This code initializes the SQLite database, defines functions to get classes, book a class, and retrieve bookings by email.
# It uses SQLite for data storage and includes basic error handling for booking operations.

