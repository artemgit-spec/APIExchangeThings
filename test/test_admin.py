import pytest


"""def test_create_admin(client):
    resp = client.post(
        "/admin/reg-admin",
        json={"name": "admin2", "password": "admin2", "email": "user2@example.com"},
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "status_code": 201,
        "default": "Создан новый администратор",
    }"""


@pytest.mark.parametrize(
    "token, fil, status, answer",
    [
        ("admin", "admins", 200, [{"name": "admin"}]),
        (
            "admin",
            "users",
            200,
            [
                {"name": "user1"},
                {"name": "user2"},
                {"name": "user3"},
                {"name": "user4"},
            ],
        ),
        ("user2", "admins", 403, {"detail": "У вас недостаточно прав"}),
    ],
    indirect=["token"],
)
def test_all_admins(token, fil, status, answer, client):
    resp = client.get(
        "/admin/all-admins", params={"filter": fil}, headers={"Authorization": token}
    )
    assert resp.status_code == status
    assert resp.json() == answer
