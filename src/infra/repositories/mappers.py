from src.domain.entities import Contact, Lead, Operator, OperatorSource, Source
from src.infra.db.models import (
    ContactModel,
    LeadModel,
    OperatorModel,
    OperatorSourceModel,
    SourceModel,
)


class OperatorMapper:
    @staticmethod
    def to_domain(model: OperatorModel, current_load: int = 0) -> Operator:
        return Operator(
            id=model.id,
            name=model.name,
            is_active=model.is_active,
            max_load=model.max_load,
            current_load=current_load,
        )

    @staticmethod
    def to_model(entity: Operator) -> OperatorModel:
        return OperatorModel(
            id=entity.id,
            name=entity.name,
            is_active=entity.is_active,
            max_load=entity.max_load,
        )


class LeadMapper:
    @staticmethod
    def to_domain(model: LeadModel) -> Lead:
        return Lead(
            id=model.id,
            external_id=model.external_id,
            name=model.name,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: Lead) -> LeadModel:
        return LeadModel(
            id=entity.id,
            external_id=entity.external_id,
            name=entity.name,
        )


class SourceMapper:
    @staticmethod
    def to_domain(model: SourceModel) -> Source:
        return Source(id=model.id, name=model.name, is_active=model.is_active)

    @staticmethod
    def to_model(entity: Source) -> SourceModel:
        return SourceModel(id=entity.id, name=entity.name, is_active=entity.is_active)


class ContactMapper:
    @staticmethod
    def to_domain(model: ContactModel) -> Contact:
        return Contact(
            id=model.id,
            lead_id=model.lead_id,
            source_id=model.source_id,
            operator_id=model.operator_id,
            status=model.status,
            message=model.message,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: Contact) -> ContactModel:
        return ContactModel(
            id=entity.id,
            lead_id=entity.lead_id,
            source_id=entity.source_id,
            operator_id=entity.operator_id,
            status=entity.status,
            message=entity.message,
        )


class OperatorSourceMapper:
    @staticmethod
    def to_domain(model: OperatorSourceModel) -> OperatorSource:
        return OperatorSource(
            operator_id=model.operator_id,
            source_id=model.source_id,
            weight=model.weight,
        )

    @staticmethod
    def to_model(entity: OperatorSource) -> OperatorSourceModel:
        return OperatorSourceModel(
            operator_id=entity.operator_id,
            source_id=entity.source_id,
            weight=entity.weight,
        )
