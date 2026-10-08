import json
import os
import time
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"


@dataclass(frozen=True)
class NvidiaResponse:
    text: str
    latency_ms: int
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    raw: dict


class NvidiaProvider:
    """Minimal OpenAI-compatible NVIDIA hosted inference adapter."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY is required for the real benchmark")
        self.base_url = (base_url or os.getenv("NVIDIA_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.model = model or os.getenv("NVIDIA_MODEL") or DEFAULT_MODEL

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 4096,
        seed: int | None = None,
    ) -> NvidiaResponse:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
            "extra_body": {"chat_template_kwargs": {"enable_thinking": False}},
        }
        if seed is not None:
            payload["seed"] = seed

        request = Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        started = time.perf_counter()
        try:
            with urlopen(request, timeout=180) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"NVIDIA inference failed ({exc.code}): {body[:1000]}") from exc
        except URLError as exc:
            raise RuntimeError(f"NVIDIA inference connection failed: {exc.reason}") from exc
        latency_ms = int((time.perf_counter() - started) * 1000)

        choices = raw.get("choices") or []
        if not choices:
            raise RuntimeError(f"NVIDIA response contained no choices: {raw}")
        text = choices[0].get("message", {}).get("content") or ""
        usage = raw.get("usage") or {}
        return NvidiaResponse(
            text=text,
            latency_ms=latency_ms,
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
            total_tokens=usage.get("total_tokens"),
            raw=raw,
        )
