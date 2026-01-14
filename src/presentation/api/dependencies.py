from sqlalchemy.orm import Session

from src.infra.db import get_db
from src.infra.repositories import (
    SQLAlchemyOperatorRepository,
    SQLAlchemyLeadRepository,
    SQLAlchemySourceRepository,
    SQLAlchemyContactRepository,
    SQLAlchemyOperatorSourceRepository,
)
from src.app.services import LeadDistributionService


def get_operator_repo(db: Session):
    return SQLAlchemyOperatorRepository(db)


def get_lead_repo(db: Session):
    return SQLAlchemyLeadRepository(db)


def get_source_repo(db: Session):
    return SQLAlchemySourceRepository(db)


def get_contact_repo(db: Session):
    return SQLAlchemyContactRepository(db)


def get_operator_source_repo(db: Session):
    return SQLAlchemyOperatorSourceRepository(db)


def get_distribution_service(db: Session):
    return LeadDistributionService(
        operator_repo=SQLAlchemyOperatorRepository(db),
        lead_repo=SQLAlchemyLeadRepository(db),
        source_repo=SQLAlchemySourceRepository(db),
        contact_repo=SQLAlchemyContactRepository(db),
        operator_source_repo=SQLAlchemyOperatorSourceRepository(db),
    )
