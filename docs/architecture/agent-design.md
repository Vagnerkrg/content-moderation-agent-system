# Design dos Agentes

## Visão Geral

O sistema utiliza uma arquitetura multiagente onde cada agente possui uma responsabilidade específica dentro do processo de moderação.

A separação de responsabilidades permite maior organização, facilidade de manutenção e possibilidade de evolução futura do sistema.

---

# Agente Analisador

## Responsabilidade

Realizar a primeira análise do comentário enviado pelo aluno.

## Entrada

Campo do estado:

comentario_original

## Processamento

O agente deve analisar o conteúdo e identificar a categoria do comentário:

- positivo;
- neutro;
- potencialmente problemático.

Possíveis problemas identificados:

- spam;
- linguagem ofensiva;
- violação de diretrizes.

## Saída

Atualiza:


analise_do_agente


---

# Agente Pesquisador de Políticas

## Responsabilidade

Pesquisar as políticas da comunidade quando o comentário apresentar algum possível problema.

## Entrada

Utiliza:


analise_do_agente


## Ferramenta

Utiliza Tavily Search para encontrar diretrizes relevantes.

As políticas podem inicialmente ser simuladas em textos simples.

## Saída

Atualiza:


politicas_relevantes


---

# Agente Revisor

## Responsabilidade

Consolidar a análise do comentário e as políticas encontradas.

## Entrada

Recebe:


analise_do_agente

politicas_relevantes


## Processamento

Gera uma recomendação de moderação.

Exemplos:


Aprovar

Remover por Spam

Editar por linguagem inadequada


## Saída

Atualiza:


status_da_moderacao

justificativa_final


---

# Comunicação Entre Agentes

O compartilhamento de informações será realizado através do estado global do LangGraph:


AgentState


Cada agente recebe o estado atual e retorna alterações nos campos sob sua responsabilidade.

---

# Princípio Arquitetural

Cada agente deve possuir uma única responsabilidade principal.

Benefícios:

- código mais organizado;
- testes isolados;
- facilidade de substituição de componentes;
- evolução para arquiteturas multiagentes mais complexas.