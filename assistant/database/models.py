# assistant/database/models.py

"""
Define a estrutura (schema) para as tabelas do banco de dados SQLite.
Neste caso, uma tabela simples para registrar o histórico de interações.
"""

# SQL para criar a tabela de histórico, se ela não existir.
CREATE_HISTORY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS interaction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_input TEXT,
    agent_action TEXT,        -- Qual ferramenta foi usada ou se foi resposta direta
    action_details TEXT,    -- Parâmetros da ferramenta ou detalhes da ação
    tool_output TEXT,         -- Saída bruta da ferramenta (se aplicável)
    agent_response TEXT,      -- Resposta final formatada para o usuário
    success BOOLEAN           -- Indica se a interação geral foi bem-sucedida
);
"""

