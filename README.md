# Visual Novel Test Server

간단한 비주얼 노벨 프로토타입을 제공하는 파이썬 Flask 서버입니다. 미리 정의된 장면과 선택지를 API 형태로 반환합니다.

## 실행 방법

1. 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

2. 서버 실행
   ```bash
   python app.py
   ```

3. 예시 요청
   - 서버 상태 확인: `GET /`
   - 스토리 전체 보기: `GET /api/story`
   - 특정 장면 보기: `GET /api/story/<scene_id>`
   - 선택 전송: `POST /api/story/<scene_id>/choice` with body `{ "choiceId": "..." }`

서버는 기본적으로 `http://127.0.0.1:5000`에서 동작합니다.
