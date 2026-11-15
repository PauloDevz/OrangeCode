
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

from orangecode.core.config import Config
from orangecode.core.project import ProjectManager
from orangecode.providers.registry import PROVIDERS
from orangecode.providers.client import ProviderError
from orangecode.agent.runner import AgentRunner


console = Console()
session = PromptSession()
history = []

style = Style.from_dict({
    "prompt": "#D97735 bold",
})

PERMISSION_LABELS = {
    "create_file": "Criar arquivos",
    "overwrite_file": "Substituir arquivos",
    "edit_file": "Editar arquivos",
    "execute_command": "Executar comandos"
}


def banner():
    console.clear()

    logo = Text()
    logo.append("✳ ", style="bold #D97735")
    logo.append("OrangeCode", style="bold white")
    logo.append("\nAI CODING AGENT", style="#D97735")

    console.print(
        Panel(
            logo,
            border_style="#D97735",
            padding=(1, 3),
            expand=False
        )
    )

    console.print(
        "[dim]Seu agente de programação no terminal.[/dim]\n"
    )


def show_providers():
    table = Table(
        title="PROVEDORES DISPONÍVEIS",
        border_style="#D97735"
    )

    table.add_column("Provedor")
    table.add_column("Modelo")
    table.add_column("Status")

    for name, info in PROVIDERS.items():
        configured = bool(Config.get_key(name)) or name == "ollama"
        status = "Configurado" if configured else "Sem token"

        table.add_row(name, info["model"], status)

    console.print(table)


def select_provider():
    show_providers()

    name = console.input(
        "\n[#D97735]Provedor:[/] "
    ).strip().lower()

    if name not in PROVIDERS:
        console.print("[red]Provedor inválido.[/]")
        return

    Config.set("provider", name)
    Config.set("model", "")
    history.clear()

    console.print(f"[green]Provedor selecionado: {name}[/]")


def configure_key():
    provider = Config.get("provider")

    if provider == "ollama":
        console.print("[yellow]O Ollama normalmente não exige token.[/]")
        return

    if provider not in PROVIDERS:
        console.print("[red]Selecione um provedor primeiro.[/]")
        return

    token = session.prompt(
        f"Token de {provider}: ",
        is_password=True
    ).strip()

    if not token:
        console.print("[yellow]Token vazio.[/]")
        return

    Config.set_key(provider, token)
    console.print("[green]Token salvo localmente.[/]")


def select_model():
    provider = Config.get("provider")

    if provider not in PROVIDERS:
        console.print("[red]Selecione um provedor primeiro.[/]")
        return

    current = Config.get("model") or PROVIDERS[provider]["model"]

    console.print(f"[dim]Modelo atual: {current}[/]")

    model = console.input(
        "\n[#D97735]Novo modelo:[/] "
    ).strip()

    if model:
        Config.set("model", model)
        history.clear()
        console.print("[green]Modelo atualizado.[/]")


def show_permissions():
    mode = Config.get_permission_mode()

    mode_names = {
        "ask": "Perguntar sempre",
        "auto": "Automático",
        "custom": "Personalizado"
    }

    table = Table(
        title="PERMISSÕES DO OrangeCode",
        border_style="#D97735"
    )

    table.add_column("Operação")
    table.add_column("Exigir autorização")

    for key, label in PERMISSION_LABELS.items():
        enabled = Config.get_permission(key)

        if mode == "ask":
            status = "[green]Sim[/]"
        elif mode == "auto":
            status = "[yellow]Não[/]"
        else:
            status = "[green]Sim[/]" if enabled else "[yellow]Não[/]"

        table.add_row(label, status)

    console.print(
        Panel(
            f"Modo atual: [bold #D97735]{mode_names.get(mode, mode)}[/]",
            border_style="#D97735"
        )
    )

    console.print(table)

    console.print(
        "[dim]Comandos: /permissions ask | auto | custom[/]"
    )


