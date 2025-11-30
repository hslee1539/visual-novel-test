from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, List

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LM_STUDIO_URL = os.environ.get("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
LM_STUDIO_MODEL = os.environ.get("LM_STUDIO_MODEL", "lmstudio-community/Meta-Llama-3-8B-Instruct")


def extract_json_content(text: str) -> str:
    """LM Studio가 앞뒤로 설명을 붙여 보내는 경우에도 JSON 본문을 추출한다."""

    # ```json ... ``` 블록 우선 처리
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        return fenced.group(1)

    # 첫 번째 여는 중괄호부터 마지막 닫는 중괄호까지 추출
    curly = re.search(r"\{.*\}", text, re.DOTALL)
    if curly:
        return curly.group(0)

    return text


def fallback_story() -> Dict[str, Any]:
    return {
        "title": "짱구네 소풍 대작전",
        "start": "prologue",
        "scenes": {
            "prologue": {
                "speaker": "짱구",
                "dialogue": "오늘은 유치원 소풍 날! 뭘 챙겨야 멋질까?",
                "background": "linear-gradient(135deg, #fff3c4 0%, #ffe0b2 50%, #ffcab1 100%)",
                "prompt": "따뜻한 아침 햇살 아래 짱구가 알록달록한 소풍 가방을 메고 거실에서 준비하는 장면, 가족 사진이 걸린 집안, 파스텔 톤, 부드러운 그림체",
                "choices": [
                    {"text": "엄마에게 준비 점검 받기", "next": "check_bag"},
                    {"text": "카스카베 방범대 호출하기", "next": "call_friends"},
                ],
            },
            "check_bag": {
                "speaker": "미사에",
                "dialogue": "간식, 물, 여벌 옷 다 챙겼어? 가방이 터질 것 같은데!",
                "background": "linear-gradient(135deg, #ffe9d6 0%, #ffd7c2 45%, #ffc7b6 100%)",
                "prompt": "주방 테이블 위에 펼쳐진 도시락과 음료수, 잔소리하는 엄마와 서둘러 가방을 정리하는 짱구, 따뜻한 주황색 조명, 코믹한 일러스트",
                "choices": [
                    {"text": "간식 욕심을 부린다", "next": "snack_overflow"},
                    {"text": "액션가면 벨트를 챙긴다", "next": "action_belt"},
                ],
            },
            "snack_overflow": {
                "speaker": "미사에",
                "dialogue": "이 많은 과자를 다 먹으려고? 조금만 줄이자!",
                "background": "linear-gradient(135deg, #ffdccb 0%, #ffcbb8 50%, #ffb9ad 100%)",
                "prompt": "과자 봉지와 젤리가 산처럼 쌓인 테이블, 놀란 표정의 엄마와 활짝 웃는 짱구, 만화풍 표정 강조, 파스텔 배경",
                "choices": [
                    {"text": "과자를 주머니에 몰래 숨긴다", "next": "hide_snack"},
                    {"text": "친구들과 나누기로 한다", "next": "share_snack"},
                ],
            },
            "share_snack": {
                "speaker": "훈이",
                "dialogue": "계획대로 나눠야지! 이만큼이면 모두 충분해.",
                "background": "linear-gradient(135deg, #eaf3ff 0%, #d8e7ff 50%, #c8d8ff 100%)",
                "prompt": "훈이가 노트에 과자 분배표를 그리고 짱구와 친구들이 둘러보는 장면, 깔끔한 파란 톤, 귀여운 만화 스타일",
                "choices": [
                    {"text": "훈이에게 분배를 맡긴다", "next": "bus_gossip"},
                    {"text": "철수에게 몰래 더 준다", "next": "rally"},
                ],
            },
            "action_belt": {
                "speaker": "짱구",
                "dialogue": "액션가면 벨트! 삐비빅— 아빠가 싫어하지만 멋있잖아.",
                "background": "linear-gradient(135deg, #f3e8ff 0%, #e6d9ff 50%, #d9c8ff 100%)",
                "prompt": "액션가면 벨트를 들고 포즈 잡는 짱구, 방 안에 장난감이 흩어져 있고 보라색 네온 느낌이 은은한 코믹 일러스트",
                "choices": [
                    {"text": "짱아에게 자랑한다", "next": "jangasurprise"},
                    {"text": "조용히 가방 안에 숨긴다", "next": "call_friends"},
                ],
            },
            "jangasurprise": {
                "speaker": "짱아",
                "dialogue": "삐! 삐! 버튼을 눌렀더니 벨트 불빛이 번쩍!",
                "background": "linear-gradient(135deg, #ffe9f4 0%, #ffd4e6 50%, #ffc1dc 100%)",
                "prompt": "벨트 불빛에 눈이 반짝이는 아기 짱아, 핑크색 장난감 방, 귀엽고 화사한 수채화 느낌",
                "choices": [
                    {"text": "엄마에게 들키기 전에 끈다", "next": "bus_gossip"},
                    {"text": "짱아에게 과자를 약속한다", "next": "snack_oath"},
                ],
            },
            "snack_oath": {
                "speaker": "짱구",
                "dialogue": "과자 한 봉지로 짱아와 비밀 합의 완료!",
                "background": "linear-gradient(135deg, #fff0ed 0%, #ffe1de 50%, #ffd3d7 100%)",
                "prompt": "짱아와 비밀 약속을 나누며 과자 봉지를 건네는 짱구, 두 사람이 웃는 클로즈업, 포근한 핑크톤",
                "choices": [
                    {"text": "버스로 향한다", "next": "bus_gossip"}
                ],
            },
            "call_friends": {
                "speaker": "철수",
                "dialogue": "방범대 집결! 소풍 계획을 짜 보자.",
                "background": "linear-gradient(135deg, #e4f7ff 0%, #d0ecff 50%, #bde2ff 100%)",
                "prompt": "놀이터 벤치에 모여 작전을 짜는 카스카베 방범대, 노란 학교 버스가 멀리 보이는 맑은 하늘, 명랑한 만화풍",
                "choices": [
                    {"text": "훈이에게 좌석 배치 맡기기", "next": "plan_route"},
                    {"text": "맹구에게 도시락을 부탁하기", "next": "ask_mangoo"},
                ],
            },
            "plan_route": {
                "speaker": "훈이",
                "dialogue": "선생님 근처가 안전하지. 앞자리부터 차지하자!",
                "background": "linear-gradient(135deg, #e1f1ff 0%, #cfe4ff 50%, #bad7ff 100%)",
                "prompt": "유치원 버스 배치도를 손가락으로 가리키는 훈이, 친구들이 고개를 끄덕이며 듣는 장면, 밝은 파란색 교실 분위기",
                "choices": [
                    {"text": "앞자리를 선점한다", "next": "bus_gossip"},
                    {"text": "선생님을 도와드린다", "next": "teacher_help"},
                ],
            },
            "ask_mangoo": {
                "speaker": "맹구",
                "dialogue": "돌 모양 주먹밥을 싸 왔어. 바꾸고 싶으면 말해!",
                "background": "linear-gradient(135deg, #e4ffe8 0%, #d0f8d4 50%, #bdf1c1 100%)",
                "prompt": "돌 모양 주먹밥을 자랑하는 맹구와 신기해하는 친구들, 초록빛 공원 배경, 깨끗한 만화 스타일",
                "choices": [
                    {"text": "맹구 도시락을 칭찬한다", "next": "bus_gossip"},
                    {"text": "더 맛있는 반찬을 약속한다", "next": "picnic_start"},
                ],
            },
            "rally": {
                "speaker": "철수",
                "dialogue": "왜 나만 많이 줘? 그래도 고마워!",
                "background": "linear-gradient(135deg, #e5f4ff 0%, #d2e6ff 50%, #c0d8ff 100%)",
                "prompt": "철수가 과자 봉지를 들고 살짝 당황한 표정, 옆에서 웃는 짱구, 버스 앞에서 파란 하늘이 보이는 장면",
                "choices": [
                    {"text": "철수와 계획을 세운다", "next": "bus_gossip"},
                    {"text": "모두에게 더 나눠준다", "next": "picnic_start"},
                ],
            },
            "teacher_help": {
                "speaker": "선생님",
                "dialogue": "짐을 들어줘서 고마워. 덕분에 출발이 빠르겠는걸!",
                "background": "linear-gradient(135deg, #f3f7ff 0%, #e0ebff 50%, #ceddfa 100%)",
                "prompt": "유치원 선생님 짐을 옮기는 아이들, 버스 옆에서 밝게 웃는 선생님, 부드러운 파스텔 톤의 하늘",
                "choices": [
                    {"text": "버스에 먼저 탄다", "next": "bus_gossip"},
                    {"text": "친구들을 챙긴다", "next": "picnic_start"},
                ],
            },
            "tummyache": {
                "speaker": "나레이션",
                "dialogue": "버스 출발 전 과자를 다 먹은 짱구, 배가 살살 아프다...",
                "background": "linear-gradient(135deg, #ffe7e1 0%, #ffd7d1 50%, #ffc4c2 100%)",
                "prompt": "버스 의자에 축 처져 앉아 배를 붙잡는 짱구, 창밖으로 스쳐 지나가는 거리, 따뜻한 핑크빛 만화 연출",
                "choices": [
                    {"text": "그늘에서 잠시 쉰다", "next": "ending_rest"}
                ],
            },
            "bus_gossip": {
                "speaker": "나레이션",
                "dialogue": "유치원 버스 안은 웃음소리로 가득하다. 각자 도시락 자랑이 한창!",
                "background": "linear-gradient(135deg, #e9f6ff 0%, #d4eaff 50%, #c2ddff 100%)",
                "prompt": "노란 유치원 버스 안, 아이들이 도시락을 들고 떠드는 모습, 창밖으로 맑은 하늘과 들판, 명랑한 니메이션 스타일",
                "choices": [
                    {"text": "도시락 자랑 대회에 참여한다", "next": "picnic_start"},
                    {"text": "잠든 짱아를 지켜준다", "next": "nap_guard"},
                ],
            },
            "nap_guard": {
                "speaker": "선생님",
                "dialogue": "짱아를 챙겨줘서 고마워. 덕분에 조용히 갈 수 있겠네.",
                "background": "linear-gradient(135deg, #f1f8ff 0%, #deecff 50%, #cde1ff 100%)",
                "prompt": "버스 창가에서 잠든 짱아를 담요로 덮어주는 짱구, 차분한 파란색 조명, 포근한 느낌",
                "choices": [
                    {"text": "무사히 도착하기", "next": "picnic_start"}
                ],
            },
            "picnic_start": {
                "speaker": "나레이션",
                "dialogue": "드디어 소풍 장소 도착! 햇살 아래 돗자리를 펼친다.",
                "background": "linear-gradient(135deg, #fff7e0 0%, #ffeac6 50%, #ffdcb3 100%)",
                "prompt": "초록빛 잔디밭 위에 돗자리를 펴는 아이들과 선생님, 봄 햇살과 흩날리는 벚꽃, 따뜻한 파스텔 색감",
                "choices": [
                    {"text": "액션가면 팀 놀이에 참여한다", "next": "ranger_game"},
                    {"text": "나뭇잎과 돌을 모은다", "next": "leaf_collect"},
                ],
            },
            "ranger_game": {
                "speaker": "철수",
                "dialogue": "나는 히어로! 짱구는 어떤 역할을 할래?",
                "background": "linear-gradient(135deg, #e5edff 0%, #d2ddff 50%, #c1cfff 100%)",
                "prompt": "소풍 장소에서 액션 히어로 놀이를 하는 아이들, 나무와 하늘이 배경, 역동적인 포즈의 만화풍",
                "choices": [
                    {"text": "히로인 구출 작전", "next": "ending_hero"},
                    {"text": "악당 역할로 방해", "next": "ending_villain"},
                ],
            },
            "leaf_collect": {
                "speaker": "맹구",
                "dialogue": "나뭇잎 왕관, 돌 보물! 함께 모을래?",
                "background": "linear-gradient(135deg, #e7ffe7 0%, #d3f6d2 50%, #c0efc0 100%)",
                "prompt": "초록 잔디 위에서 나뭇잎과 돌을 모으는 맹구와 짱구, 주변에 피어난 들꽃, 상큼한 초록색 파스텔",
                "choices": [
                    {"text": "맹구와 교환하여 보물을 만든다", "next": "ending_peace"},
                    {"text": "잎으로 왕관을 만들어 씌운다", "next": "ending_king"},
                ],
            },
            "ending_hero": {
                "speaker": "나레이션",
                "dialogue": "짱구의 활약으로 철수 팀이 승리! 모두에게 박수를 받았다.",
                "background": "linear-gradient(135deg, #def5ff 0%, #cbe8ff 50%, #b8d9ff 100%)",
                "prompt": "히어로 망토를 두르고 포즈를 취하는 짱구, 친구들이 박수 치는 공원, 밝은 하늘과 풍선, 축제 같은 분위기",
                "choices": [],
            },
            "ending_villain": {
                "speaker": "나레이션",
                "dialogue": "악당 역할을 완벽 소화! 친구들이 웃음바다가 되었다.",
                "background": "linear-gradient(135deg, #ffeaf3 0%, #ffd6e7 50%, #ffc2da 100%)",
                "prompt": "장난스러운 악당 복장을 한 짱구가 웃으며 달아나고 친구들이 웃으며 쫓는 장면, 분홍빛 공원 배경",
                "choices": [],
            },
            "ending_peace": {
                "speaker": "나레이션",
                "dialogue": "돌 보물과 잎 왕관을 맞바꾼 평화의 휴식 시간. 도시락이 더 맛있다.",
                "background": "linear-gradient(135deg, #f0fff4 0%, #dbf6e2 50%, #c8edcf 100%)",
                "prompt": "잔디밭에서 돌 보물과 잎 왕관을 서로 나누며 웃는 아이들, 피크닉 매트 위 도시락, 평화로운 초록풍",
                "choices": [],
            },
            "ending_king": {
                "speaker": "나레이션",
                "dialogue": "잎 왕관을 쓴 짱구, 오늘의 자연 왕으로 사진을 남겼다!",
                "background": "linear-gradient(135deg, #fff3df 0%, #ffe3c5 50%, #ffd5b0 100%)",
                "prompt": "잎 왕관을 쓰고 포즈를 취하는 짱구를 스마트폰으로 찍는 친구들, 황금빛 오후 햇살, 따뜻한 파스텔 톤",
                "choices": [],
            },
            "ending_rest": {
                "speaker": "나레이션",
                "dialogue": "배 아픈 짱구는 그늘에서 조금 쉬었다. 다음엔 과자를 천천히 먹기로 약속한다.",
                "background": "linear-gradient(135deg, #ffecec 0%, #ffdede 50%, #ffd1d1 100%)",
                "prompt": "나무 그늘 아래 돗자리에서 배를 만지며 쉬는 짱구, 옆에 물병과 도시락, 살랑거리는 바람, 잔잔한 핑크빛",
                "choices": [],
            },
        },
    }


story_state: Dict[str, Any] = {
    "theme": "짱구네 소풍 대작전",
    "history": [],
    "current_id": None,
    "use_fallback": False,
    "main_plan": None,
    "characters": None,
    "fallback": fallback_story(),
}


def call_lm_studio(messages: List[Dict[str, str]], temperature: float = 0.6) -> str:
    logger.debug("LM Studio 요청: %s", messages)
    response = requests.post(
        LM_STUDIO_URL,
        headers={"Content-Type": "application/json"},
        json={
            "model": LM_STUDIO_MODEL,
            "messages": messages,
            "temperature": temperature,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    logger.debug("LM Studio 응답 수신: %s", payload)
    return payload["choices"][0]["message"]["content"]


def scenario_step_agent(theme: str, history: List[Dict[str, Any]], choice_text: str | None) -> Dict[str, Any]:
    history_prompt = "\n".join(
        [f"- 선택지 '{entry['choice']}' 후 장면 요약: {entry['summary']}" for entry in history if entry.get("choice")]
    )
    prompt = (
        "너는 어린이 만화풍 비주얼 노벨의 시나리오 설계 에이전트야. "
        "이전 선택과 장면, 메인 시나리오 목표, 미리 정한 등장인물을 참고해 다음 한 장면만 설계하고 JSON으로만 답해. "
        "사용자가 메인 시나리오에서 벗어나지 않도록 선택지를 제안하며, 선택지 문구에 목표를 다시 상기시켜. "
        "반드시 지정된 등장인물(짱구는 못말려 세계관 인물만)만 사용해. "
        "choices는 0~2개이며 text만 포함하고, 선택지가 없으면 이야기를 종료해."
    )
    user_message = (
        "다음 JSON 형식으로만 응답해:\n"
        "{\n"
        "  \"summary\": \"이번 장면 요약\",\n"
        "  \"choices\": [ {\"text\": \"...\"} ]\n"
        "}\n"
        f"전체 주제: {theme}\n"
        f"메인 시나리오 개요: {story_state.get('main_plan', {}).get('overview', '개요 없음')}\n"
        f"주요 사건 순서: {story_state.get('main_plan', {}).get('milestones', [])}\n"
        f"등장인물: {story_state.get('characters', [])}\n"
        f"이전 기록:\n{history_prompt}\n"
        f"사용자가 방금 고른 선택지: {choice_text or '없음'}"
    )
    output = call_lm_studio(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message},
        ]
    )
    cleaned = extract_json_content(output)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.warning("시나리오 파싱 실패, 원문: %s", output)
        raise exc

    logger.info("장면 설계 완료 (선택지 수: %d)", len(parsed.get("choices", [])))
    return parsed


def character_agent(theme: str, scene: Dict[str, Any]) -> Dict[str, str]:
    prompt = (
        "너는 시나리오에 맞춰 캐릭터의 대사와 연출을 완성하는 에이전트야. "
        "대사 톤은 명랑하고 어린이 만화풍이며, CSS linear-gradient 배경과 디퓨전 이미지를 위한 프롬프트도 포함해. "
        "대사에는 메인 시나리오 목표를 자연스럽게 한 번 상기시키는 문장을 넣어 사용자가 흐름을 따라가도록 도와줘. "
        "반드시 미리 정의된 등장인물(짱구는 못말려 출연 인물만) 안에서 화자를 선택해. "
        "JSON 외의 문장은 절대 쓰지 마."
    )
    output = call_lm_studio(
        [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": (
                    "다음 키만 포함된 JSON으로 응답해:\n"
                    "{\n"
                    "  \"speaker\": \"...\",\n"
                    "  \"dialogue\": \"...\",\n"
                    "  \"background\": \"linear-gradient(...)\",\n"
                    "  \"prompt\": \"이미지 프롬프트\"\n"
                    "}\n"
                    f"전체 주제: {theme}\n"
                    f"장면 요약: {scene['summary']}\n"
                    f"선택지: {scene.get('choices', [])}\n"
                    f"메인 시나리오 개요: {story_state.get('main_plan', {}).get('overview', '개요 없음')}\n"
                    f"주요 사건 순서: {story_state.get('main_plan', {}).get('milestones', [])}\n"
                    f"등장인물: {story_state.get('characters', [])}"
                ),
            },
        ],
        temperature=0.7,
    )
    cleaned = extract_json_content(output)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.warning("캐릭터 파싱 실패 (scene: %s), 원문: %s", scene.get("id"), output)
        raise exc

    logger.info("캐릭터 연출 생성 완료 (scene: %s, speaker: %s)", scene.get("id"), parsed.get("speaker"))
    return parsed


