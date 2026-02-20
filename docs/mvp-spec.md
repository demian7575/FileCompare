# FileCompare Java MVP Specification

## 목표
Windows 환경에서 파일 이동/삭제/이름 변경을 **실행 전에 GUI에서 미리보기**하고,
규칙 기반으로 파일을 카테고리별 정리하며, 중복 파일을 안전하게 정리한다.

## 기술 스택
- Java 21 (LTS)
- JavaFX 21 (데스크톱 GUI)
- Gradle (빌드)
- Jackson (규칙/설정 직렬화)
- SLF4J + Logback (실행 로그)

## MVP 기능 범위
1. 폴더 스캔
   - 단일/복수 루트 폴더 선택
   - 파일 메타데이터 수집(경로, 이름, 확장자, 크기, 수정일)
2. 규칙 기반 분류
   - 확장자 기반 이동
   - 파일명 패턴 기반 이동
   - 크기 범위 기반 이동
   - 예외 경로 제외
3. 실행 전 미리보기(드라이런)
   - Move/Delete/Rename 예정 항목 테이블 표시
   - 충돌(대상 파일 존재) 사전 표시
4. 작업 실행
   - 선택 항목만 실행
   - 기본 삭제 방식: 휴지통 이동
   - 실행 결과 로그 저장(JSON Lines)
5. 중복 파일 정리
   - 1차: 파일 크기 그룹화
   - 2차: SHA-256 해시로 최종 확정
   - 그룹별 원본 유지 기준(최신/오래된/경로 우선)

## 비MVP
- 실시간 파일시스템 감시
- 클라우드 저장소 연동
- 이미지/문서 내용 기반 유사도 분석
- 다중 사용자 동시 협업

## 아키텍처
### 패키지 구조
- `com.filecompare.app`
  - `ui`: JavaFX 화면/컨트롤러
  - `core.scan`: 스캔 및 인덱싱
  - `core.rules`: 규칙 모델/평가기
  - `core.plan`: 작업 계획(Operation) 생성
  - `core.execute`: 실제 실행기/충돌 처리
  - `core.dedupe`: 중복 탐지
  - `infra.config`: 설정 로딩/저장
  - `infra.logging`: 감사 로그

### 핵심 도메인 모델
- `FileEntry`: 파일 메타데이터
- `Rule`: 조건 + 대상 경로 템플릿 + 우선순위
- `Operation`: `{type, source, target, reason, conflictStatus}`
- `ExecutionResult`: `{operationId, status, message}`
- `DuplicateGroup`: `{hash, files[]}`

## 안전 정책
- 기본은 항상 드라이런 후 실행
- 대량 작업(예: 1000건 이상) 시 2단계 확인
- 삭제는 기본 휴지통 이동, 영구 삭제는 별도 토글
- 시스템/숨김 파일 보호 옵션 기본 활성화

## 성능 목표
- 100,000 파일 스캔: 60초 이내(SSD 기준)
- UI 스레드 블로킹 금지(백그라운드 Task 사용)
- 중복 해시 계산 시 진행률 표시 및 취소 지원

## 초기 구현 순서
1. 도메인 모델 + 스캔기
2. 규칙 엔진 + 드라이런 Operation 생성
3. JavaFX 미리보기 테이블
4. 실행기(이동/리네임/휴지통)
5. 중복 탐지 및 그룹 UI
6. 로그/리포트 내보내기
