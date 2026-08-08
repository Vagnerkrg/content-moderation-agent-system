# Screenshot Evidence Plan — Content Moderation Agent System

## Informações do Documento

**Projeto:** Content Moderation Agent System
**Módulo:** Showcase / Presentation
**Documento:** Screenshot Evidence Plan
**Autor:** Vagner Ferreira
**Versão:** 1.0
**Status:** Working Document — preparação das evidências visuais da apresentação

---

# 1. Objetivo

Este documento define o plano para coleta das **evidências visuais reais** que serão utilizadas na apresentação técnica do projeto **Content Moderation Agent System**.

A apresentação deve demonstrar o sistema através de evidências reais do projeto sempre que isso agregar valor.

O objetivo não é simplesmente colocar screenshots nos slides.

Cada screenshot deve responder a uma pergunta:

> **O que esta imagem prova sobre o sistema?**

As evidências devem demonstrar principalmente:

* arquitetura
* workflow
* agentes
* AgentState
* Human-in-the-Loop
* Interrupt / Resume
* SQLite Checkpointing
* testes
* qualidade de código
* CI
* estrutura do projeto
* execução real

---

# 2. Regra principal

Os screenshots devem ser **reais**.

Não utilizar:

* screenshots simulados
* resultados inventados
* interfaces falsas
* métricas fictícias
* terminal editado
* código alterado apenas para gerar uma imagem
* imagens genéricas de internet

Sempre que possível, capturar a execução real do projeto.

---

# 3. Pasta oficial das evidências

Criar:

```text
docs/
└── showcase/
    └── evidence/
```

Estrutura esperada:

```text
docs/showcase/evidence/
│
├── 01-project-structure.png
├── 02-tests-61-passed.png
├── 03-ruff-pass.png
├── 04-compileall-pass.png
├── 05-git-status-clean.png
├── 06-human-review-interrupt.png
├── 07-human-review-state.png
├── 08-human-review-resume.png
├── 09-checkpoint-database.png
├── 10-thread-id.png
├── 11-github-actions-success.png
└── 12-github-repository.png
```

> A lista pode ser reduzida caso alguma evidência não agregue valor visual suficiente à apresentação.

---

# 4. Convenção de nomes

Todos os arquivos devem:

* utilizar inglês
* utilizar lowercase
* utilizar hífen
* possuir numeração
* descrever claramente o conteúdo

Formato:

```text
NN-description.png
```

Exemplo:

```text
02-tests-61-passed.png
```

Não utilizar:

```text
print1.png
final.png
teste.png
imagem.png
screenshot-finalissimo.png
```

---

# 5. Matriz de evidências

| ID | Evidência                   | Fonte             | Slide provável | Obrigatória  |
| -- | --------------------------- | ----------------- | -------------- | ------------ |
| 01 | Estrutura do projeto        | Terminal          | 05 ou 16       | Sim          |
| 02 | Testes 61/61                | Terminal          | 13             | Sim          |
| 03 | Ruff PASS                   | Terminal          | 13             | Sim          |
| 04 | Compileall PASS             | Terminal          | 13             | Sim          |
| 05 | Git status limpo            | Terminal          | 16             | Opcional     |
| 06 | Human Review / Interrupt    | Terminal          | 09             | Sim          |
| 07 | Estado durante Human Review | Terminal          | 09/10          | Sim          |
| 08 | Resume do workflow          | Terminal          | 10             | Sim          |
| 09 | SQLite checkpoint           | Terminal/Explorer | 11             | Sim          |
| 10 | thread_id                   | Terminal          | 10/11          | Recomendável |
| 11 | GitHub Actions              | GitHub            | 14             | Sim          |
| 12 | Repository                  | GitHub            | 16             | Opcional     |

---

# 6. Evidência 01 — Estrutura do projeto

## Arquivo

```text
01-project-structure.png
```

## Onde capturar

Terminal do projeto:

```powershell
C:\Projetos\content-moderation-agent-system
```

## Comando

```powershell
tree /F /A
```

Caso a saída fique muito grande, utilizar:

```powershell
tree src /F /A
tree tests /F /A
tree docs /F /A
```

Se necessário, fazer uma composição com as três estruturas.

## O que deve aparecer

Principalmente:

