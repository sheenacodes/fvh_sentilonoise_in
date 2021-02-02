from flask import Flask
import os
from elasticapm.contrib.flask import ElasticAPM
import logging
from flask import jsonify, request
import json
from datetime import datetime
import requests

logging.basicConfig(level=logging.INFO)
#elastic_apm = ElasticAPM()

success_response_object = {"status": "success"}
success_code = 200
failure_response_object = {"status": "failure"}
failure_code = 400


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    #elastic_apm.init_app(app)

    def get_ds_id(thing, sensor):
        # """
        # requests the datastream id corresponding to the thing and sensor links given
        # returns -1 if not found
        # """

        payload = {"thing": thing, "sensor": sensor}
        logging.info(f"getting datastream id {payload}")
        #resp = requests.get(app.config["DATASTREAMS_ENDPOINT"], params=payload)
        resp = requests.get("http://host.docker.internal:1338/datastream", params=payload)
        logging.debug(f"response: {resp.json()} ")

        id = -1
        print(resp.json())
        ds = resp.json()["Datastreams"]
        if len(ds) == 1:
            id = ds[0]["datastream_id"]

        return id

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    @app.route("/")
    def hello_world():
        return jsonify(health="ok")

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
                phenomenon_timestamp_millisec = round(dt_obj.timestamp() * 1000)
                dt_obj = datetime.utcnow()
                result_timestamp_millisec = round(dt_obj.timestamp() * 1000)
                topic = "finest.sensorthings.observations.sentilo.cesva"
                #topic = "test.sheena"
                observation = {
                    "phenomenontime_begin": phenomenon_timestamp_millisec,
                    "phenomenontime_end": None,
                    "resulttime": result_timestamp_millisec,
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
                # resp = requests.post(
                #     app.config["OBSERVATIONS_ENDPOINT"],
                #     data=json.dumps(payload),
                #     headers=headers,
                # )
                resp = requests.post("http://host.docker.internal:1337/observation", data=json.dumps(payload), headers=headers)

            return success_response_object, success_code

        except Exception as e:
            logging.error("Error at %s", "data to kafka", exc_info=e)
            #elastic_apm.capture_exception()
            return failure_response_object, failure_code

    return app
