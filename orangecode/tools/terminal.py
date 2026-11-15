import subprocess

from orangecode.core.project import ProjectManager


class TerminalTools:

    @staticmethod
    def execute(command, approved=False):
        if not approved:
            raise PermissionError("Execução exige autorização.")

        if not isinstance(command, str) or not command.strip():
            raise ValueError("Comando vazio.")

        result = subprocess.run(
            command,
            shell=True,
            cwd=str(ProjectManager.get_root()),
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout
        errors = result.stderr

        response = f"Código de saída: {result.returncode}\n"

        if output:
            response += f"\nSAÍDA:\n{output}"

        if errors:
            response += f"\nERROS:\n{errors}"

        return response[:12000]
