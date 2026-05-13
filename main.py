#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sistema de Gerenciamento de Empresas
Aplicação principal
"""

from database.connection import engine, session
from models.base import Base
from models.empresa import Empresa
from models.endereco import Endereco
from models.natureza_juridica import NaturezaJuridica
from models.porte_empresa import PorteEmpresa
from models.regime_tributario import RegimeTributario
from models.cnae import CNAE
from utils import (
    listar_todas_empresas, 
    buscar_empresa_por_cnpj,
    buscar_empresa_por_razao_social,
    exibir_todas_empresas,
    exibir_empresa_detalhes
)


def inicializar_banco():
    """Inicializa o banco de dados criando as tabelas"""
    print("✅ Importando modelos...")
    print("🗄️ Criando tabelas no banco de dados...")
    
    try:
        Base.metadata.create_all(engine)
        print("✅ Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False


def exibir_menu():
    """Exibe o menu principal"""
    print("\n" + "="*60)
    print("📋 SISTEMA DE GERENCIAMENTO DE EMPRESAS")
    print("="*60)
    print("1. Listar todas as empresas")
    print("2. Buscar empresa por CNPJ")
    print("3. Buscar empresa por razão social")
    print("4. Ver detalhes de uma empresa")
    print("5. Sair")
    print("="*60)


def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🚀 INICIANDO SISTEMA DE EMPRESAS")
    print("="*60)
    
    # Inicializar banco
    if not inicializar_banco():
        print("❌ Falha ao inicializar banco de dados. Saindo...")
        return
    
    print("\n📝 Sistema de Empresas carregado e pronto para uso!")
    print("   - Banco de dados: database/empresa.db")
    print("   - Modelos disponíveis: Empresa, Endereco, NaturezaJuridica, PorteEmpresa, RegimeTributario, CNAE")
    print("\n💡 Use 'python test.py' para inserir dados de teste")
    print("💡 Use 'python utils.py' para acessar funções de gerenciamento\n")
    
    # Menu interativo
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
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
                print(f"\n✅ Encontradas {len(empresas)} empresa(s)")
                for emp in empresas:
                    exibir_empresa_detalhes(emp)
            else:
                print("❌ Nenhuma empresa encontrada\n")
        
        elif opcao == "4":
            try:
                emp_id = int(input("Digite o ID da empresa: "))
                empresa = session.query(Empresa).get(emp_id)
                exibir_empresa_detalhes(empresa)
            except ValueError:
                print("❌ ID inválido\n")
        
        elif opcao == "5":
            print("\n👋 Até logo!\n")
            break
        
        else:
            print("❌ Opção inválida\n")


if __name__ == "__main__":
    main()

