# Agent Responsibilities

## Informações do Documento

**Projeto:** Content Moderation Agent System
**Módulo:** Agent Architecture
**Documento:** Agent Responsibilities
**Autor:** Vagner Ferreira
**Versão:** 1.0
**Status:** Draft

---

# Objetivo

Este documento define as responsabilidades dos agentes que compõem o **Content Moderation Agent System**.

A arquitetura utiliza agentes especializados, cada um responsável por uma etapa específica do processo de moderação.

A separação de responsabilidades tem como objetivo:

* reduzir o acoplamento entre componentes;
* facilitar testes unitários;
* permitir evolução independente dos agentes;
* preparar a arquitetura para orquestração com LangGraph;
* facilitar a substituição de regras por modelos de linguagem;
* tornar o fluxo de decisão mais observável e previsível.

---

# Arquitetura dos Agentes

O sistema possui atualmente quatro componentes principais relacionados à camada de agentes:

```text
BaseAgent
    │
    ├── Analyzer
    ├── Policy Researcher
    └── Moderation Reviewer
```

O `BaseAgent` estabelece o contrato arquitetural comum.

Os demais componentes implementam responsabilidades especializadas.

---

# 1. BaseAgent

## Responsabilidade

O `BaseAgent` define a interface comum que os agentes especializados devem seguir.

Ele estabelece um contrato mínimo de execução para garantir consistência entre os diferentes agentes do sistema.

## Responsabilidades

* definir a interface comum dos agentes;
* estabelecer o método de execução;
* padronizar a arquitetura dos agentes;
* servir como base para futuras implementações;
* permitir que novos agentes sejam adicionados sem alterar o contrato existente.

## Não é responsabilidade do BaseAgent

O `BaseAgent` não deve:

* realizar análise de comentários;
* pesquisar políticas;
* tomar decisões de moderação;
* acessar ferramentas externas;
* controlar o fluxo do grafo.

Sua responsabilidade é exclusivamente estrutural.

---

# 2. Comment Analyzer Agent

## Responsabilidade

O **Comment Analyzer Agent** realiza a análise inicial do comentário enviado pelo usuário.

Seu objetivo é identificar a natureza do conteúdo antes que outras etapas do sistema sejam executadas.

## Entrada

O agente recebe:

```text
comentario_original
```

## Processamento

O Analyzer avalia o comentário e identifica possíveis situações como:

* conteúdo positivo;
* conteúdo neutro;
* spam;
* linguagem ofensiva;
* linguagem inadequada;
* outros sinais de possível violação.

A implementação atual utiliza regras simples para identificação inicial.

Essa implementação poderá posteriormente ser substituída ou complementada por um modelo de linguagem.

## Saída

O resultado da análise é armazenado em:

```text
analise_do_agente
```

## Responsabilidades

* receber o comentário original;
* analisar o conteúdo;
* identificar possíveis problemas;
* classificar o comentário;
* registrar a análise no estado compartilhado;
* preservar as demais informações do estado.

## Não é responsabilidade do Analyzer

O Analyzer não deve:

* pesquisar políticas externas;
* tomar a decisão final de moderação;
* executar remoção de comentários;
* editar comentários;
* realizar intervenção humana.

---

# 3. Policy Researcher Agent

## Responsabilidade

O **Policy Researcher Agent** pesquisa as políticas e diretrizes relevantes quando o Analyzer identifica um possível problema.

Seu objetivo é fornecer contexto normativo para apoiar a decisão do agente revisor.

## Entrada

O agente utiliza principalmente:

```text
comentario_original
analise_do_agente
```

## Processamento

Quando uma possível violação é identificada, o agente realiza uma pesquisa relacionada às políticas aplicáveis.

A arquitetura foi preparada para integração com ferramentas externas, como **Tavily**.

A implementação também permite desacoplar a função de pesquisa para facilitar testes e futuras substituições da ferramenta.

## Saída

As informações encontradas são armazenadas em:

```text
politicas_relevantes
```

## Responsabilidades

* verificar se a análise indica uma possível violação;
* pesquisar políticas relacionadas;
* retornar o contexto encontrado;
* tratar resultados vazios;
* tratar falhas controladas da pesquisa;
* preservar as demais informações do estado.

## Não é responsabilidade do Policy Researcher

O agente não deve:

* classificar novamente o comentário;
* tomar a decisão final;
* executar uma ação de moderação;
* substituir a decisão do Moderation Reviewer.

---

# 4. Moderation Reviewer Agent

## Responsabilidade

O **Moderation Reviewer Agent** consolida as informações produzidas pelos agentes anteriores para gerar uma recomendação de moderação.

