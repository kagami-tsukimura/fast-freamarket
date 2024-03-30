from fastapi.testclient import TestClient


def test_find_all(client_fixture: TestClient):
    response = client_fixture.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
