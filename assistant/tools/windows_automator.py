# Módulo Conceitual de Automação do Windows

"""
Este módulo fornece funções conceituais para interagir com o sistema operacional Windows
utilizando o módulo `subprocess` do Python. O objetivo é executar comandos no CMD e PowerShell,
gerenciar arquivos e processos de forma básica.

**Importante:** Este código foi desenvolvido em um ambiente Linux e serve como um
exemplo conceitual. Os comandos específicos (`dir`, `tasklist`, `powershell`, `Get-Process`, etc.)
são destinados ao ambiente Windows. A execução e o comportamento exato devem ser
testados e potencialmente adaptados em uma máquina Windows 11 real.

A abordagem principal utiliza `subprocess.run` para executar comandos externos e capturar
sua saída e erros de forma segura e eficiente.
"""

import subprocess
import platform
import shlex # Para lidar com argumentos de comando de forma segura
import os

# Constante para verificar se estamos (hipoteticamente) no Windows
# Em um cenário real, isso determinaria o comportamento exato.
IS_WINDOWS = platform.system() == "Windows" # No ambiente atual, isso será False

def execute_command(command: list[str], shell_type: str = "cmd", timeout: int = 30) -> tuple[bool, str]:
    """
    Executa um comando no CMD ou PowerShell e retorna o resultado.

    Esta função é um wrapper genérico para `subprocess.run`, adaptada conceitualmente
    para o Windows. Ela tenta executar o comando e captura a saída padrão e o erro padrão.

    Args:
        command: Uma lista de strings representando o comando e seus argumentos.
                 Exemplo: ["dir", "C:\Users"]
        shell_type: O tipo de shell a ser usado ('cmd' ou 'powershell').
        timeout: Tempo máximo de espera em segundos para o comando completar.

    Returns:
        Uma tupla contendo:
        - bool: True se o comando foi executado com sucesso (código de retorno 0),
                False caso contrário.
        - str: A saída padrão do comando (stdout) ou a mensagem de erro (stderr)
               se a execução falhou ou gerou erros.
    """
    if not IS_WINDOWS:
        # Simulação ou aviso em ambiente não-Windows
        print(f"[AVISO] Tentando executar comando Windows '{' '.join(command)}' em ambiente não-Windows. Retornando simulação.")
        # Poderia retornar uma resposta simulada ou simplesmente indicar a falha conceitual
        # return False, "Execução simulada: Funcionalidade apenas para Windows."
        # Para fins de demonstração, tentaremos executar mesmo assim, sabendo que falhará
        # se o comando não existir em Linux (como 'dir' sem alias).
        pass # Prossegue para tentar executar, mesmo sabendo que pode falhar

    try:
        # Prepara o comando para execução
        if shell_type == "powershell":
            # Para PowerShell, geralmente chamamos 'powershell.exe -Command ...'
            # Usar shlex.join pode ser mais seguro se os comandos vierem de fontes externas
            full_command = ["powershell", "-NoProfile", "-Command"] + command
        elif shell_type == "cmd":
            # Para CMD, podemos usar 'cmd.exe /c ...'
            full_command = ["cmd", "/c"] + command
        else:
            return False, f"Tipo de shell desconhecido: {shell_type}"

        # Executa o comando
        # text=True (ou encoding='utf-8') decodifica stdout/stderr para string
        # capture_output=True captura stdout/stderr em vez de exibi-los
        # check=False evita levantar exceção automaticamente em caso de erro (código de retorno != 0)
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            encoding='cp850', # Codificação comum no CMD do Windows PT-BR, pode precisar de ajuste
            timeout=timeout,
            check=False # Não levanta exceção em erro, verificamos manualmente
        )

        # Verifica o resultado
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            error_message = f"Erro ao executar comando (código {result.returncode}):\n{result.stderr.strip()}"
            # Às vezes, o erro também está no stdout
            if result.stdout:
                error_message += f"\nSaída (stdout):\n{result.stdout.strip()}"
            return False, error_message

    except FileNotFoundError:
        # Ocorre se 'cmd' ou 'powershell' não forem encontrados no PATH
        return False, f"Erro: '{shell_type}' não encontrado. Verifique a instalação e o PATH."
    except subprocess.TimeoutExpired:
        return False, f"Erro: O comando excedeu o tempo limite de {timeout} segundos."
    except Exception as e:
        # Captura outras exceções inesperadas
        return False, f"Erro inesperado ao executar o comando: {e}"

