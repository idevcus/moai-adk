---
title: 이벤트 훅
description: 8개 자동화 훅으로 개발 프로세스 보호
---

# 이벤트 훅

MoAI-ADK는 개발 프로세스를 자동으로 보호하고 가이드하는 **8개 이벤트 훅**을 제공합니다. TypeScript로 빌드되어 고성능으로 실행됩니다.

## 훅 개요

### 전체 훅 목록

| 훅 | 이벤트 | 주요 기능 | 자동 실행 |
|---|--------|-----------|-----------|
| **file-monitor** | 파일 변경 | 파일 모니터링 및 로깅 | ✅ |
| **language-detector** | 세션 시작 | 언어 자동 감지 | ✅ |
| **policy-block** | 명령 실행 전 | 정책 위반 차단 | ✅ |
| **pre-write-guard** | 파일 쓰기 전 | 파일 검증 및 백업 | ✅ |
| **session-notice** | 세션 시작 | 개발 가이드 안내 | ✅ |
| **steering-guard** | 주기적 | 방향성 가이드 | ✅ |
| **run-tests-and-report** | 코드 변경 후 | 테스트 자동 실행 | 선택 |
| **claude-code-monitor** | 주기적 | Claude Code 상태 감시 | ✅ |

### 훅 위치

```
.claude/hooks/moai/
├── file-monitor.js
├── language-detector.js
├── policy-block.js
├── pre-write-guard.js
├── session-notice.js
├── steering-guard.js
├── run-tests-and-report.js
└── claude-code-monitor.js
```

## 1. file-monitor

### 목적

**파일 변경 모니터링 및 로깅**

코드 파일 변경을 실시간으로 추적하고 로그에 기록합니다.

### 동작 방식

```javascript
// .claude/hooks/moai/file-monitor.js

/**
 * @HOOK:FILE-MONITOR-001
 * 파일 변경 이벤트 모니터링
 */
export function onFileChange(event) {
  const { path, action } = event;

  // Winston logger로 기록
  logger.info('File changed', {
    path,
    action, // 'create' | 'modify' | 'delete'
    timestamp: new Date().toISOString(),
    user: process.env.USER
  });

  // TAG 파일 변경 감지
  if (isSourceFile(path)) {
    checkTagPresence(path);
  }

  // 민감 파일 변경 경고
  if (isSensitiveFile(path)) {
    logger.warn('Sensitive file modified', { path });
  }
}
```

### 모니터링 대상

#### 소스 코드 파일

```
감지 대상:
- src/**/*.ts
- src/**/*.js
- src/**/*.py
- src/**/*.java
- src/**/*.go
- __tests__/**/*

로그 내용:
- 파일 경로
- 변경 종류 (생성/수정/삭제)
- 타임스탬프
- TAG 존재 여부
```

#### 설정 파일

```
감지 대상:
- .moai/config.json
- .claude/settings.json
- package.json
- tsconfig.json

로그 내용:
- 변경 전후 diff
- 설정 검증 결과
```

### 로그 예시

```json
{
  "level": "info",
  "message": "File changed",
  "path": "src/auth/service.ts",
  "action": "modify",
  "hasTag": true,
  "tagId": "AUTH-001",
  "timestamp": "2024-01-15T14:30:45.123Z"
}
```

## 2. language-detector

### 목적

**프로젝트 언어 자동 감지**

세션 시작 시 프로젝트의 주 언어를 감지하고 적절한 도구를 추천합니다.

### 동작 방식

```javascript
/**
 * @HOOK:LANGUAGE-DETECTOR-001
 * 세션 시작 시 언어 자동 감지
 */
export function onSessionStart() {
  const languages = detectLanguages();

  logger.info('Languages detected', {
    languages,
    primary: languages[0]
  });

  // 도구 추천
  const tools = recommendTools(languages[0]);

  console.log(`
Detected Languages:
  - ${languages.map(l => `${l.name}: ${l.percentage}%`).join('\n  - ')}

Recommended Tools:
  - Test: ${tools.test}
  - Lint: ${tools.lint}
  - Format: ${tools.format}
  `);
}
```

### 감지 패턴

#### JavaScript/TypeScript

```
감지 파일:
- package.json
- tsconfig.json
- *.ts, *.tsx, *.js, *.jsx

도구 추천:
- Test: Vitest
- Lint: Biome
- Format: Biome
- Build: tsup
```

