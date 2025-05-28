# run_assistant.py

"""
Script principal para iniciar o Assistente de IA Local.
Permite escolher a interface (CLI ou Voz) via argumentos de linha de comando.
"""

import argparse
import sys

# Adiciona o diretório pai ao sys.path para permitir importações relativas
# Isso pode não ser necessário dependendo de como o pacote é instalado/executado
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# Importa as funções de inicialização das interfaces e outros módulos necessários
from assistant.interface import cli_interface, voice_interface
from assistant.database import db_manager
from assistant.utils.logger import log
# Importar config loader se a configuração for usada na inicialização
# from assistant.config import config_loader

def main():
    """Função principal que parseia argumentos e inicia a interface escolhida."""
    parser = argparse.ArgumentParser(description="Assistente de IA Local para Windows 11")
    parser.add_argument(
        "--interface",
        choices=["cli", "voice"],
        default="cli",
        help="Escolha a interface de interação: \"cli\" (texto) ou \"voice\" (voz). Padrão: cli"
    )
    args = parser.parse_args()

    log.info("--- Iniciando Assistente de IA Local ---")

    # Inicializa o banco de dados (cria tabelas se não existirem)
    try:
        db_manager.initialize_database()
    except Exception as e:
        log.critical(f"Falha ao inicializar o banco de dados. O histórico pode não funcionar: {e}", exc_info=True)
        print(f"ERRO CRÍTICO: Não foi possível inicializar o banco de dados: {e}", file=sys.stderr)
        # Decide se quer sair ou continuar sem DB
        # sys.exit(1)

    # Carrega configurações (exemplo)
    # try:
    #     config = config_loader.load_config()
    #     log.info("Configuração carregada com sucesso.")
    #     # Passar config para outros módulos se necessário
    # except Exception as e:
    #     log.error(f"Erro ao carregar configuração: {e}", exc_info=True)
    #     print(f"AVISO: Erro ao carregar config.yaml: {e}. Usando padrões.")

    # Inicia a interface selecionada
    if args.interface == "cli":
        try:
            cli_interface.start_cli()
        except Exception as e:
            log.critical(f"Erro fatal na interface CLI: {e}", exc_info=True)
            print(f"ERRO FATAL na interface CLI: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.interface == "voice":
        log.info("Verificando pré-requisitos para interface de voz...")
        # Verifica se as dependências de voz estão disponíveis
        try:
            import speech_recognition as sr
            # Tenta instanciar o microfone para um teste rápido
            mic_test = sr.Microphone()
            del mic_test
            log.info("Dependências de reconhecimento de voz parecem estar OK.")
        except ImportError:
            log.critical("Erro: Biblioteca SpeechRecognition não encontrada. Instale com \"pip install SpeechRecognition\".")
            print("ERRO: Biblioteca SpeechRecognition não encontrada. Interface de voz não pode iniciar.", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
             log.critical(f"Erro ao acessar o microfone: {e}. Verifique se PyAudio está instalado corretamente e se há um microfone disponível.")
             print(f"ERRO: Não foi possível acessar o microfone: {e}. Interface de voz não pode iniciar.", file=sys.stderr)
             sys.exit(1)
        except Exception as e:
            log.critical(f"Erro inesperado ao verificar pré-requisitos de voz: {e}", exc_info=True)
            print(f"ERRO inesperado ao verificar pré-requisitos de voz: {e}", file=sys.stderr)
            sys.exit(1)

        # Se as verificações passaram, inicia a interface de voz
        try:
            voice_interface.start_voice_interface()
        except Exception as e:
            log.critical(f"Erro fatal na interface de voz: {e}", exc_info=True)
            print(f"ERRO FATAL na interface de voz: {e}", file=sys.stderr)
            sys.exit(1)

    log.info("--- Assistente de IA Local encerrado ---")

if __name__ == "__main__":
    main()

