from ..utilities import db


class Tariff(db.Model):
    __tablename__ = "Tariff"
    tariff_type = db.Column(db.String(), primary_key=True)
    value = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return f"<Tariff {self.tariff_type}>"

    def save(self):
        db.session.add(self)
        db.session.commit()