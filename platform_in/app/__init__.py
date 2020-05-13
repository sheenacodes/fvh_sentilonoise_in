from flask import Flask
import os
import sys
import redis
from flask import jsonify
from elasticapm.contrib.flask import ElasticAPM
import logging

logging.basicConfig(level=logging.INFO)

elastic_apm = ElasticAPM()
# print(app.config, file=sys.stderr)


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    elastic_apm.init_app(app)

    from app.resources.observations import observations_blueprint

    app.register_blueprint(observations_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    @app.route("/")
    def check_app_running():
        return jsonify({"health": "ok"})

    return app
