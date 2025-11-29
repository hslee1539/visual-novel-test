"""`fastmcp` 호환을 위한 최소 구현.

공식 패키지를 설치할 수 없는 환경에서도 동일한 인터페이스로 도구를
등록하고 테스트할 수 있도록 아주 얇은 래퍼를 제공한다.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass
class RegisteredTool:
    """등록된 MCP 도구 정보를 담는다."""

    name: str
    description: str
    func: Callable[..., Any]

    def __call__(self, *args: Any, **kwargs: Any) -> Any:  # pragma: no cover - 간단 위임
        return self.func(*args, **kwargs)


class FastMCP:
    """도구 등록용 최소 MCP 래퍼."""

    def __init__(self, name: str, description: str | None = None):
        self.name = name
        self.description = description or ""
        self._tools: Dict[str, RegisteredTool] = {}

    def tool(self, name: str | None = None, description: str | None = None):
        """데코레이터 형태로 도구를 등록한다."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            tool_name = name or func.__name__
            tool_desc = (description or func.__doc__ or "").strip()
            self._tools[tool_name] = RegisteredTool(tool_name, tool_desc, func)
            return func

        return decorator

    @property
    def tools(self) -> Dict[str, RegisteredTool]:
        return self._tools

    def get_tool(self, name: str) -> RegisteredTool:
        return self._tools[name]

    def run(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover - 실행 경로 미사용
        raise RuntimeError(
            "이 저장소에는 네트워크 제약으로 인해 실제 MCP 런타임이 포함되어 있지 않습니다."
        )

