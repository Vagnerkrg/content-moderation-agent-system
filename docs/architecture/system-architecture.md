# System Architecture

## Informações do Documento

**Projeto:** Content Moderation Agent System  
**Módulo:** Architecture  
**Documento:** System Architecture  
**Autor:** Vagner Ferreira  
**Versão:** 1.0  
**Status:** Active

---

# Objetivo

Este documento apresenta a arquitetura técnica completa do **Content Moderation Agent System**.

O sistema utiliza uma arquitetura multiagente baseada em **LangGraph**, na qual agentes especializados colaboram através de um estado compartilhado para analisar, pesquisar políticas e gerar recomendações de moderação.

A arquitetura foi projetada para permitir:

- separação clara de responsabilidades;
- execução controlada por workflow;
- comunicação através de estado compartilhado;
- roteamento condicional;
- persistência de execução;
- recuperação de estado;
- possibilidade de intervenção humana;
- observabilidade;
- avaliação contínua dos agentes;
- evolução futura para utilização de LLMs.

---

# Visão Geral da Arquitetura

O sistema pode ser dividido nas seguintes camadas:

```text
                    Content Moderation System
                              |
                              v
                    +---------------------+
                    |   Workflow Layer    |
                    |      LangGraph      |
                    +----------+----------+
                               |
                               v
                    +---------------------+
                    |     AgentState      |
                    |  Shared State Model  |
                    +----------+----------+
                               |
             +-----------------+-----------------+
             |                 |                 |
             v                 v                 v
        +----------+     +-------------+    +-----------+
        | Analyzer |     |   Policy    |    | Reviewer  |
        |  Agent   |     | Researcher  |    |   Agent   |
        +----------+     +-------------+    +-----------+
             |                 |                 |
             +-----------------+-----------------+
                               |
                               v
                    +---------------------+
                    |   Final Decision    |
                    +---------------------+

                    O LangGraph é responsável pela orquestração.

Os agentes são responsáveis pelo processamento especializado.

O AgentState transporta as informações entre as diferentes etapas.

Componentes Principais
1. AgentState

O AgentState representa o estado compartilhado da execução.

Ele funciona como contrato de comunicação entre os agentes.

Campos principais:

comentario_original
politicas_relevantes
analise_do_agente
status_da_moderacao
justificativa_final

Cada agente recebe o estado atual e retorna as alterações relacionadas à sua responsabilidade.

Princípio

Os agentes não devem depender diretamente uns dos outros.

A comunicação ocorre através do estado compartilhado.

2. BaseAgent

O BaseAgent define o contrato comum dos agentes especializados.

Sua responsabilidade é estrutural.

Ele estabelece uma interface consistente para execução dos agentes.

O BaseAgent não deve:

analisar comentários;
pesquisar políticas;
tomar decisões;
controlar o workflow;
executar ações externas.
3. Analyzer Agent

O Analyzer Agent executa a primeira análise do comentário.

Entrada
comentario_original
Responsabilidades
analisar o conteúdo;
identificar possíveis problemas;
classificar o comentário;
registrar a análise;
preservar os demais campos do estado.
Saída
analise_do_agente
Classificações atuais
positivo
neutro
spam
linguagem inadequada
outro problema

A implementação atual utiliza regras determinísticas.

Essa camada poderá posteriormente incorporar modelos de linguagem.

4. Conditional Router

O router controla o próximo caminho do workflow.

A decisão é baseada na análise produzida pelo Analyzer.

Comentário aprovado ou neutro
Analyzer
    |
    v
Router
    |
    v
END
Comentário potencialmente problemático
Analyzer
    |
    v
Router
    |
    v
Policy Researcher

Essa decisão evita executar agentes adicionais quando eles não são necessários.

5. Policy Researcher Agent

O Policy Researcher Agent fornece contexto normativo para comentários potencialmente problemáticos.

Entrada
comentario_original
analise_do_agente
Responsabilidades
identificar políticas relevantes;
pesquisar diretrizes;
tratar resultados vazios;
tratar erros controlados;
preservar o estado original.
Saída
politicas_relevantes

A arquitetura foi preparada para integração com ferramentas externas, como mecanismos de busca de políticas.

6. Moderation Reviewer Agent

O Moderation Reviewer Agent consolida as informações produzidas pelos agentes anteriores.

Entrada
analise_do_agente
politicas_relevantes
Responsabilidades
avaliar as evidências;
interpretar as políticas;
gerar uma recomendação;
produzir uma justificativa;
preservar o estado original.
Saída
status_da_moderacao
justificativa_final
Recomendações
Aprovado
Remover
Editar

O Reviewer produz uma recomendação.

Ele não executa fisicamente a ação de moderação.

Fluxo LangGraph

O workflow atual pode ser representado através do seguinte fluxo:

flowchart TD
    START([START]) --> ANALYZER[Analyzer Agent]

    ANALYZER --> ROUTER{Conditional Router}

    ROUTER -->|Aprovado / Neutro| END_APPROVED([END])
    ROUTER -->|Potencialmente problemático| POLICY[Policy Researcher]

    POLICY --> REVIEWER[Reviewer Agent]

    REVIEWER --> END_REVIEW([END])

O arquivo fonte do diagrama está disponível em:

docs/architecture/workflow.mmd
Comunicação Entre Agentes

A comunicação utiliza o AgentState.

O fluxo conceitual é:

                    AgentState
                        |
                        v
                  Analyzer Agent
                        |
                        v
                Conditional Router
                   /           \
                  /             \
                 v               v
               END        Policy Researcher
                                  |
                                  v
                         Reviewer Agent
                                  |
                                  v
                                END

Os agentes não precisam conhecer diretamente a implementação dos outros agentes.

Essa característica reduz o acoplamento e facilita a evolução do sistema.

Fluxo Human in the Loop

A arquitetura foi preparada para suportar intervenção humana.

O conceito previsto é:

Analyzer
    |
    v
Router
    |
    v
Policy Researcher
    |
    v
Reviewer
    |
    v
Human Review
    |
    +----> Approve
    |
    +----> Reject
    |
    +----> Request Changes

A intervenção humana pode ser utilizada em situações nas quais a decisão automática não seja considerada suficientemente confiável.

O Human in the Loop representa uma camada futura de controle e segurança.

Checkpoints e Persistência

O workflow pode utilizar checkpoints para persistir o estado das execuções.

A arquitetura de persistência permite:

salvar estados intermediários;
identificar execuções através de threads;
recuperar execuções anteriores;
retomar workflows;
permitir pausas controladas;
preparar o sistema para execução resiliente.

A estratégia prevista utiliza SQLite como mecanismo inicial de persistência.

Conceitualmente:

Workflow
    |
    v
AgentState
    |
    v
Checkpoint
    |
    v
SQLite

O identificador da execução pode ser associado a uma thread para permitir recuperação posterior.

Observabilidade

A arquitetura da Milestone 5 adiciona uma camada de observabilidade ao workflow.

Os principais elementos esperados são:

Workflow Execution
        |
        +---- Agent Logs
        |
        +---- Execution Traces
        |
        +---- Performance Metrics
        |
        +---- Decision Evaluation
        |
        +---- Error Tracking

A observabilidade deverá permitir responder perguntas como:

qual agente foi executado;
quanto tempo cada agente levou;
qual decisão foi produzida;
quais políticas foram utilizadas;
onde uma execução falhou;
quantas execuções foram aprovadas;
quantas foram removidas;
quantas foram encaminhadas para edição.
Avaliação dos Agentes

O sistema deverá permitir avaliar a qualidade das decisões produzidas pelos agentes.

Exemplos de métricas:

Accuracy
Precision
Recall
F1 Score
Decision Consistency
Execution Time
Error Rate

Essas métricas poderão ser utilizadas para comparar:

regras determinísticas;
prompts;
modelos de linguagem;
versões diferentes dos agentes.
Exemplos de Execução
Cenário 1 — Comentário Neutro

Entrada:

"Este curso possui uma boa estrutura."

Fluxo:

START
  |
  v
Analyzer
  |
  v
Router
  |
  v
END

Resultado esperado:

status_da_moderacao = Aprovado
Cenário 2 — Spam

Entrada:

"Compre agora! Isso é spam."

Fluxo:

START
  |
  v
Analyzer
  |
  v
Router
  |
  v
Policy Researcher
  |
  v
Reviewer
  |
  v
END

Resultado esperado:

status_da_moderacao = Remover
Cenário 3 — Linguagem Inadequada

Entrada:

"Comentário contendo linguagem inadequada."

Fluxo:

START
  |
  v
Analyzer
  |
  v
Router
  |
  v
Policy Researcher
  |
  v
Reviewer
  |
  v
END

Resultado esperado:

status_da_moderacao = Editar
Testes

O sistema possui testes automatizados para validar os principais componentes da arquitetura.

A suíte atual valida:

comportamento do Analyzer;
comportamento do Policy Researcher;
comportamento do Reviewer;
contrato do BaseAgent;
modelos de dados;
roteamento;
compilação do workflow;
execução completa do fluxo;
cenários de spam;
cenários de linguagem inadequada;
preservação do estado;
estado final da execução.

Validação registrada:

31 passed

Também são utilizados:

ruff check .
python -m compileall src
Princípios Arquiteturais
Single Responsibility

Cada agente possui uma responsabilidade principal.

Low Coupling

Os agentes não dependem diretamente das implementações internas uns dos outros.

Shared State

A comunicação acontece através do AgentState.

Explicit Workflow

O LangGraph controla explicitamente a sequência de execução.

Testability

Os componentes podem ser testados isoladamente.

Observability

As execuções devem produzir informações suficientes para análise e diagnóstico.

Extensibility

Novos agentes e ferramentas podem ser adicionados sem alterar significativamente o contrato principal.

Human Oversight

Decisões críticas podem ser submetidas à validação humana.

Evolução Arquitetural

A arquitetura atual representa uma fundação para evolução progressiva.

Roadmap arquitetural:

Current
  |
  +--> Multi-Agent Workflow
  |
  +--> Checkpoint Persistence
  |
  +--> Human in the Loop
  |
  +--> Structured Observability
  |
  +--> Agent Evaluation
  |
  +--> LLM Integration
  |
  +--> Prompt Optimization
  |
  +--> Advanced Agent Routing
  |
  +--> Production Deployment

A evolução deve preservar os contratos fundamentais do sistema:

Agent
AgentState
Workflow
Observability
Evaluation
Estrutura Arquitetural

A organização relacionada à arquitetura é:

docs/
└── architecture/
    ├── README.md
    ├── agent-architecture.md
    ├── agent-design.md
    ├── agent-responsibilities.md
    ├── system-architecture.md
    ├── system-overview.md
    ├── workflow.md
    └── workflow.mmd
Critérios de Conclusão
 Arquitetura geral documentada
 Agentes documentados
 Responsabilidades definidas
 Fluxo LangGraph documentado
 AgentState documentado
 Comunicação entre agentes documentada
 Human in the Loop documentado
 Checkpoint e persistência documentados
 Diagrama Mermaid incluído
 Exemplos de execução adicionados
 Observabilidade prevista
 Avaliação dos agentes prevista
Autoria

Vagner Ferreira

Content Moderation Agent System
System Architecture — v1.0

Documento integrante da documentação arquitetural do projeto.