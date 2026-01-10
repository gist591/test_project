import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infra.db.models import Base
from src.domain.entities import Operator, ContactStatus


@pytest.fixture
def db_session():
    """Create in-memory DB for everyone test"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


class TestSQLAlchemyOperatorRepository:

    def test_add_and_get_operator(self, db_session):
        """Add and get operator"""
        from src.infra.repositories.sqlalchemy_operator_repo import SQLAlchemyOperatorRepository

        repo = SQLAlchemyOperatorRepository(db_session)
        operator = Operator(id=None, name="Иван", is_active=True, max_load=10)

        created = repo.add(operator)
        assert created.id is not None
        assert created.name == "Иван"

        fetched = repo.get_by_id(created.id)
        assert fetched.name == "Иван"

    def test_get_available_for_source_filters_by_load(self, db_session):
        """The test filtering operators by max_load"""
        from src.infra.repositories.sqlalchemy_operator_repo import SQLAlchemyOperatorRepository
        from src.infra.repositories.sqlalchemy_source_repo import SQLAlchemySourceRepository
        from src.infra.repositories.sqlalchemy_operator_source_repo import SQLAlchemyOperatorSourceRepository
        from src.infra.repositories.sqlalchemy_contact_repo import SQLAlchemyContactRepository
        from src.domain.entities import Source, OperatorSource, Contact

        op_repo = SQLAlchemyOperatorRepository(db_session)
        source_repo = SQLAlchemySourceRepository(db_session)
        os_repo = SQLAlchemyOperatorSourceRepository(db_session)
        contact_repo = SQLAlchemyContactRepository(db_session)

        op1 = op_repo.add(Operator(id=None, name="Op1", max_load=2))
        op2 = op_repo.add(Operator(id=None, name="Op2", max_load=10))

        source = source_repo.add(Source(id=None, name="telegram"))

        os_repo.add(OperatorSource(operator_id=op1.id, source_id=source.id, weight=10))
        os_repo.add(OperatorSource(operator_id=op2.id, source_id=source.id, weight=20))

        from src.infra.db.models import LeadModel
        lead = LeadModel(external_id="test_lead")
        db_session.add(lead)
        db_session.commit()

        contact_repo.add(Contact(id=None, lead_id=lead.id, source_id=source.id, operator_id=op1.id, status=ContactStatus.ACTIVE))
        contact_repo.add(Contact(id=None, lead_id=lead.id, source_id=source.id, operator_id=op1.id, status=ContactStatus.ACTIVE))

        available = op_repo.get_available_for_source(source.id)

        assert len(available) == 1
        assert available[0][0].id == op2.id
        assert available[0][1] == 20
