import requests
from flask import Blueprint, render_template, jsonify
from routes.auth import login_required
from utils import (
    get_historico_consultas,
    limpar_cnpj,
    update_empresa_by_cnpj,
    save_consulta,
)

consultas_bp = Blueprint('consultas', __name__)


@consultas_bp.route('/')
@login_required
def index():
    historico = get_historico_consultas()
    return render_template('consultas.html', historico=historico)


@consultas_bp.route('/cnpj/<cnpj>')
@login_required
def buscar_cnpj(cnpj):
    cnpj_limpo = limpar_cnpj(cnpj)
    if len(cnpj_limpo) != 14:
        return jsonify({'ok': False, 'erro': 'CNPJ inválido'})

    try:
        r = requests.get(f'https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}', timeout=10)
        if r.status_code != 200:
            msg = 'CNPJ não encontrado.' if r.status_code == 404 else f'Erro {r.status_code}'
            save_consulta(cnpj_limpo, 'Não encontrado')
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
        save_consulta(cnpj_limpo, 'Encontrado', registro.get('razao_social', ''))
        return jsonify({'ok': True, 'data': data})
    except Exception as exc:
        save_consulta(cnpj_limpo, 'Erro')
        return jsonify({'ok': False, 'erro': str(exc)})
