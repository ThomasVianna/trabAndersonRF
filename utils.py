"""
Funções utilitárias para gerenciar empresa
"""
from database.connection import session
from models.empresa import Empresa
from models.endereco import Endereco
from models.natureza_juridica import NaturezaJuridica
from models.porte_empresa import PorteEmpresa
from models.regime_tributario import RegimeTributario
from models.cnae import CNAE


def listar_todas_empresas():
    """Lista todas as empresas"""
    try:
        empresas = session.query(Empresa).all()
        return empresas
    except Exception as e:
        print(f"❌ Erro ao listar empresas: {e}")
        return []


def buscar_empresa_por_cnpj(cnpj):
    """Busca uma empresa pelo CNPJ"""
    try:
        empresa = session.query(Empresa).filter(Empresa.cnpj == cnpj).first()
        return empresa
    except Exception as e:
        print(f"❌ Erro ao buscar empresa: {e}")
        return None


def buscar_empresa_por_razao_social(razao_social):
    """Busca empresa pela razão social (contém)"""
    try:
        empresas = session.query(Empresa).filter(
            Empresa.razao_social.ilike(f"%{razao_social}%")
        ).all()
        return empresas
    except Exception as e:
        print(f"❌ Erro ao buscar empresa: {e}")
        return []


def deletar_empresa(empresa_id):
    """Deleta uma empresa pelo ID"""
    try:
        empresa = session.query(Empresa).get(empresa_id)
        if empresa:
            session.delete(empresa)
            session.commit()
            print(f"✅ Empresa deletada com sucesso!")
            return True
        else:
            print("❌ Empresa não encontrada")
            return False
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao deletar empresa: {e}")
        return False


def exibir_empresa_detalhes(empresa):
    """Exibe detalhes completos de uma empresa"""
    if not empresa:
        print("❌ Empresa não encontrada")
        return
    
    print("\n" + "="*60)
    print(f"📋 EMPRESA: {empresa.razao_social}")
    print("="*60)
    print(f"  ID: {empresa.id}")
    print(f"  CNPJ: {empresa.cnpj}")
    print(f"  Nome Fantasia: {empresa.nome_fantasia}")
    print(f"  Data de Abertura: {empresa.data_abertura}")
    
    if empresa.endereco:
        print(f"\n📍 ENDEREÇO:")
        print(f"  Rua: {empresa.endereco.rua}, nº {empresa.endereco.numero}")
        print(f"  Bairro: {empresa.endereco.bairro}")
        print(f"  Cidade: {empresa.endereco.cidade}")
    
    if empresa.natureza_juridica:
        print(f"\n⚖️  NATUREZA JURÍDICA: {empresa.natureza_juridica.classificacao}")
    
    if empresa.porte_empresa:
        print(f"\n📊 PORTE: {empresa.porte_empresa.categoria} ({empresa.porte_empresa.faturamento})")
    
    if empresa.regime_tributario:
        print(f"\n💰 REGIME TRIBUTÁRIO: {empresa.regime_tributario.tributacao}")
    
    if empresa.cnae:
        print(f"\n🏭 CNAE: {empresa.cnae.codigo} - {empresa.cnae.descricao}")
    
    print("\n" + "="*60 + "\n")


def exibir_todas_empresas():
    """Exibe todas as empresas em formato tabular"""
    empresas = listar_todas_empresas()
    
    if not empresas:
        print("\n❌ Nenhuma empresa cadastrada\n")
        return
    
    print("\n" + "="*120)
    print(f"{'ID':<5} {'CNPJ':<18} {'Razão Social':<40} {'Cidade':<20}")
    print("="*120)
    
    for emp in empresas:
        cidade = emp.endereco.cidade if emp.endereco else "N/A"
        print(f"{emp.id:<5} {emp.cnpj:<18} {emp.razao_social:<40} {cidade:<20}")
    
    print("="*120 + "\n")
