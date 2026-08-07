# Content Moderation Agent System

Sistema multiagente de moderação de conteúdo desenvolvido com **Python e LangGraph**, utilizando agentes especializados para analisar comentários, pesquisar políticas de moderação e produzir recomendações de decisão.

O projeto demonstra uma arquitetura de **Agentic AI com workflow controlado, estado compartilhado, persistência, roteamento condicional e Human-in-the-Loop**.

---

## Visão Geral

Sistemas de moderação de conteúdo precisam lidar com diferentes tipos de comentários e, em determinados casos, tomar decisões que exigem contexto adicional ou revisão humana.

Este projeto implementa um workflow multiagente no qual diferentes responsabilidades são separadas entre agentes especializados.

O fluxo principal é:

```text
Comentário
    │
    ▼
┌──────────────┐
│   Analyzer   │
└──────┬───────┘
       │
       ▼
  Classificação
       │
   ┌───┴───────────────┐
   │                   │
Neutro/Positivo    Problemático
   │                   │
   ▼                   ▼
  END          ┌───────────────────┐
               │ Policy Researcher │
               └─────────┬─────────┘
                         │
                         ▼
                  Human-in-the-Loop
                         │
                         ▼
                  ┌─────────────┐
                  │   Reviewer  │
                  └──────┬──────┘
                         │
                         ▼
                        END
```

---

# Problema

A moderação automática de conteúdo pode apresentar dificuldades quando um comentário contém:

* spam;
* linguagem inadequada;
* conteúdo potencialmente problemático;
* situações que exigem consulta às políticas de moderação;
* casos em que uma decisão automática precisa ser revisada por um humano.

Uma abordagem baseada em um único agente concentra responsabilidades diferentes em um mesmo componente.

Este projeto explora uma alternativa baseada em **agentes especializados e orquestração explícita**, permitindo separar:

1. análise inicial;
2. pesquisa de políticas;
3. revisão da decisão;
4. intervenção humana;
5. persistência do estado da execução.

---

# Objetivo

O objetivo é construir uma arquitetura de referência para um sistema de moderação baseado em agentes capaz de:

* analisar comentários;
* identificar conteúdo potencialmente problemático;
* consultar políticas relevantes;
* encaminhar casos complexos para revisão;
* interromper o workflow antes de uma decisão final;
* permitir intervenção humana;
* persistir o estado da execução;
* retomar o workflow posteriormente;
* manter responsabilidades bem definidas entre os agentes.

O projeto também serve como laboratório de práticas de **AI Engineering**, incluindo testes automatizados, arquitetura modular, persistência e workflows controlados.

---

# Arquitetura

O sistema utiliza **LangGraph** como camada de orquestração.

O estado compartilhado é representado por `AgentState`:

```python
class AgentState(TypedDict):
    comentario_original: str
    politicas_relevantes: str
    analise_do_agente: str
    status_da_moderacao: str
    justificativa_final: str
```

Cada nó do workflow recebe esse estado e retorna apenas as alterações relacionadas à sua responsabilidade.

## Componentes

### Analyzer

Responsável pela análise inicial do comentário.

Identifica se o conteúdo é:

* positivo;
* neutro;
* potencialmente problemático.

---

### Policy Researcher

Executado somente quando o Analyzer identifica um comentário potencialmente problemático.

Sua responsabilidade é buscar e fornecer políticas relevantes para apoiar a decisão de moderação.

---

### Reviewer

Responsável pela decisão final de moderação.

Pode produzir recomendações como:

* aprovação;
* remoção;
* edição;
* outras decisões apropriadas ao contexto analisado.

---

### Human-in-the-Loop

Casos que chegam ao Reviewer podem ser interrompidos antes da execução do agente.

Isso permite que uma pessoa:

1. consulte o estado atual;
2. analise as informações produzidas pelos agentes;
3. altere informações do estado;
4. retome o workflow;
5. permita que o Reviewer conclua a decisão.

---

# Persistência

O projeto utiliza o **SQLite Checkpointer do LangGraph** para persistir o estado das execuções.

O banco é armazenado em:

```text
data/checkpoints.db
```

Cada execução pode ser identificada por um `thread_id`.

Exemplo:

```python
config = {
    "configurable": {
        "thread_id": "moderation-thread-001"
    }
}
```

Isso permite interromper uma execução e retomá-la posteriormente mantendo o estado anterior.

---

# Human-in-the-Loop

