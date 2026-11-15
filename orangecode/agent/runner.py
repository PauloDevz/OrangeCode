
import json
import re
import shlex
from pathlib import Path

from orangecode.providers.client import ProviderClient
from orangecode.agent.tools import TOOLS
from orangecode.tools.filesystem import FileSystemTools
from orangecode.tools.terminal import TerminalTools
from orangecode.core.config import Config
from orangecode.core.project import ProjectManager


SYSTEM_PROMPT = """
Você é OrangeCode, um agente profissional de programação.

Você trabalha diretamente no projeto autorizado pelo usuário.

REGRAS GERAIS:
- Analise os arquivos antes de modificá-los.
- Não invente resultados de execução.
- Utilize as ferramentas disponíveis para trabalhar com arquivos.
- Faça alterações pequenas e coerentes.
- Preserve funcionalidades existentes.
- Execute testes quando necessário.
- Corrija erros encontrados.
- Não substitua arquivos sem necessidade.
- Explique brevemente o que foi realizado.
- Não diga que terminou se ainda não verificou o trabalho.

REGRAS DE FERRAMENTAS:
- Gere argumentos JSON válidos e compatíveis com os schemas.
- Não inclua comentários nos argumentos.
- Não utilize heredoc ou comandos multilinha.
- Prefira comandos curtos e objetivos.
- Não invente ferramentas ou parâmetros.
- Divida tarefas complexas em operações menores.

Para tarefas complexas, trabalhe em etapas e verifique cada etapa.
"""


class AgentRunner:

    def __init__(self, console):
        self.console = console

    def approve(self, title, details):
        self.console.print()
        self.console.print("[bold #D97735]AUTORIZAÇÃO NECESSÁRIA[/]")
        self.console.print(f"[bold]{title}[/]")
        self.console.print(f"[dim]{details}[/]")

        answer = self.console.input(
            "\n[#D97735]Autorizar? (s/n): [/]"
        ).strip().lower()

        return answer == "s"

    def request_permission(self, operation, title, details):
        if not Config.requires_approval(operation):
            return True

        return self.approve(title, details)

    def is_destructive_command(self, command):
        patterns = [
            r"(^|[;&|]\s*)rm(?:\s|$)",
            r"(^|[;&|]\s*)rmdir(?:\s|$)",
            r"(^|[;&|]\s*)unlink(?:\s|$)",
            r"(^|[;&|]\s*)shred(?:\s|$)",
            r"(^|[;&|]\s*)mkfs(?:\s|$)",
            r"(^|[;&|]\s*)dd(?:\s|$)",
            r"(^|[;&|]\s*)wipefs(?:\s|$)",
            r"(^|[;&|]\s*)format(?:\s|$)",
            r"git\s+reset\s+--hard",
            r"git\s+clean\s+.*-[a-zA-Z]*f",
            r"find\s+.*-delete",
            r">\s*/(?:data|system|storage)(?:/|\s|$)",
            r"\b(?:shutdown|reboot|poweroff)\b"
        ]

        return any(
            re.search(pattern, command, re.IGNORECASE)
            for pattern in patterns
        )

    def parse_arguments(self, arguments):
        if isinstance(arguments, dict):
            return arguments

        if not isinstance(arguments, str):
            raise ValueError("Argumentos da ferramenta inválidos.")

        content = arguments.strip()

        if content.startswith("```"):
            content = re.sub(
                r"^```(?:json)?\s*|\s*```$",
                "",
                content,
                flags=re.IGNORECASE
            ).strip()

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"JSON inválido nos argumentos: {error.msg}"
            )

        if not isinstance(parsed, dict):
            raise ValueError("Os argumentos precisam ser um objeto JSON.")

        return parsed

    def required(self, arguments, fields):
        for field in fields:
            if field not in arguments:
                raise ValueError(
                    f"Parâmetro obrigatório ausente: {field}"
                )

            if not isinstance(arguments[field], str):
                raise ValueError(
                    f"O parâmetro {field} precisa ser texto."
                )

    def execute_tool(self, name, arguments):
        arguments = self.parse_arguments(arguments)

        if name == "list_files":
            self.required(arguments, ["path"])
            return FileSystemTools.list_files(arguments["path"])

        if name == "read_file":
            self.required(arguments, ["path"])
            return FileSystemTools.read_file(arguments["path"])

        if name == "write_file":
            self.required(arguments, ["path", "content"])

            path = arguments["path"]
            target = ProjectManager.resolve(path)
            exists = target.exists()

            operation = "overwrite_file" if exists else "create_file"

            title = (
                "Substituir arquivo existente"
                if exists
                else "Criar arquivo"
            )

            if not self.request_permission(
                operation,
                title,
                path
            ):
                return "Operação recusada pelo usuário."

            return FileSystemTools.write_file(
                path,
                arguments["content"]
            )

        if name == "edit_file":
            self.required(
                arguments,
                ["path", "old_text", "new_text"]
            )

            path = arguments["path"]

            if not self.request_permission(
                "edit_file",
                "Modificar arquivo",
                path
            ):
                return "Operação recusada pelo usuário."

            return FileSystemTools.edit_file(
                path,
                arguments["old_text"],
                arguments["new_text"]
            )

        if name == "execute_command":
            self.required(arguments, ["command"])

            command = arguments["command"].strip()

            if not command:
                raise ValueError("O comando não pode estar vazio.")

            destructive = self.is_destructive_command(command)

            if destructive:
                allowed = self.approve(
                    "COMANDO POTENCIALMENTE DESTRUTIVO",
                    command
                )
            else:
                allowed = self.request_permission(
                    "execute_command",
                    "Executar comando no terminal",
                    command
                )

            if not allowed:
                return "Execução recusada pelo usuário."

            return TerminalTools.execute(
                command,
                approved=True
            )

        return f"Ferramenta desconhecida: {name}"

    def run_tool(self, call):
        name = call.get("name", "desconhecida")

        try:
            output = self.execute_tool(
                name,
                call.get("arguments", {})
            )
        except Exception as error:
            output = f"Erro na ferramenta {name}: {error}"

        self.console.print(f"[dim]Ferramenta: {name}[/]")

        return str(output)

    def run(self, user_message, history):
        client = ProviderClient()

        history.append({
            "role": "user",
            "content": user_message
        })

        max_steps = 8

        for step in range(max_steps):
            self.console.print(
                f"\n[dim]Etapa do agente: {step + 1}/{max_steps}[/]"
            )

            result = client.generate_with_tools(
                history,
                TOOLS,
                SYSTEM_PROMPT
            )

            if result["text"]:
                self.console.print(
                    "\n[bold #D97735]✳ OrangeCode[/]"
                )
                self.console.print(result["text"])

            calls = result["tool_calls"]

            if not calls:
                history.append({
                    "role": "assistant",
                    "content": result["text"]
                })
                return

            if result["provider_type"] == "anthropic":
                history.append({
                    "role": "assistant",
                    "content": result["assistant_message"]
                })

                tool_results = []

                for call in calls:
                    output = self.run_tool(call)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": call["id"],
                        "content": output
                    })

                history.append({
                    "role": "user",
                    "content": tool_results
                })

            else:
                history.append(result["assistant_message"])

                for call in calls:
                    output = self.run_tool(call)

                    history.append({
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "content": output
                    })

        self.console.print(
            "\n[yellow]Limite de etapas atingido. "
            "Envie outra mensagem para continuar.[/]"
        )

