import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

DB_TYPE = os.getenv('DB_TYPE', 'mongodb').lower()
if DB_TYPE != 'mongodb':
    raise ValueError("DB_TYPE deve ser 'mongodb'. Atualize seu arquivo .env.")

MONGO_URI = os.getenv('MONGO_URI', '').strip()
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost').strip()
MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))
MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'empresa').strip()
MONGO_USERNAME = os.getenv('MONGO_USERNAME', '').strip()
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '').strip()
MONGO_AUTH_SOURCE = os.getenv('MONGO_AUTH_SOURCE', 'admin').strip()

try:
    if MONGO_URI:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    else:
        client_args = {'host': MONGO_HOST, 'port': MONGO_PORT}
        if MONGO_USERNAME and MONGO_PASSWORD:
            client_args.update({
                'username': MONGO_USERNAME,
                'password': MONGO_PASSWORD,
                'authSource': MONGO_AUTH_SOURCE,
            })
        client = MongoClient(**client_args, serverSelectionTimeoutMS=5000)

    client.admin.command('ping')
except Exception as exc:
    raise ConnectionFailure(f'Não foi possível conectar ao MongoDB: {exc}') from exc

# Banco de dados e coleções
client_db = client[MONGO_DATABASE]
empresas = client_db.empresas
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

# Configurações via ENV
DB_TYPE = os.getenv('DB_TYPE', 'mongodb').lower()
if DB_TYPE != 'mongodb':
    raise ValueError("DB_TYPE deve ser 'mongodb'. Atualize seu arquivo .env.")

MONGO_URI = os.getenv('MONGO_URI', '').strip()
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost').strip()
MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))
MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'empresa').strip()
MONGO_USERNAME = os.getenv('MONGO_USERNAME', '').strip()
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '').strip()
MONGO_AUTH_SOURCE = os.getenv('MONGO_AUTH_SOURCE', 'admin').strip()

client = None
USE_MOCK = False

try:
    if MONGO_URI:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    else:
        client_args = {'host': MONGO_HOST, 'port': MONGO_PORT}
        if MONGO_USERNAME and MONGO_PASSWORD:
            client_args.update({
                'username': MONGO_USERNAME,
                'password': MONGO_PASSWORD,
                'authSource': MONGO_AUTH_SOURCE,
            })
        client = MongoClient(**client_args, serverSelectionTimeoutMS=5000)

    # Testa conexão
    client.admin.command('ping')
except Exception as exc:
    logging.warning(f'Não foi possível conectar ao MongoDB — entrando em modo DEMO: {exc}')
    USE_MOCK = True


if not USE_MOCK:
    # Banco de dados real
    client_db = client[MONGO_DATABASE]
    empresas = client_db.empresas
    clientes = client_db.clientes
    consultas = client_db.consultas
    lancamentos = client_db.lancamentos


    def _ensure_index(collection, *keys, **kwargs):
        name = kwargs.get('name')
        existing = collection.index_information()
        if name and name in existing:
            return
        try:
            collection.create_index(list(keys), **kwargs)
        except Exception as exc:
            err_text = str(exc).lower()
            if 'same name as the requested index' in err_text or 'already exists' in err_text:
                return
            raise


    _ensure_index(empresas, ('cnpj', 1), unique=True, sparse=True, name='cnpj_1')
    _ensure_index(clientes, ('cpf', 1), unique=True, sparse=True, name='cpf_1')
    _ensure_index(consultas, ('data_consulta', 1), name='data_consulta_1')
    _ensure_index(lancamentos, ('data_vencimento', 1), name='data_vencimento_1')


    def initialize_database():
        try:
            client.admin.command('ping')
            return True
        except Exception:
            return False


else:
    # Implementação simples de coleções em memória para demo/ambiente sem MongoDB
    class MockCollection:
        def __init__(self):
            self._data = []

        def _match(self, doc, query):
            if not query:
                return True
            for k, v in query.items():
                if k == '_id':
                    if doc.get('_id') == v or str(doc.get('_id')) == str(v):
                        continue
                    return False
                # Suporte mínimo para nested keys simples e regex-like strings
                if isinstance(v, dict) and ('$regex' in v or '$or' in v):
                    # não implementado detalhadamente em demo
                    return True
                if doc.get(k) != v:
                    return False
            return True

        def find(self, query=None):
            items = [d.copy() for d in self._data if self._match(d, query)]

            class Loc:
                def __init__(self, items):
                    self._items = items

                def sort(self, key, direction=1):
                    reverse = direction < 0
                    try:
                        self._items.sort(key=lambda x: x.get(key, ''), reverse=reverse)
                    except Exception:
                        pass
                    return self._items

                def limit(self, n):
                    return self._items[:n]

            return Loc(items)

        def find_one(self, query=None):
            for d in self._data:
                if self._match(d, query):
                    return d.copy()
            return None

        def insert_one(self, document):
            doc = dict(document)
            if '_id' not in doc:
                doc['_id'] = uuid4().hex
            self._data.append(doc)
            class R: inserted_id = doc['_id']
            return R()

        def update_one(self, filt, update, upsert=False):
            found = False
            for idx, d in enumerate(self._data):
                if self._match(d, filt):
                    # aplica $set apenas
                    if isinstance(update, dict) and '$set' in update:
                        for k, v in update['$set'].items():
                            d[k] = v
                        self._data[idx] = d
                    else:
                        d.update(update)
                    found = True
                    break
            if not found and upsert:
                new = dict(filt)
                if isinstance(update, dict) and '$set' in update:
                    new.update(update['$set'])
                self.insert_one(new)

        def delete_one(self, filt):
            for idx, d in enumerate(list(self._data)):
                if self._match(d, filt):
                    del self._data[idx]
                    return

        def distinct(self, key):
            vals = set()
            for d in self._data:
                v = d
                for part in key.split('.'):
                    v = v.get(part, {}) if isinstance(v, dict) else {}
                if v:
                    vals.add(v)
            return list(vals)

        def count_documents(self, filt=None):
            if not filt:
                return len(self._data)
            return len([1 for d in self._data if self._match(d, filt)])

    empresas = MockCollection()
    clientes = MockCollection()
    consultas = MockCollection()
    lancamentos = MockCollection()


    def initialize_database():
        # Em modo demo consideramos sempre inicializado
        return True

# Indica se está em modo demo (sem MongoDB)
IS_DEMO = USE_MOCK
