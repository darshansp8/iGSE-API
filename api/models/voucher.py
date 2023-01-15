from ..utilities import db


class Voucher(db.Model):
    __tablename__ = "Voucher"
    evcCode = db.Column(db.String(), primary_key=True, unique=True)
    used = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f"<Voucher {self.evcCode}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

