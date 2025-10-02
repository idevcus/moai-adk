---
name: alfred:9-update
description: MoAI-ADK 패키지 및 템플릿 업데이트 (백업 자동 생성, 설정 파일 보존)
argument-hint: [--check|--force]
tools: Read, Write, Bash, Grep, Glob
---

# 🔄 MoAI-ADK 프로젝트 업데이트

## 커맨드 개요

MoAI-ADK npm 패키지를 최신 버전으로 업데이트하고, 템플릿 파일(`.claude`, `.moai`, `CLAUDE.md`)을 안전하게 갱신합니다. 자동 백업, 설정 파일 보존, 무결성 검증을 지원합니다.

## 실행 흐름

1. **버전 확인** - 현재/최신 버전 비교
2. **백업 생성** - 타임스탬프 기반 자동 백업
3. **패키지 업데이트** - npm install moai-adk@latest
4. **템플릿 복사** - Claude Code 도구 기반 안전한 파일 복사
5. **검증** - 파일 존재 및 내용 무결성 확인

## Alfred 오케스트레이션

**실행 방식**: Alfred가 직접 실행 (전문 에이전트 위임 없음)
**예외 처리**: 오류 발생 시 `debug-helper` 자동 호출
**품질 검증**: 선택적으로 `trust-checker` 연동 가능 (--check-quality 옵션)

## 사용법

```bash
/alfred:9-update              # 업데이트 확인 및 실행
/alfred:9-update --check      # 업데이트 가능 여부만 확인
/alfred:9-update --force      # 강제 업데이트 (백업 없이)
```

## 실행 절차

### Phase 1: 버전 확인 및 검증

```bash
npm list moai-adk --depth=0   # 현재 버전
npm view moai-adk version     # 최신 버전
```

**조건부 실행**: `--check` 옵션이면 여기서 중단하고 결과만 보고

### Phase 2: 백업 생성

```bash
BACKUP_DIR=".moai-backup/$(date +%Y-%m-%d-%H-%M-%S)"
mkdir -p "$BACKUP_DIR"
cp -r .claude .moai CLAUDE.md "$BACKUP_DIR/" 2>/dev/null || true
```

**백업 구조**: `.moai-backup/YYYY-MM-DD-HH-mm-ss/{.claude, .moai, CLAUDE.md}`

**예외**: `--force` 옵션이면 건너뛰기

### Phase 3: npm 패키지 업데이트

```bash
if [ -f "package.json" ]; then
    npm install moai-adk@latest
else
    npm install -g moai-adk@latest
fi
```

### Phase 4: 템플릿 파일 복사

**복사 대상**:
```
node_modules/moai-adk/templates/
  ├── .claude/{commands,agents,output-styles,hooks}/alfred/
  ├── .moai/memory/development-guide.md
  ├── .moai/project/{product,structure,tech}.md
  └── CLAUDE.md
```

**보존 대상 (절대 덮어쓰지 않음)**:
- `.moai/specs/` - 모든 SPEC 파일
- `.moai/reports/` - 동기화 리포트
- `.moai/config.json` - 프로젝트 설정

**복사 절차**:

1. **패키지 경로 확인**: `[Bash] npm root` 또는 `npm root -g`
2. **템플릿 검증**: 템플릿 디렉토리 존재 확인
3. **파일 복사**: 각 파일 타입별로 `[Glob] → [Read] → [Write]` 패턴 적용

**공통 복사 패턴**:
```text
[Glob] {템플릿경로}/*.{md|cjs} 파일 검색
→ 각 파일마다:
  [Read] 템플릿 파일 내용
  [Write] 프로젝트 대상 경로
→ 성공 메시지 출력
```

**특수 처리**:
- **훅 파일**: 복사 후 `chmod +x` 실행 권한 부여
- **프로젝트 문서**: `[Grep]`으로 `{{PROJECT_NAME}}` 패턴 검색
  - 템플릿 상태 → 덮어쓰기
  - 사용자 수정 → 백업 후 덮어쓰기
  - 파일 없음 → 새로 생성
- **CLAUDE.md**: 프로젝트 문서와 동일한 백업 로직 적용

