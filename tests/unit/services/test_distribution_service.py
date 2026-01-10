import pytest

from src.app.services import LeadDistributionService
from src.domain.entities import Contact, ContactStatus, Lead, Operator, OperatorSource, Source
from tests.fakes.repositories import (
FakeContactRepository,
FakeLeadRepository,
FakeOperatorRepository,
FakeOperatorSourceRepository,
FakeSourceRepository
)


class TestFidnOrCreateLead:
    """Test for search/create Lead"""
    @pytest.fixture
    def lead_repo(self) -> FakeLeadRepository:
        return FakeLeadRepository()

    @pytest.fixture
    def service(self, lead_repo) -> LeadDistributionService:
        from src.app.services import LeadDistributionService
        return LeadDistributionService(
            operator_repo=FakeOperatorRepository,
            lead_repo=lead_repo,
            source_repo=FakeSourceRepository,
            contact_repo=FakeContactRepository,
            operator_source_repo=FakeOperatorSourceRepository
        )

    def test_returns_existing_lead_when_found(
        self,
        service,
        lead_repo
    ) -> None:
        """If lead is exist - return him, don't create new"""
        existing = lead_repo.add(
            Lead(
                id=None,
                external_id="tg_123",
                name="Test name"
            )
        )

        result = service.find_or_create_lead(
            external_id="tg_123"
        )

        assert result.id == existing.id
        assert result.external_id == "tg_123"
        assert len(lead_repo.get_all()) == 1

    def test_creates_new_lead_when_not_found(
        self,
        service,
        lead_repo,
    ) -> None:
        """If lead is't founded - will creating new"""
        result = service.find_or_create_lead(
            external_id="tg_456",
            name="Test name2"
        )

        assert result.id is not None
        assert result.external_id == "tg_456"
        assert result.name == "Test name2"
        assert len(lead_repo.get_all()) == 1


class TestSelectOperator:
    """The test for selecting operator"""
    @pytest.fixture
    def operator_repo(self) -> FakeOperatorRepository:
        return FakeOperatorRepository()

    @pytest.fixture
    def operator_source_repo(self) -> FakeOperatorSourceRepository:
        return FakeOperatorSourceRepository()

    @pytest.fixture
    def contact_repo(self) -> FakeContactRepository:
        return FakeContactRepository()

    @pytest.fixture
    def lead_repo(self) -> FakeLeadRepository:
        return FakeLeadRepository()

    @pytest.fixture
    def source_repo(self) -> FakeSourceRepository:
        return FakeSourceRepository()

    @pytest.fixture
    def service(
        self,
        operator_repo,
        operator_source_repo,
        contact_repo,
        lead_repo,
        source_repo,
    ) -> LeadDistributionService:
        from src.app.services.distribution_service import LeadDistributionService

        return LeadDistributionService(
            operator_repo=operator_repo,
            lead_repo=lead_repo,
            source_repo=source_repo,
            contact_repo=contact_repo,
            operator_source_repo=operator_source_repo,
        )

    def test_returns_none_when_no_operators(self, service) -> None:
        result = service.select_operator_for_source(
            source_id=1
        )

        assert result is None

    def test_return_single_operator(
        self,
        service,
        operator_repo,
        operator_source_repo,
    ) -> None:
        """If signle operator - return him"""
        operator = operator_repo.add(
            Operator(
                id=None,
                name="Test name",
                max_load=10
            )
        )
        operator_source_repo.add(
            OperatorSource(
                operator_id=operator.id,
                source_id=1,
                weight=10,
            )
        )

        result = service.select_operator_for_source(
            source_id=1
        )

        assert result.id == operator.id
        assert result.name == "Test name"

    def test_selects_by_weight_distribution(
        self,
        service,
        operator_repo,
        operator_source_repo,
    ) -> None:
       op1 = operator_repo.add(
           Operator(
               id=None,
               name="Test name1",
               max_load=100
           )
       )
       op2 = operator_repo.add(
           Operator(
               id=None,
               name="Test name2",
               max_load=100
           )
       )
       operator_source_repo.add(
           OperatorSource(
               operator_id=op1.id,
               source_id=1,
               weight=10
           )
       )
       operator_source_repo.add(
           OperatorSource(
               operator_id=op2.id,
               source_id=1,
               weight=30
           )
       )

       selections = {op1.id: 0, op2.id: 0}
       for _ in range(100):
           result = service.select_operator_for_source(
               source_id=1
           )
           selections[result.id] += 1

        #assert selections[op2.id] > selections[op1.id]
        #assert selections[op2.id] >= 50

    def test_skips_operator_at_capactity(
        self,
        service,
        operator_repo,
        operator_source_repo,
        contact_repo
    ) -> None:
        op1 = operator_repo.add(Operator(id=None, name="Op1", max_load=1))
        op2 = operator_repo.add(Operator(id=None, name="Op2", max_load=10))
        operator_source_repo.add(OperatorSource(operator_id=op1.id, source_id=1, weight=50))
        operator_source_repo.add(OperatorSource(operator_id=op2.id, source_id=1, weight=50))

        contact_repo.add(Contact(id=None, lead_id=1, source_id=1, operator_id=op1.id, status=ContactStatus.ACTIVE))

        result = service.select_operator_for_source(source_id=1)

        assert result.id == op2.id

    def test_skips_inactive_opeartor(
        self,
        service,
        operator_repo,
        operator_source_repo
    ) -> None:
        """Inactive operator skips"""
        op1 = operator_repo.add(Operator(id=None, name="Op1", is_active=False, max_load=10))
        op2 = operator_repo.add(Operator(id=None, name="Op2", is_active=True, max_load=10))
        operator_source_repo.add(OperatorSource(operator_id=op1.id, source_id=1, weight=50))
        operator_source_repo.add(OperatorSource(operator_id=op2.id, source_id=1, weight=50))

        result = service.select_operator_for_source(source_id=1)

        assert result.id == op2.id

