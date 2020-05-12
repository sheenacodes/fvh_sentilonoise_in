from app import db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict


class PlatformUser(db.Model):
    __tablename__ = "platformusers"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return f"<PlatformUser {self.username}, {self.email}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {"username": x.username, "email": x.email}

        return {"users": list(map(lambda x: to_json(x), PlatformUser.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {"message": "{} row(s) deleted".format(num_rows_deleted)}
        except:
            return {"message": "Something went wrong"}


class RevokedTokenModel(db.Model):
    __tablename__ = "revoked_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class AssetData(db.Model):
    __tablename__ = "asset_data_hstore"
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(64), index=True, unique=True)
    asset_data = db.Column(MutableDict.as_mutable(HSTORE))

    # def __init__(self, asset_name, asset_data):
    #     self.asset_data = asset_data
    #     self.asset_name = asset_name

    def __repr__(self):
        return f"<Data Stream {self.asset_name}, {self.asset_data}>"

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {"asset name": x.asset_name, "asset data": x.asset_data}

        return {"DataStreams": list(map(lambda x: to_json(x), AssetData.query.all()))}
