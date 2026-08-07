# Setup de Desenvolvimento

## Sistema de Moderação de Conteúdo Assistido por IA

## Objetivo

Este documento descreve os passos necessários para configurar o ambiente de desenvolvimento do projeto.

---

# Requisitos

## Software necessário

- Python 3.12 ou superior
- Git
- Acesso às APIs:
  - Google Gemini
  - Tavily Search

---

# Clonar o Projeto

Após o repositório estar disponível:

```bash
git clone git@github.com:Vagnerkrg/content-moderation-agent-system.git

cd content-moderation-agent-system

Ambiente Virtual

Criar o ambiente virtual:

python -m venv venv

Ativar no Windows PowerShell:

.\venv\Scripts\Activate.ps1
Instalação das Dependências

Atualizar o pip:

python -m pip install --upgrade pip

Instalar dependências do projeto:

pip install -r requirements.txt

Instalar dependências de desenvolvimento:

pip install -r requirements-dev.txt
Configuração das Variáveis de Ambiente

Criar um arquivo:

.env

na raiz do projeto.

Adicionar:

GEMINI_API_KEY="sua_chave_aqui"

TAVILY_API_KEY="sua_chave_aqui"
Estrutura do Projeto
content-moderation-agent-system/

├── src/
│   └── content_moderation/
│
├── tests/
│
├── docs/
│
├── data/
│
├── .env
├── .env.example
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
Executar Testes

Executar:

pytest

O projeto deve retornar todos os testes aprovados.

Verificação de Qualidade

Executar:

ruff check .

O código deve estar sem erros de lint.

Desenvolvimento

O fluxo recomendado é:

Criar ou alterar uma funcionalidade.
Implementar testes.
Executar pytest.
Executar ruff.
Realizar commit.
Comandos Úteis

Ver testes:

pytest -v

Ver status do Git:

git status

Ver histórico:

git log --oneline
Arquitetura

A implementação seguirá uma arquitetura baseada em:

LangGraph;
múltiplos agentes;
estado compartilhado;
checkpoints;
Human in the Loop.

O objetivo é manter cada componente isolado e com responsabilidade clara.


---

## Depois desse arquivo

Nossa documentação inicial ficará completa:

```text
docs/
│
├── architecture/
│   ├── README.md
│   ├── system-overview.md
│   ├── agent-design.md
│   └── workflow.md
│
└── development/
    └── setup.md