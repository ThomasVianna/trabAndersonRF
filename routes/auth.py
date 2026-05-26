import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@siat.com')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
ADMIN_NAME = os.getenv('ADMIN_NAME', 'Administrador')
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH')


def _valid_password(password):
    if ADMIN_PASSWORD_HASH:
        return check_password_hash(ADMIN_PASSWORD_HASH, password)
    return password == ADMIN_PASSWORD


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        if email.lower() == ADMIN_EMAIL.lower() and _valid_password(senha):
            session['admin_id'] = 'admin'
            session['admin_nome'] = ADMIN_NAME
            session['admin_email'] = ADMIN_EMAIL
            return redirect(url_for('dashboard.index'))
        flash('E-mail ou senha incorretos.', 'error')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated
