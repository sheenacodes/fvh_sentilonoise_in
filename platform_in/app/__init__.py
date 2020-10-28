from flask import Flask
import os
from elasticapm.contrib.flask import ElasticAPM
import logging
from flask import jsonify, request
import json
from datetime import datetime
import requests

logging.basicConfig(level=logging.INFO)
elastic_apm = ElasticAPM()

success_response_object = {"status": "success"}
success_code = 202
failure_response_object = {"status": "failure"}
failure_code = 400


def get_ds_id(thing, sensor):
    """
    requests the datastream id corresponding to the thing and sensor links given
    returns -1 if not found
    """
    payload = {"thing": thing, "sensor": sensor}
    logging.debug(f"getting datastream id {payload}")
    resp = requests.get("http://st_datastreams_api:4999/datastream", params=payload)
    # resp = requests.get("http://host.docker.internal:1338/datastream", params=payload)
    # print(resp.json())
    logging.debug(f"response: {resp.json()} ")

    ds = resp.json()["Datastreams"]
    if len(ds) == 1:
        return ds[0]["datastream_id"]
    else:
        return -1


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    elastic_apm.init_app(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    @app.route("/")
    def hello_world():
        return jsonify(hello="world")

    @app.route("/cesva/v1", methods=["PUT"])
    def put_sentilonoise_data():
        try:
            data = request.get_json()
            logging.debug(data)
            data_streams = data["sensors"]

            for data_stream in data_streams:
                name = data_stream["sensor"]
                thing = f"Noise-{name[0:len(name)-2]}"
                sensor = f"{name[-1].lower()}_val"
                logging.debug(thing)
                logging.debug(sensor)

                ds_id = get_ds_id(thing, sensor)
                if ds_id == -1:
                    logging.warning(f"no datastream id found for {thing} + {sensor}")

                timestamp = data_stream["observations"][0]["timestamp"]
                # ogging.info(timestamp)
                dt_obj = datetime.strptime(timestamp, "%d/%m/%YT%H:%M:%SUTC")
                timestamp_millisec = round(dt_obj.timestamp() * 1000)

                topic = "finest-observations-sentilonoise"
                observation = {
                    "phenomenontime_begin": None,
                    "phenomenontime_end": None,
                    "resulttime": timestamp_millisec,
                    "result": data_stream["observations"][0]["value"],
                    "resultquality": None,
                    "validtime_begin": None,
                    "validtime_end": None,
                    "parameters": None,
                    "datastream_id": ds_id,
                    "featureofintrest_link": None,
                }

                payload = {"topic": topic, "observation": observation}

                headers = {"Content-type": "application/json"}
                resp = requests.post(
                    "http://st_observations_api:4888/observation",
                    data=json.dumps(payload),
                    headers=headers,
                )
                # resp = requests.post("http://host.docker.internal:1337/observation", data=json.dumps(payload), headers=headers)

            return success_response_object, success_code

        except Exception as e:
            logging.error(e)
            elastic_apm.capture_exception()
            return failure_response_object, failure_code

    return app
