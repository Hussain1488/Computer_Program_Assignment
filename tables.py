from flask_login import UserMixin
from extensions import db ,bcrypt
# from flask_bcrypt import Bcrypt
import enum


class StatusEnum(enum.Enum):
    positive = "positive"
    negative = "negative"

class TypeEnum(enum.Enum):
    incr = "incr"
    decr = "decr"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    company_name = db.Column(db.String(250), nullable=False, unique=False)
    password = db.Column(db.String(250), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}>"

class SingleValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    electricity_bill = db.Column(db.Float, nullable=False)
    gas_bill = db.Column(db.Float, nullable=False)
    fuel_bill = db.Column(db.Float, nullable=False)
    waste_generate = db.Column(db.Float, nullable=False)
    recycled_waste = db.Column(db.Float, nullable=False)
    yearly_travel = db.Column(db.Float, nullable=False)
    fuel_usage = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref=db.backref('SingleValue', lazy=True))

    def __repr__(self):
        return f"<FinalValues User ID: {self.user_id}>"

class FinalValues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    energy_usage = db.Column(db.Float, nullable=False)
    waste = db.Column(db.Float, nullable=False)
    business_travel = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<FinalValues User ID: {self.user_id}>"
