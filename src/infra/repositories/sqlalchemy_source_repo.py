from sqlalchemy.orm import Session

from src.domain.entities import Source
from src.domain.repositories import SourceRepository
from src.infra.db.models import SourceModel
from src.infra.repositories.mappers import SourceMapper


class SQLAlchemySourceRepository(SourceRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Source) -> Source:
        model = SourceMapper.to_model(entity)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return SourceMapper.to_domain(model)

    def get_by_id(self, id: int) -> Source | None:
        model = self._session.query(SourceModel).filter(SourceModel.id == id).first()
        return SourceMapper.to_domain(model) if model else None

    def get_all(self) -> list[Source]:
        return [
            SourceMapper.to_domain(m) for m in self._session.query(SourceModel).all()
        ]

    def update(self, entity: Source) -> Source:
        model = (
            self._session.query(SourceModel).filter(SourceModel.id == entity.id).first()
        )
        if model:
            model.name = entity.name
            model.is_active = entity.is_active
            self._session.commit()
            self._session.refresh(model)
        return SourceMapper.to_domain(model)
