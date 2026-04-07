import sqlite3
from datetime import datetime
from config import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ishchilar jadvali
    cursor.execute('''CREATE TABLE IF NOT EXISTS staff (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        face_vector BLOB,
        phone TEXT,
        is_active INTEGER DEFAULT 1,
        language TEXT DEFAULT 'qr'
    )''')
    
    # Davomat jadvali (Selfie va GPS bilan)
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        user_id INTEGER,
        timestamp DATETIME,
        status TEXT, -- 'IN' or 'OUT'
        verification_dist REAL,
        FOREIGN KEY(user_id) REFERENCES staff(user_id)
    )''')
    
    conn.commit()
    conn.close()

def check_staff(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_active, language FROM staff WHERE user_id = ?", (user_id,))
    res = cursor.fetchone()
    conn.close()
    if res:
        return res[0] == 1, res[1]
    return False, 'qr'

def log_attendance(user_id, status, dist):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (user_id, timestamp, status, verification_dist) VALUES (?, ?, ?, ?)", 
                   (user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status, dist))
    conn.commit()
    conn.close()