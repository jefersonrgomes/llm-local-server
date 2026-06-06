from config import SYSTEM_PROMPT
from agente import executar_tarefa

def main():
    # Historico começa com o system prompt
    historico = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Agente pronto. Digite sua tarefa ou 'sair' para encerrar.\n")

    while True:
        tarefa = input("Voce: ").strip()

        if tarefa.lower() == "sair":
            print("Encerrando.")
            break

        if not tarefa:
            continue

        historico.append({"role": "user", "content": tarefa})
        executar_tarefa(historico)

# Ponto de entrada do programa
if __name__ == "__main__":
    main()