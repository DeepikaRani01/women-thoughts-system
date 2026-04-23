from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('posts.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('signup.html')

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already exists!', 'danger')
            return render_template('signup.html')

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        # Check if camera verification was successful (passed via hidden field or session)
        if request.form.get('is_verified') == 'true':
            new_user.gender_verified = True

        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('posts.dashboard'))

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if user.is_banned:
                flash('Your account has been banned due to violations of our safe space guidelines.', 'danger')
                return render_template('login.html')
            login_user(user)
            return redirect(url_for('posts.dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts.home'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
