from datetime import datetime
from flask import Blueprint, render_template
from routes.auth import login_required
from utils import (
    count_empresas,
    count_empresas_ativas,
    count_clientes,
    count_consultas,
    get_historico_consultas,
)

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    total_empresas = count_empresas()
    total_clientes = count_clientes()
    total_consultas = count_consultas()
    empresas_ativas = count_empresas_ativas()
    recentes = get_historico_consultas()[:8]
    return render_template(
        'dashboard.html',
        total_empresas=total_empresas,
        total_clientes=total_clientes,
        total_consultas=total_consultas,
        empresas_ativas=empresas_ativas,
        recentes=recentes,
        now=datetime.now().strftime('%d/%m/%Y %H:%M'),
    )
