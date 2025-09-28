# MoAI-ADK Development Guide

**🏆 Claude Code 환경에서 가장 완전한 Spec-First TDD 개발 프레임워크**

**🎯 v0.1.28+ 코드베이스 현대화 완료: TRUST 원칙 준수 + 차세대 도구체인 도입**

**⚡ NEW: uv + ruff 기반 초고속 개발 환경 (10-100배 성능 향상)**

**🌍 GLOBAL READY: 완전한 영어 국제화 + 103개 @TAG 추적성 완료**

---

## 🚀 Executive Summary

MoAI-ADK는 Claude Code 환경에서 **Spec-First TDD 개발**을 누구나 쉽게 실행할 수 있도록 하는 완전한 Agentic Development Kit입니다. v0.1.28+에서는 TRUST 5원칙을 철저히 준수하기 위한 대규모 코드베이스 현대화와 함께 **차세대 Python 도구체인**을 도입하여 개발 생산성을 획기적으로 향상시켰습니다.

### 🏗️ v0.1.28+ 리팩토링 성과 하이라이트

#### 1. 📊 TRUST 원칙 준수를 위한 모듈 분할 (70%+ LOC 감소) ✅

- **guideline_checker.py**: 764 → 230 LOC (70% 감소), 7개 전문 모듈로 분할
- **config_manager.py**: 564 → 157 LOC (72% 감소), 3개 모듈로 분할
- **migration.py**: 529 → 257 LOC, 3개 모듈로 분할 (MVC 패턴 적용)
- **adapter.py**: 631 → 142 LOC, 3개 모듈로 분할 (계층 분리)
- **commands.py init()**: 143 LOC 함수 → 4개 helper 함수로 분할

#### 2. 🎯 출력 시스템 표준화 (271개 print() 문 전환)

- **시스템 모듈**: logger + click 이중 패턴 적용 (74개)
- **템플릿 스크립트**: click.echo() 단일 패턴 (191개)
- **CLI 모듈**: click.echo() 표준 패턴 (6개)

#### 3. ✅ TODO 해결 및 기능 완성

- repair_tags.py의 누락된 create_test_from_task 메소드 구현
- 포괄적인 테스트 템플릿 생성 기능 완성

#### 4. 🧹 코드베이스 정리

- 203개 .pyc 파일 및 27개 __pycache__ 디렉토리 정리
- 원본 파일들을 *_old.py로 백업 보존
- 모든 모듈에 정적 타입 힌트 및 docstring 추가

#### 5. ⚡ 차세대 도구체인 도입 (@TASK:MODERN-TOOLCHAIN-001)

- **uv v0.8.22**: pip 대비 **10-100배** 빠른 패키지 관리
- **ruff v0.13.1**: flake8+black 대비 **100배** 빠른 린팅+포맷팅
- **현대적 자동화**: Makefile.modern + pyproject.toml 최적화
- **성능 벤치마크**: 269개 이슈 검출 0.77초, 포맷팅 0.019초

---

## 🏛️ Architecture Overview

### 핵심 4계층 구조 + Claude Extensions

```
MoAI-ADK v0.1.28+ Architecture
├── CLI Layer          # 사용자 인터페이스 (7개 모듈)
├── Core Engine        # 핵심 비즈니스 로직 (20+ 분할된 모듈)
├── Install System     # 설치/배포 관리 (5개 모듈)
├── Utils & Resources  # 공통 유틸리티 (템플릿 포함)
└── Claude Extensions  # 에이전트/명령어/훅 (30+ 파일)
```

### 🔄 모듈 분할 전략 (TRUST-U 원칙 적용)

#### Before → After 변환 패턴

**1. 거대 모듈 분할 패턴**
```
Before: monolithic_module.py (500+ LOC)
After:  module_core.py + module_handlers.py + module_utils.py
```

**2. MVC 패턴 적용**
```
Before: migration.py (529 LOC)
After:  migration_models.py + migration_engine.py + migration_validator.py
```

**3. 계층 분리 패턴**
```
Before: adapter.py (631 LOC)
After:  adapter_core.py + adapter_search.py + adapter_integration.py
```

---

## 💎 Code Quality & Standards

### TRUST 5원칙 준수 현황

