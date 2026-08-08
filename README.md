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
┌─────────────────────┐
│   Analyzer Agent    │
└──────────┬──────────┘
           │
           ▼
     Classificação
           │
     ┌─────┴─────────┐
     │               │
     ▼               ▼
  Neutro/Positivo  Problemático
     │               │
     ▼               ▼
    END      ┌─────────────────────┐
             │  Policy Researcher  │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │      Reviewer       │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │    HUMAN REVIEW     │
             │                     │
             │ Workflow pausado    │
             │ para intervenção    │
             └──────────┬──────────┘
                        │
                 Decisão humana
                        │
                 ┌──────┴──────┐
                 │             │
              Aprovado      Rejeitado
                 │             │
                 └──────┬──────┘
                        │
                        ▼
              ┌─────────────────┐
              │  Final Action   │
              └─────────────────┘
```

---

# Problema

A moderação automática de conteúdo pode apresentar dificuldades quando um comentário contém:

* spam;
* linguagem inadequada;
* conteúdo potencialmente problemático;
* situações que exigem consulta às políticas de moderação;
* casos ambíguos;
* situações em que uma decisão automatizada precisa ser revisada por uma pessoa.

Uma abordagem baseada em um único agente concentra responsabilidades diferentes em um mesmo componente.

Este projeto explora uma alternativa baseada em **agentes especializados e orquestração explícita**, permitindo separar:

1. análise inicial;
2. pesquisa de políticas;
3. revisão da recomendação;
4. intervenção humana;
5. persistência do estado;
6. execução da ação final.

---

# Objetivo

O objetivo é construir uma arquitetura de referência para um sistema de moderação baseado em agentes capaz de:

* analisar comentários;
* identificar conteúdo potencialmente problemático;
* consultar políticas relevantes;
* produzir recomendações de moderação;
* encaminhar casos complexos para revisão;
* interromper o workflow antes da ação final;
* permitir intervenção humana;
* registrar a decisão humana;
* persistir o estado da execução;
* retomar workflows pausados;
* preservar o contexto original da execução;
* manter responsabilidades bem definidas entre os agentes.

O projeto também funciona como laboratório de práticas de **AI Engineering**, incluindo:

* arquitetura modular;
* workflows controlados;
* testes automatizados;
* persistência;
* roteamento condicional;
* tratamento de erros;
* Human-in-the-Loop;
* rastreabilidade de decisões.

---

# Arquitetura

O sistema utiliza **LangGraph** como camada de orquestração do workflow multiagente.

O estado compartilhado é representado por `AgentState`.

Exemplo conceitual:

```python
class AgentState(TypedDict):
    comentario_original: str
    politicas_relevantes: str
    analise_do_agente: str
    status_da_moderacao: str
    justificativa_final: str
    decisao_humana: str
    observacao_humana: str
```

Cada nó do workflow recebe o estado compartilhado e retorna apenas as alterações relacionadas à sua responsabilidade.

---

## Componentes

### Analyzer

Responsável pela análise inicial do comentário.

Identifica se o conteúdo é:

* positivo;
* neutro;
* potencialmente problemático.

O Analyzer também pode identificar situações que exigem investigação adicional.

---

### Policy Researcher

Executado quando o Analyzer identifica um comentário potencialmente problemático.

Sua responsabilidade é buscar e fornecer políticas relevantes para apoiar a decisão de moderação.

O componente separa a etapa de **pesquisa de contexto** da etapa de decisão.

---

### Reviewer

Responsável por analisar:

* comentário original;
* análise produzida pelo Analyzer;
* políticas relevantes;
* contexto disponível.

A partir dessas informações, o Reviewer produz uma recomendação de moderação.

As recomendações podem incluir:

* aprovação;
* remoção;
* edição;
* avaliação adicional;
* outras ações apropriadas ao contexto.

---

### Human-in-the-Loop

O sistema permite interromper o workflow antes da execução da ação final.

Durante a pausa, um moderador pode:

1. consultar o estado atual;
2. analisar a recomendação produzida;
3. revisar o contexto;
4. registrar uma decisão;
5. adicionar uma observação;
6. retomar o workflow;
7. permitir a execução da ação final.

A decisão humana é mantida separadamente da recomendação produzida pelo agente.

Isso permite distinguir claramente:

```text
Recomendação automatizada
          │
          ▼
     Revisão humana
          │
          ▼
    Decisão humana
          │
          ▼
      Ação final
```

---

# Human-in-the-Loop

O Human-in-the-Loop é implementado através da interrupção controlada do workflow.

O objetivo é permitir que uma pessoa intervenha antes de uma ação potencialmente irreversível.

Conceitualmente:

```text
Analyzer
    │
    ▼
Policy Researcher
    │
    ▼
Reviewer
    │
    ▼
┌──────────────────────────────┐
│        HUMAN REVIEW          │
│                              │
│ Workflow pausado             │
│ antes da ação final          │
└──────────────┬───────────────┘
               │
        Decisão humana
               │
        ┌──────┴──────┐
        │             │
     Aprovado      Rejeitado
        │             │
        └──────┬──────┘
               │
               ▼
        Final Action
```

A documentação detalhada da arquitetura está disponível em:

```text
docs/architecture/human-in-the-loop.md
```

O documento descreve:

* fluxo de pausa;
* intervenção humana;
* inspeção do estado;
* atualização do estado;
* decisão humana;
* observações;
* retomada do workflow;
* persistência;
* tratamento de ambiguidade;
* cenários de aprovação e rejeição;
* decisões arquiteturais;
* evolução futura.

---

## Interrupção do Workflow

A interrupção é configurada durante a construção do workflow.

Exemplo conceitual:

```python
workflow = build_workflow(
    checkpointer=checkpointer,
    interrupt_before=["executar_acao_final"],
)
```

Isso permite que os agentes responsáveis pela análise e recomendação concluam suas etapas antes da intervenção humana.

---

## Inspeção do Estado

Durante a pausa, o estado da execução pode ser consultado utilizando o contexto da execução:

```python
paused_state = workflow.get_state(config)
```

Isso permite que o moderador tenha acesso às informações produzidas pelo workflow antes de tomar uma decisão.

---

## Registro da Decisão Humana

A decisão humana é armazenada separadamente da recomendação automatizada.

Exemplo:

```python
workflow.update_state(
    config,
    {
        "decisao_humana": "aprovado",
        "observacao_humana": (
            "Recomendação aprovada pelo moderador."
        ),
    },
)
```

Os principais campos utilizados são:

```text
decisao_humana
observacao_humana
```

Essa separação permite preservar:

* recomendação do agente;
* decisão humana;
* justificativa da intervenção;
* contexto original.

Esse modelo é importante para **auditoria, rastreabilidade e avaliação futura da qualidade das decisões automatizadas**.

---

## Retomada

Após a intervenção humana, o workflow pode ser retomado utilizando o mesmo contexto de execução:

```python
workflow.invoke(
    None,
    config=config,
)
```

O `thread_id` permite recuperar a execução anterior e preservar o estado associado ao workflow.

---

# Persistência

O projeto utiliza o **SQLite Checkpointer** para persistir o estado das execuções do LangGraph.

O banco é armazenado em:

```text
data/checkpoints.db
```

Conceitualmente:

```text
Workflow
    │
    ▼
SQLite Checkpointer
    │
    ├── Estado inicial
    │
    ├── Estado após Analyzer
    │
    ├── Estado após Policy Researcher
    │
    ├── Estado após Reviewer
    │
    ├── Estado durante Human Review
    │
    └── Estado após retomada
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

Isso permite interromper uma execução e retomá-la posteriormente mantendo o contexto persistido.

---

# Comentários Ambíguos

Casos ambíguos são tratados como situações que podem exigir avaliação humana.

Exemplo:

```text
"Talvez seja uma promoção, mas não tenho certeza."
```

Um comentário desse tipo pode exigir informações adicionais antes de uma decisão definitiva.

O fluxo pode seguir:

```text
Analyzer
    │
    ▼
Comentário potencialmente ambíguo
    │
    ▼
Policy Researcher
    │
    ▼
Reviewer
    │
    ▼
Human Review
    │
    ▼
Decisão humana
```

O sistema não deve assumir automaticamente que uma situação ambígua deve ser aprovada ou rejeitada.

A intervenção humana permite adicionar contexto e controlar a decisão final.

---

# Decisão Humana

A decisão humana representa a autoridade final sobre o caso quando o workflow é configurado para exigir revisão.

A recomendação automatizada não é sobrescrita silenciosamente.

Em vez disso, o sistema mantém as duas informações:

```text
Análise automatizada
        │
        ▼
Recomendação do Reviewer
        │
        ▼
Intervenção humana
        │
        ▼
Decisão humana
        │
        ▼
Ação final
```

Essa abordagem melhora a rastreabilidade e permite avaliar posteriormente:

* quando o agente acertou;
* quando o agente errou;
* quando o humano discordou;
* quais tipos de casos exigem intervenção;
* quais recomendações são mais confiáveis.

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
├── docs/
│   └── architecture/
│       └── human-in-the-loop.md
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
│       ├── human_review/
│       │   └── ...
│       │
│       ├── persistence/
│       │   └── checkpointer.py
│       │
│       ├── runtime/
│       │   └── ...
│       │
│       ├── state/
│       │   └── agent_state.py
│       │
│       └── tools/
│
├── tests/
│   │
│   ├── agents/
│   │   ├── test_analyzer.py
│   │   ├── test_base.py
│   │   ├── test_models.py
│   │   ├── test_policy_researcher.py
│   │   └── test_reviewer.py
│   │
│   ├── graph/
│   │   ├── test_execution_flow.py
│   │   ├── test_human_in_the_loop.py
│   │   ├── test_human_review_state.py
│   │   ├── test_routing.py
│   │   └── test_workflow.py
│   │
│   ├── human_review/
│   │   ├── test_human_approval_scenarios.py
│   │   └── test_interface.py
│   │
│   ├── persistence/
│   │   ├── test_checkpointer.py
│   │   └── test_workflow_checkpoint.py
│   │
│   ├── runtime/
│   │   └── test_threads.py
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

* Python 3.12 ou superior;
* ambiente virtual Python;
* credenciais das APIs utilizadas pelo projeto, quando necessário.

---

# Instalação

Clone o repositório:

```bash
git clone https://github.com/Vagnerkrg/content-moderation-agent-system.git
```

Entre no diretório:

```bash
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

```powershell
pip install -e .
```

Para instalar as dependências de desenvolvimento:

```powershell
pip install -e ".[dev]"
```

---

# Configuração

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Configure no `.env` as credenciais necessárias para os serviços externos utilizados pelo projeto.

Exemplo:

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
        interrupt_before=["executar_acao_final"],
    )
```

---

# Exemplos de Comentários

## Comentário Neutro

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

## Comentário Potencialmente Problemático

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
Reviewer
   │
   ▼
Human Review
   │
   ▼
Final Action
```

A decisão final pode resultar em uma recomendação de remoção.

---

## Linguagem Inadequada

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
Reviewer
   │
   ▼
Human Review
   │
   ▼
Final Action
```

O Reviewer pode recomendar uma ação de edição, dependendo do contexto e das políticas encontradas.

---

# Testes

O projeto segue uma abordagem orientada a testes.

Execute toda a suíte:

```powershell
pytest
```

Estado atual:

```text
61 passed in 0.75s
```

Os testes cobrem:

* comportamento dos agentes;
* modelos e validações;
* roteamento;
* execução do workflow;
* preservação do estado;
* Human-in-the-Loop;
* aprovação humana;
* rejeição humana;
* comentários ambíguos;
* interface de revisão;
* persistência;
* checkpoints;
* `thread_id`;
* retomada de execuções.

---

# Qualidade de Código

O projeto utiliza **Ruff** para validação estática.

Execute:

```powershell
ruff check .
```

Resultado atual:

```text
All checks passed!
```

---

# Compilação

A compilação dos módulos Python pode ser validada com:

```powershell
python -m compileall src
```

A execução deve concluir sem erros.

---

# Validação Atual

No estado atual do projeto:

```text
ruff check .
→ All checks passed!

python -m compileall src
→ Compilação concluída sem erros

pytest
→ 61 passed
```

Essas verificações fornecem uma validação básica de:

* qualidade estática;
* integridade sintática;
* comportamento automatizado;
* integração entre componentes;
* persistência;
* Human-in-the-Loop.

---

# Qualidade e Engenharia

O projeto busca demonstrar práticas utilizadas em sistemas reais de **AI Engineering**:

* separação de responsabilidades;
* agentes especializados;
* estado compartilhado;
* roteamento explícito;
* workflows determinísticos;
* persistência;
* checkpoints;
* `thread_id`;
* Human-in-the-Loop;
* intervenção humana controlada;
* testes automatizados;
* validação estática;
* configuração por ambiente;
* tratamento controlado de erros;
* arquitetura modular;
* rastreabilidade de decisões.

A intenção não é apenas demonstrar o uso de um framework de agentes, mas construir uma base arquitetural que possa evoluir para um sistema de moderação mais completo.

---

# Roadmap

Possíveis evoluções do projeto:

* interface dedicada para revisão humana;
* painel de moderação;
* observabilidade das execuções;
* tracing dos agentes;
* métricas de qualidade;
* avaliação automática das decisões;
* datasets de avaliação;
* armazenamento de histórico de decisões;
* autenticação do painel de revisão;
* execução assíncrona;
* deployment;
* integração com APIs externas de moderação;
* avaliação de diferentes modelos de linguagem;
* sistema de auditoria;
* métricas de intervenção humana;
* avaliação de concordância entre agente e moderador.

---

# Status

**Projeto em desenvolvimento.**

Funcionalidades atualmente implementadas:

* arquitetura multiagente;
* Analyzer;
* Policy Researcher;
* Reviewer;
* roteamento condicional;
* estado compartilhado;
* SQLite Checkpointer;
* persistência do estado;
* `thread_id`;
* Human-in-the-Loop;
* interrupção controlada do workflow;
* inspeção do estado;
* atualização do estado;
* registro da decisão humana;
* retomada do workflow;
* cenários de aprovação;
* cenários de rejeição;
* tratamento de comentários ambíguos;
* testes automatizados;
* validação com Ruff;
* validação de compilação Python.

### Validação atual

```text
61 testes passando
Ruff: All checks passed
Compileall: sem erros
```

---

# Documentação

A documentação arquitetural complementar está disponível em:

```text
docs/architecture/
```

Principal documento relacionado ao Human-in-the-Loop:

```text
docs/architecture/human-in-the-loop.md
```

Esse documento apresenta os detalhes de implementação e as decisões arquiteturais relacionadas à intervenção humana.

---

# Autor

**Vagner Ferreira**

Data Scientist | AI/Data Engineer | LLM & Agentic Systems

Brasil

---

## Licença

Este projeto é destinado a fins educacionais, experimentais e de portfólio profissional.
