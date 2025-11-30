# Visual Novel Test

간단한 파이썬(Flask) 기반 웹 비주얼 노벨 예제입니다. "짱구네 소풍 대작전"이라는 짧은 이야기를 선택형으로 즐길 수 있습니다.
LM Studio를 통해 시나리오 설계 에이전트와 캐릭터 에이전트가 **장면 단위로** 줄거리를 만들어냅니다. 사용자가 선택지를 고를 때마다 다음 장면이 새로 생성되며, LM Studio가 동작하지 않거나 응답 실패 시에는 기존 고정 스토리로 안전하게 폴백합니다.

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

### LM Studio 설정
- 기본값은 `http://localhost:1234/v1/chat/completions` 엔드포인트와 `lmstudio-community/Meta-Llama-3-8B-Instruct` 모델을 사용합니다.
- 다른 주소나 모델을 쓰려면 환경 변수로 덮어쓸 수 있습니다.
  ```bash
  export LM_STUDIO_URL="http://localhost:1234/v1/chat/completions"
  export LM_STUDIO_MODEL="your-model-name"
  flask --app app run
  ```

## 구조
- `app.py`: Flask 앱과 스토리 데이터, API 엔드포인트를 정의합니다.
- `templates/index.html`: 기본 페이지 레이아웃.
- `static/app.js`: 스토리 불러오기, 선택지 표시, 기록 관리 등의 클라이언트 로직.
- `static/style.css`: 간단한 UI 스타일.

## 커스터마이징 팁
- `app.py`의 `fallback_story()`를 수정하면 폴백으로 사용되는 장면을 원하는 대로 바꿀 수 있습니다.
- `static/style.css`에서 색상과 배경을 변경해 분위기를 조정할 수 있습니다.
