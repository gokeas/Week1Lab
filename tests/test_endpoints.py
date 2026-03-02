import urllib.parse


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Basic sanity checks for known activities
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success(client):
    activity = "Basketball Team"
    email = "tester1@mergington.edu"
    url_activity = urllib.parse.quote(activity)

    resp = client.post(f"/activities/{url_activity}/signup?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate(client):
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    url_activity = urllib.parse.quote(activity)

    # First signup should succeed
    resp1 = client.post(f"/activities/{url_activity}/signup?email={email}")
    assert resp1.status_code == 200

    # Second signup should fail with 400
    resp2 = client.post(f"/activities/{url_activity}/signup?email={email}")
    assert resp2.status_code == 400
    data = resp2.json()
    assert "already" in data.get("detail", "").lower()


def test_signup_nonexistent_activity(client):
    activity = "Nonexistent Club"
    email = "noone@mergington.edu"
    url_activity = urllib.parse.quote(activity)

    resp = client.post(f"/activities/{url_activity}/signup?email={email}")
    assert resp.status_code == 404


def test_root_redirect(client):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (302, 307)
    # Make sure redirect target is the static index
    assert resp.headers.get("location") == "/static/index.html"
