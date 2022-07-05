import logging
import os

from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import database_exists, create_database

from .models import CompoundSummary


def row2dict(row) -> dict:
    """Converting Row (SQLAlchemy) into dictionary.

    Args:
        row: instance of SQLAlchemy Row

    Returns:
        dict where keys are column names and values are field values
    """
    d = {}
    for column in row.__table__.c:
        d[column.name] = str(getattr(row, column.name))

    return d


class Storage(object):
    """Storage class implements database integration layer

    While initiating, constructor is getting environment
    variable 'DATABASE_URL' which expect to contain connection
    string to database.
    """
    def __init__(self, debug=False) -> None:
        self.debug = debug

        db_connect_string = os.environ.get('DATABASE_URL', None)
        if not db_connect_string:
            # !Warning!
            # checked in wsl only

            # if connection string is not set, get the first IP of local host
            cmd = 'hostname -I | cut -d " " -f1'
            ip = os.popen(cmd).read().strip()

            USER = 'cdt'
            PASSWORD = 'cdt'
            DATABASE = 'compound_data_tool'
            PORT = 5432

            db_connect_string = \
                f"postgresql://{USER}:{PASSWORD}@{ip}:{PORT}/{DATABASE}"

        # if not db_connect_string:
        #     raise RuntimeError(
        #         'DATABASE_URL is not set at running '
        #         'environment. Please set it before cdt use.')

        echo = self.debug
        self.engine = create_engine(db_connect_string, echo=echo)

        self.Session = sessionmaker(bind=self.engine)
        logging.debug(f"Session object initiated: {self.Session}")

        logging.debug("Create database and tables if needed...")
        self._create_db()

    def _create_db(self) -> None:
        """Prepare database structures if they are missing:
            * database (declared within DATABASE_URL) env var if it is
            * data tables
        """
        if not database_exists(self.engine.url):
            logging.info('Creating database...')
            create_database(self.engine.url)

        Base = declarative_base()

        table_name = CompoundSummary.__tablename__
        eng = self.engine

        table_exists = inspect(eng).has_table(table_name)
        if not table_exists:  # If table don't exist, Create.
            logging.debug(f"Creating database tables "
                          f"because {table_name} doesn't exists.")
            Base.metadata.create_all(eng, tables=[CompoundSummary.__table__])

    def save(self, summary: CompoundSummary) -> None:
        """Saving compound summary to database.

        Args:
            summary: instance of CompoundSummary
        """
        logging.debug(f"Saving {summary} to the database")
        with self.Session() as sess:
            sess.merge(summary)
            sess.commit()

    def get(self, compound: str) -> CompoundSummary:
        """Retreiving compound summary from database.

        Args:
            compound: hetcode of desired compound

        Returns:
            instance of CompoundSummary
        """
        stmt = select(CompoundSummary).\
            where(CompoundSummary.compound == compound)
        with self.Session() as sess:
            row = sess.scalars(stmt).first()

            if row:
                return row2dict(row)
            else:
                return None
