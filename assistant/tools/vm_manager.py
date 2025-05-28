# Módulo Conceitual de Gerenciamento de Máquinas Virtuais (VMs)

"""
Este módulo fornece funções conceituais para interagir com softwares de virtualização
como VirtualBox (usando `VBoxManage`) e VMware (usando `vmrun`) através do módulo `subprocess`.

**Importante:** Este código é conceitual e desenvolvido em ambiente Linux.
Ele assume que `VBoxManage` (para VirtualBox) ou `vmrun` (para VMware Workstation/Player)
estão instalados, configurados corretamente e disponíveis no PATH do sistema
na máquina Windows 11 onde o assistente será executado.

Os comandos exatos e seus comportamentos devem ser verificados e possivelmente
adaptados no ambiente Windows real. A interação com VMs pode exigir configurações
específicas (como permissões, rede, Guest Additions/VMware Tools) que estão
fora do escopo deste módulo.
"""

import subprocess
import platform
import shlex

# Constante para verificar se estamos (hipoteticamente) no Windows
IS_WINDOWS = platform.system() == "Windows"

# --- Funções Auxiliares --- #

def _execute_vm_command(command: list[str], tool_name: str, timeout: int = 60) -> tuple[bool, str]:
    """
    Função auxiliar interna para executar comandos de ferramentas de VM (`VBoxManage`, `vmrun`).

    Args:
        command: Lista de strings representando o comando completo (incluindo o nome da ferramenta).
        tool_name: Nome da ferramenta (usado para mensagens de erro).
        timeout: Tempo máximo de espera em segundos.

    Returns:
        Uma tupla (sucesso, saida_ou_erro).
    """
    if not IS_WINDOWS:
        print(f"[AVISO] Tentando executar comando VM 
              '{\' \'.join(command)}\' em ambiente não-Windows. Retornando simulação.")
        # Em um ambiente real, poderíamos parar aqui ou tentar executar mesmo assim.
        # Para demonstração, tentaremos executar.
        pass

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding='utf-8', # Tentar UTF-8 como padrão, pode precisar de ajuste
            timeout=timeout,
            check=False
        )

        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            error_message = f"Erro ao executar {tool_name} (código {result.returncode}):\n{result.stderr.strip()}"
            if result.stdout:
                error_message += f"\nSaída (stdout):\n{result.stdout.strip()}"
            return False, error_message

    except FileNotFoundError:
        return False, f"Erro: Ferramenta 
              '{tool_name}' não encontrada. Verifique a instalação e o PATH."
    except subprocess.TimeoutExpired:
        return False, f"Erro: O comando {tool_name} excedeu o tempo limite de {timeout} segundos."
    except Exception as e:
        return False, f"Erro inesperado ao executar {tool_name}: {e}"

# --- Funções de Gerenciamento de VirtualBox --- #

def list_vbox_vms() -> tuple[bool, str]:
    """
    Lista todas as máquinas virtuais registradas no VirtualBox usando `VBoxManage list vms`.

    Returns:
        Uma tupla (sucesso, saida_ou_erro).
    """
    command = ["VBoxManage", "list", "vms"]
    return _execute_vm_command(command, "VBoxManage")

def start_vbox_vm(vm_name_or_uuid: str, headless: bool = False) -> tuple[bool, str]:
    """
    Inicia uma máquina virtual do VirtualBox especificada.

    Args:
        vm_name_or_uuid: O nome ou UUID da VM a ser iniciada.
        headless: Se True, inicia a VM sem interface gráfica (modo headless).
                  Padrão é False (inicia com GUI).

    Returns:
        Uma tupla (sucesso, saida_ou_erro).
    """
    command = ["VBoxManage", "startvm", vm_name_or_uuid]
    if headless:
        command.extend(["--type", "headless"])
    else:
        command.extend(["--type", "gui"]) # Ou 'separate' dependendo da versão/preferência

    # Iniciar VM pode demorar, talvez um timeout maior seja necessário
    return _execute_vm_command(command, "VBoxManage", timeout=120)

def stop_vbox_vm(vm_name_or_uuid: str, force: bool = False) -> tuple[bool, str]:
    """
    Desliga uma máquina virtual do VirtualBox especificada.

    Args:
        vm_name_or_uuid: O nome ou UUID da VM a ser desligada.
        force: Se True, força o desligamento (poweroff) em vez de um ACPI shutdown.
               Padrão é False (tentar ACPI shutdown).

    Returns:
        Uma tupla (sucesso, saida_ou_erro).
    """
    command = ["VBoxManage", "controlvm", vm_name_or_uuid]
    if force:
        command.append("poweroff")
    else:
        command.append("acpipowerbutton") # Tenta um desligamento suave

    # Desligar também pode demorar
    return _execute_vm_command(command, "VBoxManage", timeout=90)

# --- Funções de Gerenciamento de VMware --- #

# Nota: vmrun requer o caminho para o arquivo .vmx da VM.
# A localização padrão pode variar (ex: Documentos\Virtual Machines)
# Seria necessário configurar ou descobrir esses caminhos.

def list_vmware_running_vms() -> tuple[bool, str]:
    """
    Lista as máquinas virtuais VMware em execução usando `vmrun list`.

    Returns:
        Uma tupla (sucesso, saida_ou_erro).
    """
    command = ["vmrun", "list"]
    return _execute_vm_command(command, "vmrun")

