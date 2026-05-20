#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema de Gerenciamento de Empresas
Aplicação principal usando MongoDB.
"""

from database.connection import initialize_database
from utils import (
    listar_todas_empresas,
    buscar_empresa_por_cnpj,
    buscar_empresa_por_razao_social,
    buscar_empresa_por_id,
    exibir_todas_empresas,
    exibir_empresa_detalhes,
)


def inicializar_banco():
    """Verifica a conexão com o MongoDB."""
    print("Conectando ao MongoDB...")
    if initialize_database():
        print("Conexão com MongoDB estabelecida.")
        return True

    print("Falha ao conectar ao MongoDB.")
    return False


def exibir_menu():
    """Exibe o menu principal."""
    print("\n" + "=" * 60)
    print("SISTEMA DE GERENCIAMENTO DE EMPRESAS")
    print("=" * 60)
    print("1. Listar todas as empresas")
    print("2. Buscar empresa por CNPJ")
    print("3. Buscar empresa por razão social")
    print("4. Ver detalhes de uma empresa")
    print("5. Sair")
    print("=" * 60)


def main():
    """Função principal do sistema."""
    print("\n" + "=" * 60)
    print("INICIANDO SISTEMA DE EMPRESAS")
    print("=" * 60)

    if not inicializar_banco():
        print("Falha ao inicializar banco de dados. Saindo...")
        return

    print("\nSistema de Empresas carregado.")
    print("Banco de dados: MongoDB")
    print("Coleção: empresas")
    print("Use 'python test.py' para inserir dados de teste.\n")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            exibir_todas_empresas()

        elif opcao == "2":
            cnpj = input("Digite o CNPJ: ").strip()
            empresa = buscar_empresa_por_cnpj(cnpj)
            exibir_empresa_detalhes(empresa)

        elif opcao == "3":
            razao = input("Digite a razão social (ou parte dela): ").strip()
            empresas = buscar_empresa_por_razao_social(razao)
            if empresas:
                print(f"\nForam encontradas {len(empresas)} empresa(s).")
                for emp in empresas:
                    exibir_empresa_detalhes(emp)
            else:
                print("Nenhuma empresa encontrada.\n")

        elif opcao == "4":
            emp_id = input("Digite o ID da empresa: ").strip()
            empresa = buscar_empresa_por_id(emp_id)
            exibir_empresa_detalhes(empresa)

        elif opcao == "5":
            print("\nAté logo!\n")
            break

        else:
            print("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()

