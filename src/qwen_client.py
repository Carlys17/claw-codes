"""
Qwen / Alibaba Cloud API Client

Support for using Qwen models (via DashScope or Alibaba Cloud) as an alternative to Claude.

Environment Variables:
    QWEN_API_KEY: Your DashScope/API Key
    QWEN_BASE_URL: API endpoint (default: https://dashscope.aliyuncs.com/api/v1)
    QWEN_MODEL: Model to use (default: qwen-max)
    ALIBABA_CLOUD_ACCESS_KEY_ID: For Alibaba Cloud auth (optional)
    ALIBABA_CLOUD_ACCESS_KEY_SECRET: For Alibaba Cloud auth (optional)
"""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Any, Generator, Optional


# Default configuration
DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
DEFAULT_MODEL = "qwen-max"
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7


@dataclass
class QwenMessage:
    """A single message in the conversation."""
    role: str  # "user", "assistant", or "system"
    content: str


@dataclass
class QwenRequest:
    """Request payload for Qwen API."""
    model: str = field(default_factory=lambda: DEFAULT_MODEL)
    messages: list[QwenMessage] = field(default_factory=list)
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    stream: bool = False
    tools: Optional[list[dict[str, Any]]] = None
    tool_choice: Optional[str] = None

    def to_json(self) -> dict[str, Any]:
        """Convert request to JSON payload."""
        payload = {
            "model": self.model,
            "input": {
                "messages": [
                    {"role": msg.role, "content": msg.content}
                    for msg in self.messages
                ]
            },
            "parameters": {
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            }
        }
        if self.tools:
            payload["input"]["tools"] = self.tools
        if self.tool_choice:
            payload["parameters"]["tool_choice"] = self.tool_choice
        if self.stream:
            payload["parameters"]["stream"] = True
        return payload


@dataclass
class QwenResponse:
    """Response from Qwen API."""
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    finish_reason: str
    request_id: Optional[str] = None

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class QwenStreamChunk:
    """A chunk from streaming Qwen API response."""
    content: str
    finish_reason: Optional[str] = None


@dataclass
class AuthConfig:
    """Authentication configuration for Qwen API."""
    api_key: Optional[str] = None
    base_url: Optional[str] = None

    @classmethod
    def from_env(cls) -> 'AuthConfig':
        """Load auth config from environment variables."""
        api_key = os.environ.get('QWEN_API_KEY', '').strip()
        base_url = os.environ.get('QWEN_BASE_URL', DEFAULT_BASE_URL).strip()

        # Also check for Alibaba Cloud specific env vars
        if not api_key:
            # Try DashScope key
            api_key = os.environ.get('DASHSCOPE_API_KEY', '').strip()

        return cls(api_key=api_key or None, base_url=base_url)

    def is_configured(self) -> bool:
        """Check if API key is configured."""
        return self.api_key is not None and len(self.api_key) > 0


