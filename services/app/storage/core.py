import logging
import os

from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from .models import CompoundSummary


def row2dict(row):
    d = {}
    for column in row.__table__.c:
        d[column.name] = str(getattr(row, column.name))

    return d


class Storage(object):
    def __init__(self, debug=False):
        self.debug = debug

        pgconnect_string = os.environ.get('DATABASE_URL')
        if not pgconnect_string:
            raise RuntimeError('DATABASE_URL is not set at running environment.'
                'Please set it before cdt use.')
        # "postgresql://cdt:cdt@localhost:5432/compound_data_tool"
        echo = self.debug
        self.engine = create_engine(pgconnect_string, echo=echo)

        self.Session = sessionmaker(bind=self.engine)
        logging.debug(f"Session object initiated: {self.Session}")

    def _create_db(self):
        if not database_exists(self.engine.url):
            logging.info('Creating database...')
            create_database(self.engine.url)

        Base = declarative_base()
        # Base.metadata.drop_all()
        # Base.metadata.create_all()

        table_name = CompoundSummary.__tablename__
        eng = self.engine

        table_exists = inspect(eng).has_table(table_name)
        if not table_exists:  # If table don't exist, Create.
            logging.debug(f"Creating database tables "\
                f"because {table_name} doesn't exists.")
            Base.metadata.create_all(eng, tables=[CompoundSummary.__table__])
    
    def save(self, summary: CompoundSummary) -> None:
        """Saving compound summary to database"""
        logging.debug(f"Saving {summary} to the database")
        with self.Session() as sess:
            sess.merge(summary)
            sess.commit()

    def get(self, compound: str) -> CompoundSummary:
        stmt = select(CompoundSummary).\
            where(CompoundSummary.compound == compound)
        with self.Session() as sess:
            row = sess.scalars(stmt).first()
            
            if row:
                return row2dict(row)
            else:
                return None

        