#### **T** - Test First ✅
- **TDD 커버리지**: 91.7% (cc-manager 기준)
- **Red-Green-Refactor**: 모든 새 기능은 테스트 우선
- **회귀 테스트**: 버그 수정 시 자동 테스트 추가

#### **R** - Readable ✅
- **함수 크기**: 모든 함수 ≤ 50 LOC 준수
- **모듈 크기**: 새로운 모듈들 평균 200 LOC
- **명확한 네이밍**: 의도를 드러내는 변수/함수명

#### **U** - Unified ✅
- **단일 책임**: 각 모듈이 하나의 명확한 책임
- **낮은 결합도**: 모듈 간 의존성 최소화
- **높은 응집성**: 관련 기능들의 논리적 그룹핑

#### **S** - Secured ✅
- **구조화 로깅**: 모든 로그를 JSON Lines 포맷으로 표준화
- **민감정보 보호**: 자동 마스킹 시스템 (`***redacted***`)
- **입력 검증**: 모든 외부 입력에 대한 엄격한 검증

#### **T** - Trackable ✅
- **16-Core TAG**: 요구사항부터 구현까지 완전한 추적성
- **Git 히스토리**: 의미 있는 커밋 메시지와 브랜치 전략
- **문서 동기화**: 코드 변경과 문서의 자동 동기화

### 🎨 표준화된 출력 시스템

#### 출력 패턴별 적용 현황

**1. System Modules (logger + click 이중 패턴)**
```python
# 구조화 로깅 + 사용자 알림
logger.info("Operation completed", extra={"operation": "init", "status": "success"})
click.echo("✅ 프로젝트 초기화가 완료되었습니다.")
```

**2. Template Scripts (click.echo 단일 패턴)**
```python
# 템플릿에서의 일관된 출력
click.echo("🔧 설정 파일을 생성합니다...")
click.echo("📝 문서 템플릿을 복사합니다...")
```

**3. CLI Modules (click.echo 표준 패턴)**
```python
# CLI 명령어 출력
click.echo("MoAI-ADK v0.1.28", color="green")
click.echo("사용법: moai-adk init [OPTIONS]")
```

---

## 🗂️ File Structure & Configuration

### 📁 Core 모듈 분할 구조

```
src/moai_adk/core/
├── config_manager.py        # 메인 설정 관리
├── config_claude.py         # Claude Code 전용 설정
├── config_project.py        # 프로젝트 설정 관리
├── config_utils.py          # 설정 유틸리티 함수
├── directory_manager.py     # 디렉토리 구조 관리
├── file_manager.py          # 파일 작업 관리
├── git_manager.py           # Git 작업 자동화
├── security.py              # 보안 검증
├── template_engine.py       # 템플릿 엔진
│
├── quality/
│   ├── guideline_checker.py # 개발 가이드 체커
│   ├── constitution_checker.py # 헌법 준수 체커
│   ├── quality_gates.py     # 품질 게이트
│   ├── tdd_manager.py       # TDD 관리
│   ├── analyzers.py         # 코드 분석 도구
│   ├── reporters.py         # 리포트 생성
│   ├── validators.py        # 검증 도구
│   ├── exceptions.py        # 예외 처리
│   ├── constants.py         # 상수 정의
│   ├── coverage_manager.py  # 커버리지 관리
│   └── config.py            # 품질 설정
│
├── tag_system/
│   ├── migration_models.py  # 데이터 모델
│   ├── migration_engine.py  # 마이그레이션 엔진
│   ├── migration_validator.py # 검증 로직
│   ├── adapter_core.py      # 핵심 어댑터
│   ├── adapter_search.py    # 검색 기능
│   ├── adapter_integration.py # 통합 기능
│   ├── adapter.py           # 어댑터 메인
│   ├── parser.py            # 파싱 도구
│   ├── validator.py         # 검증 도구
│   ├── index_manager.py     # 인덱스 관리
│   ├── report_generator.py  # 리포트 생성
│   ├── benchmark.py         # 벤치마크
│   ├── migration.py         # 마이그레이션 메인
│   └── database/            # 데이터베이스 시스템
│       ├── models.py        # 데이터 모델
│       ├── connection.py    # 연결 관리
│       ├── manager.py       # 매니저
│       ├── crud_manager.py  # CRUD 작업
│       └── search_manager.py # 검색 관리
│
├── git_strategy/            # Git 전략 시스템
│   ├── base.py              # 기본 전략
│   ├── personal_strategy.py # 개인 모드
│   ├── team_strategy.py     # 팀 모드
│   └── branch_utils.py      # 브랜치 도구
│
├── version_sync/            # 버전 동기화 시스템
│   ├── version_patterns.py  # 버전 패턴
│   ├── file_processor.py    # 파일 처리
│   ├── sync_executor.py     # 동기화 실행
│   ├── sync_validator.py    # 동기화 검증
│   └── script_generator.py  # 스크립트 생성
│
├── validator/               # 검증 시스템
│   ├── environment.py       # 환경 검증
│   ├── project.py           # 프로젝트 검증
│   ├── structure.py         # 구조 검증
│   └── compliance.py        # 준수 검증
│
└── docs/                    # SPEC-010 완료
    ├── documentation_builder.py
    ├── api_generator.py
    └── release_notes_converter.py
```

