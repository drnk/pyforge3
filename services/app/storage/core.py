import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from .models import CompoundSummary


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
        Base.metadata.drop_all()
        Base.metadata.create_all()

    def save(self, summary: CompoundSummary):
        """Saving compound summary to database"""
        logging.debug(f"Saving {summary} to the database")
        with self.Session() as sess:
            sess.add(summary)
            sess.commit()
