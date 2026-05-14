from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

DB_TYPE = os.getenv('DB_TYPE', 'sqlite').lower()

if DB_TYPE == 'sqlserver':
    DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 18 for SQL Server')
    DB_SERVER = os.getenv('DB_SERVER', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '1433')
    DB_DATABASE = os.getenv('DB_DATABASE', 'empresa')
    DB_USERNAME = os.getenv('DB_USERNAME', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_TRUSTED_CONNECTION = os.getenv('DB_TRUSTED_CONNECTION', 'no').lower() in ('yes', 'true', '1')
    DB_ENCRYPT = os.getenv('DB_ENCRYPT', 'no').lower() in ('yes', 'true', '1')

    if DB_TRUSTED_CONNECTION:
        odbc_str = (
            f"Driver={{{DB_DRIVER}}};"
            f"Server={DB_SERVER},{DB_PORT};"
            f"Database={DB_DATABASE};"
            "Trusted_Connection=yes;"
        )
    else:
        if not DB_USERNAME or not DB_PASSWORD:
            raise ValueError(
                'Por favor configure DB_USERNAME e DB_PASSWORD ou habilite DB_TRUSTED_CONNECTION=yes'
            )
        odbc_str = (
            f"Driver={{{DB_DRIVER}}};"
            f"Server={DB_SERVER},{DB_PORT};"
            f"Database={DB_DATABASE};"
            f"UID={DB_USERNAME};"
            f"PWD={DB_PASSWORD};"
        )

    if DB_ENCRYPT:
        odbc_str += 'Encrypt=yes;TrustServerCertificate=yes;'

    DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_str)}"
    db_type_str = "SQL Server"

elif DB_TYPE == 'sqlite':
    DB_SQLITE_PATH = os.getenv('DB_SQLITE_PATH', 'database/empresa.db')
    os.makedirs(os.path.dirname(DB_SQLITE_PATH) or '.', exist_ok=True)
    DATABASE_URL = f'sqlite:///{DB_SQLITE_PATH}'
    db_type_str = "SQLite"

else:
    raise ValueError(f"Tipo de banco de dados inválido: {DB_TYPE}. Use 'sqlserver' ou 'sqlite'")

try:
    if DB_TYPE == 'sqlserver':
        engine = create_engine(
            DATABASE_URL,
            echo=False,
            fast_executemany=True
        )
    else:  # sqlite
        engine = create_engine(
            DATABASE_URL,
            echo=False,
            connect_args={'check_same_thread': False}
        )
    
    Session = sessionmaker(bind=engine)
    session = Session()
    print(f"✅ Conexão com {db_type_str} estabelecida com sucesso!")

except Exception as e:
    print(f"❌ Erro ao conectar ao {db_type_str}: {e}")
    raise