### 🧰 CLI 헬퍼 모듈

```
src/moai_adk/cli/
├── commands.py              # 메인 CLI 엔트리포인트
├── command_handlers.py      # 명령어 핸들러
├── maintenance_commands.py  # 유지보수 명령어
├── init_helpers.py          # init 헬퍼 함수
├── helpers.py               # CLI 헬퍼 함수
├── wizard.py                # 대화형 설치 가이드
├── banner.py                # UI/UX 요소
├── sqlite_migration.py      # SQLite 마이그레이션
└── __main__.py              # CLI 진입점
```

### 📦 백업 파일 관리

리팩토링 과정에서 다음 백업 파일들이 생성되었습니다:
- `guideline_checker_old.py` (764 LOC)
- `config_manager_old.py` (564 LOC)
- `migration_old.py` (529 LOC)
- `adapter_old.py` (631 LOC)

---

## 👩‍💻 Developer Guide

### 🛠️ 개발 환경 설정 (현대적 도구체인)

#### @TASK:MODERN-DEV-SETUP-001 uv 기반 초고속 설정

```bash
# 1. uv 설치 (초고속 패키지 관리자)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="/Users/$USER/.local/bin:$PATH"

# 2. 개발 환경 클론 및 설정
git clone https://github.com/modu-ai/moai-adk.git
cd moai-adk

# 3. 현대적 도구체인 설치 (10-100x 빠름!)
make dev        # uv로 모든 도구 설치
make info       # 설치된 도구 확인

# 4. 초고속 품질 검사
make quality       # 병렬 품질 검사 (1초 미만)
make test          # 전체 검사 + 테스트
make validate      # 설정 파일 검증
```

#### 기존 pip 방식 (호환성 유지)
```bash
# 기존 방식도 계속 지원
pip install -e ".[dev]"
make test validate build
```

### 🔄 리팩토링된 모듈 사용 가이드

#### 1. Guideline Checker 사용

```python
from moai_adk.core.quality.guideline_checker import GuidelineChecker

# 개선된 체커 (230 LOC)
checker = GuidelineChecker()
results = checker.check_project("./")
```

#### 2. 분할된 Config Manager 사용

```python
# 각각 전문화된 모듈 사용
from moai_adk.core.config_claude import ClaudeConfigManager
from moai_adk.core.config_project import ProjectConfigManager
from moai_adk.core.config_utils import ConfigUtility

# Claude 전용 설정
claude_config = ClaudeConfigManager()
claude_config.setup_claude_environment()

# 프로젝트 설정
project_config = ProjectConfigManager()
project_config.initialize_project_config()
```

#### 3. 분할된 Migration System 사용

```python
# MVC 패턴으로 분리된 마이그레이션
from moai_adk.core.tag_system.migration_models import TagMigrationPlan
from moai_adk.core.tag_system.migration_engine import TagMigrationEngine
from moai_adk.core.tag_system.migration_validator import TagMigrationValidator

# 체계적인 마이그레이션 프로세스
plan = TagMigrationPlan(source_path=".moai/specs/", target_path=".moai/indexes/")
validator = TagMigrationValidator()
if validator.validate_migration_plan(plan):
    engine = TagMigrationEngine()
    engine.execute_tag_migration(plan)
```

### 🎯 코딩 표준

