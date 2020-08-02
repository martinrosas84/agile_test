import sqlite3

class DbConnection:
    
    def __init__(self):
        self.connection = sqlite3.connect('cache.db')
        self.cursor = self.connection.cursor()