"""SQLAlchemy models for Storage module."""
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class CompoundSummary(Base):
    """CompoundSummary model."""
    __tablename__ = 'compounds_summary'

    compound = Column(String, primary_key=True)
    name = Column(String)
    formula = Column(String)
    inchi = Column(String)
    inchi_key = Column(String)
    smiles = Column(String)
    cross_links_count = Column(Integer)
    updated = Column(
        DateTime,
        server_default=func.now()
    )

    def __str__(self):
        return f"CompoundSummary({self.compound})"
