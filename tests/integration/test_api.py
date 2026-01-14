import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infra.db import get_db
from src.infra.db.models import Base


@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_file}")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    from main import app
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


class TestOperatorsAPI:

    def test_create_operator(self, client):
        response = client.post("/operators/", json={
            "name": "Иван",
            "max_load": 5
        })

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Иван"
        assert data["max_load"] == 5
        assert data["is_active"] is True
        assert data["current_load"] == 0

    def test_list_operators(self, client):
        client.post("/operators/", json={"name": "Op1"})
        client.post("/operators/", json={"name": "Op2"})

        response = client.get("/operators/")

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_operator(self, client):
        created = client.post("/operators/", json={"name": "Иван"}).json()

        response = client.get(f"/operators/{created['id']}")

        assert response.status_code == 200
        assert response.json()["name"] == "Иван"

    def test_update_operator(self, client):
        created = client.post("/operators/", json={"name": "Иван", "max_load": 5}).json()

        response = client.patch(f"/operators/{created['id']}", json={
            "is_active": False,
            "max_load": 10
        })

        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False
        assert data["max_load"] == 10


class TestSourcesAPI:

    def test_create_source(self, client):
        response = client.post("/sources/", json={"name": "telegram_bot"})

        assert response.status_code == 201
        assert response.json()["name"] == "telegram_bot"

    def test_list_sources(self, client):
        client.post("/sources/", json={"name": "telegram"})
        client.post("/sources/", json={"name": "whatsapp"})

        response = client.get("/sources/")

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_assign_operator_to_source(self, client):
        op = client.post("/operators/", json={"name": "Op1"}).json()
        source = client.post("/sources/", json={"name": "telegram"}).json()

        response = client.post(f"/sources/{source['id']}/operators", json={
            "operator_id": op["id"],
            "weight": 30
        })

        assert response.status_code == 201
        assert response.json()["weight"] == 30

    def test_get_source_distribution(self, client):
        op1 = client.post("/operators/", json={"name": "Op1"}).json()
        op2 = client.post("/operators/", json={"name": "Op2"}).json()
        source = client.post("/sources/", json={"name": "telegram"}).json()

        client.post(f"/sources/{source['id']}/operators", json={"operator_id": op1["id"], "weight": 10})
        client.post(f"/sources/{source['id']}/operators", json={"operator_id": op2["id"], "weight": 30})

        response = client.get(f"/sources/{source['id']}/distribution")

        assert response.status_code == 200
        data = response.json()
        assert data["source"]["name"] == "telegram"
        assert len(data["operators"]) == 2


class TestContactsAPI:
    def test_create_contact_assigns_operator(self, client):
        op = client.post("/operators/", json={"name": "Иван", "max_load": 10}).json()
        source = client.post("/sources/", json={"name": "telegram"}).json()
        client.post(f"/sources/{source['id']}/operators", json={
            "operator_id": op["id"],
            "weight": 10
        })

        response = client.post("/contacts/", json={
            "external_lead_id": "tg_123456",
            "source_id": source["id"],
            "message": "Привет!"
        })

        assert response.status_code == 201
        data = response.json()
        assert data["contact"]["operator_id"] == op["id"]
        assert data["contact"]["status"] == "active"
        assert data["lead"]["external_id"] == "tg_123456"
        assert data["operator"]["name"] == "Иван"

    def test_create_contact_unassigned_when_no_operators(self, client):
        source = client.post("/sources/", json={"name": "telegram"}).json()

        response = client.post("/contacts/", json={
            "external_lead_id": "tg_999",
            "source_id": source["id"]
        })

        assert response.status_code == 201
        data = response.json()
        assert data["contact"]["operator_id"] is None
        assert data["contact"]["status"] == "unassigned"
        assert data["operator"] is None

    def test_same_lead_multiple_contacts(self, client):
        op = client.post("/operators/", json={"name": "Op1"}).json()
        source1 = client.post("/sources/", json={"name": "telegram"}).json()
        source2 = client.post("/sources/", json={"name": "whatsapp"}).json()
        client.post(f"/sources/{source1['id']}/operators", json={"operator_id": op["id"], "weight": 10})
        client.post(f"/sources/{source2['id']}/operators", json={"operator_id": op["id"], "weight": 10})

        client.post("/contacts/", json={"external_lead_id": "tg_123", "source_id": source1["id"]})
        client.post("/contacts/", json={"external_lead_id": "tg_123", "source_id": source2["id"]})

        leads = client.get("/leads/").json()
        assert len(leads) == 1

        lead_detail = client.get(f"/leads/{leads[0]['id']}").json()
        assert len(lead_detail["contacts"]) == 2

    def test_list_contacts(self, client):
        source = client.post("/sources/", json={"name": "telegram"}).json()
        client.post("/contacts/", json={"external_lead_id": "tg_1", "source_id": source["id"]})
        client.post("/contacts/", json={"external_lead_id": "tg_2", "source_id": source["id"]})

        response = client.get("/contacts/")

        assert response.status_code == 200
        assert len(response.json()) == 2


class TestLeadsAPI:

    def test_list_leads(self, client):
        source = client.post("/sources/", json={"name": "telegram"}).json()
        client.post("/contacts/", json={"external_lead_id": "tg_1", "source_id": source["id"]})
        client.post("/contacts/", json={"external_lead_id": "tg_2", "source_id": source["id"]})

        response = client.get("/leads/")

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_lead_with_contacts(self, client):
        source = client.post("/sources/", json={"name": "telegram"}).json()
        client.post("/contacts/", json={
            "external_lead_id": "tg_555",
            "source_id": source["id"],
            "lead_name": "Пётр"
        })

        leads = client.get("/leads/").json()

        response = client.get(f"/leads/{leads[0]['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["lead"]["name"] == "Пётр"
        assert data["lead"]["external_id"] == "tg_555"
        assert len(data["contacts"]) == 1
