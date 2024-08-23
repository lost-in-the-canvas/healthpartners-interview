import sqlite3
from datetime import datetime
import logging

def setup_database():
    conn = sqlite3.connect('./database/runtime_log.database')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS run_log (
            id INTEGER PRIMARY KEY,
            last_run_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_current_time():
    conn = sqlite3.connect('./database/runtime_log.database')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO run_log (id, last_run_time)
        VALUES (1, ?)
        ON CONFLICT(id) DO UPDATE SET last_run_time=excluded.last_run_time
    ''', (datetime.now().isoformat(),))
    conn.commit()
    conn.close()
    logging.debug("Logged current time: %s", datetime.now().isoformat())

def get_last_run_time():
    conn = sqlite3.connect('./database/runtime_log.database')
    cursor = conn.cursor()
    cursor.execute('SELECT last_run_time FROM run_log WHERE id=1')
    row = cursor.fetchone()
    conn.close()
    if row:
        return datetime.fromisoformat(row[0])
    return None