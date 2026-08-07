# Workflow Architecture

## Informações do Documento

**Projeto:** Content Moderation Agent System  
**Módulo:** Architecture  
**Documento:** Workflow Architecture  
**Autor:** Vagner Ferreira  
**Versão:** 1.0

---

# Objetivo

Este documento descreve o fluxo de execução do sistema de moderação de conteúdo baseado em **LangGraph**.

O workflow utiliza um estado compartilhado (`AgentState`) para transportar as informações entre os agentes e permite decisões condicionais durante a execução.

---

# Arquitetura do Workflow

O fluxo é composto pelos seguintes componentes:

- Analyzer Agent
- Conditional Router
- Policy Researcher
- Reviewer
- End

O Analyzer realiza a primeira análise do comentário.

A partir dessa análise, o workflow decide se o comentário deve:

1. Finalizar imediatamente, quando considerado positivo ou neutro.
2. Prosseguir para pesquisa de políticas, quando considerado potencialmente problemático.

Comentários problemáticos percorrem então os agentes de pesquisa e revisão antes de receber uma recomendação final.

---

# Fluxo de Execução

```mermaid
flowchart TD
    START([START]) --> ANALYZER[Analyzer Agent]

    ANALYZER --> ROUTER{Conditional Router}

    ROUTER -->|Aprovado / Neutro| END_APPROVED([END])
    ROUTER -->|Potencialmente problemático| POLICY[Policy Researcher]

    POLICY --> REVIEWER[Reviewer Agent]

    REVIEWER --> END_REVIEW([END])

    Fluxo Detalhado
1. Start

O workflow recebe um AgentState contendo o comentário original e os campos necessários para transportar as informações durante a execução.

2. Analyzer Agent

O AnalyzerAgent realiza a análise inicial do comentário.

Responsabilidades:

Receber o comentário original.
Identificar possíveis termos problemáticos.
Produzir uma análise inicial.
Atualizar analise_do_agente.

Exemplo:

Comentário:
"Este curso é excelente."

Resultado:

"Comentário classificado como positivo ou neutro."
3. Conditional Router

O router avalia o resultado produzido pelo Analyzer.

Comentário neutro ou positivo

O fluxo é finalizado diretamente.

Analyzer
   |
   v
Router
   |
   +----> END
Comentário potencialmente problemático

O fluxo continua para o pesquisador de políticas.

Analyzer
   |
   v
Router
   |
   +----> Policy Researcher

Essa decisão evita executar agentes adicionais quando eles não são necessários.

4. Policy Researcher

O Policy Researcher consulta as políticas relevantes para o comentário identificado como potencialmente problemático.

Responsabilidades:

Receber o estado compartilhado.
Consultar políticas relevantes.
Atualizar politicas_relevantes.
Preservar os demais dados do estado.

Quando nenhuma ferramenta externa está configurada, o agente utiliza uma indicação de diretrizes internas.

5. Reviewer Agent

O Reviewer consolida as informações produzidas pelos agentes anteriores.

Entradas principais:

analise_do_agente
politicas_relevantes

O agente produz:

status_da_moderacao
justificativa_final

As recomendações possíveis são:

Aprovado
Remover
Editar
Estado Compartilhado

Todos os agentes utilizam o mesmo AgentState.

comentario_original
politicas_relevantes
analise_do_agente
status_da_moderacao
justificativa_final

O estado permite que cada agente acrescente informações sem perder os dados produzidos anteriormente.

Fluxo de Dados
                    AgentState
                        |
                        v
                +---------------+
                |    Analyzer    |
                +---------------+
                        |
                        v
                +---------------+
                | Conditional   |
                |    Router     |
                +---------------+
                  /           \
                 /             \
                v               v
             END          +-------------+
                          |   Policy    |
                          | Researcher  |
                          +-------------+
                                |
                                v
                         +-------------+
                         |   Reviewer  |
                         +-------------+
                                |
                                v
                               END
Princípios Arquiteturais
Estado compartilhado

Os agentes não precisam conhecer diretamente uns aos outros.

A comunicação acontece por meio do AgentState.

Separação de responsabilidades

Cada agente possui uma responsabilidade específica:

Componente	Responsabilidade
Analyzer	Análise inicial
Router	Decisão do próximo caminho
Policy Researcher	Pesquisa de políticas
Reviewer	Recomendação final
AgentState	Transporte de informações
Execução condicional

O workflow evita executar agentes desnecessariamente.

Comentários aprovados ou neutros não precisam passar pelo pesquisador de políticas e pelo revisor.

Extensibilidade

A arquitetura permite adicionar novos agentes e novas decisões sem alterar o contrato principal do estado compartilhado.

Cenários de Execução
Cenário 1 — Comentário aprovado
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

Resultado:

status_da_moderacao = Aprovado
Cenário 2 — Comentário potencialmente problemático
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

O resultado depende das políticas encontradas.

Cenário 3 — Spam
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
Cenário 4 — Linguagem inadequada
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
Validação

O workflow possui testes automatizados cobrindo:

Compilação do grafo.
Aceitação do AgentState.
Registro dos agentes.
Roteamento condicional.
Fluxo de comentários aprovados.
Fluxo de comentários problemáticos.
Detecção de spam.
Recomendação de edição.
Preservação do comentário original.
Estado final da execução.

A validação atual do projeto apresenta:

31 passed

Além disso:

ruff check .
All checks passed!

E a compilação dos módulos Python é validada com:

python -m compileall src
Evolução Futura

O workflow poderá evoluir para incluir:

LLM para análise semântica.
Pesquisa externa de políticas.
Human-in-the-loop.
Checkpoint e recuperação de execução.
Métricas de execução.
Observabilidade.
Novos agentes especializados.
Roteamento baseado em múltiplos critérios.
Checklist
 Representar fluxo em Mermaid
 Documentar componentes
 Documentar comunicação entre agentes
 Documentar estado compartilhado
 Documentar decisões condicionais
 Documentar cenários de execução
 Documentar validação
 Exportar imagem do grafo
 Atualizar README principal

Autor: Vagner Ferreira
Documento: Workflow Architecture
Versão: 1.0