from openai import OpenAI

cliente = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="nao-importa"
)

# Inicializa o histórico de mensagens
historico = []

print("Chat iniciado. Digite 'sair' para encerrar.\n")

while True:
    pergunta = input("Você: ")
    if pergunta.lower() == "sair":
        print("Chat encerrado.")
        break

    #Adiciona a mensagem do usuário ao histórico
    historico.append({"role": "user", "content": pergunta})

    # Envia o histórico de mensagens para o modelo
    resposta = cliente.chat.completions.create(
        model="local-model",
        messages=historico
    )

    resposta_texto = resposta.choices[0].message.content

    # Adiciona a resposta do modelo ao histórico
    historico.append({"role": "assistant", "content": resposta_texto})

    print(f"\nModelo: {resposta_texto}\n")