#### Python

```
감지 파일:
- requirements.txt
- pyproject.toml
- setup.py
- *.py

도구 추천:
- Test: pytest
- Lint: ruff
- Format: black
- Type: mypy
```

#### Java

```
감지 파일:
- pom.xml
- build.gradle
- *.java

도구 추천:
- Test: JUnit
- Build: Maven/Gradle
- Format: Google Java Format
```

### 출력 예시

```
✓ Language Detection
  - TypeScript: 65%
  - Python: 25%
  - Go: 10%

Primary Language: TypeScript

Recommended Tools:
  - Test Runner: Vitest
  - Linter: Biome
  - Formatter: Biome
  - Build Tool: tsup

Run 'moai doctor' for detailed diagnostics.
```

## 3. policy-block

### 목적

**정책 위반 차단**

위험한 명령어나 패턴을 자동으로 차단합니다.

### 동작 방식

```javascript
/**
 * @HOOK:POLICY-BLOCK-001
 * 정책 위반 명령어 차단
 */
export function onCommandExecute(command) {
  const blockedPatterns = [
    /rm\s+-rf/,           // 강제 삭제
    /sudo/,               // 관리자 권한
    /chmod\s+777/,        // 전체 권한
    /--force/,            // 강제 실행
    /DROP\s+TABLE/i       // SQL 삭제
  ];

  for (const pattern of blockedPatterns) {
    if (pattern.test(command)) {
      logger.warn('Blocked command', { command, pattern });

      throw new PolicyViolationError(
        `Command blocked by security policy: ${command}\n` +
        `Pattern: ${pattern}\n` +
        `If you need to run this, use git-manager with approval.`
      );
    }
  }
}
```

### 차단 대상

#### 파일 시스템

```
차단 명령어:
- rm -rf /
- rm -rf *
- sudo rm

허용 방법:
- 사용자 확인 필요
- @agent-git-manager로 요청
```

#### Git 작업

```
차단 명령어:
- git push --force
- git reset --hard
- git branch -D main

허용 방법:
- @agent-git-manager로 요청
- 사용자 명시적 승인
```

#### 데이터베이스

```
차단 명령어:
- DROP TABLE
- TRUNCATE TABLE
- DELETE without WHERE

허용 방법:
- 마이그레이션 스크립트 사용
- 사용자 승인
```

### 차단 예시

```
❌ Command Blocked

Command: rm -rf node_modules/
Reason: Potentially destructive operation
Policy: File deletion requires confirmation

Recommendation:
  Use: @agent-git-manager "clean node_modules"

This ensures:
  ✓ Backup before deletion
  ✓ User confirmation
  ✓ Audit logging
```

## 4. pre-write-guard

### 목적

**파일 쓰기 전 검증 및 백업**

파일을 쓰기 전에 검증하고 자동 백업을 생성합니다.

### 동작 방식

```javascript
/**
 * @HOOK:PRE-WRITE-GUARD-001
 * 파일 쓰기 전 검증
 */
export async function onBeforeWrite(file) {
  // 1. 파일 존재 확인
  if (existsSync(file.path)) {
    // 백업 생성
    await createBackup(file.path);
    logger.info('Backup created', { path: file.path });
  }

  // 2. TAG BLOCK 확인 (소스 파일)
  if (isSourceFile(file.path) && !hasTagBlock(file.content)) {
    logger.warn('Missing TAG BLOCK', { path: file.path });

    const suggestion = generateTagBlock(file.path);
    console.warn(`
⚠️  Missing TAG BLOCK in ${file.path}

Suggested TAG BLOCK:
${suggestion}

Add this to the top of your file.
    `);
  }

  // 3. TRUST 원칙 검증
  const violations = checkTrustViolations(file.content);
  if (violations.length > 0) {
    logger.warn('TRUST violations detected', { path: file.path, violations });

    console.warn(`
⚠️  TRUST Violations in ${file.path}

${violations.map(v => `- ${v.rule}: ${v.message}`).join('\n')}

Consider fixing these before committing.
    `);
  }

  // 4. 민감정보 검사
  const secrets = detectSecrets(file.content);
  if (secrets.length > 0) {
    throw new SecurityError(
      `Sensitive information detected in ${file.path}\n` +
      `Found: ${secrets.join(', ')}\n` +
      `Use environment variables instead.`
    );
  }
}
```