def list_directory_windows(path: str = ".") -> tuple[bool, str]:
    """
    Lista o conteúdo de um diretório no Windows usando o comando 'dir'.

    Args:
        path: O caminho do diretório a ser listado. Padrão é o diretório atual.

    Returns:
        Uma tupla (sucesso, saida_ou_erro).
    """
    # Validação básica do caminho (pode ser mais robusta)
    # No Windows real, seria importante validar e normalizar o path.
    safe_path = path # Em um cenário real, sanitizar ou validar o path
    return execute_command(["dir", safe_path], shell_type="cmd")

def list_processes_windows() -> tuple[bool, str]:
    """
    Lista os processos em execução no Windows usando 'tasklist' (CMD) ou 'Get-Process' (PowerShell).
    Prefere PowerShell por fornecer mais detalhes, mas tem 'tasklist' como fallback.

    Returns:
        Uma tupla (sucesso, saida_ou_erro).
    """
    success, output = execute_command(["Get-Process"], shell_type="powershell")
    if success:
        return True, output
    else:
        # Tenta o fallback com tasklist se Get-Process falhar
        print("[INFO] Falha ao usar Get-Process, tentando tasklist...")
        return execute_command(["tasklist"], shell_type="cmd")

def start_program_windows(program_path: str) -> tuple[bool, str]:
    """
    Tenta iniciar um programa no Windows usando o comando 'start'.

    Args:
        program_path: O caminho para o executável ou um nome de programa no PATH (ex: 'notepad.exe').

    Returns:
        Uma tupla (sucesso, saida_ou_erro). 'start' geralmente não produz stdout significativo.
    """
    # O comando 'start' no CMD é usado para iniciar programas em uma nova janela.
    # Ele geralmente retorna imediatamente, então capturar output pode não ser útil.
    # Usamos uma abordagem ligeiramente diferente com subprocess.Popen para não esperar.

    if not IS_WINDOWS:
        print(f"[AVISO] Tentando iniciar programa Windows '{program_path}' em ambiente não-Windows. Retornando simulação.")
        # return False, "Execução simulada: Funcionalidade apenas para Windows."
        pass # Tenta executar mesmo assim

try:
        # Usar Popen para não bloquear esperando o programa terminar.
        # shell=True pode ser um risco de segurança se program_path vier de input não confiável.
        # É mais seguro passar o comando como lista se possível, mas 'start' funciona melhor com shell=True.
        # Alternativa mais segura: usar ['cmd', '/c', 'start', '', program_path]
        process = subprocess.Popen(["cmd", "/c", "start", "", program_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Não esperamos pelo processo terminar com wait() ou communicate()
        # Apenas verificamos se Popen conseguiu iniciar.
        # Uma verificação mais robusta envolveria checar se o processo realmente iniciou (ex: via list_processes_windows após um delay)

        # stdout, stderr = process.communicate(timeout=5) # Poderia esperar um pouco para ver se há erro imediato
        # if process.returncode is not None and process.returncode != 0:
        #     return False, f"Falha ao iniciar o processo (código {process.returncode}): {stderr.decode(errors='ignore')}"

        return True, f"Comando para iniciar '{program_path}' enviado."

    except FileNotFoundError:
        return False, f"Erro: 'cmd' não encontrado. Verifique a instalação e o PATH."
    except Exception as e:
        return False, f"Erro inesperado ao tentar iniciar o programa: {e}"

# --- Exemplo de Uso (para teste conceitual) ---
if __name__ == "__main__":
    print("--- Teste Conceitual do Módulo de Automação Windows ---")

    print("\n1. Listando diretório atual (via CMD 'dir'):")
    success, output = list_directory_windows(".")
    if success:
        print("Sucesso:")
        print(output)
    else:
        print("Falha:")
        print(output)

    print("\n2. Listando processos (via PowerShell 'Get-Process' ou CMD 'tasklist'):")
    success, output = list_processes_windows()
    if success:
        print("Sucesso:")
        print(output) # A saída pode ser longa
    else:
        print("Falha:")
        print(output)

    print("\n3. Tentando iniciar 'notepad.exe' (via CMD 'start'):")
    # Este comando provavelmente falhará em Linux, mas demonstra a chamada.
    success, output = start_program_windows("notepad.exe")
    if success:
        print("Sucesso:")
        print(output)
    else:
        print("Falha:")
        print(output)

    print("\n4. Executando comando PowerShell arbitrário ('Get-Date'):")
    success, output = execute_command(["Get-Date"], shell_type="powershell")
    if success:
        print("Sucesso:")
        print(output)
    else:
        print("Falha:")
        print(output)

    print("\n5. Executando comando CMD com erro ('comando_invalido'):")
    success, output = execute_command(["comando_invalido"], shell_type="cmd")
    if success:
        print("Sucesso (inesperado):")
        print(output)
    else:
        print("Falha (esperado):")
        print(output)

    print("\n--- Fim do Teste Conceitual ---")

