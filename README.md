# llm-local-server

Laboratórios em Python para conversar com um modelo de linguagem (LLM) rodando
localmente via [LM Studio](https://lmstudio.ai/), usando a biblioteca `openai`
apontada para o servidor local.

## Pré-requisitos

- Python 3.9+
- [LM Studio](https://lmstudio.ai/) com um modelo carregado e o servidor local
  ativo em `http://localhost:1234/v1`
- Dependência Python:

```bash
pip install openai
```

## Scripts

| Arquivo | Descrição |
| --- | --- |
| `chat-v1-simple.py` | Faz uma única pergunta ao modelo e imprime a resposta. |
| `chat-v2-memory.py` | Chat interativo no terminal que mantém o histórico da conversa. |
| `chat-v3-tool-calling.py` | Demonstra *tool calling*: o modelo decide chamar uma ferramenta (`ler_arquivo`) e responde com base no conteúdo lido. |
| `notas.txt` | Arquivo de texto de exemplo lido pelo `chat-v3-tool-calling.py`. |
| `tarefas.txt` | Arquivo de texto de exemplo (lista de tarefas) para uso com os labs. |

## Como usar

1. Abra o LM Studio, carregue um modelo e inicie o servidor local.
2. Execute um dos scripts:

```bash
python chat-v1-simple.py
# ou
python chat-v2-memory.py
# ou
python chat-v3-tool-calling.py
```

No `chat-v2-memory.py`, digite `sair` para encerrar a conversa.

> O `chat-v3-tool-calling.py` requer um modelo que suporte *tool calling* e que
> o `notas.txt` esteja no mesmo diretório.

> A `api_key` usada nos scripts é fictícia de propósito — o servidor local do
> LM Studio não valida a chave.
