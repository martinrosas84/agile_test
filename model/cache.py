import sqlite3

class DbConnection:
    
    def __init__(self):
        self.connection = sqlite3.connect('cache.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def save_image_data(self, data):
        self.cursor.execute('INSERT INTO image_data(id, author, camera, tags, cropped_picture, full_picture) VALUES(?,?,?,?,?,?)',
                (data['id'], data['author'], data['camera'], data['tags'], data['cropped_picture'], data['full_picture']))
        self.connection.commit()

    def close(self):
        self.cursor.close()