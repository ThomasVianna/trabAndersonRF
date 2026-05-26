from flask import Blueprint, render_template, request, redirect, url_for
from routes.auth import login_required
from utils import get_clientes, create_cliente, delete_cliente_by_id

clientes_bp = Blueprint('clientes', __name__)


@clientes_bp.route('/')
@login_required
def index():
    q = request.args.get('q', '')
    clientes = get_clientes(q=q)
    return render_template('clientes.html', clientes=clientes, q=q)


@clientes_bp.route('/cadastrar', methods=['POST'])
@login_required
def cadastrar():
    create_cliente({
        'nome': request.form.get('nome', '').strip(),
        'cpf': request.form.get('cpf', '').strip(),
        'email': request.form.get('email', '').strip(),
        'telefone': request.form.get('telefone', '').strip(),
        'situacao': request.form.get('situacao', 'Ativo'),
    })
    return redirect(url_for('clientes.index'))


@clientes_bp.route('/deletar/<id>', methods=['POST'])
@login_required
def deletar(id):
    delete_cliente_by_id(id)
    return redirect(url_for('clientes.index'))
