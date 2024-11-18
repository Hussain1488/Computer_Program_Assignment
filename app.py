from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('dashboard/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('Auth/login.html')
  else:
    return render_template('login.html')
  

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('Auth/register.html')

if __name__ == "__main__":
  app.run(debug=True)