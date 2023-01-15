from ..utilities import db
from datetime import datetime


class Reading(db.Model):
    __tablename__ = "Reading"
    readingId = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    customerId = db.Column(db.String(), nullable=False, unique=True)
    submissionDate = db.Column(db.DateTime(), nullable=False)
    elecReadingDay = db.Column(db.Float(), nullable=False)
    elecReadingNight = db.Column(db.Float(), nullable=False)
    gasReading = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return f"<Reading {self.readingId}>"

    def save(self):
        db.session.add(self)
        db.session.commit()
