"""
Funções utilitárias para gerenciar empresas no MongoDB.
"""
import re
from bson.objectid import ObjectId
from database.connection import empresas


def _format_id(document):
    return str(document.get('_id')) if document else None


def _validar_cnpj(cnpj):
    if not cnpj or not cnpj.strip():
        raise ValueError('CNPJ não pode ser vazio')
    cnpj_clean = re.sub(r'\D', '', cnpj)
    if len(cnpj_clean) != 14:
        raise ValueError('CNPJ deve ter 14 dígitos')
    return cnpj.strip()


def _validar_string(nome, valor):
    if not valor or not valor.strip():
        raise ValueError(f'{nome} não pode ser vazio')
    return valor.strip()


def validar_empresa_documento(empresa):
    if not isinstance(empresa, dict):
        raise ValueError('Empresa deve ser um dicionário')

    empresa['cnpj'] = _validar_cnpj(empresa.get('cnpj'))
    empresa['razao_social'] = _validar_string('razao_social', empresa.get('razao_social'))
    empresa['nome_fantasia'] = _validar_string('nome_fantasia', empresa.get('nome_fantasia'))
    empresa['data_abertura'] = _validar_string('data_abertura', empresa.get('data_abertura'))

    endereco = empresa.get('endereco') or {}
    empresa['endereco'] = {
        'rua': _validar_string('endereco.rua', endereco.get('rua')),
        'numero': _validar_string('endereco.numero', endereco.get('numero')),
        'bairro': _validar_string('endereco.bairro', endereco.get('bairro')),
        'cidade': _validar_string('endereco.cidade', endereco.get('cidade')),
    }

    natureza = empresa.get('natureza_juridica') or {}
    empresa['natureza_juridica'] = {
        'classificacao': _validar_string('natureza_juridica.classificacao', natureza.get('classificacao')),
        'descricao': _validar_string('natureza_juridica.descricao', natureza.get('descricao')),
    }

    porte = empresa.get('porte_empresa') or {}
    empresa['porte_empresa'] = {
        'categoria': _validar_string('porte_empresa.categoria', porte.get('categoria')),
        'faturamento': _validar_string('porte_empresa.faturamento', porte.get('faturamento')),
    }

    regime = empresa.get('regime_tributario') or {}
    empresa['regime_tributario'] = {
        'tributacao': _validar_string('regime_tributario.tributacao', regime.get('tributacao')),
        'descricao': _validar_string('regime_tributario.descricao', regime.get('descricao')),
    }

    cnae = empresa.get('cnae') or {}
    empresa['cnae'] = {
        'codigo': _validar_string('cnae.codigo', cnae.get('codigo')),
        'descricao': _validar_string('cnae.descricao', cnae.get('descricao')),
    }

    return empresa


def listar_todas_empresas():
    try:
        return list(empresas.find({}).sort('razao_social', 1))
    except Exception as e:
        print(f'Erro ao listar empresas: {e}')
        return []


def buscar_empresa_por_id(empresa_id):
    try:
        if not ObjectId.is_valid(empresa_id):
            return None
        return empresas.find_one({'_id': ObjectId(empresa_id)})
    except Exception as e:
        print(f'Erro ao buscar empresa por ID: {e}')
        return None


def buscar_empresa_por_cnpj(cnpj):
    try:
        return empresas.find_one({'cnpj': cnpj})
    except Exception as e:
        print(f'Erro ao buscar empresa: {e}')
        return None


def buscar_empresa_por_razao_social(razao_social):
    try:
        regex = {'$regex': re.escape(razao_social), '$options': 'i'}
        return list(empresas.find({'razao_social': regex}))
    except Exception as e:
        print(f'Erro ao buscar empresa: {e}')
        return []


def exibir_empresa_detalhes(empresa):
    if not empresa:
        print('Empresa não encontrada')
        return

    print('\n' + '=' * 60)
    print(f'EMPRESA: {empresa.get("razao_social")}')
    print('=' * 60)
    print(f'ID: {_format_id(empresa)}')
    print(f'CNPJ: {empresa.get("cnpj")}')
    print(f'Nome Fantasia: {empresa.get("nome_fantasia")}')
    print(f'Data de Abertura: {empresa.get("data_abertura")}')

    endereco = empresa.get('endereco', {})
    if endereco:
        print('\nENDEREÇO:')
        print(f'  Rua: {endereco.get("rua")}, nº {endereco.get("numero")}')
        print(f'  Bairro: {endereco.get("bairro")}')
        print(f'  Cidade: {endereco.get("cidade")}')

    natureza = empresa.get('natureza_juridica', {})
    if natureza:
        print(f'\nNATUREZA JURÍDICA: {natureza.get("classificacao")}')

    porte = empresa.get('porte_empresa', {})
    if porte:
        print(f'\nPORTE: {porte.get("categoria")} ({porte.get("faturamento")})')

    regime = empresa.get('regime_tributario', {})
    if regime:
        print(f'\nREGIME TRIBUTÁRIO: {regime.get("tributacao")}')

    cnae = empresa.get('cnae', {})
    if cnae:
        print(f'\nCNAE: {cnae.get("codigo")} - {cnae.get("descricao")}')

    print('\n' + '=' * 60 + '\n')


def exibir_todas_empresas():
    empresas_list = listar_todas_empresas()

    if not empresas_list:
        print('\nNenhuma empresa cadastrada\n')
        return

    print('\n' + '=' * 120)
    print(f"{'ID':<24} {'CNPJ':<18} {'Razão Social':<40} {'Cidade':<20}")
    print('=' * 120)

    for emp in empresas_list:
        cidade = emp.get('endereco', {}).get('cidade', 'N/A')
        print(f"{_format_id(emp):<24} {emp.get('cnpj', ''):<18} {emp.get('razao_social', ''):<40} {cidade:<20}")

    print('=' * 120 + '\n')
