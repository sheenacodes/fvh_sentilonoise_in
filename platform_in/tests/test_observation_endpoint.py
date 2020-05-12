import os
from confluent_kafka import Consumer
import requests
import string
import random
import json


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))


def test_post_observation(test_app, test_database):
    client = test_app.test_client()

    # uncomment when authentication
    # # register user
    # email = randomString()
    # password = "nevermind"
    # username = randomString()
    # body = {"email": email, "password": password, "username": username}

    # resp = client.post(
    #     "/registration", data=json.dumps(body), content_type="application/json",
    # )
    # data = json.loads(resp.data.decode())

    # # verify user registartion success
    # assert resp.status_code == 201

    # # login and get access token
    # body = {"password": password, "username": username}

    # resp = client.post(
    #     "/login", data=json.dumps(body), content_type="application/json",
    # )

    # data = json.loads(resp.data.decode())
    # print(data)

    # assert resp.status_code == 200
    # token = data["access_token"]

    # make request body
    body = {
        "ObservationsPostData": {
            "ObservationBatchId": randomString(),
            "ObservationSchemaid": randomString(),
            "ObservationList": [
                {
                    "observed_value": random.randint(0, 100),
                    "observed_time": "2019-01-26T12:00:40.930",
                },
                {
                    "observed_value": random.randint(0, 100),
                    "observed_time": "2019-01-26T13:00:40.930",
                },
                {
                    "observed_value": random.randint(0, 100),
                    "observed_time": "2019-01-26T14:00:40.930",
                },
            ],
        }
    }

    # kafka_consumer = Consumer({
    #     'bootstrap.servers': 'host.docker.internal:9092',
    #     'group.id': 'testgroup'
    #     })

    # kafka_consumer.subscribe(['from_python'])
    # post request
    # resp = client.post(
    #     "/observation",
    #     data=json.dumps(body),
    #     content_type="application/json",
    #     headers=dict(Authorization="Bearer " + token),
    # )

    #post request
    resp = client.put(
        "/cesva/v1",
        data=json.dumps(body),
        content_type="application/json")
    data = json.loads(resp.data.decode())
    print(data)
    # verify output
    assert resp.status_code == 202
    # TODO test whole response
    assert "success" == data["status"]

    # TODO check task status
    # while True:
    #     task_id = data["message"]["task_id"]
    #     resp = client.get(
    #         f"/status/{task_id}>", data=json.dumps(body), content_type="application/json",
    #     )
    #     data = json.loads(resp.data.decode())
    #     print(data)
    #     assert resp.status_code == 200
    #     if data["message"]["task_status"]=="finished":
    #         assert data["message"]["task_status"]==True

    # while True:
    #     msg = kafka_consumer.poll(1.0)

    #     if msg is None:
    #         print("None")
    #         continue
    #     if msg.error():
    #         print("Consumer error: {}".format(msg.error()))
    #         continue
    #     if msg.value():
    #         print('Received message: {}'.format(msg.value().decode('utf-8')))
    #         break

    # kafka_consumer.close()

