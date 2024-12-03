from flask import Flask, render_template, url_for, request, redirect, flash
from flask_migrate import Migrate
from extensions import db, bcrypt
from classes import User, FootPrintData, Standard
import logging
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


app = Flask(__name__)

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize extensions
db.init_app(app)  # Initialize db with app here
bcrypt.init_app(app)  # Initialize bcrypt with app here
migrate = Migrate(app, db)
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Routes
@app.route('/')
def index():
    flash('Login successful!', 'success') # Success message
    return render_template('dashboard/index.html')

@app.route('/calculate')
def calculate():
    return render_template('dashboard/informant_form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            app.logger.info(f"User {username} logged in successfully")
            flash('Login successful!', 'success')  # Success message
            return redirect(url_for('index'))
        else:
            app.logger.error(f"Invalid login attempt for user {username}")
            flash('Invalid username or password.', 'danger')
    return render_template('Auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already taken.', 'warning')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('Auth/register.html')

if __name__ == "__main__":
    app.run(debug=True)