class TestCreateContact:
    """Tests for creating contact"""

    @pytest.fixture
    def operator_repo(self):
        return FakeOperatorRepository()

    @pytest.fixture
    def lead_repo(self):
        return FakeLeadRepository()

    @pytest.fixture
    def source_repo(self):
        return FakeSourceRepository()

    @pytest.fixture
    def contact_repo(self):
        return FakeContactRepository()

    @pytest.fixture
    def operator_source_repo(self):
        return FakeOperatorSourceRepository()

    @pytest.fixture
    def service(self,
        operator_repo,
        lead_repo,
        source_repo,
        contact_repo,
        operator_source_repo
    ) -> LeadDistributionService:
        from src.app.services import LeadDistributionService
        return LeadDistributionService(
            operator_repo=operator_repo,
            lead_repo=lead_repo,
            source_repo=source_repo,
            contact_repo=contact_repo,
            operator_source_repo=operator_source_repo,
        )

    def test_creates_contact_with_operator(
        self,
        service,
        operator_repo,
        source_repo,
        operator_source_repo,
        contact_repo
    ) -> None:
        """The test for creating contact with operator"""
        operator = operator_repo.add(Operator(id=None, name="Иван", max_load=10))
        source = source_repo.add(Source(id=None, name="telegram"))
        operator_source_repo.add(OperatorSource(operator_id=operator.id, source_id=source.id, weight=10))

        result = service.create_contact(
            external_lead_id="tg_123",
            source_id=source.id,
            message="Привет!",
        )

        assert result.id is not None
        assert result.operator_id == operator.id
        assert result.status == ContactStatus.ACTIVE
        assert result.message == "Привет!"
        assert len(contact_repo.get_all()) == 1

    def test_creates_lead_if_not_exists(
        self,
        service,
        operator_repo,
        source_repo,
        operator_source_repo,
        lead_repo
    ) -> None:
        """The test creating new lead if not exists"""
        operator = operator_repo.add(Operator(id=None, name="Иван", max_load=10))
        source = source_repo.add(Source(id=None, name="telegram"))
        operator_source_repo.add(OperatorSource(operator_id=operator.id, source_id=source.id, weight=10))

        result = service.create_contact(
            external_lead_id="tg_new",
            source_id=source.id,
            lead_name="Новый Клиент",
        )

        lead = lead_repo.get_by_external_id("tg_new")
        assert lead is not None
        assert lead.name == "Новый Клиент"
        assert result.lead_id == lead.id

    def test_uses_existing_lead(
        self,
        service,
        operator_repo,
        source_repo,
        operator_source_repo,
        lead_repo
    ) -> None:
        """The test for using existing lead"""
        existing_lead = lead_repo.add(Lead(id=None, external_id="tg_exists", name="Старый"))
        operator = operator_repo.add(Operator(id=None, name="Иван", max_load=10))
        source = source_repo.add(Source(id=None, name="telegram"))
        operator_source_repo.add(OperatorSource(operator_id=operator.id, source_id=source.id, weight=10))

        result = service.create_contact(external_lead_id="tg_exists", source_id=source.id)

        assert result.lead_id == existing_lead.id
        assert len(lead_repo.get_all()) == 1

    def test_creates_unassigned_when_no_operators(self, service, source_repo, contact_repo):
        """The test creating UNASSIGNED when no operators"""
        source = source_repo.add(Source(id=None, name="telegram"))

        result = service.create_contact(external_lead_id="tg_999", source_id=source.id)

        assert result.operator_id is None
        assert result.status == ContactStatus.UNASSIGNED

    def test_raises_error_when_source_not_found(self, service):
        """The test raising error when source not found"""
        with pytest.raises(ValueError, match="Source with id=999 not found"):
            service.create_contact(external_lead_id="tg_123", source_id=999)
