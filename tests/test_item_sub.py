from fastapi.testclient import TestClient


def test_find_all(client_fixture: TestClient):
    response = client_fixture.get("/item_subs")
    assert response.status_code == 200
    item_subs = response.json()
    assert len(item_subs) == 2


def test_find_by_id_success(client_fixture: TestClient):
    response = client_fixture.get("/item_subs/1")
    assert response.status_code == 200
    item_sub = response.json()
    assert item_sub["id"] == 1


def test_find_by_id_failure(client_fixture: TestClient):
    response = client_fixture.get("/item_subs/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "ItemSub not found"


def test_find_by_name_one(client_fixture: TestClient):
    response = client_fixture.get("/item_subs?name=PC1")
    assert response.status_code == 200
    item_sub = response.json()
    assert item_sub[0]["name"] == "PC1"


def test_find_by_name_multi(client_fixture: TestClient):
    response = client_fixture.get("/item_subs?name=PC")
    assert response.status_code == 200
    item_sub = response.json()
    assert item_sub[0]["name"] == "PC1"
    assert item_sub[1]["name"] == "PC2"


def test_create(client_fixture: TestClient):
    # 親クラスのItem作成
    response = client_fixture.post(
        "/items", json={"name": "iPhone", "price": 140000, "user_id": 1}
    )
    assert response.status_code == 201
    item = response.json()
    assert item["id"] == 3
    assert item["name"] == "iPhone"

    response = client_fixture.get("/items")
    assert len(response.json()) == 3

    # ItemSubの作成
    response = client_fixture.post("/item_subs", json={"name": "iPhone"})
    assert response.status_code == 201
    item_sub = response.json()
    assert item_sub["id"] == 3
    assert item_sub["name"] == "iPhone"


def test_update_success(client_fixture: TestClient):
    # 親クラスのItem作成
    response = client_fixture.post(
        "/items", json={"name": "iPhone", "price": 140000, "user_id": 1}
    )
    assert response.status_code == 201
    item = response.json()
    assert item["id"] == 3
    assert item["name"] == "iPhone"

    response = client_fixture.put("/item_subs/1", json={"name": "iPhone"})
    assert response.status_code == 200
    item_sub = response.json()
    assert item_sub["name"] == "iPhone"


def test_update_failure(client_fixture: TestClient):
    # 親クラスのItem作成
    response = client_fixture.post(
        "/items", json={"name": "iPhone", "price": 140000, "user_id": 1}
    )
    assert response.status_code == 201
    item = response.json()
    assert item["id"] == 3
    assert item["name"] == "iPhone"

    response = client_fixture.put("/item_subs/10", json={"name": "iPhone"})
    assert response.status_code == 404


def test_delete_success(client_fixture: TestClient):
    response = client_fixture.delete("/item_subs/1")
    assert response.status_code == 200
    response = client_fixture.get("/item_subs")
    item_subs = response.json()
    assert len(item_subs) == 1


def test_delete_failure(client_fixture: TestClient):
    response = client_fixture.delete("/item_subs/10")
    assert response.status_code == 404
    response = client_fixture.get("/item_subs")
    item_subs = response.json()
    assert len(item_subs) == 2
