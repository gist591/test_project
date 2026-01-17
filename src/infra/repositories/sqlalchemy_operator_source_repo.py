from sqlalchemy.orm import Session

from src.domain.entities import OperatorSource
from src.domain.repositories import OperatorSourceRepository
from src.infra.db.models import OperatorSourceModel
from src.infra.repositories.mappers import OperatorSourceMapper


class SQLAlchemyOperatorSourceRepository(OperatorSourceRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: OperatorSource) -> OperatorSource:
        model = OperatorSourceMapper.to_model(entity)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return OperatorSourceMapper.to_domain(model)

    def get_by_id(self, id: int) -> OperatorSource | None:
        return None  # Составной ключ

    def get_all(self) -> list[OperatorSource]:
        return [
            OperatorSourceMapper.to_domain(m)
            for m in self._session.query(OperatorSourceModel).all()
        ]

    def update(self, entity: OperatorSource) -> OperatorSource:
        model = (
            self._session.query(OperatorSourceModel)
            .filter(
                OperatorSourceModel.operator_id == entity.operator_id,
                OperatorSourceModel.source_id == entity.source_id,
            )
            .first()
        )
        if model:
            model.weight = entity.weight
            self._session.commit()
            self._session.refresh(model)
        return OperatorSourceMapper.to_domain(model)

    def get_by_source_id(self, source_id: int) -> list[OperatorSource]:
        models = (
            self._session.query(OperatorSourceModel)
            .filter(OperatorSourceModel.source_id == source_id)
            .all()
        )
        return [OperatorSourceMapper.to_domain(m) for m in models]

    def get_by_operator_id(self, operator_id: int) -> list[OperatorSource]:
        models = (
            self._session.query(OperatorSourceModel)
            .filter(OperatorSourceModel.operator_id == operator_id)
            .all()
        )
        return [OperatorSourceMapper.to_domain(m) for m in models]

    def delete(self, operator_id: int, source_id: int) -> bool:
        result = (
            self._session.query(OperatorSourceModel)
            .filter(
                OperatorSourceModel.operator_id == operator_id,
                OperatorSourceModel.source_id == source_id,
            )
            .delete()
        )
        self._session.commit()
        return result > 0