### 검증 항목

#### TAG BLOCK 존재

```typescript
// ✅ Good
// @FEATURE:AUTH-001 | Chain: @REQ → @DESIGN → @TASK → @TEST
export class AuthService {
  // ...
}

// ❌ Bad (경고 발생)
export class AuthService {
  // TAG BLOCK 없음
}
```

#### TRUST 원칙

```typescript
// ✅ Good: 함수 ≤50 LOC
function authenticate(email, password) {
  // 45 LOC
}

// ❌ Bad: 함수 >50 LOC (경고)
function processOrder(order) {
  // 65 LOC - 리팩토링 필요
}
```

#### 민감정보

```typescript
// ❌ Bad: 하드코딩된 비밀 (차단)
const apiKey = 'sk_live_abc123';
const password = 'mypassword';

// ✅ Good: 환경 변수
const apiKey = process.env.API_KEY;
const password = process.env.DB_PASSWORD;
```

### 백업 시스템

```
백업 위치: .moai/backups/
백업 형식: {filename}.{timestamp}.bak

예시:
  service.ts
  → .moai/backups/service.ts.20240115-143045.bak

보관 기간: 7일
자동 정리: 매일 자정
```

## 5. session-notice

### 목적

**세션 시작 안내**

Claude Code 세션 시작 시 개발 가이드를 표시합니다.

### 동작 방식

```javascript
/**
 * @HOOK:SESSION-NOTICE-001
 * 세션 시작 알림
 */
export function onSessionStart() {
  const projectName = readProjectName();
  const mode = readConfig().mode;

  console.log(`
🗿 MoAI-ADK v0.0.1

Project: ${projectName}
Mode: ${mode}

3-Stage Workflow:
  /moai:1-spec  → SPEC 작성
  /moai:2-build → TDD 구현
  /moai:3-sync  → 문서 동기화

On-Demand Support:
  @agent-debug-helper "오류내용"

TRUST 5 Principles:
  ✓ Test First
  ✓ Readable
  ✓ Unified
  ✓ Secured
  ✓ Trackable

Run '/moai:help' for more information.
  `);
}
```

### 표시 내용

```
프로젝트 정보:
- 프로젝트명
- 모드 (Personal/Team)
- 버전

핵심 명령어:
- 3단계 워크플로우
- 에이전트 호출 방법
- TRUST 5원칙

다음 단계:
- 첫 SPEC 작성
- 도움말 확인
```

## 6. steering-guard

### 목적

**개발 방향성 가이드**

주기적으로 개발 방향을 체크하고 가이드합니다.

### 동작 방식

```javascript
/**
 * @HOOK:STEERING-GUARD-001
 * 개발 방향성 가이드 (30분마다)
 */
export function onPeriodic() {
  const status = analyzeProjectStatus();

  // 장시간 Draft SPEC 경고
  if (status.draftSpecs.length > 0) {
    const oldDrafts = status.draftSpecs.filter(s =>
      isOlderThan(s.createdAt, '2 hours')
    );

    if (oldDrafts.length > 0) {
      console.warn(`
⚠️  Draft SPECs Pending

${oldDrafts.map(s => `- ${s.id}: ${s.title} (${s.age})`).join('\n')}

Next Step:
  /moai:2-build ${oldDrafts[0].id}
      `);
    }
  }

  // 구현 완료, 동기화 필요
  if (status.needsSync) {
    console.info(`
ℹ️  Documentation Sync Needed

${status.modifiedFiles.length} files modified
${status.newTags.length} new TAGs detected

Next Step:
  /moai:3-sync
    `);
  }

  // 테스트 실패 경고
  if (status.failingTests > 0) {
    console.warn(`
⚠️  ${status.failingTests} Test(s) Failing

Run tests:
  npm test

Debug:
  @agent-debug-helper "테스트 실패 분석"
    `);
  }
}
```

### 체크 항목

- Draft SPEC 방치 여부
- 문서 동기화 필요 여부
- 테스트 실패 상태
- TRUST 준수율 하락
- TAG 체인 불완전

## 7. run-tests-and-report

### 목적

**테스트 자동 실행 및 리포트**

코드 변경 후 자동으로 테스트를 실행합니다 (선택적).

### 동작 방식

