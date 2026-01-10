import pytest

from src.domain.entities import OperatorSource


class TestOperatorSource:
    @pytest.fixture
    def os(self) -> OperatorSource:
        return OperatorSource(
            operator_id=1,
            source_id=2,
            weight=30,
        )

    def test_create_operator_source_with_weight(self, os) -> None:
        assert os.operator_id == 1
        assert os.source_id == 2
        assert os.weight == 30