```text
src/
tests/
docs/
.github/
```

E dentro de `src`:

```text
agents/
graph/
human_review/
persistence/
runtime/
state/
tools/
```

## Objetivo

Demonstrar que o projeto possui uma organização arquitetural clara.

## Slide provável

**Slide 05 — StateGraph Architecture**

ou

**Slide 16 — Conclusão**

---

# 7. Evidência 02 — Testes

## Arquivo

```text
02-tests-61-passed.png
```

## Onde capturar

Terminal na raiz do projeto.

## Comando

```powershell
python -m pytest
```

## O que deve aparecer

Preferencialmente:

```text
collected 61 items
...
61 passed
```

## Importante

O screenshot deve mostrar claramente:

```text
61 passed
```

Sempre que possível, incluir também o início da sessão mostrando:

```text
Python 3.12.3
pytest
rootdir
```

## Objetivo

Provar que a suíte automatizada está passando.

## Slide

**Slide 13 — Testing & Quality**

---

# 8. Evidência 03 — Ruff

## Arquivo

```text
03-ruff-pass.png
```

## Comando

```powershell
ruff check .
```

## Resultado esperado

```text
All checks passed!
```

## Objetivo

Demonstrar validação automática de qualidade e linting.

## Slide

**Slide 13 — Testing & Quality**

---

# 9. Evidência 04 — Compileall

## Arquivo

```text
04-compileall-pass.png
```

## Comando

```powershell
python -m compileall src
```

## Resultado esperado

Execução sem erros.

## Objetivo

Demonstrar que o código Python do diretório `src` pode ser compilado sem erros de sintaxe.

## Slide

**Slide 13 — Testing & Quality**

---

# 10. Evidência 05 — Git Status

## Arquivo

```text
05-git-status-clean.png
```

## Comando

```powershell
git status
```

## O que deve aparecer

Idealmente:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

## Objetivo

Demonstrar que o estado local está sincronizado com o repositório.

## Slide provável

**Slide 16 — Conclusão**

Esta evidência é opcional.

Não utilizar caso ocupe espaço sem contribuir para a narrativa.

---

# 11. Evidência 06 — Human-in-the-Loop / Interrupt

## Arquivo

```text
06-human-review-interrupt.png
```

## Objetivo

Esta é uma das evidências mais importantes da apresentação.

Precisamos demonstrar que o workflow realmente chega ao ponto de revisão humana e **interrompe antes da ação final**.

## Onde capturar

Terminal.

Executar o fluxo real de Human-in-the-Loop disponibilizado pelo projeto.

Antes de executar, verificar o entry point/documentação oficial do projeto.

Não criar uma execução artificial somente para gerar o screenshot.

## O que deve aparecer

Idealmente:

```text
Analyzer
    ↓
Policy Researcher
    ↓
Reviewer
    ↓
Human Review
```

E uma indicação clara de que o workflow está aguardando decisão humana.

## Objetivo

Provar:

> Human-in-the-Loop é parte real da arquitetura.

## Slide

**Slide 09 — Human-in-the-Loop**

---

# 12. Evidência 07 — Estado durante Human Review

## Arquivo

```text
07-human-review-state.png
```

## Objetivo

Mostrar que o estado do agente pode ser inspecionado durante a pausa.

## O que deve aparecer

Sempre que possível:

```text
thread_id
comentario_original
analise_do_agente
politicas_relevantes
status_da_moderacao
justificativa_final
```

ou os campos equivalentes realmente existentes no `AgentState`.

## Importante

Não inventar nomes de campos.

Os campos exibidos no screenshot devem corresponder ao código atual.

## Slide

**Slide 09 — Human-in-the-Loop**

ou

**Slide 10 — Interrupt / Resume**

---

# 13. Evidência 08 — Resume

## Arquivo

```text
08-human-review-resume.png
```

## Objetivo

Demonstrar que o workflow pode continuar depois da decisão humana.

## O que deve aparecer

Idealmente uma sequência:

```text
Execution paused
        ↓
Human decision
        ↓
Resume
        ↓
Final Action
```

E o mesmo:

```text
thread_id
```

deve ser utilizado para demonstrar continuidade da execução.

## Slide

**Slide 10 — Interrupt / Resume**