**오류 처리**:
- Glob 결과 없음 → 템플릿 경로 재확인
- Write 실패 → `mkdir -p` 후 재시도
- Read 실패 → 해당 파일 건너뛰고 로그 기록

### Phase 5: 업데이트 검증

**검증 항목**:

1. **파일 존재 확인** ([Glob]):
   - `.claude/{commands,agents,hooks}/alfred/` 파일 개수
   - `.moai/memory/development-guide.md`, `.moai/project/*.md`, `CLAUDE.md`

2. **내용 검증** ([Read]):
   - `development-guide.md` 버전 정보
   - `CLAUDE.md` @TAG 시스템 섹션
   - commands 파일들의 YAML frontmatter

3. **버전 확인** ([Bash]):
   ```bash
   npm list moai-adk --depth=0  # 새 버전 확인
   ```

**예상 파일 개수**:
- commands/alfred: ~10개
- agents/alfred: ~9개
- hooks/alfred: ~4개
- memory: 1개 (development-guide.md)
- project: 3개 (product, structure, tech)
- 루트: 1개 (CLAUDE.md)

**검증 실패 시**:
- 파일 누락 → Phase 4 재실행
- 버전 불일치 → Phase 3 재실행
- 내용 손상 → 백업 복원 후 재시작

**선택적 품질 검증**:
`--check-quality` 옵션 제공 시 `trust-checker` 호출하여 추가 검증 (Level 1 빠른 스캔)

## 출력 예시

```text
🔍 MoAI-ADK 업데이트 확인 중...
📦 현재: v0.0.1 → 최신: v0.0.2 ✅

💾 백업 생성: .moai-backup/2025-09-30-23-45-00/
📦 패키지 업데이트: npm install moai-adk@0.0.2 ✅

📄 템플릿 복사 중...
   ✅ .claude/commands/alfred/ (10개)
   ✅ .claude/agents/alfred/ (9개)
   ✅ .claude/hooks/alfred/ (4개)
   ✅ .moai/memory/development-guide.md
   ✅ .moai/project/*.md (3개)
   ✅ CLAUDE.md

🔍 검증 완료:
   ✅ 파일 개수 일치
   ✅ 내용 무결성 확인
   ✅ 버전 확인 (v0.0.2)

✨ 업데이트 완료! 백업: .moai-backup/2025-09-30-23-45-00/

⚠️ Claude Code 재시작 필요
롤백: moai restore --from=2025-09-30-23-45-00
```

## 안전 장치

**자동 백업**:
- `--force` 옵션 없으면 항상 백업 생성
- 백업 위치: `.moai-backup/YYYY-MM-DD-HH-mm-ss/`
- 수동 삭제 전까지 영구 보존

**충돌 방지**:
- `.moai/specs/` - 사용자 SPEC 파일 절대 건드리지 않음
- `.moai/config.json` - 프로젝트 설정 보존
- `.moai/reports/` - 동기화 리포트 보존

**롤백 지원**:
```bash
moai restore --list                       # 백업 목록
moai restore --from=2025-09-30-23-45-00  # 특정 백업 복원
moai restore --latest                     # 최근 백업 복원
```

## 핵심 오류 처리

**npm install 실패**:
- `npm cache clean --force` 후 재시도
- 인터넷 연결 및 권한 확인

**템플릿 디렉토리 없음**:
- `npm root` 경로 확인
- 패키지 재설치 (`npm install moai-adk@latest`)

**파일 복사 실패**:
- `mkdir -p {대상경로}` 디렉토리 생성
- 디스크 용량 확인 (`df -h`)

**검증 실패**:
- Phase 4 재실행 (파일 누락)
- Phase 3 재실행 (버전 불일치)
- 백업 복원 후 재시작 (내용 손상)

## 관련 명령어

- `/alfred:8-project` - 프로젝트 초기화/재설정
- `moai restore` - 백업 복원
- `moai doctor` - 시스템 진단
- `moai status` - 현재 상태 확인

## 버전 호환성

- **v0.0.x → v0.0.y**: 패치 업데이트 (완전 호환)
- **v0.0.x → v0.1.x**: 마이너 업데이트 (설정 확인 권장)
- **v0.x.x → v1.x.x**: 메이저 업데이트 (마이그레이션 가이드 필수)
