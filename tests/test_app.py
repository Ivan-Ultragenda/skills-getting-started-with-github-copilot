from fastapi.testclient import TestClient
import copy
import src.app as app_module

client = TestClient(app_module.app)
BASE = copy.deepcopy(app_module.activities)

import pytest

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset in-memory activities before each test
    app_module.activities = copy.deepcopy(BASE)
    yield
    app_module.activities = copy.deepcopy(BASE)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    for key in BASE.keys():
        assert key in data


def test_signup_adds_participant():
    email = "test.user@example.com"
    r = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")
    assert email in app_module.activities["Chess Club"]["participants"]


def test_unregister_removes_participant():
    email = "remove.me@example.com"
    # add first
    r1 = client.post(f"/activities/Programming%20Class/signup?email={email}")
    assert r1.status_code == 200
    assert email in app_module.activities["Programming Class"]["participants"]
    # delete
    r2 = client.delete(f"/activities/Programming%20Class/participants?email={email}")
    assert r2.status_code == 200
    assert email not in app_module.activities["Programming Class"]["participants"]
