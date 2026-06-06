from openai import OpenAI
import json
import os

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
            "description": "Lê o conteúdo de um arquivo de texto",
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
    },
    {
        "type": "function",
        "function": {
            "name": "listar_arquivos",
            "description": "Lista todos os arquivos disponiveis na pasta atual",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "salvar_arquivo",
            "description": "Salva ou cria um arquivo de texto com o conteudo fornecido",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_arquivo": {
                        "type": "string",
                        "description": "Nome do arquivo a salvar"
                    },
                    "conteudo": {
                        "type": "string",
                        "description": "Conteudo a ser salvo no arquivo"
                    }
                },
                "required": ["nome_arquivo", "conteudo"]
            }
        }
    }
]

# --- IMPLEMENTAÇÃO DAS FERRAMENTAS ---
def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Erro: Arquivo '{nome_arquivo}' não encontrado."
    
def listar_arquivos():
    arquivos = [f for f in os.listdir(".") if os.path.isfile(f)]
    return "Arquivos disponiveis: " + ", ".join(arquivos)

def salvar_arquivo(nome_arquivo, conteudo):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    return f"Arquivo '{nome_arquivo}' salvo com sucesso."

# Mapeia nome da funcao para a funcao real
#Pensa nisso como uma lista telefonica: nome -> quem atende

mapa_ferramentas = {
    "ler_arquivo": ler_arquivo,
    "listar_arquivos": listar_arquivos,
    "salvar_arquivo": salvar_arquivo
}

# --- LOOP DE INTERAÇÃO DO AGENTE ---
def executar_tarefa(mensagens):
    passo = 1 # contador so pra visualizarmos o que acontece
    while True:
        resposta = cliente.chat.completions.create(
            model="qwen2.5-7b-instruct",
            messages=mensagens,
            tools=ferramentas
        )
        
        motivo = resposta.choices[0].finish_reason
        #Modelo terminou - hora de responder ao usuario 
        if motivo == "stop":
            conteudo = resposta.choices[0].message.content
            mensagens.append({"role": "assistant", "content": conteudo})
            print(f"\nAgente: {conteudo}\n")
            break

        elif motivo == "tool_calls":
            mensagens.append(resposta.choices[0].message) # adiciona a mensagem do modelo que chamou a ferramenta   
            
            for tool_call in resposta.choices[0].message.tool_calls:
                nome = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                                
                print(f"[Passo {passo}] usando: {nome} {args}")
                passo += 1               
                resultado = mapa_ferramentas[nome](**args) #chama a funcao passando os argumentos
                mensagens.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": resultado
                })
        else:
            print(f"[encerrado - motivo: {motivo}]")
            break

# --- LOOP INTERATIVO (a novidade do degrau 5) ---

# Instrução de comportamento do agente (chamada de "system prompt")
# E como um manual de conduta que o modelo le antes de começar.

historico = [
    {
        "role": "system", 
        "content": (
            "Voce e um assistente que ajuda a gerenciar arquivos. "
            "Voce tem acesso a ferramentas para listar, ler e salvar arquivos. "
            "Use as ferramentas sempre que necessario para completar as tarefas. "
            "Responda sempre em portugues."
            )
    }
]

print("Agente pronto. Digite sua tarefa ou 'sair' para encerrar.\n")

while True:
    tarefa = input("Voce: ").strip()
    if tarefa.lower() == "sair":
        print("Encerrando agente. Até a próxima!")
        break
    
    if not tarefa:
        continue            
    
    # Adiciona a tarefa ao historico e executa
    historico.append({"role": "user", "content": tarefa})
    executar_tarefa(historico)