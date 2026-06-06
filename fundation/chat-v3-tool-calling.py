from openai import OpenAI
import json

cliente = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="nao-importa"
)

# --- DEFINIÇÃO DA FERRAMENTA ---
#Aqui voce descreve a ferramenta pro modelo
#O modelo le essa descricao pra saber quando e como usar a ferramenta

ferramentas = [
    {
        "type": "function",
        "function": {
            "name": "ler_arquivo",
            "description": "Lê o conteúdo de um arquivo de texto no computador",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_arquivo":{
                        "type": "string",
                        "description": "O nome do arquivo a ser lido, ex: notas.txt"
                    }
                },
                "required": ["nome_arquivo"]
            }
        }
    }
]

# --- A FERRAMENTA DE VERDADE ( codigo python normal) ---
def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Erro: Arquivo '{nome_arquivo}' não encontrado."

# --- CONVERSA ---
pergunta = "Qual o dia e hora apresentado no arquivo notas.txt?"

mensagens= [
    {"role": "user", "content": pergunta}
]   

print(f"Voce: {pergunta}\n")

#Primeira chamada: o modelo responde com a ferramenta que ele quer usar + os argumentos
resposta = cliente.chat.completions.create(
    model="local-model",
    messages=mensagens,
    tools=ferramentas
)

motivo = resposta.choices[0].finish_reason

#Verifica se o modelo pediu para usar uma ferramenta

if motivo == "tool_calls":
    tool_call = resposta.choices[0].message.tool_calls[0]
    nome_funcao = tool_call.function.name
    argumentos = json.loads(tool_call.function.arguments)

    print(f"[Modelo pediu para usar a ferramenta: {nome_funcao}]")
    print(f"[Argumentos recebido: {argumentos}]\n")

    #Seu codigo executa a ferramenta
    resultado = ler_arquivo(argumentos["nome_arquivo"])

    #Devolve o resultado para o modelo
    mensagens.append(resposta.choices[0].message) #adiciona a mensagem do modelo no historico
    mensagens.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": resultado
    }) #adiciona a resposta da ferramenta no historico

    #Segunda chamada: o modelo recebe o resultado da ferramenta e responde pro usuario
    resposta_final = cliente.chat.completions.create(
        model="local-model",
        messages=mensagens,
        tools=ferramentas
    )

    print(f"Modelo: {resposta_final.choices[0].message.content}\n")

else:
    #Modelo respondeu direto, sem usar ferramenta
    print(f"Modelo: {resposta.choices[0].message.content}\n")