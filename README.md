# Assistente de IA Local para Windows 11

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%2011-blue)](https://www.microsoft.com/windows/windows-11)

Um assistente de IA local para Windows 11 que entende comandos em português brasileiro, automatiza tarefas no sistema operacional, gerencia máquinas virtuais e busca informações online quando necessário.

## ✨ Funcionalidades

* 🗣️ **Interação Multimodal:** Aceita comandos via texto (CLI) ou voz
* 🧠 **Processamento de Linguagem Natural:** Utiliza LangChain e LLMs para entender comandos em português
* 💻 **Automação do Windows:** Executa comandos CMD/PowerShell, lista arquivos/processos, inicia programas
* 🖥️ **Gerenciamento de VMs:** Controla VirtualBox e VMware (listar, iniciar, parar VMs)
* 🔍 **Busca de Informações:** Capacidade de buscar dados online para responder perguntas
* 📝 **Histórico e Logging:** Registra interações em banco de dados SQLite e logs detalhados

## 🚀 Início Rápido

### Pré-requisitos

* Windows 11
* Python 3.10+ (recomendado 3.11)
* Git (opcional)
* VirtualBox/VMware (opcional, para gerenciamento de VMs)
* Microfone (opcional, para interface de voz)

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/windows-assistant.git
   cd windows-assistant
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o assistente:
   ```bash
   copy config.yaml.example config.yaml
   # Edite config.yaml com suas configurações
   ```

5. Execute o assistente:
   ```bash
   python run_assistant.py  # Interface CLI (padrão)
   # ou
   python run_assistant.py --interface voice  # Interface de voz
   ```

## 📋 Exemplos de Comandos

* "liste os arquivos na área de trabalho"
* "quais processos estão em execução?"
* "abra o bloco de notas"
* "liste minhas máquinas virtuais do VirtualBox"
* "inicie a VM chamada UbuntuServer"
* "pesquise sobre inteligência artificial"

## 🏗️ Arquitetura

O assistente segue uma arquitetura modular em Python:

* **`core`**: Orquestra o fluxo entre interface e agente
* **`interface`**: Módulos para interação (CLI, voz)
* **`agent`**: Agente LangChain para processamento de linguagem natural
* **`tools`**: Ferramentas para automação (Windows, VMs)
* **`database`**: Gerencia o histórico de interações
* **`config`**: Carrega configurações da aplicação
* **`utils`**: Utilitários como logging

## ⚙️ Configuração

O arquivo `config.yaml` permite configurar:

* Provedor e modelo de LLM (OpenAI, Ollama, etc.)
* Chaves de API necessárias
* Caminhos para VMs do VMware
* Nível de logging

## 🔧 Adaptação para Windows

Como o desenvolvimento foi realizado em ambiente Linux, os módulos que interagem com o Windows são implementados conceitualmente. Ao usar no Windows 11:

* Verifique se os comandos funcionam no seu terminal
* Ajuste a codificação se necessário (cp1252, utf-8)
* Certifique-se que os executáveis estejam no PATH
* Considere permissões de administrador para certos comandos

## 🧩 Extensibilidade

O design modular facilita a adição de novas funcionalidades:

* **Novas Ferramentas:** Adicione novos arquivos em `tools/` e registre no agente
* **Novas Interfaces:** Crie novos módulos em `interface/` (ex: GUI)
* **Melhore o Agente:** Experimente diferentes configurações de LangChain

## 🤝 Contribuição

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre como contribuir.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📊 Roadmap

- [*] Implementação de interface gráfica (GUI)
- [*] Integração com mais serviços online
- [*] Suporte a múltiplos idiomas
- [*] Aprendizado contínuo baseado no histórico de interações

## 📞 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub ou entre em contato através de [PABLOO.GASPAR@HOTMAIL.COM].
