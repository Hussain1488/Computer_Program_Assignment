from flask import Flask, render_template, url_for, request, redirect, flash,make_response
from flask_migrate import Migrate
from extensions import db, bcrypt
from tables import User, SingleValue, FinalValues
import classes
import logging
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import uuid


app = Flask(__name__)




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to the login view if unauthorized
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"



# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

db.init_app(app)  
bcrypt.init_app(app)

migrate = Migrate(app, db)
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch user by ID

@app.route('/')
def index():
    if current_user.is_authenticated:
        flash(f'Hello {current_user.username}!', 'success')  # Success message
    else:
        flash(f'Hello Gust!', 'success')
    return render_template('dashboard/index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
       
    if request.method == 'GET':
        return render_template('dashboard/create.html')
    else:
        unique_id = request.cookies.get('user_id')
        if not unique_id:
            unique_id = str(uuid.uuid4())
            response = make_response(render_template('dashboard/create.html'))
            response.set_cookie('user_id', unique_id, max_age=60*60*24*365)  # Setting the cookie
            return response
        try:
            electricity_bill = float(request.form.get('electricity_bill', 0))
            gas_bill = float(request.form.get('gas_bill', 0))
            fuel_bill = float(request.form.get('fuel_bill', 0))
            waste_generate = float(request.form.get('waste_generate', 0))
            recycled_waste = float(request.form.get('recycled_waste', 0))
            yearly_travel = float(request.form.get('yearly_travel', 0))
            fuel_usage = float(request.form.get('fuel_usage', 0))
        
            if any(value < 0 for value in [electricity_bill, gas_bill, fuel_bill, waste_generate, recycled_waste, yearly_travel, fuel_usage]):
                raise ValueError("Inputs cannot be negative.")
            company_name = ''
            if current_user.is_authenticated:
                company_name = current_user.company_name
            else: company_name = request.form.get('company_name')
            
            existing_value = SingleValue.query.filter_by(company_name=company_name).first()
            if existing_value:
                raise ValueError(f"Company '{company_name}' already exists.")
            
            new_value = SingleValue(
                    electricity_bill=electricity_bill,
                    gas_bill=gas_bill,
                    fuel_bill=fuel_bill,
                    waste_generate=waste_generate,
                    recycled_waste=recycled_waste,
                    yearly_travel=yearly_travel,
                    fuel_usage=fuel_usage,
                    company_name=company_name,
                    unique_id=unique_id,
                    user_id=current_user.id if current_user.is_authenticated else None
                )
            
            
            energy_usage = classes.final_energy(electricity_bill, gas_bill,fuel_bill)
            waste = classes.final_waste(waste_generate,recycled_waste)
            business_travel = classes.final_travel(yearly_travel, fuel_usage)
            
            db.session.add(new_value)
            db.session.commit()
            
            final_values = FinalValues(
                single_id=new_value.id,
                energy_usage=energy_usage,
                waste=waste,
                business_travel=business_travel,
            )
            db.session.add(final_values)
            db.session.commit()
            
        except ValueError as ve:
            flash(f'Input Error: {str(ve)}', 'danger')
            return render_template('dashboard/create.html', form_data=request.form)
        except Exception as e:
            # Log the error (optional)
            app.logger.error(f"Unexpected error: {e}")
            flash(f'An unexpected error occurred. Please try again. {e}', 'danger')
            return render_template('dashboard/create.html', form_data=request.form)
        flash('your data has been stored successfuly', 'success')
        return render_template('dashboard/create.html', form_data=request.form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
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
        email_validator = classes.email_validator(email)
        if not email_validator:
            flash('wrong email format', 'danger')
            return redirect(url_for('register', request=request))
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        company_name = request.form.get('company_name')
        if password != re_password: 
            flash('password doesn\'t match.', 'danger')
            return redirect(url_for('register', request=request))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already taken.', 'warning')
            return redirect(url_for('register', request=request))

        new_user = User(username=username, email=email, company_name=company_name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('Auth/register.html')

@app.route('/overview', methods=['GET'])
def overview():
    try:
        single = SingleValue.query.all()
        final = FinalValues.query.all()
        final_data = [record.to_dict() for record in final]
        
        energy_usage_values = [record['energy_usage'] for record in final_data]
        waste_values = [record['waste'] for record in final_data]
        business_travel_values = [record['business_travel'] for record in final_data]
        suggestions= []
        stats = {
            "energy_usage": {
                "min": min(energy_usage_values) if energy_usage_values else None,
                "max": max(energy_usage_values) if energy_usage_values else None,
                "avg": sum(energy_usage_values) / len(energy_usage_values) if energy_usage_values else None

            },
            "waste": {
                "min": min(waste_values) if waste_values else None,
                "max": max(waste_values) if waste_values else None,
                "avg": sum(waste_values) / len(waste_values) if waste_values else None

            },
            "business_travel": {
                "min": min(business_travel_values) if business_travel_values else None,
                "max": max(business_travel_values) if business_travel_values else None,
                "avg": sum(business_travel_values) / len(business_travel_values) if business_travel_values else None
            }
        }
        
        user_id = current_user.id if current_user.is_authenticated else None
        unique_id = request.cookies.get('user_id')
        user_single_records = (
            SingleValue.query.filter_by(user_id=user_id).first()
            if user_id
            else SingleValue.query.filter_by(unique_id=unique_id).first()
        )
        user_final_data = []
        user_final_records = []
        if user_single_records != None:
            app.logger.error(f'Error Fetching Records user_single_records: {user_single_records}')
            user_final_records = FinalValues.query.filter_by(single_id=user_single_records.id).first()
            user_final_data = [user_final_records.to_dict()] if user_final_records else []
            if final:
                suggestions = classes.generate_dynamic_suggestions(user_final_records.energy_usage, user_final_records.waste, user_final_records.business_travel, stats)

            app.logger.error(f'Error Fetching Records user_final_records: {user_final_records}')

        
        # app.logger.debug(f"Final Records: {final}")
        
        # return single_recoreds

        
        
        
        
        return render_template('dashboard/overview.html',
                               user_single=user_single_records, 
                               user_final=user_final_records, 
                               single=single, 
                               final=final, 
                               user_id=user_id,
                               stats =stats ,
                               user_final_data=user_final_data,
                               suggestions=suggestions
                               )
    except Exception as ex:
        app.logger.error(f'Error Fetching Records: {ex}')
        flash(f'Error accured: {ex}')
        return redirect('/')
    

@app.route('/logout')
def logout():
    logout_user()  # Logs out the current user
    flash('You have been logged out.', 'info')  # Optional flash message
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
