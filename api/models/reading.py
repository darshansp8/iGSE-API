from sqlalchemy import desc

from ..utilities import db
from datetime import datetime


class Reading(db.Model):
    __tablename__ = "Reading"
    readingId = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    customerId = db.Column(db.String(), nullable=False)
    submissionDate = db.Column(db.DateTime(), nullable=False)
    elecReadingDay = db.Column(db.Float(), nullable=False)
    elecReadingNight = db.Column(db.Float(), nullable=False)
    gasReading = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return f"<Reading {self.readingId}>"

    @classmethod
    def get_reading_by_id(cls, customer_id):
        return cls.query.order_by(desc(Reading.submissionDate)).filter_by(customerId=customer_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
