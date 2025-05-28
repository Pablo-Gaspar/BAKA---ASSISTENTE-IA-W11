# assistant/core/orchestrator.py

"""
Orquestra o fluxo de entrada e saída entre a interface e o agente.
Em uma implementação mais complexa, poderia lidar com gerenciamento de estado,
seleção de perfil de usuário, etc.

Nesta versão simplificada, ele apenas encaminha a entrada para o agente
e retorna a resposta.
"""

from ..agent.langchain_agent import process_user_command
from ..utils.logger import log

def handle_input(user_input: str, source_interface: str = "unknown") -> str:
    """
    Ponto central para lidar com a entrada do usuário de qualquer interface.

    Args:
        user_input: O texto do comando do usuário.
        source_interface: Identificador da interface de origem (ex: \"cli\", \"voice\").

    Returns:
        A resposta textual do assistente.
    """
    log.info(f"Recebida entrada da interface 
             {\"source_interface\"}: 
             {\"user_input[:100]}...\"")

    # Chama diretamente o processador do agente LangChain
    response = process_user_command(user_input)

    log.info(f"Retornando resposta para a interface 
             {\"source_interface\"}: 
             {\"response[:100]}...\"")
    return response

# Poderiam existir outras funções aqui para inicialização, shutdown, etc.

