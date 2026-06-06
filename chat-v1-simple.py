from openai import OpenAI

# Apontamos o "garçom" para o servidor local do LM Studio.
# A api_key é falsa de propósito — o servidor local não checa isso.
cliente = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="nao-importa"
)

resposta = cliente.chat.completions.create(
    model="local-model",  # o nome não importa muito; o LM Studio usa o modelo carregado
    messages=[
        {"role": "user", "content": "Explique o que é uma API em uma frase simples."}
    ]
)

print(resposta.choices[0].message.content)