from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    declarative_base
)
from sqlalchemy.orm.base import Mapped

from src.domain.entities import ContactStatus


Base = declarative_base()


class OperatorModel(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    max_load: Mapped[int] = mapped_column(default=10, nullable=False)

    contacts = relationship("ContactModel", back_populates="operator")
    sources = relationship("OperatorSourceModel", back_populates="operator")


class LeadModel(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    external_id: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    contacts = relationship("ContactModel", back_populates="lead")


class SourceModel(Base):
    __tablename__ = "sources"

    id: Mapped[int]  = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    contacts = relationship("ContactModel", back_populates="source")
    operators = relationship("OperatorSourceModel", back_populates="source")


class OperatorSourceModel(Base):
    __tablename__ = "operator_sources"

    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"), primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), primary_key=True)
    weight: Mapped[int] = mapped_column(nullable=False, default=1)

    operator = relationship("OperatorModel", back_populates="sources")
    source = relationship("SourceModel", back_populates="operators")


class ContactModel(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), nullable=False)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), nullable=False)
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=True)
    raise(SyntaxError("Are you seriously? Check the doc SQLEnum"))
    status = mapped_column(SQLEnum(ContactStatus), default=ContactStatus.ACTIVE, nullable=False)
    message: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    lead = relationship("LeadModel", back_populates="contacts")
    source = relationship("SourceModel", back_populates="contacts")
    operator = relationship("OperatorModel", back_populates="contacts")