def reset_story_state(theme: str = "짱구네 소풍 대작전") -> None:
    story_state.update(
        {
            "theme": theme,
            "history": [],
            "current_id": None,
            "use_fallback": False,
            "main_plan": None,
            "characters": None,
            "fallback": fallback_story(),
        }
    )


def plan_main_scenario(theme: str) -> Dict[str, Any]:
    prompt = (
        "너는 어린이 만화풍 비주얼 노벨의 메인 시나리오를 설계하는 에이전트야. "
        "이야기의 큰 흐름이 처음부터 끝까지 이어지도록 개요와 주요 사건 3~5개를 JSON으로만 작성해."
    )
    user_message = (
        "다음 JSON 형식으로만 응답해:\n"
        "{\n"
        "  \"overview\": \"전체 개요\",\n"
        "  \"milestones\": [\"주요 사건\", ...]\n"
        "}\n"
        f"전체 주제: {theme}"
    )
    output = call_lm_studio(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.5,
    )
    cleaned = extract_json_content(output)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.warning("메인 시나리오 설계 파싱 실패, 원문: %s", output)
        raise exc

    logger.info("메인 시나리오 설계 완료: %s", parsed.get("overview"))
    return parsed


def plan_characters(theme: str) -> List[Dict[str, str]]:
    prompt = (
        "너는 어린이 만화풍 비주얼 노벨의 등장인물을 선별하는 에이전트야. "
        "반드시 '짱구는 못말려' 시리즈에 등장하는 인물만 고르고, 이름과 한 줄 소개를 JSON으로만 작성해. "
        "메인 시나리오를 원활하게 진행할 3~6명의 주요 캐릭터를 제안해."
    )
    user_message = (
        "다음 JSON 형식으로만 응답해:\n"
        "{\n"
        "  \"characters\": [ {\"name\": \"이름\", \"role\": \"특징/역할\"} ]\n"
        "}\n"
        f"전체 주제: {theme}"
    )
    output = call_lm_studio(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.5,
    )
    cleaned = extract_json_content(output)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.warning("등장인물 설계 파싱 실패, 원문: %s", output)
        raise exc

    characters = parsed.get("characters", [])
    logger.info("등장인물 설계 완료: %s", [c.get("name") for c in characters])
    return characters


