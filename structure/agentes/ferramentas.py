import os

# --- IMPLEMENTACAO DAS FERRAMENTAS ---

def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Erro: arquivo '{nome_arquivo}' nao encontrado."

def listar_arquivos():
    arquivos = [f for f in os.listdir(".") if os.path.isfile(f)]
    return "Arquivos: " + ", ".join(arquivos)

def salvar_arquivo(nome_arquivo, conteudo):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return f"Arquivo '{nome_arquivo}' salvo."

# --- MAPA: nome (string) → funcao real ---
# O agente usa este mapa pra saber qual funcao chamar
MAPA_FERRAMENTAS = {
    "ler_arquivo": ler_arquivo,
    "listar_arquivos": listar_arquivos,
    "salvar_arquivo": salvar_arquivo
}

# --- DESCRICOES: o que o modelo le pra saber como usar cada ferramenta ---
DEFINICOES_FERRAMENTAS = [
    {
        "type": "function",
        "function": {
            "name": "ler_arquivo",
            "description": "Le o conteudo de um arquivo de texto",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_arquivo": {
                        "type": "string",
                        "description": "Nome do arquivo a ler"
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
            "description": "Lista todos os arquivos na pasta atual",
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
            "description": "Salva ou cria um arquivo de texto",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_arquivo": {"type": "string"},
                    "conteudo": {"type": "string"}
                },
                "required": ["nome_arquivo", "conteudo"]
            }
        }
    }
]