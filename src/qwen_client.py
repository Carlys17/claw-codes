"""
Qwen / Alibaba Cloud API Client

Support for using Qwen models via:
- DashScope (standard Qwen API)
- Alibaba Cloud Coding Plan (OpenAI/Anthropic compatible)

Environment Variables:
    QWEN_API_KEY: Your DashScope/API Key
    QWEN_BASE_URL: API endpoint (default: auto-detect based on URL pattern)
    QWEN_MODEL: Model to use (default: qwen-max)
    QWEN_API_MODE: API mode - "dashscope", "openai", or "anthropic" (default: auto)
    ALIBABA_CLOUD_ACCESS_KEY_ID: For Alibaba Cloud auth (optional)
    ALIBABA_CLOUD_ACCESS_KEY_SECRET: For Alibaba Cloud auth (optional)

Coding Plan Endpoints:
    OpenAI-compatible:  https://coding-intl.dashscope.aliyuncs.com/v1
    Anthropic-compatible: https://coding-intl.dashscope.aliyuncs.com/apps/anthropic
"""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generator, Optional


class ApiMode(Enum):
    """API protocol mode."""
    DASHSCOPE = "dashscope"  # Native Qwen API
    OPENAI = "openai"        # OpenAI-compatible (Coding Plan)
    ANTHROPIC = "anthropic"  # Anthropic-compatible (Coding Plan)


# Default configuration
DEFAULT_MODEL = "qwen-max"
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7

# Coding Plan endpoints
CODING_PLAN_OPENAI_URL = "https://coding-intl.dashscope.aliyuncs.com/v1"
CODING_PLAN_ANTHROPIC_URL = "https://coding-intl.dashscope.aliyuncs.com/apps/anthropic"
DASHSCOPE_URL = "https://dashscope.aliyuncs.com/api/v1"


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
    api_mode: ApiMode = ApiMode.DASHSCOPE

    @classmethod
    def from_env(cls) -> 'AuthConfig':
        """Load auth config from environment variables."""
        api_key = os.environ.get('QWEN_API_KEY', '').strip()

        # Also check for DashScope key
        if not api_key:
            api_key = os.environ.get('DASHSCOPE_API_KEY', '').strip()

        # Get base URL
        base_url = os.environ.get('QWEN_BASE_URL', '').strip()

        # Auto-detect API mode from URL or explicit setting
        api_mode_str = os.environ.get('QWEN_API_MODE', 'auto').lower()

        if not base_url:
            # Default based on API mode
            if api_mode_str == 'openai':
                base_url = CODING_PLAN_OPENAI_URL
            elif api_mode_str == 'anthropic':
                base_url = CODING_PLAN_ANTHROPIC_URL
            else:
                base_url = DASHSCOPE_URL

        # Auto-detect mode from URL if not explicitly set
        if api_mode_str == 'auto':
            if CODING_PLAN_OPENAI_URL.rstrip('/') in base_url:
                api_mode = ApiMode.OPENAI
            elif CODING_PLAN_ANTHROPIC_URL.rstrip('/') in base_url:
                api_mode = ApiMode.ANTHROPIC
            else:
                api_mode = ApiMode.DASHSCOPE
        else:
            api_mode = ApiMode(api_mode_str)

        return cls(api_key=api_key or None, base_url=base_url, api_mode=api_mode)

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

    Supports 3 API modes:
    1. DashScope (native Qwen API)
    2. OpenAI-compatible (Alibaba Cloud Coding Plan)
    3. Anthropic-compatible (Alibaba Cloud Coding Plan)

    Usage:
        # DashScope mode
        client = QwenClient.from_env()

        # Coding Plan OpenAI-compatible mode
        export QWEN_API_MODE=openai
        client = QwenClient.from_env()

        # Coding Plan Anthropic-compatible mode
        export QWEN_API_MODE=anthropic
        client = QwenClient.from_env()

        response = client.send_message(request)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DASHSCOPE_URL,
        model: str = DEFAULT_MODEL,
        api_mode: ApiMode = ApiMode.DASHSCOPE,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.api_mode = api_mode
        self._default_headers = self._build_headers()

    def _build_headers(self) -> dict[str, str]:
        """Build headers based on API mode."""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }
        if self.api_mode == ApiMode.DASHSCOPE:
            headers['X-DashScope-SSE'] = 'enable'
        return headers

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
            model=model,
            api_mode=auth.api_mode
        )

    def send_message(self, request: QwenRequest) -> QwenResponse:
        """Send a non-streaming message to Qwen API."""
        if self.api_mode == ApiMode.OPENAI:
            return self._send_openai_mode(request)
        elif self.api_mode == ApiMode.ANTHROPIC:
            return self._send_anthropic_mode(request)
        else:
            return self._send_dashscope_mode(request)

    def _send_dashscope_mode(self, request: QwenRequest) -> QwenResponse:
        """Send request using DashScope native API."""
        url = f"{self.base_url}/services/aigc/text-generation/generation"
        return self._do_request(url, request)

    def _send_openai_mode(self, request: QwenRequest) -> QwenResponse:
        """Send request using OpenAI-compatible API (Coding Plan)."""
        url = f"{self.base_url}/chat/completions"
        return self._do_request(url, request)

    def _send_anthropic_mode(self, request: QwenRequest) -> QwenResponse:
        """Send request using Anthropic-compatible API (Coding Plan)."""
        url = f"{self.base_url}/v1/messages"
        return self._do_request(url, request)

    def _do_request(self, url: str, request: QwenRequest) -> QwenResponse:
        """Execute HTTP request and parse response."""
        payload = self._build_payload(request)
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

    def _build_payload(self, request: QwenRequest) -> dict[str, Any]:
        """Build payload based on API mode."""
        if self.api_mode == ApiMode.OPENAI:
            # OpenAI-compatible format
            return {
                "model": self.model,
                "messages": [
                    {"role": msg.role, "content": msg.content}
                    for msg in request.messages
                ],
                "max_tokens": request.max_tokens,
                "temperature": request.temperature,
                "stream": request.stream,
            }
        elif self.api_mode == ApiMode.ANTHROPIC:
            # Anthropic-compatible format
            messages = []
            system_prompt = None
            for msg in request.messages:
                if msg.role == "system":
                    system_prompt = msg.content
                else:
                    messages.append({"role": msg.role, "content": msg.content})
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": request.max_tokens,
            }
            if system_prompt:
                payload["system"] = system_prompt
            return payload
        else:
            # DashScope native format
            return request.to_json()

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
