from flask import jsonify, request, Blueprint, current_app
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime
from app import swagger
from flasgger.utils import swag_from
import json
import os
import redis
from rq import Queue, Connection
from flask_jwt_extended import jwt_required
from app.models import AssetData
from confluent_kafka.admin import AdminClient, NewTopic

datastreams_blueprint = Blueprint("datastream", __name__)
api = Api(datastreams_blueprint)


class DataStream(Resource):
    def get(self):
        """
        gets list of all data streams
        """
        asset_data = AssetData.return_all()
        if asset_data:
            response = jsonify(asset_data)
            response.status_code = 200
            return response
        else:
            result = {"message": "No exisitng datastreams"}
            response = jsonify(result)
            response.status_code = 200
            return response

    # @jwt_required
    # @swag_from("apispec/observation.yml")
    def post(self):
        """
        Post new datastream : creates a new topic in kafka
        """

        data = request.get_json()
        topic = data["datastream_id"]
        topic_prefix = "test.sputhan.finest"

        admin_client = AdminClient(
            {
                "bootstrap.servers": current_app.config["KAFKA_BROKERS"],
                "security.protocol": current_app.config["SECURITY_PROTOCOL"],
                "sasl.mechanism": current_app.config["SASL_MECHANISM"],
                "sasl.username": current_app.config["SASL_UNAME"],
                "sasl.password": current_app.config["SASL_PASSWORD"],
                "ssl.ca.location": current_app.config["CA_CERT"],
            }
        )

        # TODO get datastream id from request data
        # TODO set datastream to postgres
        # TODO topic configs - partitions - ?
        fs = admin_client.create_topics(
            [
                NewTopic(
                    f"{topic_prefix}.{topic}", num_partitions=3, replication_factor=1,
                )
            ]
        )
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                logging.info("Topic {} created".format(topic))  # log to ELK
                result = {
                    "message": "Topic {} created".format(topic),
                    "status": "success",
                }
                response = jsonify(result)
                response.status_code = 200
                return response
            except Exception as e:
                logging.error("Failed to create topic {}: {}".format(topic, e))
                # TODO handle output message better
                result = {
                    "message": "Failed to create topic {}: {}".format(topic, e),
                    "status": "failure",
                }
                response = jsonify(result)
                response.status_code = 400
                return response


api.add_resource(DataStream, "/datastream")

