import pytest


@pytest.mark.parametrize(
    "token, data, status, answer",
    [
        (
            "user1",
            {
                "name": "string",
                "description": "string",
                "date_added": "2025-09-09T08:57:55.478953",
            },
            200,
            {"status_code": 201, "detail": "Создана карточка товара"},
        )
    ],
    indirect=["token"],
)
def test_create_thing(token, data, status, answer, client):
    resp = client.post(
        "/things/create-thing", json=data, headers={"Authorization": token}
    )
    assert resp.status_code == status
    assert resp.json() == answer


@pytest.mark.parametrize(
    "token, id, data, status, answer",
    [
        (
            "user1",
            1,
            {"name": "new_name", "description": "new_description"},
            200,
            {
                "status_code": 200,
                "detail": "Изменили название на new_name и описание на new_description",
            },
        ),
        (
            "user2",
            3,
            {"name": "string", "description": "new_description"},
            200,
            {"status_code": 200, "detail": "Изменили описание на new_description"},
        ),
        (
            "user1",
            2,
            {"name": "new_name", "description": "string"},
            200,
            {"status_code": 200, "detail": "Изменили название на new_name"},
        ),
        (
            "user2",
            4,
            {"name": "string", "description": "string"},
            200,
            {"status_code": 200, "detail": "Изменения не были внесены"},
        ),
    ],
    indirect=["token"],
)
def test_update_info_thing(token, id, data, status, answer, client):
    resp = client.patch(
        f"/things/update-thing/{id}", json=data, headers={"Authorization": token}
    )
    assert resp.status_code == status
    assert resp.json() == answer


@pytest.mark.parametrize(
    "token, id, status, answer",
    [("user3", 5, 200, {"status_code": 200, "detail": "Предмет удален"})],
    indirect=["token"],
)
def test_delete_thing(token, id, status, answer, client):
    resp = client.delete(f"/things/delete-thing/{id}", headers={"Authorization": token})
    assert resp.status_code == status
    assert resp.json() == answer
