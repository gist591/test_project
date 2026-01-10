import pytest
from src.domain.entities import Source


class TestSource:
    @pytest.fixture
    def source(self) -> Source:
        return Source(
            id=1,
            name="telegram_bot",
        )

    def test_create_source(self, source) -> None:
        """The test create source with name"""
        assert source.id == 1
        assert source.name == "telegram_bot"
        assert source.is_active is True
