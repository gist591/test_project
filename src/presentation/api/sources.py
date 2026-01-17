from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.domain.entities import OperatorSource, Source
from src.infra.db import get_db
from src.infra.repositories import (
    SQLAlchemyOperatorRepository,
    SQLAlchemyOperatorSourceRepository,
    SQLAlchemySourceRepository,
)
from src.presentation.api.schemas import (
    OperatorSourceCreate,
    OperatorSourceResponse,
    SourceCreate,
    SourceDistributionResponse,
    SourceResponse,
)

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.post("/", response_model=SourceResponse, status_code=201)
def create_source(data: SourceCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemySourceRepository(db)
    source = Source(id=None, name=data.name)
    created = repo.add(source)
    return SourceResponse(id=created.id, name=created.name, is_active=created.is_active)


@router.get("/", response_model=list[SourceResponse])
def list_sources(db: Session = Depends(get_db)):
    repo = SQLAlchemySourceRepository(db)
    return [
        SourceResponse(id=s.id, name=s.name, is_active=s.is_active)
        for s in repo.get_all()
    ]


@router.get("/{source_id}", response_model=SourceResponse)
def get_source(source_id: int, db: Session = Depends(get_db)):
    repo = SQLAlchemySourceRepository(db)
    source = repo.get_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return SourceResponse(id=source.id, name=source.name, is_active=source.is_active)


@router.post(
    "/{source_id}/operators", response_model=OperatorSourceResponse, status_code=201
)
def assign_operator_to_source(
    source_id: int,
    data: OperatorSourceCreate,
    db: Session = Depends(get_db),
):
    source_repo = SQLAlchemySourceRepository(db)
    op_repo = SQLAlchemyOperatorRepository(db)
    os_repo = SQLAlchemyOperatorSourceRepository(db)

    if not source_repo.get_by_id(source_id):
        raise HTTPException(status_code=404, detail="Source not found")
    if not op_repo.get_by_id(data.operator_id):
        raise HTTPException(status_code=404, detail="Operator not found")

    os = OperatorSource(
        operator_id=data.operator_id,
        source_id=source_id,
        weight=data.weight,
    )
    created = os_repo.add(os)
    return OperatorSourceResponse(
        operator_id=created.operator_id,
        source_id=created.source_id,
        weight=created.weight,
    )


@router.get("/{source_id}/distribution", response_model=SourceDistributionResponse)
def get_source_distribution(source_id: int, db: Session = Depends(get_db)):
    source_repo = SQLAlchemySourceRepository(db)
    os_repo = SQLAlchemyOperatorSourceRepository(db)

    source = source_repo.get_by_id(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    assignments = os_repo.get_by_source_id(source_id)
    return SourceDistributionResponse(
        source=SourceResponse(
            id=source.id, name=source.name, is_active=source.is_active
        ),
        operators=[
            OperatorSourceResponse(
                operator_id=a.operator_id,
                source_id=a.source_id,
                weight=a.weight,
            )
            for a in assignments
        ],
    )
