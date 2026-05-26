"""scripts/seed_demo.py

Popula dados de demonstração no modo demo ou no MongoDB configurado.
Uso:
    python scripts/seed_demo.py
"""
from datetime import datetime
from database.connection import initialize_database, IS_DEMO, empresas, clientes, consultas, lancamentos


def seed():
    ok = initialize_database()
    print('Inicializando seed — conexão ao DB:', 'DEMO' if IS_DEMO else 'MONGO')

    empresas_demo = [
        {
            'cnpj': '12345678000190',
            'razao_social': 'Acme Contábil LTDA',
            'nome_fantasia': 'Acme Contábil',
            'situacao': 'ATIVA',
            'regime_tributario': {'tributacao': 'Simples Nacional'},
            'endereco': {'cidade': 'São Paulo', 'rua': 'Rua Exemplo', 'numero': '100', 'bairro': 'Centro'},
        },
        {
            'cnpj': '98765432000106',
            'razao_social': 'Beta Serviços ME',
            'nome_fantasia': 'Beta Serviços',
            'situacao': 'ATIVA',
            'regime_tributario': {'tributacao': 'Lucro Presumido'},
            'endereco': {'cidade': 'Campinas', 'rua': 'Avenida Demo', 'numero': '500', 'bairro': 'Jardim'},
        },
    ]

    clientes_demo = [
        {'cpf': '11122233344', 'nome': 'Carlos Silva', 'email': 'carlos@example.com', 'telefone': '(11) 99999-0000', 'situacao': 'Ativo'},
        {'cpf': '55566677788', 'nome': 'Mariana Costa', 'email': 'mariana@example.com', 'telefone': '(19) 98888-1111', 'situacao': 'Ativo'},
    ]

    consultas_demo = [
        {'tipo': 'CNPJ', 'documento': '12345678000190', 'resultado': 'Encontrado', 'razao_social': 'Acme Contábil LTDA', 'data_consulta': datetime.utcnow()},
        {'tipo': 'CNPJ', 'documento': '98765432000106', 'resultado': 'Encontrado', 'razao_social': 'Beta Serviços ME', 'data_consulta': datetime.utcnow()},
    ]

    lancamentos_demo = [
        {'descricao': 'Serviço contábil - Maio', 'tipo': 'Receita', 'valor': 1200.0, 'status': 'Pendente', 'data_vencimento': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'descricao': 'Pagamento fornecedores', 'tipo': 'Despesa', 'valor': 700.0, 'status': 'Pago', 'data_vencimento': datetime.utcnow(), 'created_at': datetime.utcnow()},
    ]

    # Inserir/atualizar empresas
    for e in empresas_demo:
        try:
            empresas.update_one({'cnpj': e['cnpj']}, {'$set': e}, upsert=True)
            print('Upsert empresa', e['razao_social'])
        except Exception as exc:
            print('Erro ao inserir empresa', e['cnpj'], exc)

    # Inserir/atualizar clientes
    for c in clientes_demo:
        try:
            clientes.update_one({'cpf': c['cpf']}, {'$set': c}, upsert=True)
            print('Upsert cliente', c['nome'])
        except Exception as exc:
            print('Erro ao inserir cliente', c.get('cpf'), exc)

    # Inserir consultas
    for q in consultas_demo:
        try:
            consultas.insert_one(q)
            print('Inserida consulta', q['documento'])
        except Exception as exc:
            print('Erro ao inserir consulta', exc)

    # Inserir lançamentos
    for l in lancamentos_demo:
        try:
            lancamentos.insert_one(l)
            print('Inserido lancamento', l['descricao'])
        except Exception as exc:
            print('Erro ao inserir lancamento', exc)

    print('Seed finalizado.')


if __name__ == '__main__':
    seed()
