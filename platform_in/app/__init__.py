from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager
import os
import sys
import redis
from flask import jsonify
from elasticapm.contrib.flask import ElasticAPM
import logging

db = SQLAlchemy()

jwt = JWTManager()

elastic_apm = ElasticAPM()
# print(app.config, file=sys.stderr)

template = {
    "swagger": "2.0",
    "info": {
        "title": "Experimental: platform incoming endpoints : in Dev",
        "description": "API for 'IoT' Observations data",
        "contact": {
            "responsibleOrganization": "FVH",
            "responsibleDeveloper": "sheena",
            "email": "sheena.puthanpurayil@fvh.fi",
            "url": "www.forumvirium.fi",
        },
        "version": "0.0.1",
    },
    "securitySchemes": {
        "basic": {"type": "http", "scheme": "basic"},
        "bearerAuth": {
            "description": "JWT Authorization",
            "type": "http",
            "scheme": "bearer",
            "in": "header",
            "bearerFormat": "JWT",
        },
    },
}

swagger = Swagger(template=template)


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    elastic_apm.init_app(app)

    # register blueprints
    from app.resources.user import users_blueprint

    app.register_blueprint(users_blueprint)

    from app import models

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token["jti"]
        return models.RevokedTokenModel.is_jti_blacklisted(jti)

    from app.resources.observations import observations_blueprint
    app.register_blueprint(observations_blueprint)

    from app.resources.datastreams import datastreams_blueprint
    app.register_blueprint(datastreams_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}
    
    @app.route("/")
    def hello_world():
        return jsonify(hello="world")

    return app

