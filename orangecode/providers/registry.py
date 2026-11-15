PROVIDERS = {
    "openai": {
        "model": "gpt-4.1",
        "base_url": "https://api.openai.com/v1",
        "type": "openai"
    },
    "groq": {
        "model": "openai/gpt-oss-120b",
        "base_url": "https://api.groq.com/openai/v1",
        "type": "openai"
    },
    "gemini": {
        "model": "gemini-2.5-flash",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "type": "openai"
    },
    "deepseek": {
        "model": "deepseek-chat",
        "base_url": "https://api.deepseek.com/v1",
        "type": "openai"
    },
    "openrouter": {
        "model": "openai/gpt-4.1-mini",
        "base_url": "https://openrouter.ai/api/v1",
        "type": "openai"
    },
    "anthropic": {
        "model": "claude-sonnet-4-5",
        "base_url": "https://api.anthropic.com",
        "type": "anthropic"
    },
    "ollama": {
        "model": "qwen2.5-coder:7b",
        "base_url": "http://localhost:11434/v1",
        "type": "openai"
    }
}
