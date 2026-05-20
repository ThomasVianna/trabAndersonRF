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
            'razao_social': 'InovaTech Desenvolvimento S/A',
            'nome_fantasia': 'InovaTech',
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
        {
            'cnpj': '11.222.333/0001-44',
            'razao_social': 'Alimentos Bom Sabor LTDA',
            'nome_fantasia': 'Bom Sabor',
            'data_abertura': '2018-03-10',
            'endereco': {
                'rua': 'Rua das Flores',
                'numero': '250',
                'bairro': 'Jardim América',
                'cidade': 'Campinas',
            },
            'natureza_juridica': {
                'classificacao': 'Sociedade Limitada',
                'descricao': 'Empresa com capital dividido em quotas',
            },
            'porte_empresa': {
                'categoria': 'PME',
                'faturamento': 'R$ 81 mil a R$ 4,8 milhões',
            },
            'regime_tributario': {
                'tributacao': 'Simples Nacional',
                'descricao': 'Regime tributário simplificado para pequenas empresas',
            },
            'cnae': {
                'codigo': '4721',
                'descricao': 'Comércio varejista de mercadorias em geral',
            },
        },
        {
            'cnpj': '22.333.444/0001-55',
            'razao_social': 'Saúde Viva Serviços Médicos ME',
            'nome_fantasia': 'Saúde Viva',
            'data_abertura': '2021-09-05',
            'endereco': {
                'rua': 'Avenida Brasil',
                'numero': '1500',
                'bairro': 'Centro',
                'cidade': 'Belo Horizonte',
            },
            'natureza_juridica': {
                'classificacao': 'Microempresa Individual',
                'descricao': 'Empresa pequena com empresário individual',
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
                'codigo': '8621',
                'descricao': 'Atividades de atendimento hospitalar',
            },
        },
        {
            'cnpj': '33.444.555/0001-66',
            'razao_social': 'Construir Engenharia S/A',
            'nome_fantasia': 'Construir',
            'data_abertura': '2015-11-12',
            'endereco': {
                'rua': 'Av. dos Andradas',
                'numero': '850',
                'bairro': 'São Pedro',
                'cidade': 'Porto Alegre',
            },
            'natureza_juridica': {
                'classificacao': 'Sociedade Anônima',
                'descricao': 'Empresa com capital dividido em ações',
            },
            'porte_empresa': {
                'categoria': 'Grande Empresa',
                'faturamento': 'Acima de R$ 300 milhões',
            },
            'regime_tributario': {
                'tributacao': 'Lucro Real',
                'descricao': 'Regime tributário baseado no lucro real',
            },
            'cnae': {
                'codigo': '4120',
                'descricao': 'Construção de edifícios',
            },
        },
        {
            'cnpj': '44.555.666/0001-77',
            'razao_social': 'Escola Saber Crescer EIRELI',
            'nome_fantasia': 'Saber Crescer',
            'data_abertura': '2017-02-28',
            'endereco': {
                'rua': 'Rua do Mercado',
                'numero': '45',
                'bairro': 'Vila Nova',
                'cidade': 'Curitiba',
            },
            'natureza_juridica': {
                'classificacao': 'Empresa Individual de Responsabilidade Limitada',
                'descricao': 'Empresa individual com responsabilidade limitada',
            },
            'porte_empresa': {
                'categoria': 'PME',
                'faturamento': 'R$ 81 mil a R$ 4,8 milhões',
            },
            'regime_tributario': {
                'tributacao': 'Simples Nacional',
                'descricao': 'Regime tributário simplificado para pequenas empresas',
            },
            'cnae': {
                'codigo': '8511',
                'descricao': 'Ensino fundamental',
            },
        },
        {
            'cnpj': '55.666.777/0001-88',
            'razao_social': 'Logística Rápida Transporte LTDA',
            'nome_fantasia': 'Logística Rápida',
            'data_abertura': '2016-07-18',
            'endereco': {
                'rua': 'Rodovia BR-101',
                'numero': '1200',
                'bairro': 'Distrito Industrial',
                'cidade': 'Recife',
            },
            'natureza_juridica': {
                'classificacao': 'Sociedade Limitada',
                'descricao': 'Empresa com capital dividido em quotas',
            },
            'porte_empresa': {
                'categoria': 'PME',
                'faturamento': 'R$ 81 mil a R$ 4,8 milhões',
            },
            'regime_tributario': {
                'tributacao': 'Lucro Presumido',
                'descricao': 'Regime tributário simplificado baseado em margem de lucro presumida',
            },
            'cnae': {
                'codigo': '4922',
                'descricao': 'Transporte rodoviário de carga',
            },
        },
        {
            'cnpj': '66.777.888/0001-99',
            'razao_social': 'Moda Casual Atacado ME',
            'nome_fantasia': 'Moda Casual',
            'data_abertura': '2022-05-22',
            'endereco': {
                'rua': 'Rua do Comércio',
                'numero': '310',
                'bairro': 'Centro',
                'cidade': 'Fortaleza',
            },
            'natureza_juridica': {
                'classificacao': 'Microempresa Individual',
                'descricao': 'Empresa pequena com empresário individual',
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
                'codigo': '4645',
                'descricao': 'Comércio atacadista de artigos do vestuário e acessórios',
            },
        },
        {
            'cnpj': '77.888.999/0001-00',
            'razao_social': 'Consultoria Verde Sustentável LTDA',
            'nome_fantasia': 'Verde Sustentável',
            'data_abertura': '2018-12-01',
            'endereco': {
                'rua': 'Alameda Santos',
                'numero': '212',
                'bairro': 'Jardins',
                'cidade': 'São Paulo',
            },
            'natureza_juridica': {
                'classificacao': 'Sociedade Limitada',
                'descricao': 'Empresa com capital dividido em quotas',
            },
            'porte_empresa': {
                'categoria': 'PME',
                'faturamento': 'R$ 81 mil a R$ 4,8 milhões',
            },
            'regime_tributario': {
                'tributacao': 'Lucro Presumido',
                'descricao': 'Regime tributário simplificado baseado em margem de lucro presumida',
            },
            'cnae': {
                'codigo': '7490',
                'descricao': 'Atividades profissionais, científicas e técnicas diversas',
            },
        },
    ]

    try:
        for empresa in empresas_teste:
            validar_empresa_documento(empresa)

        empresas.insert_many(empresas_teste)
        print("Dados de teste inseridos com sucesso.\n")
        print("Resumo dos dados inseridos:")
        print("  - Empresas: 10")
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
