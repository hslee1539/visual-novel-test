"""비주얼 노벨 MCP 서버 구현.

`fastmcp`를 활용해 `start_env` 도구를 MCP 런타임에 등록하고,
주어진 환경 설정을 기반으로 게임 실행 URL을 생성한다.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from secrets import token_urlsafe
from urllib.parse import urlencode, urljoin

from fastmcp import FastMCP


DEFAULT_BASE_URL = "https://novel.example/"
DEFAULT_SCENARIO = "intro"


@dataclass(slots=True)
class EnvironmentConfig:
    """게임 환경 구성을 표현한다.

    Attributes:
        base_url: 게임이 호스팅되는 기본 URL.
        scenario: 시작할 시나리오 이름.
        language: 게임 기본 언어 코드.
        difficulty: 난이도 레벨 (예: "easy", "normal", "hard").
        extras: 추가 쿼리 파라미터를 넣을 때 사용한다.
    """

    base_url: str = DEFAULT_BASE_URL
    scenario: str = DEFAULT_SCENARIO
    language: str = "ko"
    difficulty: str = "normal"
    extras: dict[str, str] = field(default_factory=dict)

    def to_query_params(self) -> list[tuple[str, str]]:
        """환경 설정을 URL 쿼리 파라미터 목록으로 변환한다."""

        params: list[tuple[str, str]] = [
            ("scenario", self.scenario),
            ("lang", self.language),
            ("difficulty", self.difficulty),
        ]
        params.extend(_dict_items_sorted(self.extras))
        return params


def _dict_items_sorted(data: dict[str, str]) -> list[tuple[str, str]]:
    """일관된 URL 생성을 위해 키 순서로 정렬된 (key, value) 목록을 반환한다."""

    return sorted(data.items())


def build_game_url(config: EnvironmentConfig) -> str:
    """환경 설정으로부터 완전한 게임 URL을 생성한다.

    Args:
        config: `EnvironmentConfig` 인스턴스.

    Returns:
        게임을 바로 실행할 수 있는 URL 문자열.
    """

    query = urlencode(config.to_query_params())
    return urljoin(config.base_url, f"play?{query}")


mcp = FastMCP(
    name="visual-novel-mcp",
    description="비주얼 노벨을 위한 게임 URL 빌더 MCP 서버",
)


@mcp.tool(description="별도 입력 없이 즉시 시작 가능한 게임 URL을 생성한다.")
def start_env(config: EnvironmentConfig | dict[str, str] | None = None) -> str:
    """환경을 준비하고 즉시 실행 가능한 게임 URL을 반환한다.

    Args:
        config: (선택) `EnvironmentConfig` 혹은 동일한 키를 가진 딕셔너리.
            생략 시 내부 기본 설정으로 세션을 만들어 준다.

    Returns:
        생성된 게임 URL.
    """

    normalized = _ensure_config(config)
    normalized.extras.setdefault("session", _generate_session_token())
    normalized.extras.setdefault("autostart", "1")
    return build_game_url(normalized)


def _ensure_config(config: EnvironmentConfig | dict[str, str] | None) -> EnvironmentConfig:
    """입력값을 `EnvironmentConfig` 로 변환한다."""

    if config is None:
        return EnvironmentConfig()

    if isinstance(config, EnvironmentConfig):
        return config

    extras = {
        key: value
        for key, value in config.items()
        if key not in {"base_url", "scenario", "language", "difficulty"}
    }

    return EnvironmentConfig(
        base_url=str(config.get("base_url", DEFAULT_BASE_URL)),
        scenario=str(config.get("scenario", DEFAULT_SCENARIO)),
        language=str(config.get("language", "ko")),
        difficulty=str(config.get("difficulty", "normal")),
        extras=extras,
    )


def _generate_session_token() -> str:
    """게임 세션 식별자를 생성한다."""

    return token_urlsafe(12)
