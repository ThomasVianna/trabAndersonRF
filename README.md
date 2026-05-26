# SIAT — Sistema Inteligente de Análise Tributária

Aplicação web em Flask integrada a um backend MongoDB. O frontend do projeto foi preservado da pasta SIAT_integrado, e o backend agora utiliza seu banco MongoDB.

## Requisitos
- Python 3.10+
- MongoDB em execução

## Instalação
1. Ative o ambiente virtual:
```powershell
.\.venv\Scripts\Activate.ps1
```
2. Instale dependências:
```powershell
pip install -r requirements.txt
```
3. Configure o MongoDB no arquivo `.env`.

## `.env` mínimo
```env
DB_TYPE=mongodb
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=empresa
ADMIN_EMAIL=admin@siat.com
ADMIN_PASSWORD=admin123
ADMIN_NAME=Administrador
```

## Executar
```powershell
python app.py
```

Acesse `http://localhost:5000`.

## Login padrão
- E-mail: `admin@siat.com`
- Senha: `admin123`

## Seeds de demonstração
Para preencher a aplicação com dados de exemplo (empresas, clientes, consultas e lançamentos), execute:

```powershell
python scripts/seed_demo.py
```

O script funciona tanto no modo demo quanto quando um MongoDB está configurado.

## Como subir o projeto para o GitHub (passo a passo)
1. Crie um repositório novo no GitHub (pelo site ou usando a CLI `gh`).

2. No seu repositório local (pasta do projeto), se ainda não for um repositório Git:

```bash
git init
git add .
git commit -m "Preparar projeto para apresentação"
```

3. Adicione o remote e envie (substitua pela URL do seu repositório):

```bash
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git push -u origin main
```

Alternativa com GitHub CLI (`gh`):

```bash
gh repo create SEU_USUARIO/SEU_REPO --public --source=. --remote=origin --push
```

4. Convidar integrantes do grupo (via web): vá em Settings → Manage access → Invite collaborators

## O que o grupo precisa saber para apresentar
- Como ativar o ambiente virtual e instalar dependências:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- Como iniciar a aplicação:

```powershell
python app.py
```

- Endpoints/fluxos relevantes para demonstrar (ordem sugerida):
	- Landing page: `/`
	- Login: `/auth/login` (use as credenciais padrão)
	- Dashboard: `/dashboard/` (após login)
	- Consultas CNPJ: `/consultas/` e usar o formulário de consulta
	- Empresas: `/empresas/` — listar, cadastrar e deletar
	- Clientes: `/clientes/` — listar, cadastrar e deletar
	- Financeiro: `/financeiro/` — cadastrar lançamentos e visualizar resumo
	- Relatórios: `/relatorios/`

- Caso não exista MongoDB, use o modo demo (funciona automaticamente).
- Para popular dados antes da apresentação rode: `python scripts/seed_demo.py`.

## Checklist rápido para apresentação
- [ ] Instalar dependências e ativar venv
- [ ] Rodar `python scripts/seed_demo.py` (opcional, preencher dados)
- [ ] Rodar `python app.py` e abrir `http://localhost:5000`
- [ ] Fazer login com `admin@siat.com` / `admin123`
- [ ] Demonstrar os fluxos listados acima
- [ ] Mostrar o arquivo `CONTRIBUTORS.md` como crédito ao grupo

## Observações finais
- Não comite segredos (chave `SECRET_KEY`, credenciais reais). Use `.env` e não o repositório público.
- Se quiser, eu posso gerar automaticamente um `git commit` aqui e preparar um comando `git push` — para efetivar o push você precisará inserir suas credenciais/autorizar via `gh`.

Boa apresentação — quer que eu faça o commit localmente com uma mensagem sugerida agora? 

## Modo Demo (sem MongoDB)
Se não houver um servidor MongoDB disponível, o projeto entra automaticamente em modo "demo" usando coleções em memória. Isso permite apresentar o frontend e fluxos básicos sem dependências externas.

Para usar o modo demo, basta não configurar `MONGO_URI` ou não iniciar o MongoDB — a aplicação continuará rodando e aceitará operações básicas (cadastramento, consultas e demonstrações de telas).

## Equipe
Veja os contribuidores em [CONTRIBUTORS.md](CONTRIBUTORS.md)