O Human-in-the-Loop é implementado através da interrupção do workflow antes do Reviewer.

Conceitualmente:

```text
Analyzer
    │
    ▼
Policy Researcher
    │
    ▼
┌──────────────────────────┐
│ INTERVENÇÃO HUMANA       │
│                          │
│ get_state()              │
│ update_state()           │
└────────────┬─────────────┘
             │
             ▼
          Reviewer
             │
             ▼
            END
```

Durante a interrupção, o estado pode ser consultado:

```python
current_state = workflow.get_state(config)
```

E informações adicionais podem ser registradas:

```python
workflow.update_state(
    config,
    {
        "justificativa_final": (
            "Revisão humana realizada antes da decisão."
        )
    },
)
```

O workflow pode então continuar utilizando o mesmo `thread_id`.

---

# Stack Tecnológica

| Tecnologia                  | Função                                 |
| --------------------------- | -------------------------------------- |
| Python 3.12+                | Linguagem principal                    |
| LangGraph                   | Orquestração do workflow multiagente   |
| LangChain                   | Componentes e integração com modelos   |
| SQLite                      | Persistência local                     |
| langgraph-checkpoint-sqlite | Persistência do estado do LangGraph    |
| Pydantic                    | Validação de estruturas de dados       |
| pytest                      | Testes automatizados                   |
| pytest-asyncio              | Suporte a testes assíncronos           |
| Ruff                        | Linting e qualidade de código          |
| python-dotenv               | Gerenciamento de variáveis de ambiente |
| Tavily                      | Pesquisa externa de políticas          |
| Google GenAI                | Integração com modelo de linguagem     |

---

# Estrutura do Projeto

```text
content-moderation-agent-system/
│
├── data/
│   └── checkpoints.db
│
├── src/
│   └── content_moderation/
│       │
│       ├── agents/
│       │   ├── analyzer.py
│       │   ├── base.py
│       │   ├── models.py
│       │   ├── policy_researcher.py
│       │   └── reviewer.py
│       │
│       ├── graph/
│       │   ├── routing.py
│       │   └── workflow.py
│       │
│       ├── persistence/
│       │   └── checkpointer.py
│       │
│       ├── state/
│       │   └── agent_state.py
│       │
│       └── tools/
│
├── tests/
│   │
│   ├── agents/
│   │
│   ├── graph/
│   │   ├── test_execution_flow.py
│   │   ├── test_human_in_the_loop.py
│   │   ├── test_human_review_state.py
│   │   ├── test_routing.py
│   │   └── test_workflow.py
│   │
│   ├── persistence/
│   │   ├── test_checkpointer.py
│   │   └── test_workflow_checkpoint.py
│   │
│   └── test_project.py
│
├── .env.example
├── pyproject.toml
├── README.md
└── ...
```

---

# Requisitos

* Python 3.12 ou superior
* ambiente virtual Python
* credenciais das APIs utilizadas pelo projeto, quando necessário

---

# Instalação

Clone o repositório e entre no diretório:

```bash
git clone https://github.com/Vagnerkrg/content-moderation-agent-system.git

cd content-moderation-agent-system
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente no Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -e .
```

Para instalar as dependências de desenvolvimento:

```bash
pip install -e ".[dev]"
```

---

# Configuração

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Configure no `.env` as credenciais necessárias para os serviços externos utilizados pelo projeto.

Exemplo conceitual:

```env
GOOGLE_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key
```

> Nunca versione credenciais reais no repositório.

---

# Execução

O workflow pode ser construído através de:

```python
workflow = build_workflow()
```

Para utilizar persistência:

```python
with get_checkpointer() as checkpointer:
    workflow = build_workflow(
        checkpointer=checkpointer,
    )
```

Para habilitar Human-in-the-Loop:

```python
with get_checkpointer() as checkpointer:
    workflow = build_workflow(
        checkpointer=checkpointer,
        interrupt_before=["reviewer"],
    )
```

---

# Exemplos de Comentários

## Comentário neutro

```text
"Este curso é excelente."
```

Fluxo esperado:

```text
Analyzer
   │
   ▼
Neutro
   │
   ▼
 END
```

O comentário não necessita de pesquisa de políticas nem revisão adicional.

---

## Comentário potencialmente problemático

```text
"Compre agora! Isso é spam."
```

Fluxo esperado:

