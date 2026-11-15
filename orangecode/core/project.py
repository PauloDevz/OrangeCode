from pathlib import Path
from orangecode.core.config import Config


class ProjectManager:

    DEFAULT_DIR = Path.home() / "OrangeCode" / "workspace"

    @classmethod
    def get_root(cls):
        configured = Config.get("project_dir")

        root = Path(configured).expanduser() if configured else cls.DEFAULT_DIR
        root.mkdir(parents=True, exist_ok=True)

        return root.resolve()

    @classmethod
    def set_root(cls, path):
        root = Path(path).expanduser().resolve()

        if not root.exists() or not root.is_dir():
            raise ValueError("O diretório informado não existe.")

        Config.set("project_dir", str(root))
        return root

    @classmethod
    def resolve(cls, path):
        root = cls.get_root()
        target = (root / path).resolve()

        if not target.is_relative_to(root):
            raise PermissionError("Acesso fora do projeto não permitido.")

        return target
