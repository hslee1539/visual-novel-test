# visual-novel-test

비주얼 노벨용 MCP 서버를 `fastmcp` 스타일로 단순하게 구현한 예제다. `start_env()` 함수는 별도의 입력 없이 바로 플레이할 수 있는 게임 세션을 만들고 URL을 반환하며, MCP 도구로 등록되어 있다.

## 구성

- `src/fastmcp/`: 네트워크 제약 환경에서도 쓸 수 있는 최소 `fastmcp` 호환 래퍼.
- `src/visual_novel_mcp/server.py`: 환경 설정 데이터 모델과 URL 생성 로직, `fastmcp` 도구 등록.
- `tests/test_server.py`: URL 생성 및 유효성 검증, 도구 등록 상태 테스트.

## 사용 예시

```python
from visual_novel_mcp import mcp, start_env

# 서버가 알아서 새 세션을 만들고 바로 실행되는 URL을 돌려준다.
url = start_env()

print(url)  # https://novel.example/play?scenario=intro&lang=ko&difficulty=normal&session=...

# MCP 클라이언트가 필요하다면 등록된 도구 메타데이터도 확인할 수 있다.
tool = mcp.get_tool("start_env")
print(tool.description)
```

## 테스트 실행

```bash
python -m pytest
```
