# llm-local-server

Laboratórios em Python para conversar com um modelo de linguagem (LLM) rodando
localmente via [LM Studio](https://lmstudio.ai/), usando a biblioteca `openai`
apontada para o servidor local.

O projeto tem duas partes:

- **`fundation/`** — labs progressivos (v1 a v5), cada um adicionando um conceito:
  da chamada mais simples até um agente interativo com ferramentas.
- **`structure/agentes/`** — o agente do v5 refatorado em módulos, mostrando como
  organizar o código em um pequeno projeto.

## Pré-requisitos

- Python 3.9+
- [LM Studio](https://lmstudio.ai/) com um modelo carregado e o servidor local
  ativo em `http://localhost:1234/v1`
  - Os scripts v1–v4 usam o nome genérico `"local-model"` (o LM Studio usa o
    modelo que estiver carregado). O `chat-v5-agente-interativo.py` e o pacote
    `structure/agentes` apontam para `qwen2.5-7b-instruct` — ajuste para o nome
    do modelo que você carregou (em `structure/agentes/config.py`, basta mudar
    a constante `MODELO`).
- Dependência Python:

```bash
pip install openai
```

## `fundation/` — labs progressivos

| Arquivo | Descrição |
| --- | --- |
| `chat-v1-simple.py` | Faz uma única pergunta ao modelo e imprime a resposta. |
| `chat-v2-memory.py` | Chat interativo no terminal que mantém o histórico da conversa. |
| `chat-v3-tool-calling.py` | Demonstra *tool calling*: o modelo decide chamar uma ferramenta (`ler_arquivo`) e responde com base no conteúdo lido. |
| `chat-v4-agent-loop-mult-tool-calling.py` | Loop de agente com várias ferramentas (`ler_arquivo`, `listar_arquivos`, `salvar_arquivo`): o modelo encadeia chamadas até concluir a tarefa. |
| `chat-v5-agente-interativo.py` | Agente interativo no terminal com *system prompt* e histórico: aceita várias tarefas em sequência usando as mesmas ferramentas. |
| `notas.txt` | Arquivo de texto de exemplo lido pelos labs. |
| `tarefas.txt` | Arquivo de texto de exemplo (lista de tarefas) usado pelos labs. |

Para rodar (a partir da raiz do projeto):

```bash
python fundation/chat-v1-simple.py
# ou v2, v3, v4, v5...
```

No `chat-v2-memory.py` e no `chat-v5-agente-interativo.py`, digite `sair` para
encerrar.

## `structure/agentes/` — agente modularizado

Mesma ideia do v5, separada em módulos com responsabilidade única:

| Arquivo | Descrição |
| --- | --- |
| `config.py` | Configurações centrais (modelo, URL, API key, *system prompt*). |
| `ferramentas.py` | Implementação das ferramentas + suas descrições para o modelo. |
| `agente.py` | Loop do agente (`executar_tarefa`). |
| `main.py` | Ponto de entrada com o loop interativo. |

Como os módulos se importam por nome, execute a partir da própria pasta:

```bash
cd structure/agentes
python main.py
```

## Notas

> Os agentes podem **gerar arquivos** (ex.: `resumo*.txt`, `prioridades.txt`) ao
> rodar. Eles são saídas dos labs e não são versionados (veja o `.gitignore`).

> Os scripts de *tool calling* (v3+) requerem um modelo que suporte essa função e
> que os arquivos de entrada estejam acessíveis no diretório de execução.

> A `api_key` usada nos scripts é fictícia de propósito — o servidor local do
> LM Studio não valida a chave.
