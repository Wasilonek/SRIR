from webservices import db
from datetime import datetime


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_received = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    program_result = db.Column(db.String, nullable=False)
    program_code = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Result %r>' % self.program_result
