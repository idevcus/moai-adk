# SPEC-002: 코드 TAG 관리 시스템 구축

> **@REQ:CODE-TAG-002** "src/moai_adk 코드베이스 전체에 16-Core TAG 시스템 적용 및 자동 관리"

## 📋 개요

**SPEC ID**: SPEC-002
**제목**: 코드 TAG 관리 시스템 구축
**슬러그**: `code-tag-management`
**작성일**: 2025-09-18
**상태**: DRAFT

### 목적
`/Users/goos/MoAI/MoAI-ADK/src/moai_adk` 디렉토리의 모든 Python 코드에 16-Core TAG 시스템을 적용하여 완전한 추적성과 자동화된 관리를 구현합니다.

### 범위
- Python 소스 코드 파일 (.py) 전체
- 기존 `.moai/indexes/tags.json` 시스템과의 완전 통합
- 자동화된 TAG 검증 및 복구 시스템
- 실시간 TAG 추적성 모니터링

## 🎯 EARS 형식 요구사항

### WHEN 조건 (시점 기반 요구사항)

**WHEN-001**:
```
WHEN 개발자가 src/moai_adk 디렉토리의 Python 파일을 생성하거나 수정하면,
시스템은 자동으로 적절한 16-Core TAG를 감지하고 파일 상단에 주석으로 추가해야 한다.
```

**WHEN-002**:
```
WHEN TAG 인덱싱 스크립트가 실행되면,
시스템은 5초 이내에 모든 Python 파일을 스캔하고 TAG 정보를 .moai/indexes/tags.json에 업데이트해야 한다.
```

**WHEN-003**:
```
WHEN Git commit이 발생하면,
시스템은 pre-commit hook을 통해 TAG 일관성을 검증하고 오류 시 commit을 차단해야 한다.
```

**WHEN-004**:
```
WHEN 개발자가 `/moai:6-sync` 명령을 실행하면,
시스템은 모든 TAG를 재스캔하고 추적성 체인을 복구하며 문서를 자동 동기화해야 한다.
```

### IF 조건 (상태 기반 요구사항)

**IF-001**:
```
IF Python 파일에 TAG 주석이 누락되어 있다면,
시스템은 파일의 기능과 위치를 분석하여 적절한 TAG를 자동 제안하고 추가해야 한다.
```

**IF-002**:
```
IF TAG 형식이 16-Core 명명 규칙에 어긋난다면,
시스템은 WARNING을 발생시키고 올바른 형식으로 자동 수정을 제안해야 한다.
```

**IF-003**:
```
IF 중복된 TAG가 발견된다면,
시스템은 충돌을 해결하고 고유한 식별자를 부여하여 추적성을 보장해야 한다.
```

**IF-004**:
```
IF TAG와 파일 내용이 불일치한다면,
시스템은 불일치 리포트를 생성하고 수동 검토를 위한 알림을 발생시켜야 한다.
```

### WHILE 진행 중 요구사항

**WHILE-001**:
```
WHILE 개발 세션이 활성 상태인 동안,
시스템은 파일 변경을 실시간으로 모니터링하고 TAG 변경 사항을 즉시 인덱스에 반영해야 한다.
```

**WHILE-002**:
```
WHILE 대량의 파일 스캔이 진행되는 동안,
시스템은 진행 상황을 표시하고 중단 가능한 인터페이스를 제공해야 한다.
```

**WHILE-003**:
```
WHILE TAG 검증 프로세스가 실행되는 동안,
시스템은 메모리 사용량을 500MB 이하로 유지하고 성능 저하를 방지해야 한다.
```

### WHERE 위치/컨텍스트 요구사항

**WHERE-001**:
```
WHERE src/moai_adk의 핵심 모듈에서,
시스템은 @CORE, @API, @CLI 등의 기능별 TAG를 우선적으로 적용해야 한다.
```

**WHERE-002**:
```
WHERE 테스트 파일이 없는 소스 코드에서,
시스템은 @DEBT:NO-TEST TAG를 자동 추가하고 TDD 강제 경고를 발생시켜야 한다.
```

**WHERE-003**:
```
WHERE Git 저장소 루트 디렉토리에서,
시스템은 .moai/scripts/tag-manager.py 스크립트를 통해 전체 TAG 시스템을 관리해야 한다.
```

**WHERE-004**:
```
WHERE VS Code 환경에서,
시스템은 TAG 자동완성과 실시간 검증을 위한 확장 기능과 호환되어야 한다.
```

### UBIQUITOUS 항상 적용 요구사항

**UBIQUITOUS-001**:
```
UBIQUITOUS 모든 Python 파일에 대해,
시스템은 파일 상단에 최소 1개 이상의 16-Core TAG 주석을 보장해야 한다.
```

