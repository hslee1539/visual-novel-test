import pytest

from visual_novel_mcp.server import (
    DEFAULT_BASE_URL,
    DEFAULT_SCENARIO,
    EnvironmentConfig,
    build_game_url,
    mcp,
    start_env,
)


def test_build_game_url_basic():
    config = EnvironmentConfig(
        base_url="https://novel.example/",
        scenario="intro",
        language="ko",
        difficulty="easy",
    )

    url = build_game_url(config)

    assert url == "https://novel.example/play?scenario=intro&lang=ko&difficulty=easy"


def test_build_game_url_with_extras_sorted():
    config = EnvironmentConfig(
        base_url="https://novel.example/",
        scenario="episode1",
        extras={"bgm": "on", "skip": "false"},
    )

    url = build_game_url(config)

    # extras should be sorted by key for predictable URLs
    assert (
        url
        == "https://novel.example/play?scenario=episode1&lang=ko&difficulty=normal&bgm=on&skip=false"
    )


def test_start_env_creates_session_without_input():
    url = start_env()

    assert url.startswith(f"{DEFAULT_BASE_URL}play?")
    assert "scenario=intro" in url
    assert "session=" in url
    assert "autostart=1" in url


def test_start_env_accepts_dict_and_uses_defaults_when_missing():
    url = start_env({"feature": "debug"})

    assert url.startswith(f"{DEFAULT_BASE_URL}play?")
    assert f"scenario={DEFAULT_SCENARIO}" in url
    assert "lang=ko" in url
    assert "feature=debug" in url


def test_start_env_registered_as_fastmcp_tool():
    tool = mcp.get_tool("start_env")

    assert tool.name == "start_env"
    assert "URL" in tool.description
    assert tool({"base_url": "https://novel.example/", "scenario": "intro"}).startswith(
        "https://novel.example/play?"
    )


def test_start_env_fills_missing_fields():
    url = start_env({"base_url": "https://custom.example/"})

    assert url.startswith("https://custom.example/play?")
    assert "scenario=intro" in url
