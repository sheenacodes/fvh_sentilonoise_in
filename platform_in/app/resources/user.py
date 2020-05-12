from flask import jsonify, request, Blueprint
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime
from app import swagger
from flasgger.utils import swag_from
from app.models import PlatformUser, RevokedTokenModel
from app import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)


users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)


def validate_post_registeruser(request):
    # todo check empty strings. enforce min length
    validation_status = True
    result = {}
    try:
        data = request.json

        if not ("username" in data and "email" in data and "password" in data):
            result = {
                "status": "failure",
                "message": "Insufficient Data: Username, email, password are required",
            }
            validation_status = False

        if (
            data["username"].strip() == ""
            or data["email"].strip() == ""
            or data["password"].strip() == ""
        ):
            result = {
                "status": "failure",
                "message": "Insufficient Data: Username, email, password are required",
            }
            validation_status = False

    except Exception as e:
        logging.error(e)
        result = {"status": "failure", "message": "Invalid Input, Check JSON schema"}
        validation_status = False

    response = jsonify(result)
    response.status_code = 400

    return validation_status, response


def validate_post_loginuser(request):
    # todo check empty strings. enforce min length
    validation_status = True
    result = {}
    try:
        data = request.json

        if not ("username" in data and "password" in data):
            result = {
                "status": "failure",
                "message": "Insufficient Data: Username, password are required",
            }
            validation_status = False

        if (data["username"].strip() == "" or data["password"].strip() == ""):
            result = {
                "status": "failure",
                "message": "Insufficient Data: Username, password are required",
            }
            validation_status = False

    except Exception as e:
        logging.error(e)
        result = {"status": "failure", "message": "Invalid Input, Check JSON schema"}
        validation_status = False

    response = jsonify(result)
    response.status_code = 400

    return validation_status, response

def failure_response(message):
    result = {"status": "failure", "message": message}
    response = jsonify(result)
    response.status_code = 400
    return response   


class UserRegistration(Resource):
    @swag_from("apispec/register_user_spec.yml")
    def post(self):
        """
        Post new user
        """
        validation_status, response = validate_post_registeruser(request)

        if not validation_status:
            return response

        data = request.json

        try:
            user = PlatformUser.query.filter_by(username=data["username"]).first()
        except Exception as e:
            logging.error(e)
            return failure_response(message="Database Error")

        if user is not None:
            return failure_response(message="Username exists. Choose another")

        try:
            email = PlatformUser.query.filter_by(email=data["email"]).first()
        except Exception as e:
            logging.error(e)
            return failure_response(message="Database Error")

        if email is not None:
            return failure_response(message="email exists")

        try:
            user = PlatformUser(
                username=data["username"],
                email=data["email"],
                password=data["password"],
            )
            db.session.add(user)
            db.session.commit()

            del data["password"]
            result = {"status": "success", "message": data}
            response = jsonify(result)
            response.status_code = 201
            return response

        except Exception as e:
            logging.error(e)
            return failure_response(message="Database Error")


class UserLogin(Resource):
    @swag_from("apispec/login_user_spec.yml")
    def post(self):
        validation_status, response = validate_post_loginuser(request)

        if not validation_status:
            return response

        data = request.json

        try:
            user = PlatformUser.query.filter_by(username=data["username"]).first()
        except Exception as e:
            logging.error(e)
            return failure_response(message="Database Error")

        if not user:
            return failure_response(message="username not found")

        if user.check_password(data["password"]):
            access_token = create_access_token(identity=data["username"])
            refresh_token = create_refresh_token(identity=data["username"])
            result = {
                "message": "User {} was logged in ".format(data["username"]),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            response = jsonify(result)
            response.status_code = 200
            return jsonify(result)
        else:
            return failure_response(message="wrong credentials")

        


class UserLogoutAccess(Resource):
    @jwt_required
    @swag_from("apispec/logout.yml")
    def post(self):
        jti = get_raw_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message": "Access token has been revoked"},200
        except:
            return {"message": "Something went wrong"}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    @swag_from("apispec/logout.yml")
    def post(self):
        jti = get_raw_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message": "Refresh token has been revoked"}
        except:
            return {"message": "Something went wrong"}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    @swag_from("apispec/logout.yml")
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token}


# class AllUsers(Resource):
#     def get(self):
#         return PlatformUser.return_all()

#     def delete(self):
#         return PlatformUser.delete_all()

api.add_resource(UserRegistration, "/registration")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogoutAccess, "/logout/access")
api.add_resource(UserLogoutRefresh, "/logout/refresh")
api.add_resource(TokenRefresh, "/token/refresh")

