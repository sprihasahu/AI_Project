import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "pension.db")

def get_connection():
    os.makedirs(DATABASE_DIR, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pensioners (
        pensioner_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ppo_number TEXT UNIQUE NOT NULL,
        date_of_birth TEXT,
        bank_name TEXT,
        account_number TEXT NOT NULL,
        ifsc TEXT NOT NULL,
        email TEXT,
        mobile TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS life_certificates (
        certificate_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pensioner_id INTEGER NOT NULL,
        submitted_ppo TEXT NOT NULL,
        submitted_account TEXT NOT NULL,
        submitted_ifsc TEXT NOT NULL,
        status TEXT NOT NULL,
        rejection_reason TEXT,
        submission_date TEXT NOT NULL,
        FOREIGN KEY (pensioner_id)
        REFERENCES pensioners (pensioner_id)
    )
    """)
    
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    print("SQLite database and tables created successfully.")