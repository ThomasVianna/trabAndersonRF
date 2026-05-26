import re
from datetime import datetime
from bson.objectid import ObjectId
from database.connection import empresas, clientes, consultas, lancamentos
from database.connection import IS_DEMO


def limpar_cnpj(cnpj):
    return re.sub(r'\D', '', (cnpj or '').strip())


def formatar_cnpj(cnpj):
    raw = limpar_cnpj(cnpj)
    if len(raw) != 14:
        return cnpj or ''
    return f'{raw[:2]}.{raw[2:5]}.{raw[5:8]}/{raw[8:12]}-{raw[12:]}'


def _prepare_empresa(doc):
    if doc is None:
        return None
    empresa = dict(doc)
    empresa['id'] = str(empresa.get('_id'))
    empresa['cnpj_formatado'] = formatar_cnpj(empresa.get('cnpj', ''))
    empresa.setdefault('endereco', {})
    empresa.setdefault('regime_tributario', {})
    empresa.setdefault('cnae', {})
    empresa.setdefault('natureza_juridica', {})
    empresa.setdefault('porte_empresa', {})
    return empresa


def get_empresas(q=None):
    query = {}
    if q:
        q = q.strip()
        regex = {'$regex': re.escape(q), '$options': 'i'}
        query = {
            '$or': [
                {'cnpj': {'$regex': q}},
                {'razao_social': regex},
            ]
        }
    docs = list(empresas.find(query).sort('razao_social', 1))
    return [_prepare_empresa(doc) for doc in docs]


def find_empresa_by_cnpj(cnpj):
    cnpj_clean = limpar_cnpj(cnpj)
    doc = empresas.find_one({'cnpj': cnpj_clean})
    return _prepare_empresa(doc)


def find_empresa_by_id(id_value):
    # Tenta corresponder tanto ObjectId (Mongo) quanto string (mock/demo)
    try:
        try:
            oid = ObjectId(id_value)
        except Exception:
            oid = id_value
        doc = empresas.find_one({'_id': oid})
        if not doc and not IS_DEMO:
            # fallback: tente com a string do ObjectId
            doc = empresas.find_one({'_id': str(oid)})
        return _prepare_empresa(doc)
    except Exception:
        try:
            # última tentativa: buscar por string id
            doc = empresas.find_one({'_id': str(id_value)})
            return _prepare_empresa(doc)
        except Exception:
            return None


def create_empresa(data):
    data = dict(data)
    if 'cnpj' in data:
        data['cnpj'] = limpar_cnpj(data['cnpj'])
    data['created_at'] = datetime.utcnow()
    empresas.insert_one(data)


def update_empresa_by_cnpj(cnpj, data):
    cnpj_clean = limpar_cnpj(cnpj)
    data = dict(data)
    if 'cnpj' in data:
        data['cnpj'] = limpar_cnpj(data['cnpj'])
    data['updated_at'] = datetime.utcnow()
    empresas.update_one({'cnpj': cnpj_clean}, {'$set': data}, upsert=True)


def delete_empresa_by_id(id_value):
    try:
        try:
            empresas.delete_one({'_id': ObjectId(id_value)})
        except Exception:
            empresas.delete_one({'_id': id_value})
    except Exception:
        pass


def get_unique_regimes():
    values = empresas.distinct('regime_tributario.tributacao')
    return [{'id': idx + 1, 'tributacao': v} for idx, v in enumerate(values) if v]


def get_clientes(q=None):
    query = {}
    if q:
        regex = {'$regex': re.escape(q.strip()), '$options': 'i'}
        query = {'$or': [{'nome': regex}, {'cpf': regex}]}
    docs = list(clientes.find(query).sort('nome', 1))
    result = []
    for doc in docs:
        item = dict(doc)
        item['id'] = str(doc.get('_id'))
        result.append(item)
    return result


def create_cliente(data):
    data = dict(data)
    data['cpf'] = re.sub(r'\D', '', (data.get('cpf') or '').strip())
    data['created_at'] = datetime.utcnow()
    clientes.insert_one(data)


def delete_cliente_by_id(id_value):
    try:
        try:
            clientes.delete_one({'_id': ObjectId(id_value)})
        except Exception:
            clientes.delete_one({'_id': id_value})
    except Exception:
        pass


def get_historico_consultas():
    docs = list(consultas.find({}).sort('data_consulta', -1).limit(50))
    result = []
    for doc in docs:
        item = dict(doc)
        item['id'] = str(doc.get('_id'))
        result.append(item)
    return result


def save_consulta(documento, resultado, razao_social=''):
    consultas.insert_one({
        'tipo': 'CNPJ',
        'documento': limpar_cnpj(documento),
        'resultado': resultado,
        'razao_social': razao_social,
        'data_consulta': datetime.utcnow(),
    })


def get_lancamentos():
    docs = list(lancamentos.find({}).sort('data_vencimento', 1))
    result = []
    for doc in docs:
        item = dict(doc)
        item['id'] = str(doc.get('_id'))
        result.append(item)
    return result


def create_lancamento(data):
    record = dict(data)
    record['valor'] = float(data.get('valor') or 0)
    record['data_vencimento'] = data.get('vencimento')
    record['created_at'] = datetime.utcnow()
    lancamentos.insert_one(record)


def delete_lancamento_by_id(id_value):
    try:
        try:
            lancamentos.delete_one({'_id': ObjectId(id_value)})
        except Exception:
            lancamentos.delete_one({'_id': id_value})
    except Exception:
        pass


def resumo_financeiro():
    receitas = 0.0
    despesas = 0.0
    pendentes = 0.0
    for item in get_lancamentos():
        if item.get('tipo') == 'Receita':
            receitas += float(item.get('valor') or 0)
        else:
            despesas += float(item.get('valor') or 0)
        if item.get('status') != 'Pago':
            pendentes += float(item.get('valor') or 0)
    return receitas, despesas, pendentes


def count_empresas():
    return empresas.count_documents({})


def count_empresas_ativas():
    return empresas.count_documents({'situacao': 'ATIVA'})


def count_clientes():
    return clientes.count_documents({})


def count_consultas():
    return consultas.count_documents({})
