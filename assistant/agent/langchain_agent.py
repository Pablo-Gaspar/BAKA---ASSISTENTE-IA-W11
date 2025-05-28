# assistant/agent/langchain_agent.py

"""
Implementa o agente de IA usando LangChain para processar comandos,
selecionar ferramentas e gerar respostas.
"""

# LangChain Imports (requer instalação: pip install langchain langchain-core langchain-community)
# Nota: A escolha específica do LLM (ex: OpenAI, Anthropic, um modelo local via Ollama)
# dependerá da configuração do usuário e da disponibilidade de chaves de API ou modelos locais.
# Este exemplo usará placeholders ou estruturas genéricas.
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent # Exemplo com ReAct
from langchain_core.tools import Tool
# Placeholder para um LLM. Em um cenário real, importe e instancie um LLM específico.
# from langchain_openai import ChatOpenAI
# from langchain_community.llms import Ollama
from langchain_core.language_models.base import BaseLanguageModel # Para type hinting

# Importa as funções das ferramentas (conceitualmente)
# Em uma estrutura real, esses módulos seriam importados diretamente.
# Para este exemplo, vamos definir funções placeholder que simulam a chamada.
from ..tools import windows_automator, vm_manager # Assume que __init__.py em tools expõe as funções
from ..database import db_manager
from ..utils.logger import log

# --- Placeholder LLM --- #
# Em um ambiente real, substitua isso pela inicialização do LLM desejado.
# Exemplo: llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key="SUA_CHAVE_API")
# Exemplo: llm = Ollama(model="llama3")
class PlaceholderLLM(BaseLanguageModel):
    def invoke(self, input, config=None, stop=None, **kwargs):
        # Simula uma resposta do LLM baseada na entrada
        prompt = str(input)
        log.warning("Usando PlaceholderLLM. Respostas serão simuladas.")
        if "liste os arquivos" in prompt.lower():
            return "Action: list_directory\nAction Input: ."
        elif "liste processos" in prompt.lower():
            return "Action: list_processes\nAction Input: "
        elif "abra o bloco de notas" in prompt.lower():
            return "Action: start_program\nAction Input: notepad.exe"
        elif "liste as vms" in prompt.lower():
            return "Action: list_vbox_vms\nAction Input: "
        else:
            return "Final Answer: Desculpe, como um LLM de placeholder, não entendi seu comando. Por favor, tente um dos comandos simulados (listar arquivos, listar processos, abrir bloco de notas, listar VMs)."

    async def ainvoke(self, input, config=None, stop=None, **kwargs):
        # Versão assíncrona do placeholder
        return self.invoke(input, config, stop, **kwargs)

    @property
    def _llm_type(self) -> str:
        return "placeholder-llm"

# --- Definição das Ferramentas LangChain --- #

