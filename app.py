from __future__ import annotations

from flask import Flask, jsonify, render_template

app = Flask(__name__)

story_data = {
    "title": "항구의 아침",
    "start": "prologue",
    "scenes": {
        "prologue": {
            "speaker": "지우",
            "dialogue": "새벽의 항구... 오늘도 배가 늦겠지?",
            "background": "#cce8ff",
            "choices": [
                {"text": "항구를 둘러본다", "next": "docks"},
                {"text": "친구에게 전화한다", "next": "call_friend"},
            ],
        },
        "docks": {
            "speaker": "선장",
            "dialogue": "오늘은 파도가 잔잔해. 조금만 기다리면 배가 뜰 거야.",
            "background": "#b3d4fc",
            "choices": [
                {"text": "도움을 제안한다", "next": "help_prepare"},
                {"text": "커피를 사러 간다", "next": "coffee"},
            ],
        },
        "call_friend": {
            "speaker": "지우",
            "dialogue": "민서야, 오늘 새벽 항구에 왔어. 너도 올래?",
            "background": "#d9e7ff",
            "choices": [
                {"text": "민서가 온다", "next": "friend_arrives"},
                {"text": "전화가 끊어진다", "next": "missed_call"},
            ],
        },
        "help_prepare": {
            "speaker": "선장",
            "dialogue": "정말 고맙군! 같이 밧줄을 점검하자고.",
            "background": "#c5e1ff",
            "choices": [
                {"text": "신속하게 돕는다", "next": "ready_to_depart"},
                {"text": "느긋하게 돕는다", "next": "sunrise"},
            ],
        },
        "coffee": {
            "speaker": "바리스타",
            "dialogue": "따뜻한 커피 한 잔이면 기다림도 견딜 만하죠.",
            "background": "#f6e0b5",
            "choices": [
                {"text": "선장에게 가져다준다", "next": "gift_coffee"},
                {"text": "혼자 마신다", "next": "calm_wait"},
            ],
        },
        "friend_arrives": {
            "speaker": "민서",
            "dialogue": "역시 너는 늘 멋진 장소를 찾아. 같이 기다려볼까?",
            "background": "#d0f0ff",
            "choices": [
                {"text": "함께 사진을 찍는다", "next": "photo"},
                {"text": "배에 대해 묻는다", "next": "ask_about_boat"},
            ],
        },
        "missed_call": {
            "speaker": "나레이션",
            "dialogue": "전파 상황이 좋지 않은가 보다. 조용히 파도 소리를 듣는다.",
            "background": "#e8edf3",
            "choices": [
                {"text": "항구를 산책한다", "next": "harbor_walk"},
                {"text": "앉아서 스케치한다", "next": "sketch"},
            ],
        },
        "ready_to_depart": {
            "speaker": "선장",
            "dialogue": "준비 끝! 첫 항해에 같이 타볼래?",
            "background": "#b8d8ff",
            "choices": [
                {"text": "승선한다", "next": "sail"},
                {"text": "안전하게 거절한다", "next": "sunrise"},
            ],
        },
        "sunrise": {
            "speaker": "나레이션",
            "dialogue": "동쪽 하늘이 붉게 물든다. 기다림도 누군가와 함께라면 따뜻하다.",
            "background": "#ffd2a6",
            "choices": [
                {"text": "새로운 하루를 맞이한다", "next": "ending"}
            ],
        },
        "gift_coffee": {
            "speaker": "선장",
            "dialogue": "이런 세심한 선물이 있다니! 선원들도 좋아할 거야.",
            "background": "#f1d9a9",
            "choices": [
                {"text": "선원들과 대화한다", "next": "crew_talk"},
                {"text": "몰래 한 모금 마신다", "next": "calm_wait"},
            ],
        },
        "calm_wait": {
            "speaker": "지우",
            "dialogue": "파도 소리를 들으며 마음이 차분해진다.",
            "background": "#e9f7ff",
            "choices": [
                {"text": "다시 선장을 찾는다", "next": "help_prepare"},
                {"text": "풍경을 사진으로 남긴다", "next": "photo"},
            ],
        },
        "photo": {
            "speaker": "민서",
            "dialogue": "사진이 마음에 들어! 우리의 아침이 기록됐어.",
            "background": "#d7f0ff",
            "choices": [
                {"text": "배 이야기를 나눈다", "next": "ask_about_boat"},
                {"text": "다시 커피를 사러 간다", "next": "coffee"},
            ],
        },
        "ask_about_boat": {
            "speaker": "선장",
            "dialogue": "이 배는 오래됐지만 믿을 만하지. 곧 새 도장을 칠 거야.",
            "background": "#cfe3ff",
            "choices": [
                {"text": "도장 일을 돕는다", "next": "crew_talk"},
                {"text": "감탄하며 바라본다", "next": "sunrise"},
            ],
        },
        "crew_talk": {
            "speaker": "선원",
            "dialogue": "새로운 항해를 앞두고 설레. 너도 함께 이야기할래?",
            "background": "#d9ebff",
            "choices": [
                {"text": "항해 계획을 듣는다", "next": "sail"},
                {"text": "격려의 말을 건넨다", "next": "ending"},
            ],
        },
        "harbor_walk": {
            "speaker": "지우",
            "dialogue": "조용한 새벽, 어부들의 준비 소리가 들린다.",
            "background": "#e1f5ff",
            "choices": [
                {"text": "배경음을 녹음한다", "next": "sketch"},
                {"text": "돌아와서 기다린다", "next": "calm_wait"},
            ],
        },
        "sketch": {
            "speaker": "지우",
            "dialogue": "파도와 부표를 그리며 시간을 보낸다.",
            "background": "#f1f5ff",
            "choices": [
                {"text": "선장에게 보여준다", "next": "gift_coffee"},
                {"text": "친구에게 보낸다", "next": "friend_arrives"},
            ],
        },
        "sail": {
            "speaker": "나레이션",
            "dialogue": "첫 항해는 짧지만 강렬했다. 바람과 함께 새로운 시작을 맞는다.",
            "background": "#b8e2ff",
            "choices": [
                {"text": "새로운 이야기로 이어진다", "next": "ending"}
            ],
        },
        "ending": {
            "speaker": "나레이션",
            "dialogue": "항구의 아침은 끝났지만, 다음 만남을 기약한다.",
            "background": "#fef4d2",
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
