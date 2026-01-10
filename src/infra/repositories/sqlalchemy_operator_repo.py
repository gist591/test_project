from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import func

from src.domain.entities import Operator, ContactStatus
from src.domain.repositories import OperatorRepository
from src.infra.db.models import OperatorModel, OperatorSourceModel, ContactModel
from src.infra.repositories.mappers import OperatorMapper


class SQLAlchemyOperatorRepository(OperatorRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Operator) -> Operator:
        model = OperatorMapper.to_model(entity)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return OperatorMapper.to_domain(model, current_load=0)

    def get_by_id(self, id: int) -> Optional[Operator]:
        model = self._session.query(OperatorModel).filter(OperatorModel.id == id).first()
        if not model:
            return None
        return OperatorMapper.to_domain(model, self._count_active_contacts(id))

    def get_all(self) -> List[Operator]:
        models = self._session.query(OperatorModel).all()
        return [OperatorMapper.to_domain(m, self._count_active_contacts(m.id)) for m in models]

    def update(self, entity: Operator) -> Operator:
        model = self._session.query(OperatorModel).filter(OperatorModel.id == entity.id).first()
        if model:
            model.name = entity.name
            model.is_active = entity.is_active
            model.max_load = entity.max_load
            self._session.commit()
            self._session.refresh(model)
        return OperatorMapper.to_domain(model, self._count_active_contacts(entity.id))

    def get_available_for_source(self, source_id: int) -> List[Tuple[Operator, int]]:
        """Get available filtered by current_load and max_load operators for source"""
        active_count_subq = (
            self._session.query(
                ContactModel.operator_id,
                func.count(ContactModel.id).label("active_count")
            )
            .filter(ContactModel.status == ContactStatus.ACTIVE)
            .group_by(ContactModel.operator_id)
            .subquery()
        )

        results = (
            self._session.query(
                OperatorModel,
                OperatorSourceModel.weight,
                func.coalesce(active_count_subq.c.active_count, 0).label("current_load")
            )
            .join(OperatorSourceModel, OperatorModel.id == OperatorSourceModel.operator_id)
            .outerjoin(active_count_subq, OperatorModel.id == active_count_subq.c.operator_id)
            .filter(
                OperatorSourceModel.source_id == source_id,
                OperatorModel.is_active == True,
            )
            .all()
        )

        available = []
        for op_model, weight, current_load in results:
            if current_load < op_model.max_load:
                operator = OperatorMapper.to_domain(op_model, current_load=current_load)
                available.append((operator, weight))

        return available

    def _count_active_contacts(self, operator_id: int) -> int:
        return (
            self._session.query(func.count(ContactModel.id))
            .filter(
                ContactModel.operator_id == operator_id,
                ContactModel.status == ContactStatus.ACTIVE
            )
            .scalar() or 0
        )