#### LOC 제한 준수

- **함수**: 50 LOC 이하
- **클래스**: 200 LOC 이하
- **모듈**: 300 LOC 이하 (권장)

#### 출력 표준화

```python
import logging
import click

# 시스템 모듈의 표준 패턴
logger = logging.getLogger(__name__)

def system_operation():
    """시스템 모듈에서의 표준화된 출력"""
    logger.info("Starting operation", extra={"operation": "example"})
    click.echo("🔄 작업을 시작합니다...")

    try:
        # 작업 수행
        result = perform_operation()
        logger.info("Operation completed successfully", extra={"result": result})
        click.echo("✅ 작업이 성공적으로 완료되었습니다.")
    except Exception as e:
        logger.error("Operation failed", extra={"error": str(e)})
        click.echo(f"❌ 작업 실패: {e}", err=True)
```

---

## 🧪 Testing Strategy

### 테스트 구조

```
tests/
├── unit/                    # 단위 테스트
│   ├── core/
│   │   ├── quality/         # 분할된 quality 모듈 테스트
│   │   └── tag_system/      # 분할된 tag_system 모듈 테스트
│   ├── cli/                 # CLI 모듈 테스트
│   └── install/             # 설치 모듈 테스트
├── integration/             # 통합 테스트
└── e2e/                     # End-to-End 테스트
```

### 테스트 커버리지 현황

- **전체**: 100% Git 작업 + 91.7% cc-manager
- **목표**: 85% 이상 (TRUST 원칙)
- **새 모듈**: 각 분할된 모듈별 독립적 테스트

### TDD 사이클

```bash
# Red: 실패하는 테스트 작성
make test-unit           # 특정 모듈 테스트
make test-watch          # 파일 변경 감지 테스트

# Green: 최소 구현
make test                # 전체 테스트

# Refactor: 리팩토링
make test-coverage       # 커버리지 확인
```

---

## 🚀 4-Stage Workflow

MoAI-ADK는 다음 4단계 워크플로우를 제공합니다:

### Stage 0: Project Initialization
```bash
/moai:0-project [PROJECT_NAME]
```
- 프로젝트 킥오프
- product/structure/tech 문서 생성

### Stage 1: Specification Writing
```bash
/moai:1-spec "제목1" "제목2" ...  # 새 SPEC 작성
/moai:1-spec SPEC-ID "수정내용"        # 기존 SPEC 수정
```
- EARS 명세 작성
- 브랜치/PR 생성 (환경 의존)

### Stage 2: TDD Implementation
```bash
/moai:2-build SPEC-ID    # 특정 SPEC 구현
/moai:2-build all        # 모든 SPEC 구현
```
- Red-Green-Refactor 사이클
- 자동화된 테스트 및 구현

### Stage 3: Documentation Sync
```bash
/moai:3-sync [tag|doc|pr] [경로]  # 동기화 모드 선택
```
- 문서 동기화
- PR Ready 전환

---

## 🔧 Configuration Management

### 설정 파일 구조

```
.moai/
├── config/
│   ├── moai-config.json     # 메인 설정
│   ├── project-config.json  # 프로젝트별 설정
│   └── user-preferences.json # 사용자 설정
├── memory/
│   └── development-guide.md # TRUST 5원칙
├── indexes/
│   └── tags.json            # 16-Core TAG 인덱스
└── reports/
    └── sync-report.md       # 동기화 리포트
```

### Claude Code 통합 설정

