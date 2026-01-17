from .connection import DATABASE_URL, SessionLocal, engine, get_db
from .models import (
    Base,
    ContactModel,
    LeadModel,
    OperatorModel,
    OperatorSourceModel,
    SourceModel,
)


def init_db():
    Base.metadata.create_all(bind=engine)


__all__ = [
    "DATABASE_URL",
    "Base",
    "ContactModel",
    "LeadModel",
    "OperatorModel",
    "OperatorSourceModel",
    "SessionLocal",
    "SourceModel",
    "engine",
    "get_db",
    "init_db",
]
