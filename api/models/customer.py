from ..utilities import db


class Customer(db.Model):

    __tablename__ = 'Customer'
    customer_id = db.Column(db.String(), primary_key=True, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    propertyType = db.Column(db.String(), nullable=False)
    bedroomNum = db.Column(db.Integer(), nullable=False)
    balance = db.Column(db.Float())
    type = db.Column(db.String())

    def __repr__(self):
        return f"<User {self.customer_id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user_by_id(cls, customer_id):
        return cls.query.get_or_404(customer_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