---

# 14. Evidência 09 — SQLite Checkpoint

## Arquivo

```text
09-checkpoint-database.png
```

## Onde capturar

Explorador de arquivos ou terminal.

Local esperado:

```text
data/
└── checkpoints.db
```

## Comando possível

```powershell
Get-ChildItem data
```

ou:

```powershell
Get-ChildItem data -Force
```

## Objetivo

Demonstrar que o workflow possui persistência real.

## Slide

**Slide 11 — Persistence**

---

# 15. Evidência 10 — thread_id

## Arquivo

```text
10-thread-id.png
```

## Objetivo

Mostrar o identificador utilizado para diferenciar e retomar execuções.

## O que deve aparecer

Exemplo conceitual:

```text
thread_id:
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

O valor deve ser real.

Não substituir por um UUID inventado.

## Slide

**Slide 10 — Interrupt / Resume**

ou

**Slide 11 — Persistence**

---

# 16. Evidência 11 — GitHub Actions

## Arquivo

```text
11-github-actions-success.png
```

## Onde capturar

No GitHub:

```text
Repository
    ↓
Actions
    ↓
Continuous Integration
```

## O que deve aparecer

Uma execução real bem-sucedida.

Preferencialmente mostrar:

```text
Continuous Integration
✓
```

E, se possível:

```text
Python 3.12
Ruff
Compile
Pytest
```

## Objetivo

Demonstrar que a qualidade não depende apenas da execução local.

Existe validação automatizada no GitHub.

## Slide

**Slide 14 — Continuous Integration**

---

# 17. Evidência 12 — Repository

## Arquivo

```text
12-github-repository.png
```

## Onde capturar

Página principal do repositório:

```text
Vagnerkrg/content-moderation-agent-system
```

## O que deve aparecer

Preferencialmente:

* nome do projeto
* descrição
* estrutura
* documentação
* status relevante

## Objetivo

Utilizar como evidência final do projeto publicado.

## Slide

**Slide 16 — Conclusão**

Esta evidência é opcional.

---

# 18. Evidências prioritárias

Se for necessário reduzir o número de screenshots, priorizar nesta ordem:

### Prioridade 01

```text
02-tests-61-passed.png
```

### Prioridade 02

```text
06-human-review-interrupt.png
```

### Prioridade 03

```text
07-human-review-state.png
```

### Prioridade 04

```text
08-human-review-resume.png
```

### Prioridade 05

```text
11-github-actions-success.png
```

### Prioridade 06

```text
09-checkpoint-database.png
```

### Prioridade 07

```text
01-project-structure.png
```

### Prioridade 08

```text
03-ruff-pass.png
04-compileall-pass.png
```

---

# 19. O que NÃO precisa virar screenshot

Não é necessário capturar screenshot de tudo.

Não transformar em imagem:

* README inteiro
* arquivos de documentação
* código dos agentes
* código completo do StateGraph
* arquivos de configuração
* todos os testes
* todos os diretórios
* todos os commits

A apresentação deve utilizar screenshots apenas quando eles funcionarem como **evidência visual**.

---

# 20. Regra para screenshots de terminal

Sempre que possível:

1. Abrir PowerShell
2. Maximizar ou utilizar tamanho suficiente
3. Entrar na raiz do projeto
4. Ativar o `venv` correto
5. Executar o comando real
6. Limpar a tela antes da execução, se necessário
7. Capturar o resultado completo
8. Garantir que o comando e o resultado estejam visíveis

Evitar screenshots onde:

* o texto está cortado
* o resultado final não aparece
* existem muitas linhas irrelevantes
* o caminho está incorreto
* aparece outro projeto
* o Python pertence a outro ambiente virtual

---

# 21. Validação do ambiente antes dos screenshots

Antes de capturar qualquer evidência de execução:

```powershell
python -c "import sys; print(sys.executable)"
```

O resultado esperado deve apontar para:

```text
C:\Projetos\content-moderation-agent-system\venv\Scripts\python.exe
```

Também validar:

```powershell
python --version
```

Esperado:

```text
Python 3.12.x
```

E:

```powershell
where.exe python
```

O primeiro resultado deve ser o Python do `venv` do projeto.

---

# 22. Checklist de coleta

## Ambiente

* [ ] `venv` correto ativado
* [ ] Python correto
* [ ] projeto correto
* [ ] Git sincronizado

## Qualidade

* [ ] Testes capturados
* [ ] Ruff capturado
* [ ] Compileall capturado

## Arquitetura

* [ ] Estrutura do projeto capturada

## Human-in-the-Loop

* [ ] Workflow interrompido
* [ ] Estado pausado capturado
* [ ] Decisão humana registrada
* [ ] Workflow retomado

## Persistence

* [ ] `thread_id` capturado
* [ ] SQLite checkpoint capturado

## CI

* [ ] GitHub Actions capturado

## Repository

* [ ] Página final do GitHub capturada, se necessário

---

# 23. Relação com os 16 slides

A distribuição inicial recomendada é:

| Slide | Evidência                                                                |
| ----- | ------------------------------------------------------------------------ |
| 01    | Nenhuma                                                                  |
| 02    | Nenhuma                                                                  |
| 03    | Nenhuma                                                                  |
| 04    | Diagrama criado na apresentação                                          |
| 05    | `01-project-structure.png` opcional                                      |
| 06    | Nenhuma                                                                  |
| 07    | `07-human-review-state.png` opcional                                     |
| 08    | Diagrama criado na apresentação                                          |
| 09    | `06-human-review-interrupt.png`                                          |
| 10    | `08-human-review-resume.png` + `10-thread-id.png`                        |
| 11    | `09-checkpoint-database.png`                                             |
| 12    | Nenhuma                                                                  |
| 13    | `02-tests-61-passed.png` + `03-ruff-pass.png` + `04-compileall-pass.png` |
| 14    | `11-github-actions-success.png`                                          |
| 15    | Nenhuma                                                                  |
| 16    | `12-github-repository.png` opcional                                      |

---

# 24. Regra para o terceiro prompt

Depois que todas as evidências forem coletadas, será criado um terceiro documento:

```text
PRESENTATION_EVIDENCE_PROMPT.md
```

Esse prompt será entregue junto com:

```text
presentation-content.md
presentation-prompt.md
```

O terceiro prompt deverá explicar para a ferramenta de geração:

* quais screenshots existem
* o que cada screenshot comprova
* qual slide deve receber cada screenshot
* onde posicionar cada screenshot
* qual tamanho aproximado utilizar
* quais screenshots são obrigatórios
* quais são opcionais
* como preservar a legibilidade
* como integrar screenshot + diagrama
* quais imagens não devem ser utilizadas
* que nenhuma evidência deve ser inventada

---

# 25. Fluxo de trabalho

A ordem recomendada é:

```text
01
Repositório atualizado
        ↓
