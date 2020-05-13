from flask import jsonify, request, Blueprint, current_app
from flask_restful import Resource, Api, abort
from datetime import datetime
import json
import os
import redis
from rq import Queue, Connection
from app.tasks import create_task_push_sentilo_noise_data

import logging

logging.basicConfig(level=logging.INFO)

observations_blueprint = Blueprint("observations", __name__)
api = Api(observations_blueprint)


class NoiseObservation(Resource):
    def put(self):
        """
        Post new observation
        """
        data = request.get_json()
        logging.debug(f"post observation: {data}")

        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
            q = Queue()
            task = q.enqueue(
                create_task_push_sentilo_noise_data,
                data,
                job_timeout=120,
                result_ttl=120,
            )

            response_object = {
                "status": "success",
                "message": {"task_id": task.get_id()},
            }
            return response_object, 202

api.add_resource(NoiseObservation, "/cesva/v1")


class TaskStatus(Resource):
    def get(self, task_id):
        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
            q = Queue()
            task = q.fetch_job(task_id)
        if task:
            response_object = {
                "status": "success",
                "message": {
                    "task_id": task.get_id(),
                    "task_status": task.get_status(),
                    "task_result": task.result,
                },
            }
        else:
            response_object = {"status": "error"}
        return jsonify(response_object)


api.add_resource(TaskStatus, "/taskstatus/<task_id>")