class QwenAPIError(Exception):
    """Error from Qwen API."""

    def __init__(self, message: str, status_code: Optional[int] = None, body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class QwenClient:
    """
    Client for Qwen / Alibaba Cloud DashScope API.

    Usage:
        client = QwenClient.from_env()
        response = client.send_message(request)

        # Or streaming:
        for chunk in client.stream_message(request):
            print(chunk.content, end='')
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self._default_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'X-DashScope-SSE': 'enable'
        }

    @classmethod
    def from_env(cls) -> 'QwenClient':
        """Create client from environment variables."""
        auth = AuthConfig.from_env()
        if not auth.is_configured():
            raise QwenAPIError(
                "Qwen API key not configured. Set QWEN_API_KEY or DASHSCOPE_API_KEY environment variable."
            )

        model = os.environ.get('QWEN_MODEL', DEFAULT_MODEL)
        return cls(
            api_key=auth.api_key,
            base_url=auth.base_url,
            model=model
        )

    def send_message(self, request: QwenRequest) -> QwenResponse:
        """Send a non-streaming message to Qwen API."""
        url = f"{self.base_url}/services/aigc/text-generation/generation"

        payload = request.to_json()
        data = json.dumps(payload).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=data,
            headers=self._default_headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode('utf-8'))
                return self._parse_response(result)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else None
            raise QwenAPIError(
                f"Qwen API error: {e.reason}",
                status_code=e.code,
                body=error_body
            )
        except urllib.error.URLError as e:
            raise QwenAPIError(f"Connection error: {e.reason}")

    def stream_message(
        self,
        request: QwenRequest
    ) -> Generator[QwenStreamChunk, None, None]:
        """Stream a message to Qwen API using SSE."""
        url = f"{self.base_url}/services/aigc/text-generation/generation"

        request.stream = True
        payload = request.to_json()
        data = json.dumps(payload).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=data,
            headers=self._default_headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                buffer = ""
                for line in response:
                    line = line.decode('utf-8').strip()
                    if line.startswith('data:'):
                        data_str = line[5:].strip()
                        if data_str == '[DONE]':
                            break
                        try:
                            chunk_data = json.loads(data_str)
                            chunk = self._parse_stream_chunk(chunk_data)
                            if chunk:
                                yield chunk
                        except json.JSONDecodeError:
                            continue
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else None
            raise QwenAPIError(
                f"Qwen API streaming error: {e.reason}",
                status_code=e.code,
                body=error_body
            )
        except urllib.error.URLError as e:
            raise QwenAPIError(f"Connection error: {e.reason}")

    def _parse_response(self, result: dict[str, Any]) -> QwenResponse:
        """Parse Qwen API response."""
        output = result.get('output', {})
        usage = result.get('usage', {})

        content = ""
        finish_reason = "stop"

        if 'choices' in output:
            choices = output['choices']
            if choices:
                content = choices[0].get('message', {}).get('content', '')
                finish_reason = choices[0].get('finish_reason', 'stop')
        elif 'text' in output:
            content = output['text']

        return QwenResponse(
            content=content,
            model=result.get('model', self.model),
            input_tokens=usage.get('input_tokens', 0),
            output_tokens=usage.get('output_tokens', 0),
            finish_reason=finish_reason,
            request_id=result.get('request_id')
        )

    def _parse_stream_chunk(self, chunk_data: dict[str, Any]) -> Optional[QwenStreamChunk]:
        """Parse a streaming chunk from Qwen API."""
        output = chunk_data.get('output', {})

        content = ""
        finish_reason = None

        if 'choices' in output:
            choices = output['choices']
            if choices:
                delta = choices[0].get('delta', {})
                content = delta.get('content', '')
                finish_reason = choices[0].get('finish_reason')
        elif 'text' in output:
            content = output['text']

        if not content and not finish_reason:
            return None

        return QwenStreamChunk(
            content=content,
            finish_reason=finish_reason
        )

    # Aliyun/OpenAI compatible method for easier integration
    def create_completion(
        self,
        messages: list[dict[str, str]],
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        stream: bool = False,
    ) -> QwenResponse | Generator[QwenStreamChunk, None, None]:
        """
        OpenAI-style completion method for easier migration.

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Max tokens to generate
            temperature: Sampling temperature
            stream: Whether to stream the response

        Returns:
            QwenResponse if not streaming, else Generator of QwenStreamChunk
        """
        request = QwenRequest(
            model=self.model,
            messages=[QwenMessage(**msg) for msg in messages],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream
        )

        if stream:
            return self.stream_message(request)
        return self.send_message(request)


def get_available_models() -> list[str]:
    """Get list of available Qwen models."""
    # Common Qwen models available via DashScope
    return [
        "qwen-turbo",
        "qwen-plus",
        "qwen-max",
        "qwen-max-longcontext",
        "qwen-7b-chat",
        "qwen-14b-chat",
        "qwen-72b-chat",
        "qwen1.5-7b-chat",
        "qwen1.5-14b-chat",
        "qwen1.5-32b-chat",
        "qwen1.5-72b-chat",
        "qwen2-7b-instruct",
        "qwen2-72b-instruct",
        "qwen2.5-7b-instruct",
        "qwen2.5-72b-instruct",
        "qwen-vl-max",
        "qwen-vl-plus",
        "qwen-audio-chat",
    ]
