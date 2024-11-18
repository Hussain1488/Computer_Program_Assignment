from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class user(db.Model):
  id = db.Collumn(db.Integer, pirmary_key = True)
  username = db.Collumn(db.String(150), nullable=False, unique=True)
  email = db.Collumn(db.String(250), nullable=False, unique=True)
  password = db.Cullumn(db.String(250), nullable=False)
  
  def set_password(self, password):
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
  def check_password(self, password):
    return bcrypt.check_password_hash(self.password, password)
  

  