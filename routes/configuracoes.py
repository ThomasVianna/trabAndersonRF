import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from routes.auth import login_required

config_bp = Blueprint('config', __name__)


@config_bp.route('/')
@login_required
def index():
    admin = {
        'nome': session.get('admin_nome', os.getenv('ADMIN_NAME', 'Administrador')),
        'email': session.get('admin_email', os.getenv('ADMIN_EMAIL', 'admin@siat.com')),
    }
    return render_template('configuracoes.html', admin=admin)


@config_bp.route('/atualizar', methods=['POST'])
@login_required
def atualizar():
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    session['admin_nome'] = nome or session.get('admin_nome', os.getenv('ADMIN_NAME', 'Administrador'))
    session['admin_email'] = email or session.get('admin_email', os.getenv('ADMIN_EMAIL', 'admin@siat.com'))
    flash('Configurações atualizadas com sucesso.', 'success')
    return redirect(url_for('config.index'))
