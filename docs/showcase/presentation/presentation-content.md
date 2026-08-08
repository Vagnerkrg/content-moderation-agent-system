# Content Moderation Agent System — Presentation Content

## Informações do Documento

**Projeto:** Content Moderation Agent System
**Módulo:** Showcase / Presentation
**Documento:** Presentation Content
**Autor:** Vagner Ferreira
**Versão:** 1.0
**Status:** Ready for presentation generation

---

# Objetivo

Este documento define o conteúdo oficial da apresentação técnica do projeto **Content Moderation Agent System**.

A apresentação deve funcionar como um **showcase técnico**, apresentando o problema, as decisões arquiteturais, o workflow multiagente, o Human-in-the-Loop, o gerenciamento de estado, a persistência, os testes e os aprendizados obtidos durante o desenvolvimento.

O README permanece como documentação técnica detalhada.

A apresentação deve complementar o README, e não reproduzi-lo.

---

# Diretrizes da Apresentação

## Público

* Engenheiros de software
* Engenheiros de IA
* Data Scientists
* Desenvolvedores interessados em Agentic AI
* Recrutadores técnicos
* Profissionais interessados em LangGraph e sistemas multiagente

## Estilo

A apresentação deve ser:

* profissional
* técnica
* visual
* objetiva
* moderna
* orientada a arquitetura
* com pouco texto por slide

## Diretriz visual

Priorizar:

* diagramas
* fluxos
* arquitetura
* ícones
* blocos de informação
* screenshots reais do projeto quando agregarem evidência

Evitar:

* grandes parágrafos
* excesso de código
* repetir o README
* elementos decorativos sem função

---

# Identidade Visual

## Tema

**Dark Mode**

A apresentação deve utilizar uma estética profissional de tecnologia/engenharia.

Preferência:

* fundo escuro
* alto contraste
* tipografia limpa
* destaques visuais discretos
* aparência de produto técnico / engineering showcase

As cores devem ser utilizadas com moderação para destacar:

* agentes
* fluxo
* estado
* Human-in-the-Loop
* resultados de testes
* CI

---

# Slide 01 — Capa

## Título

**CONTENT MODERATION AGENT SYSTEM**

## Subtítulo

**Multi-Agent Content Moderation with LangGraph & Human-in-the-Loop**

## Supporting text

> A practical study in Agentic AI Engineering

## Autor

**Vagner Ferreira**

Data Scientist | AI/Data Engineer | LLM & Agentic Systems

## Visual

Criar uma composição visual relacionada a:

**AI Agents → Workflow → Human Oversight**

Não utilizar uma fotografia genérica de robô.

---

# Slide 02 — O Problema

## Título

**Automated Content Moderation Is Not Binary**

## Conteúdo

Moderação de conteúdo envolve mais do que classificar um comentário.

### Desafios

* Conteúdo ambíguo
* Contexto de políticas
* Diferentes tipos de violações
* Risco de decisões automáticas incorretas
* Necessidade de rastreabilidade
* Necessidade de intervenção humana

## Pergunta central

> Como construir um sistema de agentes que automatize o processo sem remover o controle humano?

## Visual

Representar visualmente a diferença entre:

**Simple Classification**

versus

**Decision Workflow**

---

# Slide 03 — Objetivo

## Título

**Project Goal**

## Conteúdo

Construir um workflow capaz de:

1. Analisar o comentário
2. Identificar possíveis problemas
3. Pesquisar políticas relevantes
4. Produzir uma recomendação
5. Pausar para revisão humana
6. Registrar a decisão
7. Retomar a execução
8. Executar a ação final

## Princípio

> **Automação onde é seguro. Supervisão humana onde existe impacto.**

## Visual

Representar os oito passos como um fluxo horizontal ou vertical simplificado.

---

# Slide 04 — Solução

## Título

**Multi-Agent Moderation Workflow**

## Conteúdo visual principal

Criar um diagrama profissional:

```text
Comment
   ↓
Analyzer Agent
   ↓
Conditional Routing
   ├── Neutral / Positive → END
   │
   └── Problematic / Ambiguous
              ↓
       Policy Researcher
              ↓
         Reviewer Agent
              ↓
         Human Review
              ↓
         Final Action
              ↓
             END
```

## Destaque

Comentários positivos ou neutros não passam pelo pipeline completo.

Isso evita processamento desnecessário.

---

# Slide 05 — Arquitetura

## Título

**StateGraph Architecture**

## Conteúdo

O workflow é implementado como um **LangGraph StateGraph**.

### Componentes

* AgentState
* Analyzer
* Conditional Router
* Policy Researcher
* Reviewer
* Human Review
* Final Action
* Checkpointer

## Conceito principal

> O estado acompanha a execução inteira.

## Visual

Criar um diagrama arquitetural mostrando os componentes e suas relações.

O **AgentState** deve aparecer visualmente como o contrato que atravessa os diferentes nós.

---

