from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Translation(db.Model):
    __tablename__ = 'translations'

    text = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime)
    uid = db.Column(db.String(100), primary_key=True)
    status = db.Column(db.String(15))
    translation = db.Column(db.String(2000))

    def __init__(self, text, timestamp, uid, status, translation):
        self.text = text
        self.timestamp = timestamp
        self.uid = uid
        self.status = status
        self.translation = translation

    def __repr__(self):
        return '<Text %r>' % self.text
