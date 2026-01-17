from sqlalchemy import func
from sqlalchemy.orm import Session

from src.domain.entities import Contact, ContactStatus
from src.domain.repositories import ContactRepository
from src.infra.db.models import ContactModel
from src.infra.repositories.mappers import ContactMapper


class SQLAlchemyContactRepository(ContactRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Contact) -> Contact:
        model = ContactMapper.to_model(entity)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return ContactMapper.to_domain(model)

    def get_by_id(self, id: int) -> Contact | None:
        model = self._session.query(ContactModel).filter(ContactModel.id == id).first()
        return ContactMapper.to_domain(model) if model else None

    def get_all(self) -> list[Contact]:
        return [
            ContactMapper.to_domain(m) for m in self._session.query(ContactModel).all()
        ]

    def update(self, entity: Contact) -> Contact:
        model = (
            self._session.query(ContactModel)
            .filter(ContactModel.id == entity.id)
            .first()
        )
        if model:
            model.status = entity.status
            model.operator_id = entity.operator_id
            model.message = entity.message
            self._session.commit()
            self._session.refresh(model)
        return ContactMapper.to_domain(model)

    def get_by_lead_id(self, lead_id: int) -> list[Contact]:
        models = (
            self._session.query(ContactModel)
            .filter(ContactModel.lead_id == lead_id)
            .all()
        )
        return [ContactMapper.to_domain(m) for m in models]

    def get_by_operator_id(self, operator_id: int) -> list[Contact]:
        models = (
            self._session.query(ContactModel)
            .filter(ContactModel.operator_id == operator_id)
            .all()
        )
        return [ContactMapper.to_domain(m) for m in models]

    def count_active_by_operator(self, operator_id: int) -> int:
        return (
            self._session.query(func.count(ContactModel.id))
            .filter(
                ContactModel.operator_id == operator_id,
                ContactModel.status == ContactStatus.ACTIVE,
            )
            .scalar()
            or 0
        )
