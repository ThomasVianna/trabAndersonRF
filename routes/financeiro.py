from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from routes.auth import login_required
from utils import get_lancamentos, create_lancamento, delete_lancamento_by_id, resumo_financeiro

financeiro_bp = Blueprint('financeiro', __name__)


@financeiro_bp.route('/')
@login_required
def index():
    lancamentos = get_lancamentos()
    receitas, despesas, pendentes = resumo_financeiro()
    return render_template('financeiro.html', lancamentos=lancamentos, receitas=receitas, despesas=despesas, pendentes=pendentes)


@financeiro_bp.route('/cadastrar', methods=['POST'])
@login_required
def cadastrar():
    vencimento = request.form.get('vencimento')
    if vencimento:
        try:
            vencimento = datetime.fromisoformat(vencimento)
        except ValueError:
            vencimento = None
    create_lancamento({
        'descricao': request.form.get('descricao', '').strip(),
        'tipo': request.form.get('tipo', 'Receita'),
        'valor': request.form.get('valor', 0),
        'status': request.form.get('status', 'Pendente'),
        'vencimento': vencimento,
    })
    return redirect(url_for('financeiro.index'))


@financeiro_bp.route('/deletar/<id>', methods=['POST'])
@login_required
def deletar(id):
    delete_lancamento_by_id(id)
    return redirect(url_for('financeiro.index'))
