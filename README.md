<h1 align="center">🟠 OrangeCode</h1>

<p align="center">
  <strong>Agente de programação com IA, direto no seu terminal.</strong><br>
  Analisa, cria e edita código, executa comandos e trabalha nos arquivos do seu projeto.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Plataforma-Termux%20%7C%20Linux-D97735?style=flat-square" alt="Termux | Linux">
  <img src="https://img.shields.io/badge/Status-Em%20desenvolvimento-orange?style=flat-square" alt="Em desenvolvimento">
</p>

<p align="center">
  <a href="#-funcionalidades">Funcionalidades</a> ·
  <a href="#-instalação">Instalação</a> ·
  <a href="#-primeiros-passos">Primeiros passos</a> ·
  <a href="#-provedores-suportados">Provedores</a> ·
  <a href="#-sistema-de-permissões">Permissões</a> ·
  <a href="#-comandos">Comandos</a> ·
  <a href="#-segurança">Segurança</a>
</p>

---

## 📖 Sobre

O **OrangeCode** é um agente de programação desenvolvido em Python que roda no terminal. Você conversa com ele em linguagem natural e ele lê, cria e edita arquivos, além de executar comandos, sempre dentro do workspace do seu projeto e de acordo com as permissões que você definir.

Funciona com vários provedores de IA, inclusive modelos locais via Ollama, e foi pensado para rodar bem no **Termux** (Android) e em **Linux**.

## ✨ Funcionalidades

- 🔌 **Múltiplos provedores de IA** — troque de provedor e modelo quando quiser.
- 📂 **Leitura e gerenciamento de arquivos** dentro do workspace.
- ✍️ **Criação e edição de código** diretamente nos arquivos do projeto.
- 💻 **Execução de comandos** no terminal.
- 🔐 **Sistema de permissões configurável** (`ask`, `auto` e `custom`).
- 💾 **Configurações persistentes** entre sessões.
- 🕘 **Histórico de conversação**.

## 🤖 Provedores suportados

| Provedor | Modelo padrão |
| --- | --- |
| OpenAI | `gpt-4.1` |
| Groq | `openai/gpt-oss-120b` |
| Gemini | `gemini-2.5-flash` |
| DeepSeek | `deepseek-chat` |
| OpenRouter | `openai/gpt-4.1-mini` |
| Anthropic | `claude-sonnet-4-5` |
| Ollama | `qwen2.5-coder:7b` |

> Você pode trocar o modelo de qualquer provedor com o comando `/model`.

## 📦 Instalação

### Requisitos

- Python **3.10** ou superior
- Git
- Uma API Key do provedor escolhido (não é necessária para o Ollama)

### Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install python git -y
```

### Linux

Instale `python3`, `pip` e `git` pelo gerenciador de pacotes da sua distribuição.

### Baixando o OrangeCode

```bash
git clone https://github.com/PauloDevz/OrangeCode.git
cd OrangeCode
pip install rich prompt_toolkit httpx
```

## 🚀 Primeiros passos

Inicie o OrangeCode:

```bash
python main.py
```

Depois, dentro dele, configure o provedor e a chave:

```text
/provider      # escolha o provedor de IA
/key           # informe sua API Key
/model         # (opcional) altere o modelo
/status        # confira as configurações atuais
```

Pronto! Agora é só descrever o que você quer, por exemplo:

```text
> Crie um script em Python que renomeie todos os arquivos .txt da pasta
```

## ⚙️ Configuração

| Comando | Função |
| --- | --- |
| `/provider` | Selecionar provedor |
| `/key` | Configurar API Key |
| `/model` | Alterar modelo |
| `/status` | Ver configurações |

As configurações ficam salvas localmente e são carregadas automaticamente nas próximas execuções.

## 🔐 Sistema de permissões

O OrangeCode possui três modos de permissão:

| Modo | Comportamento |
| --- | --- |
| `ask` | Solicita autorização antes de cada ação. |
| `auto` | Executa automaticamente, mantendo confirmação para comandos identificados como destrutivos. |
| `custom` | Permissões personalizadas por ferramenta. |

**Exemplo de modo personalizado:**

```text
/permissions custom
/permissions set execute_command on
```

## 🧭 Comandos

| Comando | Descrição |
| --- | --- |
| `/help` | Exibir ajuda |
| `/providers` | Listar provedores |
| `/project` | Mostrar projeto atual |
| `/permissions` | Configurar permissões |
| `/new` | Nova conversa |
| `/clear` | Limpar terminal |
| `/exit` | Sair |

## 🗂️ Estrutura do projeto

```text
OrangeCode/
├── main.py              # ponto de entrada
├── orangecode/
│   ├── agent/           # lógica do agente
│   ├── core/            # núcleo e configurações
│   ├── providers/       # integração com os provedores de IA
│   └── tools/           # ferramentas (arquivos, comandos etc.)
├── workspace/           # área de trabalho dos seus projetos
└── .gitignore
```

## 🛡️ Segurança

- As ferramentas de arquivos **restringem o acesso ao workspace**.
- Tokens são armazenados **localmente**.
- O arquivo de configuração utiliza permissão `0600`.
- Operações podem exigir **autorização** do usuário.

> [!WARNING]
> Os comandos do terminal são executados com as permissões do ambiente (por exemplo, o Termux), **não em uma sandbox isolada**. Prefira o modo `ask` ao testar o agente em projetos importantes e revise os comandos antes de autorizar.

## 🤝 Contribuindo

Contribuições são bem-vindas! Para sugerir melhorias ou reportar bugs:

1. Abra uma [issue](https://github.com/PauloDevz/OrangeCode/issues) descrevendo o problema ou a ideia.
2. Para enviar código, faça um fork, crie uma branch e abra um Pull Request.

## 👤 Autor

**PauloDevz** — [GitHub](https://github.com/PauloDevz)

---

<p align="center">
  <strong>OrangeCode</strong> · AI Coding Agent para terminal
</p>

