# Visão Geral do Sistema

## Contexto

O Sistema de Moderação de Conteúdo Assistido por IA tem como objetivo auxiliar moderadores humanos na análise de comentários em uma plataforma de cursos online.

O sistema utiliza múltiplos agentes de inteligência artificial para analisar comentários, consultar políticas da comunidade e sugerir ações de moderação.

## Objetivo

Criar um fluxo inteligente capaz de:

- analisar comentários;
- identificar possíveis violações;
- consultar diretrizes da comunidade;
- gerar recomendações;
- permitir intervenção humana antes da decisão final.

## Arquitetura Geral

O sistema será composto por:

- AgentState compartilhado;
- Agente Analisador;
- Agente Pesquisador de Políticas;
- Agente Revisor;
- Fluxo orquestrado pelo LangGraph;
- Checkpoints utilizando SQLite;
- Human in the Loop.

## Fluxo Principal

Comentário do aluno:
Comentário
|
v
Analisador
|
v
Existe problema?
|
+---- Não ----> Aprovar
|
+---- Sim ----> Pesquisar Políticas
|
v
Revisor
|
v
Intervenção Humana
|
v
Ação Final