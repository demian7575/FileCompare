# FileCompare

Windows용 파일 정리 도구를 **Python GUI(Tkinter)** 로 구현하는 프로젝트입니다.

## 현재 상태
- Tkinter 기반 데스크톱 GUI 초기 화면 제공
- 파일 작업(이동/삭제/이름 변경) 미리보기 테이블 제공
- "Preview -> Confirm -> Apply" 안전 워크플로우 기준으로 개발 진행

## 실행 방법
사전 요구사항:
- Python 3.11+

```bash
python -m py_compile src/filecompare_app.py
python src/filecompare_app.py
```

## 문서
- MVP 설계: `docs/mvp-spec.md`
