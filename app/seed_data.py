from datetime import datetime, timedelta
import sqlite3
import pytz

def seed_classes():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    classes = [
        ("Yoga", (now + timedelta(days=1)).isoformat(), "Aarti", 5),
        ("Zumba", (now + timedelta(days=2)).isoformat(), "Vikram", 10),
        ("HIIT", (now + timedelta(days=3)).isoformat(), "Priya", 8),
    ]
    with sqlite3.connect("studio.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM classes")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO classes (name, datetime, instructor, slots) VALUES (?, ?, ?, ?)", classes)
            conn.commit()