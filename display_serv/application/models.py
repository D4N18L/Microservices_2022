from . import db
from datetime import datetime


class DisplayQrCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    qr_code = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<DisplayQrCode %r>' % self.qr_code

    def update(self, user_id):
        self.user_id = user_id
        self.is_active = True
        self.qr_code = self.qr_code
        return self

    def delete(self):
        self.is_active = False
        return self

    def convert_to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'qr_code': self.qr_code,
            'is_active': self.is_active
        }