Ele representa a camada responsável pela interpretação final das evidências disponíveis antes da execução do fluxo de decisão.

## Entrada

O agente utiliza:

```text
analise_do_agente
politicas_relevantes
```

## Processamento

O Reviewer avalia a análise e o contexto das políticas para determinar uma recomendação.

As ações previstas são:

```text
Aprovar
Remover
Editar
```

Exemplos:

```text
Comentário neutro
→ Aprovar

Spam identificado
→ Remover

Linguagem inadequada
→ Editar
```

## Saída

O resultado é registrado no estado através de:

```text
status_da_moderacao
justificativa_final
```

## Responsabilidades

* consolidar a análise;
* considerar as políticas relevantes;
* gerar uma recomendação;
* determinar a ação sugerida;
* produzir a justificativa;
* tratar situações desconhecidas de forma segura;
* preservar o estado original.

## Não é responsabilidade do Reviewer

O Reviewer não deve:

* executar diretamente a ação final;
* remover fisicamente um comentário;
* editar diretamente o conteúdo publicado;
* substituir a intervenção humana;
* controlar a infraestrutura do sistema.

A execução da ação final será responsabilidade de uma etapa posterior do workflow.

---

# Separação de Responsabilidades

A arquitetura segue uma divisão clara:

| Componente            | Responsabilidade           |
| --------------------- | -------------------------- |
| `BaseAgent`           | Define o contrato comum    |
| `Analyzer`            | Analisa o comentário       |
| `Policy Researcher`   | Pesquisa políticas         |
| `Moderation Reviewer` | Gera recomendação          |
| LangGraph             | Orquestra o fluxo          |
| Human in the Loop     | Valida/intervém na decisão |

Essa separação permite que cada componente tenha uma responsabilidade bem definida.

---

# Fluxo Conceitual

O fluxo lógico atual pode ser representado como:

```text
                    ┌──────────────────┐
                    │ Comentário       │
                    │ Original         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Analyzer         │
                    │                  │
                    │ Analisa conteúdo │
                    └────────┬─────────┘
                             │
                    Possível problema?
                       /            \
                     Não             Sim
                     │                │
                     │                ▼
                     │       ┌──────────────────┐
                     │       │ Policy Researcher│
                     │       │                  │
                     │       │ Pesquisa regras  │
                     │       └────────┬─────────┘
                     │                │
                     │                ▼
                     │       ┌──────────────────┐
                     └──────►│ Moderation       │
                             │ Reviewer         │
                             │                  │
                             │ Gera recomendação│
                             └──────────────────┘
```

Este fluxo representa a arquitetura conceitual dos agentes.

A implementação da orquestração através de `StateGraph` será realizada posteriormente na **Milestone 3 — LangGraph Workflow Implementation**.

---

# Princípios Arquiteturais

A implementação dos agentes segue os seguintes princípios:

## Single Responsibility

Cada agente possui uma responsabilidade principal.

## Baixo Acoplamento

Os agentes não devem depender diretamente da implementação interna de outros agentes.

## Estado Compartilhado

As informações necessárias para o fluxo são transportadas através do `AgentState`.

## Testabilidade

Cada agente deve poder ser testado isoladamente.

## Extensibilidade

Novos agentes podem ser adicionados sem modificar significativamente os agentes existentes.

## Orquestração Separada

Os agentes são responsáveis pelo processamento.

O controle da sequência de execução será responsabilidade do LangGraph.

---

# Evolução Planejada

A arquitetura atual representa a fundação da camada de agentes.

As próximas evoluções incluem:

1. integração dos agentes com `StateGraph`;
2. implementação de roteamento condicional;
3. persistência do estado;
4. Human in the Loop;
5. intervenção humana no `AgentState`;
6. observabilidade das execuções;
7. avaliação da qualidade das decisões;
8. evolução dos agentes para utilização de LLMs.

---

# Critérios de Conclusão

Este documento atende ao item de documentação das responsabilidades dos agentes da **Milestone 2 — Agent Architecture Implementation**.

### Checklist

* [x] Responsabilidade do `BaseAgent` documentada
* [x] Responsabilidade do `Analyzer` documentada
* [x] Responsabilidade do `Policy Researcher` documentada
* [x] Responsabilidade do `Moderation Reviewer` documentada
* [x] Entradas e saídas documentadas
* [x] Limites de responsabilidade definidos
* [x] Separação arquitetural documentada
* [x] Evolução planejada documentada

---

# Autoria

**Vagner Ferreira**

Content Moderation Agent System
Agent Architecture — v1.0

---

*Documento integrante da documentação arquitetural do projeto.*
