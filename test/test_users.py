import pytest


def test_create_user(client):
    resp = client.post(
        "/user/reg-user",
        json={"name": "user3", "password": "user3", "email": "user2@example.com"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"status_code": 201, "detail": "Пользователь зарегистрирован"}


@pytest.mark.parametrize(
    "token, status, answer",
    [("user1", 200, {"id": 1, "name": "user1", "email": "user@example.com"})],
    indirect=["token"],
)
def test_info_user(token, status, answer, client):
    resp = client.get("/user/my_info", headers={"Authorization": token})
    assert resp.status_code == status
    assert resp.json() == answer


@pytest.mark.parametrize(
    "token, data, status, answer",
    [
        (
            "user1",
            {"name": "string", "email": "new_email"},
            200,
            {"status_code": 200, "detail": "Адрес почты изменили на new_email"},
        ),
        (
            "user2",
            {"name": "new_name", "email": "string"},
            200,
            {"status_code": 200, "detail": "Логин изменили на new_name"},
        ),
        (
            "user3",
            {"name": "string", "email": "string"},
            200,
            {"status_code": 200, "detail": "Изменения не были внесены"},
        ),
    ],
    indirect=["token"],
)
def test_update_info(token, data, status, answer, client):
    resp = client.patch(
        "/user/update-info", json=data, headers={"Authorization": token}
    )
    assert resp.status_code == status
    assert resp.json() == answer


@pytest.mark.parametrize(
    "token, status, answer",
    [("user4", 200, {"status_code": 200, "detail": "Вы удалили свой аккаунт"})],
    indirect=["token"],
)
def test_delete_user(token, status, answer, client):
    resp = client.delete("/user/delete", headers={"Authorization": token})
    assert resp.status_code == status
    assert resp.json() == answer
