import logging
import os
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.orm import sessionmaker


TABLE_NAME = 'novels'
FILE_PATH = 'db.sqlite3'


class Novel(Base):
    __tablename__ = TABLE_NAME
    id = Column(Integer, autoincrement=True)
    domain = Column(String(255), nullable=False, primary_key=True)
    novel_id = Column(String(255), nullable=False, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    latest_url = Column(String(255), nullable=False)
    updated_at = Column(DateTime, nullable=False)


class NovelTableManager():
    def __init__(self, file_path=FILE_PATH):
        self.file_path = file_path

    @contextlib.contextmanager
    def create_session(self):
        engine = create_engine(f"sqlite:///{self.file_path}", echo=True)

        # create table if not exists
        Base.metadata.create_all(engine)

        SessionClass = sessionmaker(engine)
        session = SessionClass()

        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def insert_novel(self, item):
        try:
            with self.create_session() as session:

                    novel = Novel(
                        domain=item['domain'],
                        novel_id=item['novel_id'],
                        title=item['title'],
                        author=item['author'],
                        latest_url=item['latest_url'],
                        updated_at=item['updated_at'],
                    )
                    session.add(novel)
                    logging.info(f'Insert {item}')
            return True
        except:
            return False

    def update_novel(self, item):
        try:
            with self.create_session() as session:
                novel = session.query(Novel).filter(Novel.domain == item['domain'], Novel.novel_id == item['novel_id']).first()
                novel.title = item['title']
                novel.author = item['author']
                novel.latest_url = item['latest_url']
                novel.updated_at = item['updated_at']
                logging.info(f'Update {item}')
            return True
        except:
            return False

    def novel_exists(self, item):
        with self.create_session() as session:
            novel = session.query(Novel).filter(Novel.domain == item['domain'], Novel.novel_id == item['novel_id']).first()
            return True if novel else False

    def is_novel_updated(self, item):
        with self.create_session() as session:
            novel = session.query(Novel).filter(Novel.domain == item['domain'], Novel.novel_id == item['novel_id']).first()
            return novel.latest_url != item['latest_url']
