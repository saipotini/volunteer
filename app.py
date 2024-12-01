from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volunteer_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    volunteer_hours = db.relationship('VolunteerHour', backref='volunteer', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class VolunteerHour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organization = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm-password')
        
        # Validate password confirmation
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        
        # Validate password strength
        if len(password) < 8:
            flash('Password must be at least 8 characters long')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful!')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    total_hours = db.session.query(db.func.sum(VolunteerHour.hours)).filter_by(user_id=current_user.id).scalar() or 0
    recent_hours = VolunteerHour.query.filter_by(user_id=current_user.id).order_by(VolunteerHour.date.desc()).limit(5).all()
    return render_template('dashboard.html', total_hours=total_hours, recent_hours=recent_hours)

@app.route('/log_hours', methods=['GET', 'POST'])
@login_required
def log_hours():
    if request.method == 'POST':
        organization = request.form['organization']
        hours = float(request.form['hours'])
        date_str = request.form['date']
        description = request.form['description']
        
        # Convert date string to datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Create new volunteer hour entry
        new_entry = VolunteerHour(
            user_id=current_user.id, 
            organization=organization, 
            hours=hours, 
            date=date, 
            description=description
        )
        
        db.session.add(new_entry)
        db.session.commit()
        
        flash('Volunteer hours logged successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('log_hours.html')

@app.route('/view_hours')
@login_required
def view_hours():
    hours = VolunteerHour.query.filter_by(user_id=current_user.id).order_by(VolunteerHour.date.desc()).all()
    return render_template('view_hours.html', hours=hours)

# Initialize Database
def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
