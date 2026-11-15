
import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "orangecode"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_PERMISSIONS = {
    "mode": "ask",
    "create_file": True,
    "overwrite_file": True,
    "edit_file": True,
    "execute_command": True
}


class Config:
    data = {
        "provider": "groq",
        "model": "",
        "keys": {},
        "permissions": DEFAULT_PERMISSIONS.copy()
    }

    @classmethod
    def load(cls):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        if CONFIG_FILE.exists():
            try:
                saved = json.loads(CONFIG_FILE.read_text())

                if isinstance(saved, dict):
                    cls.data.update(saved)

                saved_permissions = cls.data.get("permissions", {})

                if not isinstance(saved_permissions, dict):
                    saved_permissions = {}

                cls.data["permissions"] = {
                    **DEFAULT_PERMISSIONS,
                    **saved_permissions
                }

            except (json.JSONDecodeError, OSError):
                pass

    @classmethod
    def save(cls):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(
            json.dumps(cls.data, indent=4, ensure_ascii=False)
        )
        os.chmod(CONFIG_FILE, 0o600)

    @classmethod
    def get(cls, name):
        return cls.data.get(name)

    @classmethod
    def set(cls, name, value):
        cls.data[name] = value
        cls.save()

    @classmethod
    def get_key(cls, provider):
        if not provider:
            return None
        return cls.data.get("keys", {}).get(provider)

    @classmethod
    def set_key(cls, provider, token):
        cls.data.setdefault("keys", {})[provider] = token
        cls.save()

    @classmethod
    def get_permission(cls, name):
        permissions = cls.data.setdefault(
            "permissions",
            DEFAULT_PERMISSIONS.copy()
        )

        return permissions.get(name, True)

    @classmethod
    def set_permission(cls, name, value):
        if name not in DEFAULT_PERMISSIONS:
            raise ValueError("Permissão desconhecida.")

        permissions = cls.data.setdefault(
            "permissions",
            DEFAULT_PERMISSIONS.copy()
        )

        permissions[name] = bool(value)
        cls.save()

    @classmethod
    def set_permission_mode(cls, mode):
        if mode not in ("ask", "auto", "custom"):
            raise ValueError("Modo de permissão inválido.")

        cls.data.setdefault(
            "permissions",
            DEFAULT_PERMISSIONS.copy()
        )["mode"] = mode

        cls.save()

    @classmethod
    def get_permission_mode(cls):
        return cls.data.get("permissions", {}).get("mode", "ask")

    @classmethod
    def requires_approval(cls, operation):
        mode = cls.get_permission_mode()

        if mode == "ask":
            return True

        if mode == "auto":
            return False

        if mode == "custom":
            return cls.get_permission(operation)

        return True

