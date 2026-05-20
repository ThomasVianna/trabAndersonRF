"""
Testes básicos para o sistema de empresas em MongoDB.
"""
from database.connection import empresas, initialize_database
from utils import validar_empresa_documento


def limpar_banco():
    """Limpa a coleção de empresas."""
    print("Limpando a coleção de empresas...")
    empresas.delete_many({})
    print("Coleção limpa.\n")


def inserir_dados_teste():
    """Insere dados de teste no banco."""
    print("Inserindo dados de teste...\n")

    empresas_teste = [
        {
            'cnpj': '12.345.678/0001-99',
            'razao_social': 'Tech Solutions LTDA',
            'nome_fantasia': 'TechSol',
            'data_abertura': '2020-01-15',
            'endereco': {
                'rua': 'Av. Paulista',
                'numero': '1000',
                'bairro': 'Bela Vista',
                'cidade': 'São Paulo',
            },
            'natureza_juridica': {
                'classificacao': 'Sociedade Limitada',
                'descricao': 'Empresa com capital dividido em quotas',
            },
            'porte_empresa': {
                'categoria': 'Microempresa',
                'faturamento': 'Até R$ 81 mil',
            },
            'regime_tributario': {
                'tributacao': 'Simples Nacional',
                'descricao': 'Regime tributário simplificado para pequenas empresas',
            },
            'cnae': {
                'codigo': '6202',
                'descricao': 'Atividades de consultoria em informática',
            },
        },
        {
            'cnpj': '98.765.432/0001-11',
            'razao_social': 'inovaTech Desenvolvimento S/A',
            'nome_fantasia': 'inovaTech',
            'data_abertura': '2019-06-20',
            'endereco': {
                'rua': 'Rua Augusta',
                'numero': '500',
                'bairro': 'Centro',
                'cidade': 'São Paulo',
            },
            'natureza_juridica': {
                'classificacao': 'Sociedade Anônima',
                'descricao': 'Empresa com capital dividido em ações',
            },
            'porte_empresa': {
                'categoria': 'PME',
                'faturamento': 'R$ 81 mil a R$ 4,8 milhões',
            },
            'regime_tributario': {
                'tributacao': 'Lucro Real',
                'descricao': 'Regime tributário baseado no lucro real',
            },
            'cnae': {
                'codigo': '6203',
                'descricao': 'Desenvolvimento de software personalizado',
            },
        },
    ]

    try:
        for empresa in empresas_teste:
            validar_empresa_documento(empresa)

        empresas.insert_many(empresas_teste)
        print("Dados de teste inseridos com sucesso.\n")
        print("Resumo dos dados inseridos:")
        print("  - Empresas: 2")
        print("  - Documentos validados e salvos\n")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}\n")


def testar_validacoes():
    """Testa validações dos documentos de empresa."""
    print("Testando validações...\n")

    try:
        print("Teste 1: CNPJ inválido")
        try:
            empresa_invalida = {
                'cnpj': '123',
                'razao_social': 'Teste',
                'nome_fantasia': 'Teste',
                'data_abertura': '2024-01-01',
                'endereco': {
                    'rua': 'Rua A',
                    'numero': '1',
                    'bairro': 'Centro',
                    'cidade': 'Cidade',
                },
                'natureza_juridica': {
                    'classificacao': 'Teste',
                    'descricao': 'Teste',
                },
                'porte_empresa': {
                    'categoria': 'Teste',
                    'faturamento': 'Teste',
                },
                'regime_tributario': {
                    'tributacao': 'Teste',
                    'descricao': 'Teste',
                },
                'cnae': {
                    'codigo': '1234',
                    'descricao': 'Teste',
                },
            }
            validar_empresa_documento(empresa_invalida)
            print("Validação de CNPJ falhou")
        except ValueError as e:
            print(f"CNPJ inválido detectado corretamente: {e}\n")

        print("Teste 2: Campo vazio")
        try:
            empresa_vazia = {
                'cnpj': '12.345.678/0001-99',
                'razao_social': '',
                'nome_fantasia': 'Teste',
                'data_abertura': '2024-01-01',
                'endereco': {
                    'rua': 'Rua A',
                    'numero': '1',
                    'bairro': 'Centro',
                    'cidade': 'Cidade',
                },
                'natureza_juridica': {
                    'classificacao': 'Teste',
                    'descricao': 'Teste',
                },
                'porte_empresa': {
                    'categoria': 'Teste',
                    'faturamento': 'Teste',
                },
                'regime_tributario': {
                    'tributacao': 'Teste',
                    'descricao': 'Teste',
                },
                'cnae': {
                    'codigo': '1234',
                    'descricao': 'Teste',
                },
            }
            validar_empresa_documento(empresa_vazia)
            print("Validação de campo vazio falhou")
        except ValueError as e:
            print(f"Campo vazio detectado corretamente: {e}\n")

        print("Todas as validações foram executadas.")
    except Exception as e:
        print(f"Erro ao testar validações: {e}\n")


if __name__ == '__main__':
    print('=' * 60)
    print('TESTES DO SISTEMA DE EMPRESAS')
    print('=' * 60 + '\n')

    if not initialize_database():
        print('Não foi possível conectar ao MongoDB. Verifique o arquivo .env e o servidor.')
    else:
        limpar_banco()
        inserir_dados_teste()
        testar_validacoes()

        print('=' * 60)
        print('TESTES CONCLUÍDOS')
        print('=' * 60)