# Slide 06 — Agentes Especializados

## Título

**One Responsibility per Agent**

Apresentar três agentes principais.

### Analyzer Agent

Classifica o conteúdo recebido.

### Policy Researcher

Obtém o contexto relevante das políticas.

### Reviewer Agent

Combina análise + política e produz uma recomendação.

## Por que separar?

* Single Responsibility
* Testabilidade
* Extensibilidade
* Rastreabilidade
* Menor acoplamento

## Visual

Utilizar três blocos independentes conectados ao workflow.

---

# Slide 07 — Estado Compartilhado

## Título

**AgentState as the Communication Contract**

## Conteúdo

Todos os agentes trabalham sobre um estado compartilhado.

### Estado

```text
AgentState
│
├── comentario_original
├── analise_do_agente
├── politicas_relevantes
├── status_da_moderacao
├── justificativa_final
├── decisao_humana
└── observacao_humana
```

## Conceito

Cada agente modifica somente os campos sob sua responsabilidade.

## Resultado

> O histórico completo da decisão permanece disponível durante toda a execução.

## Visual

Mostrar o `AgentState` como um objeto central passando pelos agentes.

---

# Slide 08 — Conditional Routing

## Título

**Not Every Comment Needs the Full Pipeline**

## Conteúdo

O Analyzer determina o próximo caminho.

```text
                 Analyzer
                    │
          ┌─────────┴─────────┐
          │                   │
     Neutral/Positive     Problematic
          │                   │
          ▼                   ▼
         END            Policy Researcher
                              │
                              ▼
                           Reviewer
```

## Benefícios

* Menor custo
* Menor latência
* Fluxo mais simples
* Controle explícito

## Destaque

O routing é uma função explícita e testável, em vez de lógica escondida dentro dos agentes.

---

# Slide 09 — Human-in-the-Loop

## Título

**Human Oversight Is Part of the Architecture**

## Mensagem principal

A recomendação automática não é aplicada imediatamente.

## Fluxo

```text
Analyzer
   ↓
Policy Researcher
   ↓
Reviewer
   ↓
┌─────────────────────┐
│   HUMAN CHECKPOINT  │
│                     │
│  Approve / Reject   │
└──────────┬──────────┘
           ↓
      Final Action
```

## Conceito

> A supervisão humana acontece antes da etapa com consequências reais.

## Visual

Dar destaque visual ao bloco **HUMAN CHECKPOINT**.

---

# Slide 10 — Interrupt & Resume

## Título

**A Workflow That Can Stop and Continue**

## Código

Este é o único trecho de código relevante da apresentação:

```python
workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["executar_acao_final"],
)
```

## Fluxo

```text
Execution
    ↓
Checkpoint
    ↓
Human Review
    ↓
Decision
    ↓
Resume
    ↓
Final Action
```

## Conceito

O mesmo `thread_id` identifica a execução e permite sua retomada.

## Mensagem

> A interrupção não é um erro. É uma etapa controlada do workflow.

---

# Slide 11 — Persistence

## Título

**Stateful Execution with SQLite**

## Conteúdo

O workflow utiliza SQLite como mecanismo de checkpoint.

```text
data/
└── checkpoints.db
```

Cada execução possui um:

```text
thread_id
```

## Permite

* Persistir o estado
* Pausar uma execução
* Recuperar o contexto
* Registrar decisão humana
* Retomar posteriormente

## Insight

> Persistir o estado é o que transforma uma pausa em um workflow realmente retomável.

## Visual

Mostrar:

```text
Workflow
   ↓
Checkpoint
   ↓
SQLite
   ↓
Human Decision
   ↓
Resume
```

---

# Slide 12 — Why LangGraph?

## Título

**Why LangGraph?**

## Tabela

| Requirement          | LangGraph |
| -------------------- | --------- |
| Stateful workflow    | ✅         |
| Conditional routing  | ✅         |
| Interrupt / Resume   | ✅         |
| Checkpointing        | ✅         |
| Explicit graph       | ✅         |
| Testable transitions | ✅         |

## Mensagem

LangGraph não foi utilizado apenas para "chamar agentes".

Foi utilizado para:

> **Orquestrar um workflow stateful, controlável e retomável.**

## Visual

Usar a tabela como elemento central, com destaque para:

**State → Routing → Interrupt → Persistence**

---

# Slide 13 — Testing & Quality

## Título

**Engineering Through Tests**

## Resultado

### 61 / 61 PASSED

## Validações

```text
Ruff
   ↓
PASS

Compileall
   ↓
PASS

Pytest
   ↓
61 PASSED
```

## Cobertura

* Agents
* Graph
* Routing
* Human Review
* Persistence
* Runtime
* Project Environment

## Visual

Dar grande destaque ao número:

**61 TESTS PASSED**

Se possível, utilizar screenshot real do terminal como evidência.

---

# Slide 14 — Continuous Integration

## Título

**Automated Quality Pipeline**

## Fluxo