**UBIQUITOUS-002**:
```
UBIQUITOUS 모든 TAG 변경에 대해,
시스템은 구조화된 로그를 생성하고 .moai/logs/tag-changes.log에 기록해야 한다.
```

**UBIQUITOUS-003**:
```
UBIQUITOUS 모든 자동화 스크립트에 대해,
시스템은 dry-run 옵션을 제공하고 실제 변경 전 미리보기를 보여줘야 한다.
```

**UBIQUITOUS-004**:
```
UBIQUITOUS 모든 TAG 연산에 대해,
시스템은 원자적 트랜잭션을 보장하고 실패 시 완전한 롤백을 수행해야 한다.
```

## 🎯 16-Core TAG 카테고리 매핑

### Primary Tags (핵심 기능)
- **@CORE**: 핵심 엔진 및 아키텍처 (`src/moai_adk/core/`)
- **@API**: REST API 엔드포인트 (`src/moai_adk/api/`)
- **@CLI**: 명령행 인터페이스 (`src/moai_adk/cli/`)
- **@AGENT**: 에이전트 시스템 (`src/moai_adk/agents/`)

### Quality Tags (품질 관리)
- **@TEST**: 테스트 코드 및 검증 로직
- **@PERF**: 성능 최적화 관련 코드
- **@SEC**: 보안 및 권한 관리 코드
- **@DEBT**: 기술 부채 및 TODO 항목

### Tracking Tags (추적성)
- **@REQ**: 요구사항 매핑
- **@DESIGN**: 설계 문서 연결
- **@TASK**: 구현 작업 단위
- **@BUG**: 버그 수정 및 이슈

### Meta Tags (메타데이터)
- **@VERSION**: 버전 관리 및 변경 이력
- **@DOC**: 문서화 및 주석
- **@CONFIG**: 설정 및 환경 변수
- **@UTIL**: 유틸리티 및 헬퍼 함수

## 📏 품질 기준

### 커버리지 목표
- **TAG 커버리지**: Python 파일의 95% 이상
- **추적성 체인**: 요구사항-설계-구현-테스트 90% 이상 연결
- **자동 검증**: 100% 자동화된 검증 프로세스

### 성능 목표
- **인덱싱 속도**: 1000 파일 기준 5초 이내
- **검증 속도**: 전체 프로젝트 기준 10초 이내
- **메모리 사용량**: 500MB 이하 유지

### 정확성 목표
- **TAG 형식 정확성**: 99% 이상
- **중복 TAG 제거**: 100% 자동 해결
- **잘못된 매핑**: 5% 이하 유지

## 🔧 구현 요구사항

### 자동화 스크립트
1. **tag-scanner.py**: 파일 스캔 및 TAG 추출
2. **tag-validator.py**: TAG 형식 및 일관성 검증
3. **tag-indexer.py**: tags.json 인덱스 업데이트
4. **tag-repair.py**: 손상된 TAG 자동 복구

### 통합 시스템
1. **Git hooks**: pre-commit TAG 검증
2. **VS Code extension**: 실시간 TAG 지원
3. **CI/CD pipeline**: 자동화된 품질 게이트
4. **Documentation sync**: 문서 자동 동기화

### 모니터링
1. **실시간 대시보드**: TAG 상태 모니터링
2. **품질 지표**: 커버리지 및 정확성 추적
3. **성능 메트릭**: 응답시간 및 처리량 측정
4. **알림 시스템**: 오류 및 경고 알림

## 📊 성공 지표

### 정량적 지표
- Python 파일의 95% 이상에 적절한 TAG 적용
- TAG 검증 실패율 5% 이하
- 자동 복구 성공률 90% 이상
- 인덱싱 성능 5초 이내 (1000 파일 기준)

### 정성적 지표
- 개발자 워크플로우 방해 최소화
- TAG 시스템 사용 편의성 향상
- 코드 추적성 및 유지보수성 개선
- 문서와 코드 간 일관성 유지

## 🔗 관련 문서 및 의존성

### 연관 SPEC
- **SPEC-001**: 프로젝트 기본 구조 (의존)
- **SPEC-003**: 문서 동기화 시스템 (연관)
- **SPEC-004**: CI/CD 파이프라인 (연관)

### 기술 의존성
- **Python 3.11+**: 타입 힌트 및 현대적 문법 활용
- **Git hooks**: pre-commit 검증 시스템
- **JSON**: 인덱스 데이터 저장 형식
- **VS Code**: 개발 환경 통합

### 문서 연결
- `@.moai/memory/constitution.md`: 헌법 5원칙 준수
- `@.moai/memory/engineering-standards.md`: 코딩 표준
- `@.claude/memory/tdd_guidelines.md`: TDD 가이드라인

---

> **@REQ:CODE-TAG-002** 태그를 통해 이 명세가 전체 시스템과 추적됩니다.
>
> **다음 단계**: `/moai:3-plan SPEC-002`로 Constitution 검증 및 계획 수립