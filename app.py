from __future__ import annotations

from flask import Flask, jsonify, render_template

app = Flask(__name__)

story_data = {
    "title": "짱구네 소풍 대작전",
    "start": "prologue",
    "scenes": {
        "prologue": {
            "speaker": "짱구",
            "dialogue": "오늘은 유치원 소풍 날! 뭘 챙겨야 멋질까?",
            "background": "#f9e8b8",
            "choices": [
                {"text": "엄마에게 준비 점검 받기", "next": "check_bag"},
                {"text": "카스카베 방범대 호출하기", "next": "call_friends"},
            ],
        },
        "check_bag": {
            "speaker": "미사에",
            "dialogue": "간식, 물, 여벌 옷 다 챙겼어? 가방이 터질 것 같은데!",
            "background": "#ffe3d8",
            "choices": [
                {"text": "간식 욕심을 부린다", "next": "snack_overflow"},
                {"text": "액션가면 벨트를 챙긴다", "next": "action_belt"},
            ],
        },
        "snack_overflow": {
            "speaker": "미사에",
            "dialogue": "이 많은 과자를 다 먹으려고? 조금만 줄이자!",
            "background": "#ffd7c2",
            "choices": [
                {"text": "과자를 주머니에 몰래 숨긴다", "next": "hide_snack"},
                {"text": "친구들과 나누기로 한다", "next": "share_snack"},
            ],
        },
        "hide_snack": {
            "speaker": "짱구",
            "dialogue": "주머니가 볼록해졌지만 들키지 않겠지?", 
            "background": "#fff2d4",
            "choices": [
                {"text": "버스에서 몰래 먹는다", "next": "tummyache"},
                {"text": "버스에서 친구들과 나눈다", "next": "bus_gossip"},
            ],
        },
        "share_snack": {
            "speaker": "훈이",
            "dialogue": "계획대로 나눠야지! 이만큼이면 모두 충분해.",
            "background": "#e9f1ff",
            "choices": [
                {"text": "훈이에게 분배를 맡긴다", "next": "bus_gossip"},
                {"text": "철수에게 몰래 더 준다", "next": "rally"},
            ],
        },
        "action_belt": {
            "speaker": "짱구",
            "dialogue": "액션가면 벨트! 삐비빅— 아빠가 싫어하지만 멋있잖아.",
            "background": "#f9f0ff",
            "choices": [
                {"text": "짱아에게 자랑한다", "next": "jangasurprise"},
                {"text": "조용히 가방 안에 숨긴다", "next": "call_friends"},
            ],
        },
        "jangasurprise": {
            "speaker": "짱아",
            "dialogue": "삐! 삐! 버튼을 눌렀더니 벨트 불빛이 번쩍!",
            "background": "#ffe6f1",
            "choices": [
                {"text": "엄마에게 들키기 전에 끈다", "next": "bus_gossip"},
                {"text": "짱아에게 과자를 약속한다", "next": "snack_oath"},
            ],
        },
        "snack_oath": {
            "speaker": "짱구",
            "dialogue": "과자 한 봉지로 짱아와 비밀 합의 완료!",
            "background": "#fff2f0",
            "choices": [
                {"text": "버스로 향한다", "next": "bus_gossip"}
            ],
        },
        "call_friends": {
            "speaker": "철수",
            "dialogue": "방범대 집결! 소풍 계획을 짜 보자.",
            "background": "#e1f7ff",
            "choices": [
                {"text": "훈이에게 좌석 배치 맡기기", "next": "plan_route"},
                {"text": "맹구에게 도시락을 부탁하기", "next": "ask_mangoo"},
            ],
        },
        "plan_route": {
            "speaker": "훈이",
            "dialogue": "선생님 근처가 안전하지. 앞자리부터 차지하자!",
            "background": "#d9ecff",
            "choices": [
                {"text": "앞자리를 선점한다", "next": "bus_gossip"},
                {"text": "선생님을 도와드린다", "next": "teacher_help"},
            ],
        },
        "ask_mangoo": {
            "speaker": "맹구",
            "dialogue": "돌 모양 주먹밥을 싸 왔어. 바꾸고 싶으면 말해!",
            "background": "#e5ffe4",
            "choices": [
                {"text": "맹구 도시락을 칭찬한다", "next": "bus_gossip"},
                {"text": "더 맛있는 반찬을 약속한다", "next": "picnic_start"},
            ],
        },
        "rally": {
            "speaker": "철수",
            "dialogue": "왜 나만 많이 줘? 그래도 고마워!", 
            "background": "#def1ff",
            "choices": [
                {"text": "철수와 계획을 세운다", "next": "bus_gossip"},
                {"text": "모두에게 더 나눠준다", "next": "picnic_start"},
            ],
        },
        "teacher_help": {
            "speaker": "선생님",
            "dialogue": "짐을 들어줘서 고마워. 덕분에 출발이 빠르겠는걸!",
            "background": "#f1f7ff",
            "choices": [
                {"text": "버스에 먼저 탄다", "next": "bus_gossip"},
                {"text": "친구들을 챙긴다", "next": "picnic_start"},
            ],
        },
        "tummyache": {
            "speaker": "나레이션",
            "dialogue": "버스 출발 전 과자를 다 먹은 짱구, 배가 살살 아프다...",
            "background": "#ffe5e1",
            "choices": [
                {"text": "그늘에서 잠시 쉰다", "next": "ending_rest"}
            ],
        },
        "bus_gossip": {
            "speaker": "나레이션",
            "dialogue": "유치원 버스 안은 웃음소리로 가득하다. 각자 도시락 자랑이 한창!",
            "background": "#e9f5ff",
            "choices": [
                {"text": "도시락 자랑 대회에 참여한다", "next": "picnic_start"},
                {"text": "잠든 짱아를 지켜준다", "next": "nap_guard"},
            ],
        },
        "nap_guard": {
            "speaker": "선생님",
            "dialogue": "짱아를 챙겨줘서 고마워. 덕분에 조용히 갈 수 있겠네.",
            "background": "#f0faff",
            "choices": [
                {"text": "무사히 도착하기", "next": "picnic_start"}
            ],
        },
        "picnic_start": {
            "speaker": "나레이션",
            "dialogue": "드디어 소풍 장소 도착! 햇살 아래 돗자리를 펼친다.",
            "background": "#fff7e6",
            "choices": [
                {"text": "액션가면 팀 놀이에 참여한다", "next": "ranger_game"},
                {"text": "나뭇잎과 돌을 모은다", "next": "leaf_collect"},
            ],
        },
        "ranger_game": {
            "speaker": "철수",
            "dialogue": "나는 히어로! 짱구는 어떤 역할을 할래?",
            "background": "#e3ecff",
            "choices": [
                {"text": "히로인 구출 작전", "next": "ending_hero"},
                {"text": "악당 역할로 방해", "next": "ending_villain"},
            ],
        },
        "leaf_collect": {
            "speaker": "맹구",
            "dialogue": "나뭇잎 왕관, 돌 보물! 함께 모을래?",
            "background": "#ecffe8",
            "choices": [
                {"text": "맹구와 교환하여 보물을 만든다", "next": "ending_peace"},
                {"text": "잎으로 왕관을 만들어 씌운다", "next": "ending_king"},
            ],
        },
        "ending_hero": {
            "speaker": "나레이션",
            "dialogue": "짱구의 활약으로 철수 팀이 승리! 모두에게 박수를 받았다.",
            "background": "#d9f5ff",
            "choices": [],
        },
        "ending_villain": {
            "speaker": "나레이션",
            "dialogue": "악당 역할을 완벽 소화! 친구들이 웃음바다가 되었다.",
            "background": "#ffeaf1",
            "choices": [],
        },
        "ending_peace": {
            "speaker": "나레이션",
            "dialogue": "돌 보물과 잎 왕관을 맞바꾼 평화의 휴식 시간. 도시락이 더 맛있다.",
            "background": "#f1fff5",
            "choices": [],
        },
        "ending_king": {
            "speaker": "나레이션",
            "dialogue": "잎 왕관을 쓴 짱구, 오늘의 자연 왕으로 사진을 남겼다!",
            "background": "#fdf0d9",
            "choices": [],
        },
        "ending_rest": {
            "speaker": "나레이션",
            "dialogue": "배 아픈 짱구는 그늘에서 조금 쉬었다. 다음엔 과자를 천천히 먹기로 약속한다.",
            "background": "#ffecec",
            "choices": [],
        },
    },
}


@app.get("/")
def index() -> str:
    return render_template("index.html", title=story_data["title"])


@app.get("/api/story")
def get_story() -> dict:
    return jsonify(story_data)


if __name__ == "__main__":
    app.run(debug=True)
