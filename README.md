OrangeCode

AI Coding Agent para terminal

O OrangeCode é um agente de programação desenvolvido em Python, capaz de analisar, criar e editar códigos, executar comandos e trabalhar diretamente nos arquivos dos seus projetos utilizando inteligência artificial.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-D97735?style=flat-square">
  <img src="https://img.shields.io/badge/Status-Em%20desenvolvimento-orange?style=flat-square">
</p>---

Funcionalidades

- Suporte a múltiplos provedores de IA.
- Leitura e gerenciamento de arquivos.
- Criação e edição de códigos.
- Execução de comandos no terminal.
- Sistema de permissões configurável.
- Configurações persistentes.
- Histórico de conversação.

Provedores suportados

Provedor| Modelo padrão
OpenAI| "gpt-4.1"
Groq| "openai/gpt-oss-120b"
Gemini| "gemini-2.5-flash"
DeepSeek| "deepseek-chat"
OpenRouter| "openai/gpt-4.1-mini"
Anthropic| "claude-sonnet-4-5"
Ollama| "qwen2.5-coder:7b"

Instalação

1. Instale os requisitos:

pkg update && pkg upgrade -y
pkg install python git -y

2. Clone o repositório:

git clone https://github.com/PauloDevz/OrangeCode.git

3. Entre na pasta:

cd OrangeCode

4. Instale as dependências:

pip install rich prompt_toolkit httpx

5. Inicie o OrangeCode:

python main.py

Configuração

Comando| Função
"/provider"| Selecionar provedor
"/key"| Configurar API Key
"/model"| Alterar modelo
"/status"| Ver configurações

Sistema de permissões

O OrangeCode possui três modos:

- "ask": solicita autorização.
- "auto": execução automática, mantendo confirmação para comandos identificados como destrutivos.
- "custom": permissões personalizadas.

Exemplo:

/permissions custom
/permissions set execute_command on

Comandos

Comando| Descrição
"/help"| Exibir ajuda
"/providers"| Listar provedores
"/project"| Mostrar projeto atual
"/permissions"| Configurar permissões
"/new"| Nova conversa
"/clear"| Limpar terminal
"/exit"| Sair

Estrutura do projeto

OrangeCode/
├── main.py
├── orangecode/
│   ├── agent/
│   ├── core/
│   ├── providers/
│   └── tools/
├── workspace/
└── .gitignore

Segurança

- As ferramentas de arquivos restringem o acesso ao workspace.
- Tokens são armazenados localmente.
- O arquivo de configuração utiliza permissão "0600".
- Operações podem exigir autorização.

Atenção: os comandos do terminal são executados com as permissões do ambiente Termux, não em uma sandbox isolada.

Autor

PauloDevz

"GitHub" (https://github.com/PauloDevz)

---

<p align="center">
  <strong>OrangeCode</strong> · AI Coding Agent
</p>
