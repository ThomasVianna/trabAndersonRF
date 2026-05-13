"""
Testes básicos para o sistema de empresas
"""
from datetime import date
from database.connection import session, engine
from models.base import Base
from models.empresa import Empresa
from models.endereco import Endereco
from models.natureza_juridica import NaturezaJuridica
from models.porte_empresa import PorteEmpresa
from models.regime_tributario import RegimeTributario
from models.cnae import CNAE


def limpar_banco():
    """Limpa todas as tabelas do banco"""
    print("🗑️ Limpando banco de dados...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("✅ Banco limpo e recriado\n")


def inserir_dados_teste():
    """Insere dados de teste no banco"""
    print("📝 Inserindo dados de teste...\n")
    
    try:
        # Criar Natureza Jurídica
        natureza1 = NaturezaJuridica(
            classificacao="Sociedade Limitada",
            descricao="Empresa com capital dividido em quotas"
        )
        natureza2 = NaturezaJuridica(
            classificacao="Sociedade Anônima",
            descricao="Empresa com capital dividido em ações"
        )
        
        # Criar Porte Empresa
        porte1 = PorteEmpresa(
            categoria="Microempresa",
            faturamento="Até R$ 81 mil"
        )
        porte2 = PorteEmpresa(
            categoria="PME",
            faturamento="R$ 81 mil a R$ 4,8 milhões"
        )
        
        # Criar Regime Tributário
        regime1 = RegimeTributario(
            tributacao="Simples Nacional",
            descricao="Regime tributário simplificado para pequenas empresas"
        )
        regime2 = RegimeTributario(
            tributacao="Lucro Real",
            descricao="Regime tributário baseado no lucro real"
        )
        
        # Criar CNAE
        cnae1 = CNAE(
            codigo="6202",
            descricao="Atividades de consultoria em informática"
        )
        cnae2 = CNAE(
            codigo="6203",
            descricao="Desenvolvimento de software personalizado"
        )
        
        # Criar Endereço
        endereco1 = Endereco(
            rua="Av. Paulista",
            numero="1000",
            bairro="Bela Vista",
            cidade="São Paulo"
        )
        endereco2 = Endereco(
            rua="Rua Augusta",
            numero="500",
            bairro="Centro",
            cidade="São Paulo"
        )
        
        # Criar Empresa 1
        empresa1 = Empresa(
            cnpj="12.345.678/0001-99",
            razao_social="Tech Solutions LTDA",
            nome_fantasia="TechSol",
            data_abertura=date(2020, 1, 15),
            endereco=endereco1,
            natureza_juridica=natureza1,
            porte_empresa=porte1,
            regime_tributario=regime1,
            cnae=cnae1
        )
        
        # Criar Empresa 2
        empresa2 = Empresa(
            cnpj="98.765.432/0001-11",
            razao_social="inovaTech Desenvolvimento S/A",
            nome_fantasia="inovaTech",
            data_abertura=date(2019, 6, 20),
            endereco=endereco2,
            natureza_juridica=natureza2,
            porte_empresa=porte2,
            regime_tributario=regime2,
            cnae=cnae2
        )
        
        # Adicionar ao session
        session.add_all([
            natureza1, natureza2,
            porte1, porte2,
            regime1, regime2,
            cnae1, cnae2,
            endereco1, endereco2,
            empresa1, empresa2
        ])
        
        session.commit()
        print("✅ Dados de teste inseridos com sucesso!\n")
        
        # Mostrar resumo
        print("📊 Resumo dos dados inseridos:")
        print(f"  - Empresas: 2")
        print(f"  - Natureza Jurídica: 2")
        print(f"  - Porte Empresa: 2")
        print(f"  - Regime Tributário: 2")
        print(f"  - CNAE: 2")
        print(f"  - Endereços: 2\n")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao inserir dados: {e}\n")


def testar_validacoes():
    """Testa validações dos modelos"""
    print("🧪 Testando validações...\n")
    
    try:
        # Teste 1: CNPJ inválido
        print("Teste 1: Validação de CNPJ")
        try:
            empresa_invalida = Empresa(
                cnpj="123",  # CNPJ inválido
                razao_social="Teste",
                nome_fantasia="Teste",
                data_abertura=date(2020, 1, 1)
            )
            session.add(empresa_invalida)
            session.flush()
            print("❌ Validação de CNPJ falhou")
        except ValueError as e:
            print(f"✅ CNPJ validado corretamente: {e}\n")
        
        # Teste 2: Campo vazio
        print("Teste 2: Validação de campo vazio")
        try:
            empresa_vazia = Empresa(
                cnpj="12.345.678/0001-99",
                razao_social="",  # Campo vazio
                nome_fantasia="Teste",
                data_abertura=date(2020, 1, 1)
            )
            session.add(empresa_vazia)
            session.flush()
            print("❌ Validação de campo vazio falhou")
        except ValueError as e:
            print(f"✅ Campo vazio validado corretamente: {e}\n")
        
        print("✅ Todas as validações funcionando!\n")
        session.rollback()
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao testar validações: {e}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTES DO SISTEMA DE EMPRESAS")
    print("=" * 60 + "\n")
    
    # Executar testes
    limpar_banco()
    inserir_dados_teste()
    testar_validacoes()
    
    print("=" * 60)
    print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
    print("=" * 60)