def start_vmware_vm(vmx_path: str, nogui: bool = False) -> tuple[bool, str]:
    """
    Inicia uma máquina virtual VMware especificada pelo seu arquivo .vmx.

    Args:
        vmx_path: O caminho completo para o arquivo .vmx da VM.
        nogui: Se True, tenta iniciar a VM sem interface gráfica (similar a headless).
               Padrão é False.

    Returns:
        Uma tupla (sucesso, saida_ou_erro).
    """
    command = ["vmrun"]
    if nogui:
        command.append("-T", "ws-nogui") # Para Workstation, pode variar para Player
    else:
        command.append("-T", "ws") # Ou 'player'

    command.extend(["start", vmx_path])
    if nogui:
        command.append("nogui")
    else:
        command.append("gui")

    # Pode precisar de timeout maior
    return _execute_vm_command(command, "vmrun", timeout=120)

def stop_vmware_vm(vmx_path: str, force: bool = False) -> tuple[bool, str]:
    """
    Desliga uma máquina virtual VMware especificada.

    Args:
        vmx_path: O caminho completo para o arquivo .vmx da VM.
        force: Se True, força o desligamento ('hard'). Se False, tenta um desligamento suave ('soft').
               Padrão é False.

    Returns:
        Uma tupla (sucesso, saida_ou_erro).
    """
    command = ["vmrun", "-T", "ws"] # Assumindo Workstation, ajustar se necessário
    command.append("stop")
    command.append(vmx_path)
    if force:
        command.append("hard")
    else:
        command.append("soft") # Tenta usar VMware Tools para desligamento suave

    # Pode precisar de timeout maior
    return _execute_vm_command(command, "vmrun", timeout=90)

def execute_command_in_vmware_guest(vmx_path: str, guest_user: str, guest_pass: str, command_to_run: str) -> tuple[bool, str]:
    """
    Executa um comando dentro de uma VM VMware convidada.
    **Requer VMware Tools instalado e rodando no convidado, e credenciais válidas.**

    Args:
        vmx_path: Caminho para o arquivo .vmx da VM.
        guest_user: Nome de usuário válido dentro da VM convidada.
        guest_pass: Senha para o usuário convidado.
        command_to_run: O comando completo a ser executado dentro da VM.

    Returns:
        Uma tupla (sucesso, saida_do_comando_ou_erro).
    """
    # Nota: Passar senhas diretamente na linha de comando pode ser um risco de segurança.
    # vmrun pode ter opções mais seguras ou exigir configuração prévia.
    command = [
        "vmrun",
        "-T", "ws", # Ajustar conforme necessário
        "-gu", guest_user,
        "-gp", guest_pass,
        "runProgramInGuest",
        vmx_path,
        "-activeWindow", # Ou omitir para rodar em background
        command_to_run
    ]

    # Executar comandos no guest pode demorar
    return _execute_vm_command(command, "vmrun", timeout=120)

# --- Exemplo de Uso (para teste conceitual) ---
if __name__ == "__main__":
    print("--- Teste Conceitual do Módulo de Gerenciamento de VM ---")

    print("\n1. Listando VMs do VirtualBox:")
    success, output = list_vbox_vms()
    if success:
        print("Sucesso:")
        print(output)
    else:
        print("Falha:")
        print(output)

    # --- Exemplos comentados que requerem nomes/paths específicos --- #
    # print("\n2. Tentando iniciar VM VirtualBox 'MinhaVMTeste':")
    # success, output = start_vbox_vm("MinhaVMTeste")
    # print(f"Resultado: {success} - {output}")

    # print("\n3. Tentando desligar VM VirtualBox 'MinhaVMTeste':")
    # success, output = stop_vbox_vm("MinhaVMTeste")
    # print(f"Resultado: {success} - {output}")
    # ------------------------------------------------------------- #

    print("\n4. Listando VMs VMware em execução:")
    success, output = list_vmware_running_vms()
    if success:
        print("Sucesso:")
        print(output)
    else:
        print("Falha:")
        print(output)

    # --- Exemplos comentados que requerem nomes/paths específicos --- #
    # vmx_file_path = "C:\\Users\\SeuUsuario\\Documents\\Virtual Machines\\MinhaVMware\\MinhaVMware.vmx"
    # guest_username = "usuario_vm"
    # guest_password = "senha_vm"

    # print(f"\n5. Tentando iniciar VM VMware em '{vmx_file_path}':")
    # success, output = start_vmware_vm(vmx_file_path)
    # print(f"Resultado: {success} - {output}")

    # print(f"\n6. Tentando executar 'ipconfig' na VM VMware em '{vmx_file_path}':")
    # success, output = execute_command_in_vmware_guest(vmx_file_path, guest_username, guest_password, "C:\\Windows\\System32\\ipconfig.exe")
    # print(f"Resultado: {success} - {output}")

    # print(f"\n7. Tentando desligar VM VMware em '{vmx_file_path}':")
    # success, output = stop_vmware_vm(vmx_file_path)
    # print(f"Resultado: {success} - {output}")
    # ------------------------------------------------------------- #

    print("\n--- Fim do Teste Conceitual ---")