```text
GitHub
   │
   ▼
Checkout
   │
   ▼
Python 3.12
   │
   ▼
Install Dependencies
   │
   ▼
Ruff
   │
   ▼
Compile
   │
   ▼
Pytest
   │
   ▼
PASS
```

## Mensagem

Cada Push ou Pull Request para `main` executa automaticamente as verificações de qualidade.

## Visual

Representar o pipeline como CI/CD profissional.

Se houver screenshot real do GitHub Actions com execução bem-sucedida, utilizar como evidência.

---

# Slide 15 — Engineering Challenges & Lessons

## Título

**What Was Actually Difficult?**

Dividir o slide em duas áreas.

### Challenges

**01 — Shared State**

Manter o estado consistente entre diferentes agentes.

**02 — Routing**

Separar claramente decisões de roteamento da lógica dos agentes.

**03 — Human Review**

Determinar exatamente onde interromper a execução.

**04 — Persistence**

Garantir que uma execução pudesse ser retomada sem perder contexto.

**05 — Testability**

Testar componentes isoladamente sem depender de integrações externas.

### Lessons Learned

* Estado compartilhado bem definido simplifica sistemas multiagente.
* Human-in-the-Loop deve ser uma decisão arquitetural.
* Persistência é essencial para workflows retomáveis.
* Agentes especializados são mais fáceis de testar e evoluir.
* Routing explícito torna o comportamento previsível.
* Desacoplamento aumenta significativamente a testabilidade.

---

# Slide 16 — Conclusão & Future Evolution

## Título

**Engineering Reliable Agentic Systems**

## Mensagem principal

Este projeto não foi construído apenas para demonstrar agentes.

Foi construído para explorar:

> **Como transformar agentes de IA em workflows controláveis, testáveis, persistentes e capazes de trabalhar com supervisão humana?**

## Evolução futura

```text
Current System
      │
      ├── Observability
      ├── Agent Evaluation
      ├── Production LLM
      ├── Moderation Metrics
      ├── Policy Knowledge Base
      ├── Moderator Dashboard
      └── Deployment
```

## Encerramento

**Content Moderation Agent System**

LangGraph · Multi-Agent Systems · Human-in-the-Loop · State Management · Checkpointing · CI

**Vagner Ferreira**

Data Scientist | AI/Data Engineer | LLM & Agentic Systems

---

# Screenshots / Evidence

Os screenshots abaixo podem ser utilizados na apresentação quando agregarem evidência real.

## Evidence 01 — Testes

Comando:

```powershell
pytest
```

Resultado esperado:

```text
61 passed
```

---

## Evidence 02 — Ruff

Comando:

```powershell
ruff check .
```

Resultado esperado:

```text
All checks passed!
```

---

## Evidence 03 — Compile

Comando:

```powershell
python -m compileall src
```

Resultado esperado:

Execução sem erros.

---

## Evidence 04 — Git Status

Comando:

```powershell
git status
```

Objetivo:

Demonstrar estado limpo do repositório após commit.

---

## Evidence 05 — CI

Abrir no GitHub:

**Actions → Continuous Integration**

Capturar uma execução bem-sucedida da pipeline.

---

## Evidence 06 — Repository Structure

Comando:

```powershell
tree /F /A
```

Se a saída for muito grande, capturar somente a estrutura relevante de:

```text
src/
tests/
docs/
.github/
```

---

# Regras para geração do PPTX

A ferramenta de geração de slides deve:

1. Utilizar este documento como fonte de conteúdo.
2. Criar exatamente **16 slides**.
3. Não transformar os slides em cópia do README.
4. Priorizar diagramas sobre texto.
5. Utilizar código somente no Slide 10.
6. Utilizar screenshots reais somente quando fornecidos.
7. Não inventar resultados, métricas ou funcionalidades.
8. Não apresentar funcionalidades futuras como implementadas.
9. Manter o conteúdo técnico fiel ao projeto.
10. Utilizar PT-BR no conteúdo principal.
11. Manter nomes técnicos como `AgentState`, `StateGraph`, `Human-in-the-Loop`, `thread_id`, `checkpointer` e `interrupt_before`.
12. Utilizar estética profissional de engenharia de IA.
13. Utilizar Dark Mode.
14. Manter tipografia consistente.
15. Evitar excesso de elementos decorativos.
16. Priorizar legibilidade em apresentações presenciais e compartilhamento digital.

---

# Fonte de Verdade

A apresentação deve ser baseada prioritariamente em:

* `README.md`
* `docs/architecture/`
* código existente em `src/`
* testes existentes em `tests/`
* `.github/workflows/ci.yml`

Nenhuma informação deve ser inventada.

---

# Status

**Documento:** Presentation Content
**Versão:** 1.0
**Status:** Ready for presentation generation

---

**Autor:** Vagner Ferreira
**Projeto:** Content Moderation Agent System
**Documento:** Presentation Content
**Versão:** 1.0
