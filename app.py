from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from flask import Flask, jsonify, request


@dataclass
class Choice:
    id: str
    label: str
    leads_to: str


@dataclass
class Scene:
    id: str
    speaker: Optional[str]
    text: str
    choices: List[Choice]


# 간단한 테스트용 시나리오 정의
SCENES: Dict[str, Scene] = {
    "intro": Scene(
        id="intro",
        speaker=None,
        text="눈을 뜨니 낯선 역 대합실이다. 어디로 가야 할까?",
        choices=[
            Choice(id="wait", label="잠시 주변을 살핀다", leads_to="platform"),
            Choice(id="exit", label="밖으로 나간다", leads_to="street"),
        ],
    ),
    "platform": Scene(
        id="platform",
        speaker="소녀",
        text="안녕하세요! 기차를 기다리시는 건가요?",
        choices=[
            Choice(id="ask", label="어디로 가는 기차죠?", leads_to="train"),
            Choice(id="decline", label="아니요, 그냥 둘러보고 있어요", leads_to="street"),
        ],
    ),
    "train": Scene(
        id="train",
        speaker="소녀",
        text="곧 북쪽으로 가는 기차가 도착해요. 함께 가실래요?",
        choices=[
            Choice(id="board", label="함께 탄다", leads_to="north"),
            Choice(id="refuse", label="정중히 거절한다", leads_to="street"),
        ],
    ),
    "street": Scene(
        id="street",
        speaker=None,
        text="밖은 서늘한 공기가 감돈다. 도시의 불빛이 스쳐 지나간다.",
        choices=[
            Choice(id="return", label="역으로 돌아간다", leads_to="intro"),
            Choice(id="end", label="어딘가로 사라진다", leads_to="credits"),
        ],
    ),
    "north": Scene(
        id="north",
        speaker="소녀",
        text="기차는 북쪽으로 달려간다. 새로운 여행이 시작된다!",
        choices=[
            Choice(id="end", label="끝", leads_to="credits"),
        ],
    ),
    "credits": Scene(
        id="credits",
        speaker=None,
        text="여정에 함께해 주셔서 감사합니다.",
        choices=[],
    ),
}


def serialize_scene(scene: Scene) -> dict:
    return {
        "id": scene.id,
        "speaker": scene.speaker,
        "text": scene.text,
        "choices": [
            {"id": choice.id, "label": choice.label, "leads_to": choice.leads_to}
            for choice in scene.choices
        ],
    }


app = Flask(__name__)


@app.get("/")
def index():
    """간단한 환영 메시지와 주요 엔드포인트 안내."""
    return jsonify(
        {
            "message": "비주얼 노벨 테스트 서버가 실행 중입니다.",
            "endpoints": {
                "story_overview": "/api/story",
                "scene": "/api/story/<scene_id>",
                "choice": "/api/story/<scene_id>/choice",
            },
        }
    )


@app.get("/api/story")
def get_story_overview():
    """스토리의 시작 지점과 장면 목록을 반환한다."""
    return jsonify({
        "start": "intro",
        "scenes": [serialize_scene(scene) for scene in SCENES.values()],
    })


@app.get("/api/story/<scene_id>")
def get_scene(scene_id: str):
    scene = SCENES.get(scene_id)
    if scene is None:
        return jsonify({"error": "존재하지 않는 장면"}), 404
    return jsonify(serialize_scene(scene))


@app.post("/api/story/<scene_id>/choice")
def choose(scene_id: str):
    scene = SCENES.get(scene_id)
    if scene is None:
        return jsonify({"error": "존재하지 않는 장면"}), 404

    payload = request.get_json(silent=True) or {}
    choice_id = payload.get("choiceId")
    if not isinstance(choice_id, str):
        return jsonify({"error": "choiceId가 필요합니다"}), 400

    choice = next((c for c in scene.choices if c.id == choice_id), None)
    if choice is None:
        return jsonify({"error": "유효하지 않은 선택"}), 400

    next_scene = SCENES.get(choice.leads_to)
    if next_scene is None:
        return jsonify({"error": "다음 장면이 정의되지 않았습니다"}), 500

    return jsonify({
        "current": serialize_scene(scene),
        "choice": {"id": choice.id, "label": choice.label},
        "next": serialize_scene(next_scene),
    })


def create_app() -> Flask:
    return app


if __name__ == "__main__":
    app.run(debug=True)