def fallback_scene(choice_text: str | None) -> Dict[str, Any]:
    fallback = story_state["fallback"]
    if story_state["current_id"] is None:
        story_state["current_id"] = fallback["start"]
    else:
        current_choices = fallback["scenes"][story_state["current_id"]].get("choices", [])
        if current_choices:
            next_id = next(
                (c["next"] for c in current_choices if c.get("text") == choice_text),
                current_choices[0]["next"],
            )
            story_state["current_id"] = next_id

    scene = fallback["scenes"][story_state["current_id"]]
    scene_payload = {**scene, "id": story_state["current_id"]}
    logger.info("폴백 장면 반환: %s", story_state["current_id"])
    return scene_payload


def generate_scene(choice_text: str | None = None) -> Dict[str, Any]:
    if story_state.get("use_fallback"):
        return fallback_scene(choice_text)

    try:
        if story_state.get("main_plan") is None:
            story_state["main_plan"] = plan_main_scenario(story_state["theme"])
        if story_state.get("characters") is None:
            story_state["characters"] = plan_characters(story_state["theme"])

        step = scenario_step_agent(story_state["theme"], story_state["history"], choice_text)
        details = character_agent(
            story_state["theme"],
            {"summary": step.get("summary", ""), "choices": step.get("choices", [])},
        )
        scene_id = f"scene_{len(story_state['history']) + 1}"
        scene = {**details, "choices": step.get("choices", []), "id": scene_id, "summary": step.get("summary", "")}
        story_state["current_id"] = scene_id
        story_state["history"].append({"id": scene_id, **scene, "choice": choice_text})
        logger.info("장면 생성 완료: %s", scene_id)
        return scene
    except Exception as exc:  # pragma: no cover - LM Studio 통신 오류 핸들링
        logger.warning("LM Studio 호출 실패, 폴백 스토리 사용: %s", exc)
        story_state["use_fallback"] = True
        return fallback_scene(choice_text)


