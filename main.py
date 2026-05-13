from database.connection import engine, session
from models.base import Base

from models.empresa import Empresa
from models.endereco import Endereco
from models.natureza_juridica import NaturezaJuridica
from models.porte_empresa import PorteEmpresa
from models.regime_tributario import RegimeTributario
from models.cnae import CNAE

print("✅ Importando modelos...")

# Criar todas as tabelas
print("🗄️ Criando tabelas no banco de dados...")
Base.metadata.create_all(engine)
print("✅ Tabelas criadas com sucesso!")

# Exemplo: Adicionar um teste
print("\n📝 Sistema de Empresas carregado e pronto para uso!")
print("   - Banco de dados: database/empresa.db")
print("   - Modelos disponíveis: Empresa, Endereco, NaturezaJuridica, PorteEmpresa, RegimeTributario, CNAE")