def permissions_menu(command=""):
    parts = command.strip().lower().split()

    if len(parts) == 1:
        show_permissions()
        return

    mode = parts[1]

    if mode in ("ask", "auto", "custom") and len(parts) == 2:
        Config.set_permission_mode(mode)

        names = {
            "ask": "Perguntar sempre",
            "auto": "Automático",
            "custom": "Personalizado"
        }

        console.print(
            f"[green]Modo de permissões alterado: {names[mode]}[/]"
        )

        show_permissions()
        return

    if len(parts) == 4 and parts[1] == "set":
        permission = parts[2]
        value = parts[3]

        if permission not in PERMISSION_LABELS:
            console.print("[red]Permissão desconhecida.[/]")
            console.print(
                "Opções: " + ", ".join(PERMISSION_LABELS.keys())
            )
            return

        if value not in ("on", "off"):
            console.print("[red]Use on ou off.[/]")
            return

        Config.set_permission(
            permission,
            value == "on"
        )

        Config.set_permission_mode("custom")

        console.print(
            f"[green]{PERMISSION_LABELS[permission]}: "
            f"{'autorização obrigatória' if value == 'on' else 'sem pergunta'}[/]"
        )

        show_permissions()
        return

    console.print("""
[#D97735]CONFIGURAÇÃO DE PERMISSÕES[/]

/permissions ask
/permissions auto
/permissions custom

/permissions set create_file on
/permissions set create_file off

/permissions set overwrite_file on
/permissions set overwrite_file off

/permissions set edit_file on
/permissions set edit_file off

/permissions set execute_command on
/permissions set execute_command off
""")


def show_status():
    provider = Config.get("provider")
    model = Config.get("model") or PROVIDERS[provider]["model"]

    mode_names = {
        "ask": "Perguntar sempre",
        "auto": "Automático",
        "custom": "Personalizado"
    }

    mode = Config.get_permission_mode()

    console.print(
        Panel(
            f"Provedor: {provider}\n"
            f"Modelo: {model}\n"
            f"Token: {'Configurado' if Config.get_key(provider) or provider == 'ollama' else 'Ausente'}\n"
            f"Projeto: {ProjectManager.get_root()}\n"
            f"Permissões: {mode_names.get(mode, mode)}",
            title="CONFIGURAÇÃO",
            border_style="#D97735"
        )
    )


def help_menu():
    console.print("""
[#D97735]COMANDOS[/]

  /help          Ajuda
  /providers     Listar provedores
  /provider      Trocar provedor
  /key           Configurar token
  /model         Trocar modelo
  /status        Configuração
  /project       Mostrar projeto atual
  /project caminho   Trocar projeto

  /permissions       Configurar permissões
  /permissions ask   Perguntar sempre
  /permissions auto  Modo automático
  /permissions custom  Modo personalizado

  /new           Nova conversa
  /clear         Limpar terminal
  /exit          Sair
""")


def chat(message):
    runner = AgentRunner(console)

    try:
        runner.run(message, history)

    except ProviderError as error:
        console.print(f"\n[red]Erro do provedor: {error}[/]")

        if history and history[-1].get("role") == "user":
            history.pop()

    except KeyboardInterrupt:
        console.print("\n[yellow]Operação interrompida.[/]")

    except Exception as error:
        console.print(f"\n[red]Erro: {error}[/]")


def main():
    Config.load()
    banner()

    console.print("[green]OrangeCode inicializado.[/]")
    console.print("[dim]Digite /help para ver os comandos.[/]\n")

    while True:
        try:
            command = session.prompt(
                [("class:prompt", "❯ ")],
                style=style
            ).strip()

            if not command:
                continue

            if command == "/exit":
                console.print("[#D97735]Até logo![/]")
                break

            elif command == "/help":
                help_menu()

            elif command == "/providers":
                show_providers()

            elif command == "/provider":
                select_provider()

            elif command == "/key":
                configure_key()

            elif command == "/model":
                select_model()

            elif command == "/status":
                show_status()

            elif command == "/permissions" or command.startswith("/permissions "):
                permissions_menu(command)

            elif command == "/project":
                console.print(str(ProjectManager.get_root()))

            elif command.startswith("/project "):
                path = command[len("/project "):].strip()

                try:
                    root = ProjectManager.set_root(path)
                    history.clear()
                    console.print(f"[green]Projeto definido: {root}[/]")
                except Exception as error:
                    console.print(f"[red]{error}[/]")

            elif command == "/new":
                history.clear()
                console.print("[green]Nova conversa iniciada.[/]")

            elif command == "/clear":
                banner()

            elif command.startswith("/"):
                console.print("[yellow]Comando desconhecido.[/]")

            else:
                chat(command)

        except KeyboardInterrupt:
            console.print("\n[dim]Use /exit para sair.[/]")

        except EOFError:
            break


if __name__ == "__main__":
    main()

