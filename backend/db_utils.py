import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_NAME = "rag_app_users.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates all necessary tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table for user accounts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
    ''')

    # Table for individual chat threads, linked to a user
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Modified table for chat messages, linked to a specific chat thread
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('human', 'ai')),
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- User Management Functions ---

def add_user(username: str, hashed_password: str) -> Optional[int]:
    """Adds a new user to the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)',
                     (username, hashed_password))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # This happens if the username is already taken
        return None
    finally:
        conn.close()

def get_user(username: str) -> Optional[Dict[str, Any]]:
    """Retrieves a user by their username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

# --- Chat Thread and Message Functions ---

def create_chat(user_id: int, title: str) -> int:
    """Creates a new chat thread for a user and returns the new chat_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chats (user_id, title) VALUES (?, ?)', (user_id, title))
    conn.commit()
    chat_id = cursor.lastrowid
    conn.close()
    return chat_id

def add_message_to_history(chat_id: int, role: str, content: str):
    """Adds a single message (either human or ai) to a chat's history."""
    conn = get_db_connection()
    conn.execute('INSERT INTO chat_history (chat_id, role, content) VALUES (?, ?, ?)',
                 (chat_id, role, content))
    conn.commit()
    conn.close()

def get_user_chats(user_id: int) -> List[Dict[str, Any]]:
    """Retrieves all chat threads for a specific user, ordered by most recent."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, created_at FROM chats WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    chats = cursor.fetchall()
    conn.close()
    return [dict(chat) for chat in chats]

def get_chat_messages(chat_id: int) -> List[Dict[str, Any]]:
    """Retrieves all messages for a specific chat_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role, content FROM chat_history WHERE chat_id = ? ORDER BY created_at ASC', (chat_id,))
    messages = cursor.fetchall()
    conn.close()
    return [dict(message) for message in messages]

# --- Initialize the database and tables when the module is first imported ---
create_tables()