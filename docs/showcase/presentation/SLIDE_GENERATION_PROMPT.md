# Prompt — Content Moderation Agent System Presentation

## Contexto

Você é responsável por criar uma **apresentação técnica profissional de portfólio** para o projeto **Content Moderation Agent System**, desenvolvido por **Vagner Ferreira**.

O projeto demonstra uma arquitetura prática de **Agentic AI Engineering**, utilizando:

* Python 3.12
* LangGraph
* LangChain
* Multi-Agent Architecture
* StateGraph
* Shared AgentState
* Conditional Routing
* Human-in-the-Loop
* Interrupt / Resume
* SQLite Checkpointing
* Pytest
* Ruff
* GitHub Actions

O projeto está disponível no repositório:

`https://github.com/Vagnerkrg/content-moderation-agent-system`

O README do projeto contém a documentação técnica detalhada.

A apresentação **não deve simplesmente copiar o README**.

Ela deve funcionar como um **technical showcase**, apresentando o problema, as decisões de engenharia, a arquitetura, os resultados e os aprendizados.

---

# Objetivo da apresentação

Criar uma apresentação visualmente profissional que demonstre que o autor entende não apenas como utilizar agentes de IA, mas como construir **workflows de agentes controláveis, testáveis, persistentes e supervisionados por humanos**.

A narrativa deve seguir:

**Problema → Objetivo → Arquitetura → Agentes → Estado → Routing → Human-in-the-Loop → Persistence → LangGraph → Testing → CI → Challenges → Lessons → Future → Conclusão**

---

# Quantidade de slides

Criar **16 slides**.

Não reduzir para 10 ou 11 slides.

Não criar slides excessivamente densos.

Cada slide deve transmitir **uma única ideia principal**.

---

# Idioma

Toda a apresentação deve estar em **Português do Brasil (PT-BR)**.

Termos técnicos consagrados podem permanecer em inglês quando isso for mais natural:

* Agent
* AgentState
* Human-in-the-Loop
* StateGraph
* Routing
* Checkpoint
* Interrupt / Resume
* Workflow
* Multi-Agent
* CI/CD

Não traduzir nomes de classes, funções, arquivos ou tecnologias.

---

# Estilo visual

Criar uma apresentação:

* profissional
* técnica
* moderna
* minimalista
* orientada a engenharia
* adequada para portfólio profissional
* adequada para apresentação a recrutadores e profissionais de tecnologia

Preferência visual:

**Dark Mode profissional.**

Usar fundo escuro com excelente contraste e tipografia clara.

Evitar:

* excesso de elementos decorativos
* aparência de apresentação escolar
* excesso de texto
* excesso de emojis
* ilustrações genéricas de robôs
* imagens de banco sem relação com o projeto
* gradientes exagerados
* excesso de cores
* aparência "marketing AI"

A apresentação deve parecer um **technical case study**.

---

# Identidade

Autor:

**Vagner Ferreira**

Título profissional:

**Data Scientist | AI/Data Engineer | LLM & Agentic Systems**

Projeto:

**Content Moderation Agent System**

Tecnologias principais:

**LangGraph · Multi-Agent Systems · Human-in-the-Loop · State Management · Checkpointing · CI**

---

# Slides

## Slide 01 — Capa

### CONTENT MODERATION AGENT SYSTEM

**Multi-Agent Content Moderation with LangGraph & Human-in-the-Loop**

Subtítulo:

> Um estudo prático de Engenharia de Agentes de IA

Autor:

**Vagner Ferreira**

**Data Scientist | AI/Data Engineer | LLM & Agentic Systems**

Visual:

Criar uma representação visual elegante de um workflow de agentes conectado a um checkpoint humano.

Não utilizar robôs genéricos.

---

## Slide 02 — O problema

### Automated Content Moderation Is Not Binary

Mostrar que moderação de conteúdo envolve:

* Conteúdo ambíguo
* Contexto de políticas
* Diferentes tipos de violações
* Risco de decisões automáticas incorretas
* Rastreabilidade
* Supervisão humana

Destacar a pergunta:

> Como automatizar o processo sem remover o controle humano?

Visual:

Representar a complexidade da decisão como fluxo de múltiplos fatores.

---

## Slide 03 — Objetivo

### Project Goal

Mostrar o objetivo do sistema:

1. Analisar
2. Identificar problemas
3. Pesquisar políticas
4. Recomendar ação
5. Pausar para revisão humana
6. Registrar decisão
7. Retomar execução
8. Executar ação final

Destacar:

> Automação onde é seguro. Supervisão humana onde existe impacto.

Visual:

Pipeline horizontal ou vertical com essas etapas.

---

## Slide 04 — Arquitetura geral

### Multi-Agent Moderation Workflow

Criar um **diagrama visual profissional**:

```text
Comment
   ↓
Analyzer
   ↓
Conditional Routing
   ├── Neutral → END
   │
   └── Problematic
          ↓
    Policy Researcher
          ↓
       Reviewer
          ↓
    Human Review
          ↓
     Final Action
```

O diagrama deve ser um dos principais elementos do slide.

Não utilizar ASCII art.

---

## Slide 05 — StateGraph

### LangGraph StateGraph

Mostrar visualmente:

```text
AgentState
    │
    ▼
Analyzer
    │
    ▼
Conditional Routing
   / \
  /   \
END   Policy Researcher
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

Destacar:

> O estado acompanha toda a execução.

Mostrar visualmente que os nós operam sobre o mesmo estado compartilhado.

---

## Slide 06 — Agentes especializados

### One Responsibility per Agent

Criar três cards:

**Analyzer Agent**

Classificação inicial do comentário.

**Policy Researcher**

Contexto das políticas relevantes.

**Reviewer Agent**

Análise + política → recomendação.

Abaixo:

* Single Responsibility
* Testabilidade
* Extensibilidade
* Rastreabilidade
* Baixo acoplamento

Visual:

Três componentes conectados em sequência.

---

## Slide 07 — AgentState

### AgentState as the Communication Contract

Mostrar visualmente:

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

Explicar brevemente:

> Cada agente modifica apenas os campos sob sua responsabilidade.

Destacar:

**Shared State = Communication Contract**

---

## Slide 08 — Conditional Routing

### Not Every Comment Needs the Full Pipeline

Mostrar:

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

Destacar os benefícios:

* Menor custo
* Menor latência
* Menos processamento
* Fluxo previsível
* Controle explícito

---

## Slide 09 — Human-in-the-Loop

### Human Oversight Is Part of the Architecture

Mostrar um grande checkpoint visual:

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

Mensagem principal:

> A decisão automática não é aplicada imediatamente.

Destacar que a interrupção acontece **antes da ação final**.

---

## Slide 10 — Interrupt / Resume

### A Workflow That Can Stop and Continue

Este é o único slide que deve apresentar código.

Utilizar somente:

```python
workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["executar_acao_final"],
)
```

Ao lado do código:

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

Mensagem:

> A pausa faz parte do workflow, não da interface.

---

## Slide 11 — Persistence

### Stateful Execution with SQLite

Mostrar:

```text
data/
└── checkpoints.db
```

E:

```text
thread_id
```

Explicar visualmente:

**Checkpoint**

↓

**Human Decision**

↓

**Resume**

↓

**Final Action**

Mensagem principal:

> Persistir o estado é o que torna uma pausa realmente retomável.

---

## Slide 12 — Why LangGraph?

### Por que LangGraph?

Criar uma tabela limpa:

| Requisito            | LangGraph |
| -------------------- | --------- |
| Stateful workflow    | ✅         |
| Conditional routing  | ✅         |
| Interrupt / Resume   | ✅         |
| Checkpointing        | ✅         |
| Explicit graph       | ✅         |
| Testable transitions | ✅         |

Mensagem final:

> LangGraph não foi utilizado apenas para "chamar agentes".

> Foi utilizado para orquestrar um workflow stateful e controlável.

---

## Slide 13 — Testing & Quality

### Engineering Through Tests

Grande destaque:

**61 / 61 TESTS PASSED**

Mostrar:

```text
Agents
Graph
Routing
Human Review
Persistence
Runtime
Project Environment
```

E:

```text
Ruff
PASS

Compileall
PASS

Pytest
61 PASSED
```

Não inventar cobertura percentual.

Não afirmar métricas que não estão documentadas.

---

## Slide 14 — Continuous Integration

### Automated Quality Pipeline

Mostrar o fluxo:

```text
Push / Pull Request
        ↓
GitHub Actions
        ↓
Python 3.12
        ↓
Install
        ↓
Ruff
        ↓
Compileall
        ↓
Pytest
        ↓
