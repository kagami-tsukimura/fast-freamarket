from fastapi.testclient import TestClient


def test_find_all(client_fixture: TestClient):
    response = client_fixture.get("/item_subs")
    assert response.status_code == 200
    item_subs = response.json()
    assert len(item_subs) == 2
