# assistant/interface/cli_interface.py

"""
Implementa a interface de linha de comando (CLI) para interação textual com o assistente.
"""

# Importa a função de processamento do agente (será definida no orchestrator)
# from ..core.orchestrator import handle_input
# Por enquanto, usamos a função direta do agente para teste
from ..agent.langchain_agent import process_user_command
from ..utils.logger import log

def start_cli():
    """Inicia o loop da interface de linha de comando."""
    log.info("Iniciando interface de linha de comando (CLI).")
    print("\nBem-vindo ao Assistente de IA Local! (Interface de Texto)")
    print("Digite seu comando ou 
          \"sair\" para terminar.")

    while True:
        try:
            user_input = input("\nVocê: ")
            if user_input.strip().lower() == "sair":
                log.info("Saindo da interface CLI por comando do usuário.")
                print("Até logo!")
                break

            if not user_input.strip():
                continue

            # Chama a função central de processamento
            # Em uma implementação completa, chamaria o orchestrator
            # response = handle_input(user_input, "cli")
            log.debug(f"Enviando para processamento do agente: {user_input}")
            response = process_user_command(user_input)
            log.debug(f"Resposta recebida do agente: {response}")

            print(f"\nAssistente: {response}")

        except KeyboardInterrupt:
            log.info("Saindo da interface CLI devido a KeyboardInterrupt (Ctrl+C).")
            print("\nAté logo!")
            break
        except Exception as e:
            log.error(f"Erro inesperado no loop da CLI: {e}", exc_info=True)
            print(f"Ocorreu um erro inesperado: {e}")
            # Decide se quer continuar ou parar em caso de erro
            # break

if __name__ == "__main__":
    # Para teste direto do módulo CLI
    # Nota: Isso requer que o agente e suas dependências estejam funcionando.
    from ..database.db_manager import initialize_database
    initialize_database()
    start_cli()

