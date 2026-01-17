from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.infra.db import get_db
from src.infra.repositories import (
    SQLAlchemyContactRepository,
    SQLAlchemyLeadRepository,
    SQLAlchemyOperatorRepository,
)
from src.presentation.api.dependencies import get_distribution_service
from src.presentation.api.schemas import (
    ContactCreate,
    ContactDetailResponse,
    ContactResponse,
    LeadResponse,
    OperatorResponse,
)

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=ContactDetailResponse, status_code=201)
def register_contact(data: ContactCreate, db: Session = Depends(get_db)):
    """Register contact"""
    service = get_distribution_service(db)
    lead_repo = SQLAlchemyLeadRepository(db)
    operator_repo = SQLAlchemyOperatorRepository(db)

    try:
        contact = service.create_contact(
            external_lead_id=data.external_lead_id,
            source_id=data.source_id,
            message=data.message,
            lead_name=data.lead_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    lead = lead_repo.get_by_id(contact.lead_id)
    operator = (
        operator_repo.get_by_id(contact.operator_id) if contact.operator_id else None
    )

    return ContactDetailResponse(
        contact=ContactResponse(
            id=contact.id,
            lead_id=contact.lead_id,
            source_id=contact.source_id,
            operator_id=contact.operator_id,
            status=contact.status,
            message=contact.message,
            created_at=contact.created_at,
        ),
        lead=LeadResponse(
            id=lead.id,
            external_id=lead.external_id,
            name=lead.name,
            created_at=lead.created_at,
        ),
        operator=OperatorResponse(
            id=operator.id,
            name=operator.name,
            is_active=operator.is_active,
            max_load=operator.max_load,
            current_load=operator.current_load,
        )
        if operator
        else None,
    )


@router.get("/", response_model=list[ContactResponse])
def list_contacts(db: Session = Depends(get_db)):
    repo = SQLAlchemyContactRepository(db)
    return [
        ContactResponse(
            id=c.id,
            lead_id=c.lead_id,
            source_id=c.source_id,
            operator_id=c.operator_id,
            status=c.status,
            message=c.message,
            created_at=c.created_at,
        )
        for c in repo.get_all()
    ]