02
Validação local
        ↓
03
Coleta de screenshots
        ↓
04
Revisão das evidências
        ↓
05
Criação do terceiro prompt
        ↓
06
Enviar os 3 documentos ao Claude
        ↓
07
Gerar V4 da apresentação
        ↓
08
Revisar PPTX
        ↓
09
Revisar PDF
        ↓
10
Validar exatamente 16 slides
        ↓
11
Aprovar Showcase
        ↓
12
Criar LinkedIn Post
        ↓
13
Finalizar Issue #27
```

---

# 26. Estado deste documento

Este documento é um **working document**.

Não deve ser considerado final até que:

* os screenshots tenham sido coletados;
* cada evidência tenha sido revisada;
* os nomes dos arquivos tenham sido confirmados;
* a relação entre evidências e slides tenha sido validada;
* o terceiro prompt tenha sido criado.

---

# 27. Próximo passo

Não gerar o terceiro prompt ainda.

Primeiro executar a coleta das evidências.

Começar pelas evidências mais importantes:

```text
02-tests-61-passed.png
06-human-review-interrupt.png
07-human-review-state.png
08-human-review-resume.png
09-checkpoint-database.png
10-thread-id.png
11-github-actions-success.png
```

Depois revisar cada screenshot individualmente.

Somente após essa revisão criar:

```text
PRESENTATION_EVIDENCE_PROMPT.md
```

---

**Autor:** Vagner Ferreira
**Projeto:** Content Moderation Agent System
**Documento:** Screenshot Evidence Plan
**Versão:** 1.0
