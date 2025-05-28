# Tarefas Abertas e Sugestões de Melhorias

Este documento lista tarefas abertas, limitações conhecidas e sugestões de melhorias para o Assistente de IA Local para Windows 11. Se você deseja contribuir, estas são boas oportunidades para começar.

## Adaptações para Windows

- [ ] **Teste em ambiente Windows real**: O código foi desenvolvido conceitualmente em Linux e precisa ser testado e adaptado para Windows 11.
- [ ] **Ajuste de paths**: Substituir paths absolutos por relativos ou usar `os.path.join` para maior portabilidade.
- [ ] **Codificação de caracteres**: Testar diferentes codificações (cp1252, utf-8) para garantir compatibilidade com saída de comandos Windows.
- [ ] **Verificação de comandos**: Confirmar se todos os comandos Windows funcionam conforme esperado.

## Melhorias de Funcionalidade

- [ ] **Implementação real de LLM**: Substituir o LLM placeholder por uma integração real com OpenAI, Ollama ou outro provedor.
- [ ] **API de Busca Web**: Implementar integração com uma API de busca real (Google Custom Search, SerpAPI, etc.).
- [ ] **Síntese de Voz (TTS)**: Adicionar Text-to-Speech para complementar o reconhecimento de voz.
- [ ] **Interface Gráfica**: Desenvolver uma GUI simples usando Tkinter, PyQt ou outra biblioteca.
- [ ] **Ferramentas adicionais**: Implementar ferramentas para clima, notícias, etc.

## Segurança e Robustez

- [ ] **Validação de entrada**: Implementar validação mais rigorosa de entradas do usuário.
- [ ] **Sandbox para comandos**: Considerar a implementação de um sandbox ou lista de permissões para comandos do sistema.
- [ ] **Criptografia de configuração**: Implementar criptografia para armazenar chaves de API e credenciais.
- [ ] **Testes automatizados**: Adicionar testes unitários e de integração.

## Documentação

- [ ] **Documentação de API**: Adicionar documentação detalhada da API para desenvolvedores.
- [ ] **Tutoriais**: Criar tutoriais passo a passo para casos de uso comuns.
- [ ] **Exemplos de código**: Adicionar mais exemplos de como estender o assistente.

## Extensões Futuras

- [ ] **Aprendizado contínuo**: Implementar análise do histórico para melhorar o comportamento do assistente.
- [ ] **Plugins de terceiros**: Criar um sistema de plugins para permitir que terceiros adicionem novas funcionalidades.
- [ ] **Integração com serviços cloud**: Adicionar integração com serviços como Azure, AWS ou Google Cloud.
- [ ] **Suporte a múltiplos idiomas**: Expandir o suporte além do português brasileiro.
- [ ] **Assistente proativo**: Implementar funcionalidades que permitam ao assistente tomar iniciativas baseadas em padrões de uso.

## Problemas Conhecidos

- O reconhecimento de voz pode ser impreciso em ambientes ruidosos.
- A instalação do PyAudio no Windows pode ser desafiadora para alguns usuários.
- O LLM placeholder tem capacidades limitadas comparado a um LLM real.
- Alguns comandos podem requerer privilégios de administrador no Windows.

Se você decidir trabalhar em alguma dessas tarefas, por favor abra uma issue no GitHub para discutir a implementação e evitar trabalho duplicado.