```javascript
/**
 * @HOOK:RUN-TESTS-001
 * 코드 변경 후 테스트 자동 실행
 */
export async function onCodeChange(files) {
  // 설정 확인
  if (!config.autoTest) {
    return; // 자동 테스트 비활성화됨
  }

  const affectedTests = findAffectedTests(files);

  console.log(`
Running ${affectedTests.length} test(s)...
  `);

  const result = await runTests(affectedTests);

  if (result.success) {
    console.log(`
✓ All Tests Passed

  Total: ${result.total}
  Passed: ${result.passed}
  Duration: ${result.duration}ms
    `);
  } else {
    console.error(`
✗ ${result.failed} Test(s) Failed

${result.failures.map(f => `
  ${f.test}
  ${f.error}
`).join('\n')}

Debug:
  @agent-debug-helper "테스트 실패"
    `);
  }
}
```

### 설정

```json
// .moai/config.json
{
  "hooks": {
    "runTestsAndReport": {
      "enabled": true,
      "autoTest": false,      // 자동 실행 비활성화 (기본값)
      "onSave": false,
      "onCommit": true        // 커밋 전에만 실행
    }
  }
}
```

## 8. claude-code-monitor

### 목적

**Claude Code 상태 감시**

Claude Code의 상태를 주기적으로 확인합니다.

### 동작 방식

```javascript
/**
 * @HOOK:CLAUDE-MONITOR-001
 * Claude Code 상태 감시 (5분마다)
 */
export function onPeriodic() {
  const status = checkClaudeCodeStatus();

  // 메모리 사용량 경고
  if (status.memory > 80) {
    console.warn(`
⚠️  High Memory Usage: ${status.memory}%

Recommendation:
  Restart Claude Code session
    `);
  }

  // 응답 속도 저하
  if (status.responseTime > 5000) {
    console.warn(`
⚠️  Slow Response Time: ${status.responseTime}ms

Recommendation:
  Check system resources
    `);
  }

  // 에이전트 오류
  if (status.agentErrors > 0) {
    console.error(`
✗ ${status.agentErrors} Agent Error(s) Detected

Debug:
  @agent-debug-helper "에이전트 오류"
    `);
  }
}
```

## 훅 커스터마이징

### 훅 활성화/비활성화

```json
// .claude/settings.json
{
  "hooks": {
    "enabled": true,
    "individual": {
      "file-monitor": true,
      "language-detector": true,
      "policy-block": true,
      "pre-write-guard": true,
      "session-notice": true,
      "steering-guard": false,    // 비활성화
      "run-tests-and-report": false,
      "claude-code-monitor": true
    }
  }
}
```

### 커스텀 훅 추가

```javascript
// .claude/hooks/moai/custom-hook.js

/**
 * @HOOK:CUSTOM-001
 * 커스텀 훅 예시
 */
export function onCustomEvent(data) {
  // 커스텀 로직
  logger.info('Custom hook triggered', { data });
}
```

### 훅 순서 조정

```json
// .claude/settings.json
{
  "hooks": {
    "order": [
      "session-notice",       // 가장 먼저
      "language-detector",
      "policy-block",
      "pre-write-guard",
      "file-monitor",
      "steering-guard",
      "run-tests-and-report",
      "claude-code-monitor"   // 가장 나중
    ]
  }
}
```

## 트러블슈팅

### 훅이 실행되지 않음

```bash
# 1. 훅 활성화 확인
cat .claude/settings.json | jq '.hooks.enabled'

# 2. 훅 파일 존재 확인
ls -la .claude/hooks/moai/

# 3. 권한 확인
chmod +x .claude/hooks/moai/*.js

# 4. Claude Code 재시작
```

### 훅 오류 디버깅

```bash
# 훅 로그 확인
cat .moai/logs/hooks.log

# 특정 훅 테스트
node .claude/hooks/moai/pre-write-guard.js
```

## 다음 단계

### 에이전트 활용

- **[에이전트 가이드](/claude/agents)**: 7개 에이전트
- **[명령어](/claude/commands)**: 워크플로우 명령어

### 고급 설정

- **[커스텀 에이전트](/advanced/custom-agents)**: 에이전트 생성
- **[설정 파일](/reference/configuration)**: 전체 설정 옵션

## 참고 자료

- **훅 소스**: `.claude/hooks/moai/`
- **설정 파일**: `.claude/settings.json`
- **로그 파일**: `.moai/logs/hooks.log`