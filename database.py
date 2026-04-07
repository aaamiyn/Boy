import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect("haq_system.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ishchilar jadvali (Profil)
    cursor.execute('''CREATE TABLE IF NOT EXISTS staff (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        face_vector BLOB,
        phone TEXT,
        company TEXT,
        is_active INTEGER DEFAULT 1
    )''')
    
    # Davomat jadvali (Loglar + GPS + Rasm)
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        user_id INTEGER,
        timestamp DATETIME,
        lat REAL,
        lon REAL,
        photo_url TEXT,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES staff(user_id)
    )''')
    
    # To'lovlar va Litsenziyalar
    cursor.execute('''CREATE TABLE IF NOT EXISTS licenses (
        owner_id INTEGER PRIMARY KEY,
        expiry_date DATE,
        trial_used INTEGER DEFAULT 0
    )''')
    
    conn.commit()
    conn.close()