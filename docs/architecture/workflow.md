# Workflow do Sistema LangGraph

## Visão Geral

O fluxo do sistema será orquestrado utilizando o LangGraph através de um `StateGraph`.

Cada etapa do processo será representada por um nó responsável por uma função específica.

O estado compartilhado (`AgentState`) será utilizado para transportar informações entre os agentes.

---

# Fluxo Principal

O fluxo inicial do sistema:

Comentário do aluno
|
v
+----------------+
| Analisador |
+----------------+
|
v
Existe problema?
|
+----------------+
| |
Não Sim
| |
v v
Aprovado +-----------------------+
| Pesquisador Políticas |
+-----------------------+
|
v
+---------------+
| Revisor |
+---------------+
|
v
Human in the Loop
|
v
Ação Final


---

# Nós do Grafo

## Nó: Analisador

Responsabilidade:

- receber o comentário original;
- analisar o conteúdo;
- classificar o comentário.

Entrada:


comentario_original


Saída:


analise_do_agente


---

## Nó: Pesquisador de Políticas

Responsabilidade:

- buscar informações nas diretrizes da comunidade;
- identificar possíveis violações.

Este nó será executado somente quando o comentário apresentar um possível problema.

Entrada:


analise_do_agente


Saída:


politicas_relevantes


---

## Nó: Revisor

Responsabilidade:

- avaliar a análise;
- considerar as políticas encontradas;
- gerar recomendação final.

Entrada:


analise_do_agente

politicas_relevantes


Saída:


status_da_moderacao

justificativa_final


---

# Condicional do Fluxo

Após a execução do Analisador, o sistema deverá avaliar se existe problema.

A decisão será implementada utilizando:

```python
add_conditional_edges()

Comportamento esperado:

Analisador

    |
    |
    +---- Sem problema
    |
    v

Status:
Aprovado

ou:

Analisador

    |
    |
    +---- Problema identificado
              |
              v

Pesquisador de Políticas
Human in the Loop

O sistema deverá possuir um ponto de interrupção antes da execução da ação final.

A pausa será configurada utilizando:

interrupt_before

Objetivo:

Permitir que um moderador humano revise a decisão antes que ela seja aplicada.

Interação Humana

Durante a interrupção:

O sistema deverá apresentar:

análise do agente;
políticas encontradas;
recomendação do revisor.

O moderador poderá:

aprovar;
cancelar;
modificar a justificativa.
Atualização do Estado

Quando houver intervenção humana, o sistema deverá capturar o estado atual:

graph.get_state(config)

Depois atualizar utilizando:

graph.update_state(config, new_values)

A alteração poderá modificar:

status_da_moderacao

justificativa_final
Checkpoints

O sistema utilizará SQLite para persistência dos checkpoints.

Objetivos:

preservar o estado das execuções;
permitir retomada após interrupções;
separar diferentes execuções utilizando threads.
Threads

Cada execução deverá possuir um identificador único.

Será utilizado:

uuid

Objetivo:

Evitar conflito entre diferentes processos de moderação.

Visualização do Grafo

O fluxo deverá ser visualizado utilizando:

draw_mermaid_png()

A representação visual será utilizada para:

documentação;
validação da arquitetura;
depuração do fluxo.
Resultado Esperado

Ao final, o sistema deverá possuir um fluxo completo:

Entrada
   |
Análise
   |
Decisão
   |
Pesquisa de políticas
   |
Revisão
   |
Intervenção humana
   |
Estado atualizado
   |
Ação final

Esse fluxo representa a arquitetura base do sistema de moderação assistido por IA.