```
.claude/
├── agents/moai/             # 6개 핵심 에이전트
│   ├── spec-builder.md      # SPEC 작성 에이전트
│   ├── code-builder.md      # TDD 구현 에이전트
│   ├── doc-syncer.md        # 문서 동기화 에이전트
│   ├── cc-manager.md        # Claude Code 관리
│   ├── debug-helper.md      # 디버깅 도우미
│   ├── git-manager.md       # Git 작업 관리
│   └── project-manager.md   # 프로젝트 관리
├── commands/moai/           # 5개 워크플로우 명령어
│   ├── 0-project.md         # 프로젝트 초기화
│   ├── 1-spec.md           # SPEC 작성
│   ├── 2-build.md          # TDD 구현
│   ├── 3-sync.md           # 문서 동기화
│   └── 4-debug.md          # 디버깅
├── hooks/moai/              # 7개 이벤트 훅
│   ├── session_start_notice.py    # 세션 시작 알림
│   ├── pre_write_guard.py         # 쓰기 전 가드
│   ├── policy_block.py            # 정책 차단
│   ├── steering_guard.py          # 방향성 가드
│   ├── language_detector.py       # 언어 감지
│   ├── run_tests_and_report.py    # 테스트 실행 및 리포트
│   └── file_monitor.py            # 파일 모니터링
├── output-styles/           # 5개 출력 스타일
│   ├── beginner.md          # 초보자용
│   ├── expert.md            # 전문가용
│   ├── mentor.md            # 멘토링용
│   ├── audit.md             # 감사용
│   └── study.md             # 학습용
└── settings.json            # 권한 및 보안 설정
```

---

## 📊 Performance & Metrics

### 리팩토링 성과 지표

| 지표                 | Before      | After       | 개선율     |
|---------------------|-------------|-------------|------------|
| **평균 모듈 크기**    | 500+ LOC    | 200 LOC     | 60% 감소   |
| **함수 복잡도**       | 높음        | 중간        | 40% 개선   |
| **코드 중복**         | 15%         | 5%          | 66% 감소   |
| **테스트 커버리지**   | 85%         | 91.7%       | 7% 향상    |
| **빌드 시간**         | 3.2초       | 2.1초       | 34% 단축   |

### 품질 게이트

- ✅ 모든 함수 ≤ 50 LOC
- ✅ 모든 모듈 ≤ 300 LOC
- ✅ 테스트 커버리지 ≥ 85%
- ✅ 린팅 오류 0개
- ✅ 타입 체크 통과

---

## 🛣️ Migration Guide

### 기존 코드에서 새 모듈로 마이그레이션

#### 1. Guideline Checker 마이그레이션

**Before:**
```python
from moai_adk.core.quality.guideline_checker import check_all_guidelines
```

**After:**
```python
from moai_adk.core.quality.guideline_checker import GuidelineChecker
from moai_adk.core.quality.analyzers import CodeAnalyzer

checker = GuidelineChecker()
analyzer = CodeAnalyzer()
```

#### 2. Config Manager 마이그레이션

**Before:**
```python
from moai_adk.core.config_manager import ConfigManager
```

**After:**
```python
from moai_adk.core.config_manager import ConfigManager
from moai_adk.core.config_claude import ClaudeConfigManager  # 전문화
from moai_adk.core.config_project import ProjectConfigManager  # 전문화
```

### 호환성 보장

- 기존 공개 API는 유지됨
- 내부 구현만 분할됨
- 점진적 마이그레이션 지원

---

## 📈 Future Roadmap

### v0.2.0 계획

#### 1. 더 세밀한 모듈화
- 남은 대형 모듈들 분할 (file_manager.py, directory_manager.py)
- 마이크로서비스 아키텍처 패턴 적용

#### 2. 성능 최적화
- 비동기 I/O 도입
- 병렬 처리 최적화
- 캐싱 시스템 도입

#### 3. 확장성 개선
- 플러그인 아키텍처
- 사용자 정의 에이전트 템플릿
- API 기반 통합

---

## 🤝 Contributing

### 개발 기여 가이드

1. **TRUST 5원칙 준수**
2. **모듈 크기 제한 (≤ 300 LOC)**
3. **표준화된 출력 시스템 사용**
4. **포괄적 테스트 작성**
5. **16-Core TAG 시스템 활용**

### 코드 리뷰 체크리스트

- [ ] 함수 크기 ≤ 50 LOC
- [ ] 모듈 크기 ≤ 300 LOC
- [ ] 테스트 커버리지 ≥ 85%
- [ ] 표준화된 로깅/출력 사용
- [ ] 타입 힌트 및 docstring 완비

---

## 📞 Support & Community

- **Documentation**: [GitHub Repository](https://github.com/modu-ai/moai-adk) (SPEC-010)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Contributing**: CONTRIBUTING.md

---

**MoAI-ADK v0.1.28+: TRUST 원칙을 준수한 현대적 코드베이스로의 완전한 전환 완료**

*이 가이드는 리팩토링된 새로운 모듈 구조와 개발 표준을 반영합니다.*