PASS
```

Destacar:

> Qualidade automatizada antes da integração na branch principal.

---

## Slide 15 — Engineering Challenges & Lessons

### What This Project Taught Me

Dividir o slide em duas áreas.

**Challenges**

* Shared State
* Conditional Routing
* Human Review
* Persistence
* Testability

**Lessons Learned**

* Estado compartilhado bem definido simplifica sistemas multiagente.
* Human-in-the-Loop deve ser uma decisão arquitetural.
* Persistência é essencial para workflows retomáveis.
* Agentes especializados são mais fáceis de testar e evoluir.
* Routing explícito torna o comportamento previsível.
* Desacoplamento aumenta a testabilidade.

Manter os textos curtos.

---

## Slide 16 — Conclusão

### Engineering Reliable Agentic Systems

Mensagem central:

> Este projeto não foi construído apenas para demonstrar agentes.

> Foi construído para explorar como transformar agentes de IA em workflows controláveis, testáveis, persistentes e capazes de trabalhar com supervisão humana.

Abaixo:

**Content Moderation Agent System**

**LangGraph · Multi-Agent Systems · Human-in-the-Loop · State Management · Checkpointing · CI**

Autor:

**Vagner Ferreira**

Adicionar discretamente:

**GitHub: Vagnerkrg/content-moderation-agent-system**

---

# Diagramas

Os slides 04, 05, 08, 09, 10, 11 e 14 devem possuir diagramas ou representações visuais.

Não utilizar ASCII art na versão final.

Os diagramas devem parecer diagramas de arquitetura de software.

Utilizar:

* caixas
* setas
* agrupamentos
* checkpoints
* estados
* decisões
* fluxos

Manter consistência visual entre os diagramas.

---

# Uso de imagens e screenshots

Não inventar screenshots do projeto.

Se uma imagem real do projeto melhorar significativamente algum slide, **solicitar ao usuário o screenshot necessário antes de finalizar**.

Quando solicitar um screenshot, fornecer:

1. O comando exato para executar.
2. O arquivo ou saída que deve aparecer.
3. O objetivo do screenshot na apresentação.
4. O slide onde ele será utilizado.

Exemplo:

> Para o Slide 13, preciso de um screenshot real da execução dos testes.

Comando:

```powershell
pytest
```

Screenshot necessário:

* terminal mostrando `61 passed`
* incluir o início da sessão de testes quando possível

Objetivo:

> Evidenciar o resultado real da suíte de testes.

Não solicitar screenshots se o diagrama ou conteúdo textual já for suficiente.

---

# Evidências reais

Sempre que possível, utilizar dados reais do projeto.

Dados atualmente conhecidos:

* 61 testes automatizados
* Ruff passando
* `python -m compileall src` passando
* GitHub Actions configurado
* Python 3.12
* SQLite checkpointing
* LangGraph StateGraph
* Human-in-the-Loop
* Conditional Routing

Não inventar:

* métricas de performance
* porcentagem de cobertura
* latência
* custo
* quantidade de usuários
* volume de comentários
* accuracy
* métricas de produção

Se alguma informação não estiver disponível, não criar um valor fictício.

---

# Código

Utilizar código somente quando ele explicar uma decisão arquitetural.

O único trecho de código obrigatório é:

```python
workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["executar_acao_final"],
)
```

Não colocar grandes blocos de código.

---

# Badges

A apresentação é independente do README.

**Não modificar, remover ou recriar as badges existentes no README.**

Não é necessário reproduzir as badges nos slides.

---

# Relação com o README

O README é a documentação detalhada.

A apresentação é o **showcase executivo/técnico**.

Portanto:

README:

**Detalhes → implementação → documentação**

Apresentação:

**Problema → arquitetura → decisões → resultados → aprendizados**

Evitar repetir parágrafos inteiros do README.

---

# Qualidade final

Antes de gerar a apresentação, verificar:

* exatamente 16 slides
* PT-BR
* dark mode profissional
* tipografia consistente
* diagramas legíveis
* pouco texto
* nenhum slide excessivamente carregado
* código apenas no Slide 10
* dados reais
* nenhuma métrica inventada
* arquitetura tecnicamente coerente
* Human-in-the-Loop claramente destacado
* AgentState claramente representado
* Conditional Routing claramente representado
* SQLite checkpointing claramente representado
* CI claramente representado
* conclusão forte

A apresentação deve transmitir:

**"Este projeto demonstra engenharia de agentes, não apenas uso de LLM."**

---

# Entrega

Gerar a apresentação final em:

1. **PPTX editável**
2. **PDF para distribuição**

Nome dos arquivos:

```text
content-moderation-agent-system-showcase.pptx
content-moderation-agent-system-showcase.pdf
```

Não adicionar conteúdo promocional exagerado.

O resultado deve parecer um **case técnico profissional de AI Engineering / Agentic AI**.