```text
Analyzer
   │
   ▼
Problemático
   │
   ▼
Policy Researcher
   │
   ▼
Human Review
   │
   ▼
Reviewer
   │
   ▼
Remover
```

---

## Linguagem inadequada

Exemplo conceitual:

```text
Comentário contendo linguagem inadequada.
```

Fluxo:

```text
Analyzer
   │
   ▼
Problemático
   │
   ▼
Policy Researcher
   │
   ▼
Human Review
   │
   ▼
Reviewer
   │
   ▼
Recomendar edição
```

---

# Exemplos de Decisões

O Reviewer pode produzir decisões como:

| Situação              | Decisão                    |
| --------------------- | -------------------------- |
| Comentário neutro     | Aprovar                    |
| Spam                  | Remover                    |
| Linguagem inadequada  | Recomendar edição          |
| Problema desconhecido | Avaliar contexto adicional |

A decisão é registrada no estado compartilhado do workflow.


# Demonstração

Esta seção apresenta evidências visuais da execução do sistema, incluindo o workflow multiagente, a validação automatizada e o fluxo de Human-in-the-Loop.

## Execução do Workflow

A execução do workflow é validada através da suíte de testes de fluxo, cobrindo diferentes cenários de moderação e roteamento entre os agentes.

![Execução do workflow](docs/images/execution-flow.png)

---

## Human-in-the-Loop

O workflow suporta interrupção antes da execução do `Reviewer`, permitindo que uma pessoa inspecione o estado produzido pelos agentes antes da decisão final.

![Workflow pausado para revisão humana](docs/images/human-review-paused.png)

Durante a pausa, o estado da execução pode ser consultado e atualizado pelo processo de revisão humana.

![Estado da revisão humana](docs/images/human-review-state.png)

Após a intervenção, o workflow pode ser retomado utilizando o mesmo `thread_id`, preservando o estado atualizado e permitindo que o `Reviewer` conclua a decisão.

![Workflow retomado após revisão humana](docs/images/human-review-resumed.png)

---

## Testes e Qualidade

O projeto possui uma suíte automatizada com **41 testes**, cobrindo agentes, roteamento, execução do workflow, persistência, checkpoint e Human-in-the-Loop.

![Suíte de testes](docs/images/test-suite.png)

A validação de qualidade também inclui linting com Ruff e compilação dos módulos Python.



---

# Testes

O projeto segue uma abordagem orientada a testes.

Execute toda a suíte:

```powershell
pytest
```

Estado atual da suíte:

```text
41 passed
```

Também são executadas verificações de qualidade:

```powershell
ruff check .
```

Resultado esperado:

```text
All checks passed!
```

A compilação dos módulos pode ser validada com:

```powershell
python -m compileall src
```

---

# Qualidade e Engenharia

O projeto busca demonstrar práticas utilizadas em sistemas reais de AI Engineering:

* separação de responsabilidades;
* agentes especializados;
* estado compartilhado;
* roteamento explícito;
* persistência;
* workflows determinísticos;
* Human-in-the-Loop;
* testes automatizados;
* validação estática;
* configuração por ambiente;
* tratamento controlado de erros;
* arquitetura modular.

A intenção não é apenas demonstrar o uso de um framework de agentes, mas construir uma base que possa evoluir para um sistema de moderação mais completo.

---

# Roadmap

Possíveis evoluções do projeto:

* interface para revisão humana;
* observabilidade das execuções;
* tracing dos agentes;
* métricas de qualidade;
* avaliação automática das decisões;
* datasets de avaliação;
* armazenamento de histórico de decisões;
* autenticação do painel de revisão;
* execução assíncrona;
* deployment;
* integração com APIs de moderação;
* avaliação de diferentes modelos de linguagem.

---

# Status

**Projeto em desenvolvimento.**

As funcionalidades atualmente implementadas incluem:

* arquitetura multiagente;
* Analyzer;
* Policy Researcher;
* Reviewer;
* roteamento condicional;
* SQLite Checkpoint;
* persistência do estado;
* `thread_id`;
* Human-in-the-Loop;
* interrupção antes do Reviewer;
* inspeção do estado;
* atualização do estado;
* retomada do workflow;
* suíte automatizada com 41 testes.

---

# Autor

**Vagner Ferreira**

Data Scientist | AI/Data Engineer | LLM & Agentic Systems

Brasil

---

## Licença

Este projeto é destinado a fins educacionais, experimentais e de portfólio profissional.