@app.get("/")
def index() -> str:
    return render_template("index.html", title="비주얼 노벨 생성기")


@app.get("/api/story/start")
def start_story() -> dict:
    reset_story_state()
    try:
        story_state["main_plan"] = plan_main_scenario(story_state["theme"])
        story_state["characters"] = plan_characters(story_state["theme"])
    except Exception as exc:  # pragma: no cover - LM Studio 통신 오류 핸들링
        logger.warning("메인 시나리오 설계 실패, 폴백 시나리오로 진행: %s", exc)
        story_state["use_fallback"] = True
        story_state["main_plan"] = {
            "overview": story_state["fallback"]["title"],
            "milestones": ["폴백 시나리오 순서를 따릅니다."],
        }
        story_state["characters"] = [
            {"name": "짱구", "role": "엉뚱하지만 분위기를 이끄는 주인공"},
            {"name": "미사에", "role": "짱구를 챙기며 간식을 관리하는 엄마"},
            {"name": "훈이", "role": "계획을 세우는 리더십 있는 친구"},
            {"name": "철수", "role": "예의 바르고 친구들을 돕는 친구"},
            {"name": "맹구", "role": "말수는 적지만 든든한 힘을 주는 친구"},
        ]

    scene = generate_scene()
    return jsonify({"scene": scene})


@app.post("/api/story/next")
def next_scene() -> dict:
    payload = request.get_json(force=True) or {}
    choice_text = payload.get("choice")
    scene = generate_scene(choice_text)
    return jsonify({"scene": scene})


if __name__ == "__main__":
    app.run(debug=True)
