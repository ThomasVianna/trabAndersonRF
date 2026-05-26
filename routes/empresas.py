import requests
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from routes.auth import login_required
from utils import (
    limpar_cnpj,
    get_empresas,
    get_unique_regimes,
    find_empresa_by_cnpj,
    create_empresa,
    update_empresa_by_cnpj,
    delete_empresa_by_id,
)

empresas_bp = Blueprint('empresas', __name__)


@empresas_bp.route('/')
@login_required
def index():
    q = request.args.get('q', '')
    empresas = get_empresas(q=q)
    regimes = get_unique_regimes()
    return render_template('empresas.html', empresas=empresas, q=q, regimes=regimes)


@empresas_bp.route('/cadastrar', methods=['POST'])
@login_required
def cadastrar():
    cnpj = limpar_cnpj(request.form.get('cnpj', ''))
    if not cnpj:
        return redirect(url_for('empresas.index'))
    if find_empresa_by_cnpj(cnpj):
        return redirect(url_for('empresas.index'))

    empresa = {
        'cnpj': cnpj,
        'razao_social': request.form.get('razao_social', '').strip(),
        'nome_fantasia': request.form.get('nome_fantasia', '').strip(),
        'situacao': request.form.get('situacao', 'ATIVA'),
        'regime_tributario': {'tributacao': request.form.get('regime_tributario', '').strip()},
        'cnae': {'codigo': request.form.get('cnae', '').strip(), 'descricao': ''},
        'endereco': {
            'cidade': request.form.get('cidade', '').strip(),
            'rua': request.form.get('rua', '').strip(),
            'numero': request.form.get('numero', '').strip(),
            'bairro': request.form.get('bairro', '').strip(),
        },
    }
    create_empresa(empresa)
    return redirect(url_for('empresas.index'))


@empresas_bp.route('/deletar/<id>', methods=['POST'])
@login_required
def deletar(id):
    delete_empresa_by_id(id)
    return redirect(url_for('empresas.index'))


@empresas_bp.route('/buscar-cnpj/<cnpj>')
@login_required
def buscar_cnpj(cnpj):
    cnpj_limpo = limpar_cnpj(cnpj)
    if len(cnpj_limpo) != 14:
        return jsonify({'ok': False, 'erro': 'CNPJ inválido'})

    try:
        r = requests.get(f'https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}', timeout=10)
        if r.status_code != 200:
            msg = 'CNPJ não encontrado.' if r.status_code == 404 else f'Erro {r.status_code}'
            return jsonify({'ok': False, 'erro': msg})

        data = r.json()
        registro = {
            'cnpj': cnpj_limpo,
            'razao_social': data.get('razao_social', ''),
            'nome_fantasia': data.get('nome_fantasia', ''),
            'situacao': data.get('descricao_situacao_cadastral', ''),
            'municipio': data.get('municipio', ''),
            'uf': data.get('uf', ''),
            'regime_tributario': {'tributacao': data.get('descricao_regime_tributario', '')},
            'cnae': {'codigo': str(data.get('cnae_fiscal', '')), 'descricao': data.get('cnae_fiscal_descricao', '')},
            'natureza_juridica': {
                'classificacao': data.get('descricao_natureza_juridica', ''),
                'descricao': data.get('descricao_natureza_juridica', ''),
            },
            'porte_empresa': {'categoria': data.get('descricao_porte', ''), 'faturamento': ''},
            'endereco': {
                'cidade': data.get('municipio', ''),
                'rua': f"{data.get('tipo_logradouro', '')} {data.get('logradouro', '')}".strip(),
                'numero': data.get('numero', ''),
                'bairro': data.get('bairro', ''),
            },
        }

        update_empresa_by_cnpj(cnpj_limpo, registro)
        return jsonify({'ok': True, 'data': data})
    except Exception as exc:
        return jsonify({'ok': False, 'erro': str(exc)})
