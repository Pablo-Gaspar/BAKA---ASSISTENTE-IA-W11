# assistant/database/db_manager.py

import sqlite3
import os
from datetime import datetime

# Importa o SQL para criar a tabela
from .models import CREATE_HISTORY_TABLE_SQL
from ..utils.logger import log # Importa o logger configurado

DATABASE_DIR = "/home/ubuntu/assistant/data"
DATABASE_FILE = os.path.join(DATABASE_DIR, "assistant_history.db")

def get_db_connection():
    """Estabelece e retorna uma conexão com o banco de dados SQLite."""
    os.makedirs(DATABASE_DIR, exist_ok=True)
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row # Retorna dicionários em vez de tuplas
        log.info(f"Conexão com o banco de dados 
                 {\"DATABASE_FILE\"} estabelecida.")
        return conn
    except sqlite3.Error as e:
        log.error(f"Erro ao conectar ao banco de dados 
                  {\"DATABASE_FILE\"}: {e}")
        raise # Re-levanta a exceção para que o chamador possa lidar com ela

def initialize_database():
    """
    Inicializa o banco de dados, criando a tabela de histórico se ela não existir.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(CREATE_HISTORY_TABLE_SQL)
        conn.commit()
        log.info("Banco de dados inicializado com sucesso. Tabela 
                 \"interaction_history\" verificada/criada.")
        conn.close()
    except sqlite3.Error as e:
        log.error(f"Erro ao inicializar o banco de dados: {e}")

def add_interaction_history(
    user_input: str,
    agent_action: str,
    action_details: str | None = None,
    tool_output: str | None = None,
    agent_response: str | None = None,
    success: bool = True
):
    """
    Adiciona um registro de interação ao banco de dados de histórico.

    Args:
        user_input: O comando ou pergunta original do usuário.
        agent_action: Descrição da ação tomada pelo agente (ex: \"use_tool:list_directory\", \"direct_response\").
        action_details: Parâmetros usados pela ferramenta ou detalhes da ação.
        tool_output: A saída bruta retornada pela ferramenta, se aplicável.
        agent_response: A resposta final formatada enviada ao usuário.
        success: Booleano indicando se a interação foi considerada bem-sucedida.
    """
    sql = """
    INSERT INTO interaction_history (
        user_input, agent_action, action_details, tool_output, agent_response, success
    ) VALUES (?, ?, ?, ?, ?, ?);
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (
            user_input,
            agent_action,
            action_details,
            tool_output,
            agent_response,
            success
        ))
        conn.commit()
        log.info(f"Interação registrada no histórico: 
                 {\"user_input[:50]}...\" -> 
                 {\"agent_action\"}")
        conn.close()
    except sqlite3.Error as e:
        log.error(f"Erro ao adicionar registro ao histórico: {e}")

def get_interaction_history(limit: int = 10) -> list[dict]:
    """
    Recupera os últimos registros do histórico de interações.

    Args:
        limit: O número máximo de registros a serem retornados.

    Returns:
        Uma lista de dicionários, onde cada dicionário representa uma interação.
    """
    sql = "SELECT * FROM interaction_history ORDER BY timestamp DESC LIMIT ?;"
    history = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (limit,))
        rows = cursor.fetchall()
        # Converte as linhas (sqlite3.Row) em dicionários padrão
        history = [dict(row) for row in rows]
        conn.close()
        log.info(f"Recuperados {len(history)} registros do histórico.")
    except sqlite3.Error as e:
        log.error(f"Erro ao recuperar histórico: {e}")
    return history

# --- Exemplo de Uso --- #
if __name__ == "__main__":
    print("--- Teste do Módulo DB Manager ---")
    initialize_database() # Garante que a tabela existe

    print("\n1. Adicionando uma interação de exemplo:")
    add_interaction_history(
        user_input="liste os arquivos no diretório atual",
        agent_action="use_tool:list_directory_windows",
        action_details=\"{'path': '.'}\",
        tool_output="Volume in drive C has no label.\\n Volume Serial Number is XXXX-XXXX...",
        agent_response="Aqui estão os arquivos no diretório atual: ...",
        success=True
    )

    print("\n2. Adicionando outra interação (falha simulada):")
    add_interaction_history(
        user_input="inicie a vm \"vm_inexistente\"",
        agent_action="use_tool:start_vbox_vm",
        action_details=\"{'vm_name_or_uuid': 'vm_inexistente', 'headless': False}\",
        tool_output="VBoxManage.exe: error: Could not find a machine named \'vm_inexistente\'",
        agent_response="Desculpe, não consegui encontrar uma VM com o nome \'vm_inexistente\'.",
        success=False
    )

    print("\n3. Recuperando os últimos 5 registros do histórico:")
    history_records = get_interaction_history(limit=5)
    if history_records:
        for record in history_records:
            print(f"  - ID: {record[\"id\" ]}, 
                  Timestamp: {record[\"timestamp\" ]}, 
                  Input: {record[\"user_input\"][:30]}...")
    else:
        print("Nenhum registro encontrado ou erro ao buscar.")

    print("\n--- Fim do Teste DB Manager ---")

