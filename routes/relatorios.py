from flask import Blueprint, render_template
from routes.auth import login_required
from utils import (
    count_empresas,
    count_empresas_ativas,
    count_consultas,
    count_clientes,
    resumo_financeiro,
)

relatorios_bp = Blueprint('relatorios', __name__)


@relatorios_bp.route('/')
@login_required
def index():
    empresas_total = count_empresas()
    empresas_ativas = count_empresas_ativas()
    consultas_total = count_consultas()
    clientes_ativos = count_clientes()
    receitas_total, despesas_total, _ = resumo_financeiro()
    return render_template(
        'relatorios.html',
        empresas_total=empresas_total,
        empresas_ativas=empresas_ativas,
        consultas_total=consultas_total,
        clientes_ativos=clientes_ativos,
        receitas_total=receitas_total,
        despesas_total=despesas_total,
    )
