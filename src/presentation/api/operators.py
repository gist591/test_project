from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.domain.entities import Operator
from src.infra.db import get_db
from src.infra.repositories import SQLAlchemyOperatorRepository
from src.presentation.api.schemas import (
    OperatorCreate,
    OperatorResponse,
    OperatorUpdate,
)

router = APIRouter(prefix="/operators", tags=["Operators"])


@router.post("/", response_model=OperatorResponse, status_code=201)
def create_operator(data: OperatorCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemyOperatorRepository(db)
    operator = Operator(
        id=None,
        name=data.name,
        is_active=data.is_active,
        max_load=data.max_load,
    )
    created = repo.add(operator)
    return OperatorResponse(
        id=created.id,
        name=created.name,
        is_active=created.is_active,
        max_load=created.max_load,
        current_load=created.current_load,
    )


@router.get("/", response_model=list[OperatorResponse])
def list_operators(db: Session = Depends(get_db)):
    repo = SQLAlchemyOperatorRepository(db)
    return [
        OperatorResponse(
            id=op.id,
            name=op.name,
            is_active=op.is_active,
            max_load=op.max_load,
            current_load=op.current_load,
        )
        for op in repo.get_all()
    ]


@router.get("/{operator_id}", response_model=OperatorResponse)
def get_operator(operator_id: int, db: Session = Depends(get_db)):
    repo = SQLAlchemyOperatorRepository(db)
    op = repo.get_by_id(operator_id)
    if not op:
        raise HTTPException(status_code=404, detail="Operator not found")
    return OperatorResponse(
        id=op.id,
        name=op.name,
        is_active=op.is_active,
        max_load=op.max_load,
        current_load=op.current_load,
    )


@router.patch("/{operator_id}", response_model=OperatorResponse)
def update_operator(
    operator_id: int, data: OperatorUpdate, db: Session = Depends(get_db)
):
    repo = SQLAlchemyOperatorRepository(db)
    op = repo.get_by_id(operator_id)
    if not op:
        raise HTTPException(status_code=404, detail="Operator not found")

    if data.name is not None:
        op.name = data.name
    if data.is_active is not None:
        op.is_active = data.is_active
    if data.max_load is not None:
        op.max_load = data.max_load

    updated = repo.update(op)
    return OperatorResponse(
        id=updated.id,
        name=updated.name,
        is_active=updated.is_active,
        max_load=updated.max_load,
        current_load=updated.current_load,
    )
