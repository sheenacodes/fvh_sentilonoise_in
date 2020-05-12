import os
import confluent_kafka
import requests
import string
import random
import json


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))


def test_add_user_valid(test_app, test_database):
    client = test_app.test_client()

    # make request body
    email = randomString()
    password = "nevermind"
    username = randomString()
    body = {"email": email, "password": password, "username": username}

    # post request
    resp = client.post(
        "/registration", data=json.dumps(body), content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    #verify output
    assert resp.status_code == 201
    expected_message = {"email": email, "username": username}

    assert expected_message==data["message"]
    assert "success"==data["status"]

