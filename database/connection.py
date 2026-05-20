import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Carregar variáveis de ambiente do arquivo .env
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
        client = MongoClient(MONGO_URI)
    else:
        client_args = {
            'host': MONGO_HOST,
            'port': MONGO_PORT,
        }
        if MONGO_USERNAME and MONGO_PASSWORD:
            client_args.update({
                'username': MONGO_USERNAME,
                'password': MONGO_PASSWORD,
                'authSource': MONGO_AUTH_SOURCE,
            })
        client = MongoClient(**client_args)

    client.admin.command('ping')
except Exception as e:
    raise ConnectionFailure(f"Não foi possível conectar ao MongoDB: {e}") from e

# Banco e coleção usados pelo projeto
db = client[MONGO_DATABASE]
empresas = db.empresas
empresas.create_index('cnpj', unique=True)


def initialize_database():
    """Verifica a conexão com o MongoDB."""
    try:
        client.admin.command('ping')
        return True
    except Exception:
        return False

