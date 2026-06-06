import fitz          # pymupdf — leitura de PDF
from docx import Document  # python-docx — leitura de Word

from ddgs import DDGS 
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

def buscar_na_web(query, max_resultados=3):
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(query, max_results=max_resultados))
        if not resultados:
            return "Nenhum resultado encontrado."
        texto = ""
        for i, r in enumerate(resultados, 1):
            texto += f"\nResultado {i}:\n"
            texto += f"  Título: {r['title']}\n"
            texto += f"  Resumo: {r['body']}\n"
            texto += f"  URL: {r['href']}\n"
        return texto

    except Exception as e:
        return f"Erro ao buscar na web: {str(e)}"

def ler_pdf(nome_arquivo):
    try:
        doc = fitz.open(nome_arquivo)
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        doc.close()
        return texto if texto.strip() else "PDF sem texto extraivel (pode ser imagem)."
    except Exception as e:
        return f"Erro ao ler PDF: {str(e)}"

def ler_word(nome_arquivo):
    try:
        doc = Document(nome_arquivo)
        paragrafos = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragrafos)
    except Exception as e:
        return f"Erro ao ler Word: {str(e)}"
    
def criar_pasta(nome_pasta):
    try:
        os.makedirs(nome_pasta, exist_ok=True)
        return f"Pasta '{nome_pasta}' criada com sucesso."
    except Exception as e:
        return f"Erro ao criar pasta: {str(e)}"

def mover_arquivo(nome_arquivo, pasta_destino):
    try:
        os.makedirs(pasta_destino, exist_ok=True)
        destino = os.path.join(pasta_destino, os.path.basename(nome_arquivo))
        os.rename(nome_arquivo, destino)
        return f"Arquivo '{nome_arquivo}' movido para '{pasta_destino}'."
    except FileNotFoundError:
        return f"Erro: arquivo '{nome_arquivo}' nao encontrado."
    except Exception as e:
        return f"Erro ao mover arquivo: {str(e)}"

def listar_pastas():
    pastas = [f for f in os.listdir(".") if os.path.isdir(f)]
    return "Pastas: " + ", ".join(pastas) if pastas else "Nenhuma pasta encontrada."

# --- MAPA: nome (string) → funcao real ---
# O agente usa este mapa pra saber qual funcao chamar
MAPA_FERRAMENTAS = {
    "ler_arquivo": ler_arquivo,
    "listar_arquivos": listar_arquivos,
    "salvar_arquivo": salvar_arquivo,
    "buscar_na_web": buscar_na_web,
    "ler_pdf": ler_pdf,        
    "ler_word": ler_word,
    "criar_pasta": criar_pasta,        # ← novo
    "mover_arquivo": mover_arquivo,    # ← novo
    "listar_pastas": listar_pastas     # ← novo 
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
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_na_web",
            "description": "Busca informacoes atuais na internet sobre qualquer assunto",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "O que pesquisar, ex: ultimas noticias sobre Python"
                    },
                    "max_resultados": {
                        "type": "integer",
                        "description": "Quantidade de resultados, entre 1 e 5. Padrao: 3"
                    }
                },
                "required": ["query"]
            }
        }
    },{
        "type": "function",
        "function": {
            "name": "ler_pdf",
            "description": "Le e extrai o texto de um arquivo PDF",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_arquivo": {
                        "type": "string",
                        "description": "Nome do arquivo PDF, ex: relatorio.pdf"
                    }
                },
                "required": ["nome_arquivo"]
            }
        }
    }
    ,{
        "type": "function",
        "function": {
            "name": "ler_word",
            "description": "Le e extrai o texto de um arquivo Word (.docx)",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_arquivo": {
                        "type": "string",
                        "description": "Nome do arquivo Word, ex: documento.docx"
                    }
                },
                "required": ["nome_arquivo"]
            }
        }
    },{
        "type": "function",
        "function": {
            "name": "criar_pasta",
            "description": "Cria uma nova pasta no diretorio atual",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_pasta": {
                        "type": "string",
                        "description": "Nome da pasta a criar, ex: relatorios"
                    }
                },
                "required": ["nome_pasta"]
            }
        }
    }
    ,{
        "type": "function",
        "function": {
            "name": "mover_arquivo",
            "description": "Move um arquivo para uma pasta de destino",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_arquivo": {
                        "type": "string",
                        "description": "Nome do arquivo a mover"
                    },
                    "pasta_destino": {
                        "type": "string",
                        "description": "Nome da pasta de destino"
                    }
                },
                "required": ["nome_arquivo", "pasta_destino"]
            }
        }
    }
    ,{
        "type": "function",
        "function": {
            "name": "listar_pastas",
            "description": "Lista todas as pastas no diretorio atual",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]