from extensions import db 
from flask_bcrypt import Bcrypt
import enum

bcrypt = Bcrypt()

class StatusEnum(enum.Enum):
    positive = "positive"
    negative = "negative"

class TypeEnum(enum.Enum):
    incr = "incr"
    decr = "decr"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}>"

class FootPrintData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.positive.name)
    name = db.Column(db.String(150), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    standart = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref=db.backref('footprint_data', lazy=True))

    def __repr__(self):
        return f"<FootPrintData {self.name}, User ID: {self.user_id}>"

class Standard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    type = db.Column(db.Enum(TypeEnum), nullable=False)

    def __repr__(self):
        return f"<Standard {self.name} ({self.type})>"
