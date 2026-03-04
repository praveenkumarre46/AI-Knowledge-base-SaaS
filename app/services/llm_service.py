import os
import httpx


def call_ollama(prompt: str, model: str = "llama2") -> str:
    """Call a local Ollama HTTP API to generate a completion.

    This tries POST http://localhost:11434/api/generate with a simple JSON
    payload. If the call fails, returns an informative fallback message.
    """
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": int(os.getenv("OLLAMA_MAX_TOKENS", 512)),
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()

            # Try to parse JSON result if available
            try:
                data = resp.json()
                # Ollama may return structured json or plain text; try common keys
                for key in ("text", "response", "content", "generated_text"):
                    if key in data:
                        return data[key]

                # sometimes the model stream is under 'result' or 'outputs'
                if "result" in data:
                    return str(data["result"])[:4000]

                return str(data)
            except Exception:
                return resp.text
    except Exception as e:
        return f"[LLM call failed: {e}]"
