import sqlite3
import os
from cryptography.fernet import Fernet
import hashlib
import base64

class DBTools:
    def __init__(self, db_path=None):
        if db_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(script_dir)
            self.db_path = os.path.join(root_dir, 'ledger.db')
            self._create_database()
        else:
            self.db_path = db_path
            self._create_database()
        self.key = self.load_key()
        self.fernet = Fernet(self.key)
        self._create_db_if_not_exists()


    def load_key(self):
        # Load or generate a key for Fernet
        key_file = 'secret.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        return key


    def _create_db_if_not_exists(self):
        if not os.path.exists(self.db_path):
            self._create_database()


    def _create_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    salary TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()


    def add_entry(self, url, name, title, salary, username, password):
        if salary is None or salary.strip() == "":
            salary = "na"
        
        # salt = os.urandom(16)
        # salted_password = base64.urlsafe_b64encode(salt + password.encode('utf-8'))
        # encrypted_password = self.fernet.encrypt(salted_password)

        salt = os.urandom(16)
        salted_password = salt + password.encode('utf-8')
        encrypted_password = self.fernet.encrypt(salted_password).decode('utf-8')
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO entries (url, name, title, salary, username, password) VALUES (?, ?, ?, ?, ?, ?)', (url, name, title, salary, username, encrypted_password))
            conn.commit()


    def delete_entry(self, entry_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
            conn.commit()


    def get_entries(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, url, name, title, salary, username FROM entries')
            return cursor.fetchall()

