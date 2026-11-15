from pathlib import Path
from orangecode.core.project import ProjectManager


IGNORED = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode"
}

MAX_FILE_SIZE = 1024 * 1024


class FileSystemTools:

    @staticmethod
    def list_files(path="."):
        directory = ProjectManager.resolve(path)

        if not directory.is_dir():
            raise ValueError("O caminho não é um diretório.")

        results = []

        for item in sorted(directory.iterdir()):
            if item.name in IGNORED:
                continue

            kind = "DIR" if item.is_dir() else "FILE"
            relative = item.relative_to(ProjectManager.get_root())

            results.append(f"[{kind}] {relative}")

        return "\n".join(results) or "Diretório vazio."

    @staticmethod
    def read_file(path):
        file = ProjectManager.resolve(path)

        if not file.is_file():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        if file.stat().st_size > MAX_FILE_SIZE:
            raise ValueError("Arquivo muito grande. Limite: 1 MB.")

        try:
            return file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise ValueError("O arquivo não é um texto UTF-8 válido.")

    @staticmethod
    def write_file(path, content):
        file = ProjectManager.resolve(path)

        if file.exists() and file.is_dir():
            raise IsADirectoryError("O caminho aponta para um diretório.")

        if len(content.encode("utf-8")) > MAX_FILE_SIZE:
            raise ValueError("Arquivo muito grande. Limite: 1 MB.")

        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")

        return f"Arquivo salvo: {file.relative_to(ProjectManager.get_root())}"

    @staticmethod
    def edit_file(path, old_text, new_text):
        file = ProjectManager.resolve(path)

        if not file.is_file():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        if file.stat().st_size > MAX_FILE_SIZE:
            raise ValueError("Arquivo muito grande. Limite: 1 MB.")

        content = file.read_text(encoding="utf-8")

        occurrences = content.count(old_text)

        if occurrences == 0:
            raise ValueError("O trecho original não foi encontrado.")

        if occurrences > 1:
            raise ValueError(
                f"O trecho aparece {occurrences} vezes. "
                "Forneça um trecho mais específico."
            )

        updated = content.replace(old_text, new_text, 1)
        file.write_text(updated, encoding="utf-8")

        return f"Arquivo atualizado: {path}"
