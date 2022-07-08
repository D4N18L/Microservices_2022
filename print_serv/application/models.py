from . import db
from datetime import datetime


class PrintedCode(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_printed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f"PrintedCode('{self.id}', '{self.is_printed}', '{self.created_at}', '{self.updated_at}')"

    def update(self):
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def print(self):
        self.is_printed = True
        self.update()

    def unprint(self):
        self.is_printed = False
        self.update()

    def is_printed_code(self):
        return self.is_printed

    def get_id(self):
        return self.id

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at



