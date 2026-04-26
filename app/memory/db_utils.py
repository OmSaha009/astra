import sqlite3
import uuid
from core.logging import setup_logger

logger = setup_logger(__name__)

DB_PATH = "astra.db"

def init_db():

    conn = sqlite3.connect(DB_PATH)

    conn.executescript('''
        CREATE TABLE IF NOT EXISTS session (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        );
    ''')

    logger.info("DB: Database intialized")

    conn.close()

def create_session():
    session_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO session (id) VALUES (?)", (session_id,))
    conn.commit()
    conn.close()

    return session_id

def save_message(session_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)", (session_id, role, content))
    conn.commit()
    conn.close()

def get_recent_messages(session_id, limit=100):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp LIMIT ?", (session_id, limit,))         
    messages = [{"role": row[0], "content": row[1]} for row in cur]
    logger.info(f"Returning messages: {len(messages)}")
    conn.close()
    return messages           

def get_all_sessions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("""
        SELECT s.id, s.created_at, 
               (SELECT content FROM messages WHERE session_id = s.id AND role = 'user' ORDER BY timestamp LIMIT 1) as preview
        FROM session s
        ORDER BY s.created_at DESC
        LIMIT 50
    """)
    sessions = [{"id": row[0], "created_at": row[1], "preview": row[2][:50] if row[2] else "Empty"} for row in cursor]
    conn.close()
    return list(sessions)

def delete_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.execute("DELETE FROM session WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()