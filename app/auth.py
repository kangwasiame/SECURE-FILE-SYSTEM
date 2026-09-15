from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        if not username or not email or not password:
            flash('All fields are required.', 'error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
        elif password != confirm:
            flash('Passwords do not match.', 'error')
        elif User.query.filter((User.username == username) | (User.email == email)).first():
            flash('That username or email is already registered.', 'error')
        else:
            db.session.add(User(username=username, email=email, password_hash=generate_password_hash(password)))
            db.session.commit()
            flash('Account created. You can now sign in.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username', '').strip()).first()
        if user and check_password_hash(user.password_hash, request.form.get('password', '')):
            login_user(user)
            session.permanent = True
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')


@auth_bp.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
