from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain.entities import Lead
from src.domain.repositories import LeadRepository
from src.infra.db.models import LeadModel
from src.infra.repositories.mappers import LeadMapper


class SQLAlchemyLeadRepository(LeadRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Lead) -> Lead:
        model = LeadMapper.to_model(entity)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return LeadMapper.to_domain(model)

    def get_by_id(self, id: int) -> Optional[Lead]:
        model = self._session.query(LeadModel).filter(LeadModel.id == id).first()
        return LeadMapper.to_domain(model) if model else None

    def get_all(self) -> List[Lead]:
        return [LeadMapper.to_domain(m) for m in self._session.query(LeadModel).all()]

    def update(self, entity: Lead) -> Lead:
        model = self._session.query(LeadModel).filter(LeadModel.id == entity.id).first()
        if model:
            model.external_id = entity.external_id
            model.name = entity.name
            self._session.commit()
            self._session.refresh(model)
        return LeadMapper.to_domain(model)

    def get_by_external_id(self, external_id: str) -> Optional[Lead]:
        model = self._session.query(LeadModel).filter(LeadModel.external_id == external_id).first()
        return LeadMapper.to_domain(model) if model else None
