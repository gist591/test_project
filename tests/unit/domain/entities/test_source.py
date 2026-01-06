import pytest
from src.domain.entities import OperatorSource


class TextOperatorSource:
    @pytest.fixture
    def source(self) -> OperatorSource:
        return OperatorSource(
            id=1,
            name="telegram_bot",
        )

    def test_create_source(self, source) -> None:
        """The test create source with name"""
        assert source.id == 1
        assert source.name == "telegram_bog"
        assert source.is_active is True