def setup_tools() -> list[Tool]:
    """Cria e retorna uma lista de ferramentas LangChain disponíveis para o agente."""
    tools = [
        Tool(
            name="list_directory",
            func=lambda path=".": windows_automator.list_directory_windows(path)[1], # Retorna apenas a saída/erro
            description="Útil para listar arquivos e pastas em um diretório específico no sistema Windows. O input deve ser o caminho do diretório."
        ),
        Tool(
            name="list_processes",
            func=lambda _: windows_automator.list_processes_windows()[1],
            description="Útil para listar todos os processos atualmente em execução no sistema Windows."
        ),
        Tool(
            name="start_program",
            func=lambda program: windows_automator.start_program_windows(program)[1],
            description="Útil para iniciar um programa ou aplicativo no Windows. O input deve ser o nome ou caminho do executável (ex: notepad.exe, C:\\path\\to\\app.exe)."
        ),
        Tool(
            name="list_vbox_vms",
            func=lambda _: vm_manager.list_vbox_vms()[1],
            description="Útil para listar todas as máquinas virtuais (VMs) registradas no VirtualBox."
        ),
        Tool(
            name="start_vbox_vm",
            func=lambda vm_id: vm_manager.start_vbox_vm(vm_id)[1],
            description="Útil para iniciar uma máquina virtual (VM) específica do VirtualBox. O input deve ser o nome ou UUID da VM."
        ),
        Tool(
            name="stop_vbox_vm",
            func=lambda vm_id: vm_manager.stop_vbox_vm(vm_id)[1],
            description="Útil para desligar (shutdown ACPI) uma máquina virtual (VM) específica do VirtualBox. O input deve ser o nome ou UUID da VM."
        ),
        # Adicionar ferramentas VMware de forma similar se necessário
        # Tool(
        #     name="list_vmware_running_vms",
        #     func=lambda _: vm_manager.list_vmware_running_vms()[1],
        #     description="Útil para listar as VMs VMware atualmente em execução."
        # ),
        # Ferramenta de Busca Web (Placeholder)
        Tool(
            name="web_search",
            func=lambda query: f"Resultado simulado da busca por 
                                  {\"query\"}: Informação relevante encontrada.",
            description="Útil para buscar informações na internet quando o conhecimento interno não é suficiente. O input deve ser a consulta de busca."
        ),
    ]
    log.info(f"Ferramentas LangChain configuradas: {[tool.name for tool in tools]}")
    return tools

# --- Configuração do Agente --- #

def create_assistant_agent(llm: BaseLanguageModel, tools: list[Tool]) -> AgentExecutor:
    """
    Cria e configura o agente LangChain (exemplo com ReAct).

    Args:
        llm: A instância do modelo de linguagem a ser usado.
        tools: A lista de ferramentas disponíveis para o agente.

    Returns:
        Uma instância de AgentExecutor pronta para processar entradas.
    """
    # Define o template do prompt para o agente ReAct
    # Este é um template padrão, pode ser customizado
    prompt_template = """
    Responda às seguintes perguntas da melhor forma possível. Você tem acesso às seguintes ferramentas:

    {tools}

    Use o seguinte formato:

    Pergunta: a pergunta de entrada que você deve responder
    Pensamento: você deve sempre pensar sobre o que fazer
    Ação: a ação a ser tomada, deve ser uma das [{tool_names}]
    Entrada da Ação: a entrada para a ação
    Observação: o resultado da ação
    ... (este Pensamento/Ação/Entrada da Ação/Observação pode repetir N vezes)
    Pensamento: Eu agora sei a resposta final
    Resposta Final: a resposta final para a pergunta original

    Comece!

    Pergunta: {input}
    Pensamento:{agent_scratchpad}
    """
    prompt = PromptTemplate.from_template(prompt_template)

    # Cria o agente ReAct
    agent = create_react_agent(llm, tools, prompt)

    # Cria o executor do agente
    # verbose=True ajuda na depuração, mostrando os passos do agente
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    log.info("Executor do Agente LangChain (ReAct) criado.")
    return agent_executor

# --- Função Principal de Processamento --- #

# Inicializa o LLM (placeholder), ferramentas e agente uma vez
# Em uma aplicação real, o LLM seria configurado via arquivo de config
llm_instance = PlaceholderLLM()
tools_list = setup_tools()
agent_executor_instance = create_assistant_agent(llm_instance, tools_list)

def process_user_command(user_input: str) -> str:
    """
    Processa o comando do usuário usando o agente LangChain.

    Args:
        user_input: O comando textual do usuário.

    Returns:
        A resposta final gerada pelo agente.
    """
    log.info(f"Processando comando do usuário: 
             {\"user_input\"}")
    agent_action = "direct_response" # Padrão
    action_details = None
    tool_output = None
    agent_response = ""
    success = False

    try:
        # Executa o agente
        # O resultado é um dicionário, geralmente com a chave 'output'
        response_dict = agent_executor_instance.invoke({"input": user_input})
        agent_response = response_dict.get("output", "Não foi possível gerar uma resposta.")

        # Extrair detalhes da execução para o log (isso é simplificado)
        # LangChain pode ter formas mais robustas de obter o histórico de execução
        # Aqui, apenas assumimos que a resposta final indica sucesso se não for um erro padrão.
        if "Desculpe" not in agent_response and "Erro" not in agent_response:
            success = True
            # Idealmente, o agent_executor retornaria as ferramentas usadas.
            # Como placeholder, tentamos inferir baseado na resposta ou input.
            if any(tool.name in agent_response.lower() for tool in tools_list):
                 agent_action = "inferred_tool_use"
            # Detalhes mais precisos exigiriam parsear a saída verbose do agent_executor

        log.info(f"Resposta do agente: {agent_response}")

    except Exception as e:
        log.error(f"Erro ao processar comando com LangChain: {e}", exc_info=True)
        agent_response = f"Ocorreu um erro interno ao processar seu comando: {e}"
        success = False
        agent_action = "error"
        action_details = str(e)

    # Registrar no histórico
    db_manager.add_interaction_history(
        user_input=user_input,
        agent_action=agent_action, # Simplificado
        action_details=action_details, # Simplificado
        tool_output=tool_output, # Simplificado, idealmente capturado do agent_executor
        agent_response=agent_response,
        success=success
    )

    return agent_response

# --- Aprendizado Contínuo (Conceitual) --- #

"""
Aprendizado Contínuo:

O histórico de interações registrado no banco de dados (`interaction_history`)
serve como base para aprendizado e melhoria contínua, embora a implementação
deste aprendizado não esteja no escopo inicial.

Possibilidades Futuras:
1.  **Análise Manual:** Revisar o histórico periodicamente para identificar comandos
    mal interpretados, ferramentas que falham frequentemente, ou novas funcionalidades
    desejadas pelos usuários.
2.  **Melhoria de Prompts:** Usar exemplos do histórico (bons e ruins) para refinar
    os prompts enviados ao LLM, melhorando a capacidade de raciocínio e seleção
    de ferramentas do agente.
3.  **Fine-tuning (Avançado):** Em cenários com volume suficiente de dados e recursos,
    o histórico poderia ser usado para fine-tuning de modelos de linguagem menores
    e específicos para as tarefas do assistente, potencialmente melhorando a performance
    e reduzindo a dependência de LLMs grandes e externos.
4.  **Memória Conversacional:** Integrar o histórico recente da conversa atual na memória
    do agente LangChain (ex: `ConversationBufferMemory`) para que ele possa entender
    o contexto de comandos subsequentes.
5.  **Sugestão de Comandos:** Analisar padrões de uso no histórico para sugerir
    comandos úteis ou atalhos para o usuário.

Nesta implementação, o foco está no registro robusto dos dados, que é o pré-requisito
para qualquer esforço futuro de aprendizado.
"""

# --- Exemplo de Uso --- #
if __name__ == "__main__":
    print("--- Teste do Módulo LangChain Agent ---")
    db_manager.initialize_database() # Garante DB e tabela

    test_commands = [
        "liste os arquivos na pasta atual",
        "quais processos estão rodando?",
        "por favor, abra o bloco de notas",
        "liste as vms do virtualbox",
        "qual a capital da França?" # Exemplo que pode usar busca web (simulada)
    ]

    for command in test_commands:
        print(f"\n>>> Usuário: {command}")
        response = process_user_command(command)
        print(f"<<< Assistente: {response}")

    print("\n--- Verificando Histórico Recente --- ")
    history = db_manager.get_interaction_history(limit=len(test_commands))
    for record in reversed(history): # Mostra na ordem de execução
        print(f"  - Input: {record[\"user_input\"]}")
        print(f"    Action: {record[\"agent_action\"]}")
        print(f"    Response: {record[\"agent_response\"]}")
        print(f"    Success: {record[\"success\"]}")

    print("\n--- Fim do Teste LangChain Agent ---")

