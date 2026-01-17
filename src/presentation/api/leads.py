from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.infra.db import get_db
from src.infra.repositories import SQLAlchemyContactRepository, SQLAlchemyLeadRepository
from src.presentation.api.schemas import (
    ContactResponse,
    LeadResponse,
    LeadWithContactsResponse,
)

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("/", response_model=list[LeadResponse])
def list_leads(db: Session = Depends(get_db)):
    repo = SQLAlchemyLeadRepository(db)
    return [
        LeadResponse(
            id=lead.id,
            external_id=lead.external_id,
            name=lead.name,
            created_at=lead.created_at,
        )
        for lead in repo.get_all()
    ]


@router.get("/{lead_id}", response_model=LeadWithContactsResponse)
def get_lead_with_contacts(lead_id: int, db: Session = Depends(get_db)):
    lead_repo = SQLAlchemyLeadRepository(db)
    contact_repo = SQLAlchemyContactRepository(db)

    lead = lead_repo.get_by_id(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    contacts = contact_repo.get_by_lead_id(lead_id)
    return LeadWithContactsResponse(
        lead=LeadResponse(
            id=lead.id,
            external_id=lead.external_id,
            name=lead.name,
            created_at=lead.created_at,
        ),
        contacts=[
            ContactResponse(
                id=c.id,
                lead_id=c.lead_id,
                source_id=c.source_id,
                operator_id=c.operator_id,
                status=c.status,
                message=c.message,
                created_at=c.created_at,
            )
            for c in contacts
        ],
    )
