from fastapi.testclient import TestClient


def test_find_all(client_fixture: TestClient):
    response = client_fixture.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2


def test_find_by_id_success(client_fixture: TestClient):
    response = client_fixture.get("/items/1")
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1


def test_find_by_id_failure(client_fixture: TestClient):
    response = client_fixture.get("/items/100")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_find_by_name(client_fixture: TestClient):
    response = client_fixture.get("/items/?name=PC1")
    assert response.status_code == 200
    item = response.json()
    assert len(item) == 1
    assert item[0]["name"] == "PC1"


def test_create(client_fixture: TestClient):
    response = client_fixture.post(
        "/items", json={"name": "iPhone", "price": 140000, "user_id": 1}
    )
    assert response.status_code == 201
    item = response.json()
    assert item["id"] == 3
    assert item["name"] == "iPhone"

    response = client_fixture.get("/items")
    assert len(response.json()) == 3


def test_update_success(client_fixture: TestClient):
    response = client_fixture.put(
        "/items/1", json={"name": "iPhone15Pro MAX", "price": 150000}
    )
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "iPhone15Pro MAX"
    assert item["price"] == 150000


def test_update_failure(client_fixture: TestClient):
    response = client_fixture.put(
        "/items/100", json={"name": "iPhone15Pro MAX", "price": 150000}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not updated"


def test_delete_success(client_fixture: TestClient):
    response = client_fixture.delete("/items/1")
    assert response.status_code == 200
    response = client_fixture.get("/items")
    assert len(response.json()) == 1


def test_delete_failure(client_fixture: TestClient):
    response = client_fixture.delete("/items/100")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not deleted"
    response = client_fixture.get("/items")
    assert len(response.json()) == 2
