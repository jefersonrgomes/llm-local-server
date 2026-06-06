import json
from openai import OpenAI
from config import MODELO, BASE_URL, API_KEY, SYSTEM_PROMPT
from ferramentas import MAPA_FERRAMENTAS, DEFINICOES_FERRAMENTAS

# Cria o cliente uma unica vez — reutilizado em todas as chamadas
cliente = OpenAI(base_url=BASE_URL, api_key=API_KEY)

def executar_tarefa(historico):
    """
    Recebe o historico completo e roda o loop do agente
    ate o modelo decidir que terminou (finish_reason = stop).
    """
    passo = 1
    while True:
        resposta = cliente.chat.completions.create(
            model=MODELO,
            messages=historico,
            tools=DEFINICOES_FERRAMENTAS
        )
        motivo = resposta.choices[0].finish_reason

        if motivo == "stop":
            conteudo = resposta.choices[0].message.content
            historico.append({"role": "assistant", "content": conteudo})
            print(f"\nAgente: {conteudo}\n")
            break

        elif motivo == "tool_calls":
            historico.append(resposta.choices[0].message)
            for tool_call in resposta.choices[0].message.tool_calls:
                nome = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print(f"  [passo {passo}] usando: {nome} {args}")
                passo += 1
                resultado = MAPA_FERRAMENTAS[nome](**args)
                historico.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": resultado
                })
        else:
            print(f"[encerrado — motivo inesperado: {motivo}]")
            break