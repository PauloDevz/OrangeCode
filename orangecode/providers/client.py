
import httpx
import json

from orangecode.core.config import Config
from orangecode.providers.registry import PROVIDERS


class ProviderError(Exception):
    pass


class ProviderClient:

    def __init__(self):
        self.provider = Config.get("provider") or "groq"
        self.info = PROVIDERS.get(self.provider)

        if not self.info:
            raise ProviderError("Provedor não encontrado.")

        self.model = Config.get("model") or self.info["model"]
        self.token = Config.get_key(self.provider)

        if self.provider != "ollama" and not self.token:
            raise ProviderError("Configure o token usando /key.")

    def generate_with_tools(self, messages, tools, system_prompt):
        if self.info["type"] == "anthropic":
            return self._anthropic(messages, tools, system_prompt)

        return self._openai(messages, tools, system_prompt)

    def _openai(self, messages, tools, system_prompt):
        url = self.info["base_url"].rstrip("/") + "/chat/completions"

        headers = {"Content-Type": "application/json"}

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        strict_prompt = (
            "\n\nREGRAS OBRIGATÓRIAS PARA CHAMADAS DE FERRAMENTAS:\n"
            "- Os argumentos devem ser JSON válido e seguir exatamente o schema.\n"
            "- Nunca inclua comentários dentro dos argumentos.\n"
            "- Para execute_command, use comandos curtos em uma única linha.\n"
            "- Não use heredoc, incluindo <<'PY' ou <<EOF.\n"
            "- Não coloque scripts multilinha dentro de comandos.\n"
            "- Para testes Python simples, prefira python -c com uma única linha.\n"
            "- Não invente ferramentas ou parâmetros.\n"
            "- Se uma tarefa exigir várias operações, divida em chamadas separadas.\n"
        )

        attempts = 3
        last_error = None

        for attempt in range(attempts):
            active_prompt = system_prompt

            if attempt > 0:
                active_prompt += strict_prompt
                active_prompt += (
                    "\nA chamada anterior foi rejeitada por argumentos "
                    "inválidos. Gere uma chamada nova, com JSON estritamente válido."
                )

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": active_prompt},
                    *messages
                ],
                "tools": tools,
                "tool_choice": "auto",
                "temperature": 0
            }

            try:
                with httpx.Client(timeout=180) as client:
                    response = client.post(
                        url,
                        headers=headers,
                        json=payload
                    )

                if response.status_code >= 400:
                    try:
                        error_data = response.json()
                    except ValueError:
                        error_data = {}

                    error_info = error_data.get("error", {})
                    error_code = error_info.get("code", "")
                    error_message = error_info.get(
                        "message",
                        response.text[:1500]
                    )

                    if (
                        error_code == "tool_use_failed"
                        or "Failed to parse tool call arguments" in error_message
                    ):
                        last_error = error_message

                        if attempt < attempts - 1:
                            continue

                        raise ProviderError(
                            "O modelo gerou argumentos de ferramenta "
                            "inválidos após 3 tentativas. "
                            "Tente novamente com uma instrução mais simples. "
                            f"Detalhes: {error_message[:700]}"
                        )

                    raise ProviderError(
                        f"HTTP {response.status_code}: {error_message}"
                    )

                data = response.json()
                message = data["choices"][0]["message"]

                calls = []

                for item in message.get("tool_calls", []):
                    function = item.get("function", {})

                    calls.append({
                        "id": item.get("id", ""),
                        "name": function.get("name", ""),
                        "arguments": function.get("arguments", {})
                    })

                return {
                    "text": message.get("content") or "",
                    "tool_calls": calls,
                    "assistant_message": message,
                    "provider_type": "openai"
                }

            except ProviderError:
                raise
            except httpx.TimeoutException:
                raise ProviderError("Tempo limite da conexão excedido.")
            except httpx.RequestError as error:
                raise ProviderError(f"Falha de conexão: {error}")
            except (KeyError, IndexError, ValueError, TypeError) as error:
                raise ProviderError(
                    f"Resposta inválida do provedor: {error}"
                )

        raise ProviderError(str(last_error or "Falha ao gerar resposta."))

    def _anthropic(self, messages, tools, system_prompt):
        url = self.info["base_url"].rstrip("/") + "/v1/messages"

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.token,
            "anthropic-version": "2023-06-01"
        }

        anthropic_tools = []

        for tool in tools:
            function = tool["function"]

            anthropic_tools.append({
                "name": function["name"],
                "description": function["description"],
                "input_schema": function["parameters"]
            })

        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": messages,
            "tools": anthropic_tools
        }

        try:
            with httpx.Client(timeout=180) as client:
                response = client.post(
                    url,
                    headers=headers,
                    json=payload
                )

            if response.status_code >= 400:
                raise ProviderError(
                    f"HTTP {response.status_code}: {response.text[:1500]}"
                )

            data = response.json()
            blocks = data.get("content", [])
            calls = []

            for block in blocks:
                if block.get("type") == "tool_use":
                    calls.append({
                        "id": block["id"],
                        "name": block["name"],
                        "arguments": block.get("input", {})
                    })

            return {
                "text": "".join(
                    block.get("text", "")
                    for block in blocks
                    if block.get("type") == "text"
                ),
                "tool_calls": calls,
                "assistant_message": blocks,
                "provider_type": "anthropic"
            }

        except ProviderError:
            raise
        except httpx.TimeoutException:
            raise ProviderError("Tempo limite da conexão excedido.")
        except httpx.RequestError as error:
            raise ProviderError(f"Falha de conexão: {error}")
        except (KeyError, ValueError, TypeError) as error:
            raise ProviderError(f"Resposta inválida do provedor: {error}")

