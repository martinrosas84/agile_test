import sqlite3

class DbConnection:
    
    def __init__(self):
        self.connection = sqlite3.connect('cache.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def delete_all(self):
        self.cursor.execute('delete from image_data')
        self.connection.commit()

    def save_image_data(self, data):
        self.cursor.execute('INSERT INTO image_data(id, author, camera, tags, cropped_picture, full_picture) VALUES(?,?,?,?,?,?)',
                (data['id'], data['author'], data['camera'], data['tags'], data['cropped_picture'], data['full_picture']))
        self.connection.commit()

    def search(self, term):
        self.cursor.execute('''
        select * from image_data
        where author like ?
        or camera like ? 
        or tags like ?
        ''', ('%' + term + '%', '%' + term + '%', '%' + term + '%')).fetchall()

    def close(self):
        self.cursor.close()