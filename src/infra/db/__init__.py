from .connection import engine, SessionLocal, get_db, DATABASE_URL
from .models import Base, OperatorModel, LeadModel, SourceModel, OperatorSourceModel, ContactModel


def init_db():
    Base.metadata.create_all(bind=engine)


__all__ = [
    "engine",
    "SessionLocal",
    "get_db",
    "init_db",
    "DATABASE_URL",
    "Base",
    "OperatorModel",
    "LeadModel",
    "SourceModel",
    "OperatorSourceModel",
    "ContactModel",
]
