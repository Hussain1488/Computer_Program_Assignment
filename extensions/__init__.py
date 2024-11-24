# extensions/__init__.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()  # Do not initialize with app here
bcrypt = Bcrypt()  # Do not initialize with app here
