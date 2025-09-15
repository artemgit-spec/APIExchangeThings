import pytest


@pytest.mark.parametrize(
    "token, data, status, answer",
    [
        (
            "user1",
            {"my_thing_id": 1, "exchange_thing_id": 3},
            200,
            {"status_code": 200, "detail": "Сделка отправлена"},
        )
    ],
    indirect=["token"],
)
def test_create_deal(token, data, status, answer, client):
    resp = client.post(
        "/deals/create-deal", json=data, headers={"Authorization": token}
    )
    assert resp.status_code == status
    assert resp.json() == answer


@pytest.mark.parametrize(
    "token, status, answer",
    [
        (
            "user1",
            200,
            [
                {
                    "id_my_thing": 2,
                    "id_thing_exchange": 4,
                    "answer_user": None,
                    "begin_exchange": "2025-09-09T08:57:55.478953",
                }
            ],
        )
    ],
    indirect=["token"],
)
def test_my_deal(token, status, answer, client):
    resp = client.get("/deals/my-deals", headers={"Authorization": token})
    assert resp.status_code == status
    assert resp.json() == answer


@pytest.mark.parametrize(
    "token, status, answer",
    [
        (
            "user2",
            200,
            [
                {
                    "id_my_thing": 2,
                    "id_thing_exchange": 4,
                    "answer_user": None,
                    "begin_exchange": "2025-09-09T08:57:55.478953",
                }
            ],
        )
    ],
    indirect=["token"],
)
def test_deals_exchange(token, status, answer, client):
    resp = client.get("/deals/deals-exchange", headers={"Authorization": token})
    assert resp.status_code == status
    assert resp.json() == answer


@pytest.mark.parametrize(
    "token, id, status_deal, status, answer",
    [
        (
            "user2",
            1,
            "одобрить",
            200,
            {"status_code": 200, "detail": "Сделка одобрена"},
        ),
        (
            "user2",
            2,
            "отклонить",
            200,
            {"status_code": 200, "detail": "Сделка отклонена"},
        ),
    ],
    indirect=["token"],
)
def test_decision_deal(token, id, status_deal, status, answer, client):
    resp = client.patch(
        f"/deals/decision-deal/{id}",
        params={"dec": status_deal},
        headers={"Authorization": token},
    )
    assert resp.status_code == status
    assert resp.json() == answer
