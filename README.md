# Visual Novel Test

간단한 파이썬(Flask) 기반 웹 비주얼 노벨 예제입니다. "항구의 아침"이라는 짧은 이야기를 선택형으로 즐길 수 있습니다.

## 실행 방법
1. 가상환경을 만든 뒤 의존성을 설치합니다.
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. 개발 서버를 실행합니다.
   ```bash
   flask --app app run
   ```
3. 브라우저에서 `http://127.0.0.1:5000`으로 접속합니다.

## 구조
- `app.py`: Flask 앱과 스토리 데이터, API 엔드포인트를 정의합니다.
- `templates/index.html`: 기본 페이지 레이아웃.
- `static/app.js`: 스토리 불러오기, 선택지 표시, 기록 관리 등의 클라이언트 로직.
- `static/style.css`: 간단한 UI 스타일.

## 커스터마이징 팁
- `app.py`의 `story_data` 구조에 장면을 추가하거나 내용을 바꿔 새로운 이야기를 만들 수 있습니다.
- `static/style.css`에서 색상과 배경을 변경해 분위기를 조정할 수 있습니다.
