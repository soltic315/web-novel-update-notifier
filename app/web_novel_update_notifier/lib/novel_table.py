import logging
import os
import sqlite3
import contextlib


class NovelTable():

    def __init__(self, file_path):
        self.file_path = file_path

    @contextlib.contextmanager
    def open_db(self):
        db = sqlite3.connect(
            os.path.join(os.getcwd(), self.file_path))

        cursor = db.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS novels(\
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                domain TEXT NOT NULL, \
                novel_id TEXT NOT NULL, \
                title TEXT NOT NULL, \
                author TEXT, \
                latest_url TEXT NOT NULL, \
                updated_at DATE \
            );')

        try:
            yield db
        finally:
            db.close()

    def insert_novel(self, item):
        with self.open_db() as db:
            db.execute(
                'INSERT INTO novels (domain, novel_id, title, author, latest_url, updated_at) VALUES (?, ?, ?, ?, ?, ?)', (
                    item['domain'],
                    item['novel_id'],
                    item['title'],
                    item['author'],
                    item['latest_url'],
                    item['updated_at'],
                )
            )
            db.commit()
            logging.info(f'Insert {item}')

    def update_novel(self, item):
        with self.open_db() as db:
            db.execute(
                'UPDATE novels SET title=?, author=?, latest_url=?, updated_at=? WHERE domain=? AND novel_id=?',
                (item['title'], item['author'], item['latest_url'], item['updated_at'], item['domain'], item['novel_id'],)
            )
            db.commit()
            logging.info(f'Update {item}')

    def novel_exists(self, item):
        with self.open_db() as db:
            cursor = db.execute(
                'SELECT * FROM novels WHERE domain=? AND novel_id=?',
                (item['domain'], item['novel_id'],)
            )
            return True if cursor.fetchone() else False

    def is_novel_updated(self, item):
        with self.open_db() as db:
            cursor = db.execute(
                'SELECT * FROM novels WHERE domain=? AND novel_id=?',
                (item['domain'], item['novel_id'],)
            )
            
            return cursor.fetchone()[5] != item['latest_url']
