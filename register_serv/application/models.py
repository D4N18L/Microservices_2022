from . import db
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import sha256_crypt


class Crownpass(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_picture = db.Column(db.String(100), nullable=True, default='default.jpg')
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False, unique=False)
    address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    api_key = db.Column(db.String(100), nullable=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)



    def encrypt_api_key(self):
        self.api_key = sha256_crypt.hash(self.username + str(datetime.utcnow()))

    def encrypt_password(self):
        self.password = sha256_crypt.hash(self.password)

    def __repr__(self):
        return '<Crownpass {}>'.format(self.username)

    def convert_to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'id': self.id,
            'address': self.address,
            'phone': self.phone,
            'api_key': self.api_key,
            'is_admin': self.is_admin,
            'is_active': True,
        }
