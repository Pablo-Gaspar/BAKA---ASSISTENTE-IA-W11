# assistant/interface/voice_interface.py

"""
Implementa a interface de reconhecimento de voz para interação com o assistente.
Utiliza a biblioteca SpeechRecognition para capturar e transcrever áudio.

**Pré-requisitos:**
- Biblioteca SpeechRecognition instalada (`pip install SpeechRecognition`).
- Biblioteca PyAudio instalada (`pip install PyAudio`) para acesso ao microfone (pode variar dependendo do OS e método).
- Um microfone configurado e funcionando no sistema.
- Conexão com a internet (para motores de reconhecimento online como Google Web Speech).

**Nota:** A qualidade do reconhecimento depende do microfone, ruído ambiente e do motor escolhido.
Este módulo fornece uma integração básica.
"""

import speech_recognition as sr

# Importa a função de processamento do agente
from ..agent.langchain_agent import process_user_command
from ..utils.logger import log

# Inicializa o reconhecedor e o microfone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def listen_and_recognize(timeout_seconds: int = 5, phrase_time_limit: int = 10) -> str | None:
    """
    Ouve o microfone, tenta reconhecer a fala e retorna o texto transcrito.

    Args:
        timeout_seconds: Tempo máximo (em segundos) para esperar o início da fala.
        phrase_time_limit: Tempo máximo (em segundos) que a frase pode durar.

    Returns:
        A string de texto reconhecida ou None se não foi possível reconhecer.
    """
    with microphone as source:
        # Ajusta o reconhecedor para o ruído ambiente
        log.info("Ajustando para ruído ambiente... Fale algo se quiser calibrar.")
        try:
            # recognizer.adjust_for_ambient_noise(source, duration=1)
            # Usar dynamic=True pode ser melhor em ambientes variáveis
            recognizer.dynamic_energy_threshold = True
            recognizer.adjust_for_ambient_noise(source)
            log.info("Pronto para ouvir.")
            print("Ouvindo... Fale agora!")

            # Ouve o áudio do microfone
            try:
                audio = recognizer.listen(
                    source,
                    timeout=timeout_seconds, # Tempo esperando o início da fala
                    phrase_time_limit=phrase_time_limit # Tempo máximo da fala
                )
                log.info("Áudio capturado, tentando reconhecimento...")
            except sr.WaitTimeoutError:
                log.warning("Nenhuma fala detectada dentro do tempo limite.")
                print("(Nenhuma fala detectada)")
                return None

    # Tenta reconhecer a fala usando um motor (Google Web Speech por padrão)
    try:
        # Nota: recognize_google requer conexão com a internet.
        # Para offline, pode-se usar recognize_sphinx (requer pocketsphinx)
        recognized_text = recognizer.recognize_google(audio, language="pt-BR")
        log.info(f"Texto reconhecido: 
                 {\"recognized_text\"}")
        print(f"Você disse: {recognized_text}")
        return recognized_text
    except sr.UnknownValueError:
        log.warning("Não foi possível entender o áudio.")
        print("(Não consegui entender o que você disse)")
        return None
    except sr.RequestError as e:
        # Erro ao conectar ao serviço de reconhecimento (ex: sem internet)
        log.error(f"Erro no serviço de reconhecimento de voz: {e}")
        print(f"Erro no serviço de reconhecimento: {e}")
        return None
    except Exception as e:
        log.error(f"Erro inesperado durante o reconhecimento: {e}", exc_info=True)
        print(f"Ocorreu um erro inesperado no reconhecimento: {e}")
        return None

def start_voice_interface():
    """Inicia o loop da interface de voz."""
    log.info("Iniciando interface de voz.")
    print("\nBem-vindo ao Assistente de IA Local! (Interface de Voz)")
    print("Quando ouvir \"Ouvindo...\", fale seu comando.")
    print("Diga \"sair\" para terminar ou pressione Ctrl+C.")

    # Calibração inicial
    listen_and_recognize(timeout_seconds=1, phrase_time_limit=1) # Apenas para calibrar

    while True:
        try:
            # Ouve o comando do usuário
            user_input_text = listen_and_recognize()

            if user_input_text:
                # Verifica o comando de saída
                if user_input_text.strip().lower() == "sair":
                    log.info("Saindo da interface de voz por comando do usuário.")
                    print("Até logo!")
                    break

                # Processa o comando reconhecido
                log.debug(f"Enviando para processamento do agente: {user_input_text}")
                response = process_user_command(user_input_text)
                log.debug(f"Resposta recebida do agente: {response}")

                # Exibe a resposta (textualmente por enquanto)
                print(f"\nAssistente: {response}")
                # TODO: Integrar Text-to-Speech (TTS) para resposta falada, se desejado.

            # Pequena pausa antes de ouvir novamente, se necessário
            # time.sleep(0.5)

        except KeyboardInterrupt:
            log.info("Saindo da interface de voz devido a KeyboardInterrupt (Ctrl+C).")
            print("\nAté logo!")
            break
        except Exception as e:
            log.error(f"Erro inesperado no loop da interface de voz: {e}", exc_info=True)
            print(f"Ocorreu um erro inesperado: {e}")
            # break # Decide se quer parar em caso de erro

if __name__ == "__main__":
    # Para teste direto do módulo de voz
    # Nota: Requer microfone, bibliotecas e possivelmente internet.
    from ..database.db_manager import initialize_database
    initialize_database()
    start_voice_interface()

