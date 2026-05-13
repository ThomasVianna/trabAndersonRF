from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = 'sqlite:///database/empresa.db'

try:
    # Criar diretório se não existir
    os.makedirs('database', exist_ok=True)
    
    # Criar engine com logs opcional
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Mude para True para debug
        connect_args={'check_same_thread': False}
    )
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("✅ Conexão com banco de dados estabelecida com sucesso!")
    
except Exception as e:
    print(f"❌ Erro ao conectar ao banco de dados: {e}")
    raise
