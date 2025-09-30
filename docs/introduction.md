---
title: MoAI-ADK 소개
description: TypeScript 기반 SPEC-First TDD 개발 도구
---

# MoAI-ADK 소개

> **명세 없이는 코드 없음. 테스트 없이는 구현 없음. 추적성 없이는 완성 없음.**

MoAI-ADK는 Claude Code 환경에서 **SPEC-First TDD 개발**을 자동화하는 완전한 Agentic Development Kit입니다. TypeScript 기반으로 구축되어 Python, Java, Go, Rust 등 모든 주요 프로그래밍 언어를 지원하며, 범용 개발 도구로서 일관된 개발 경험을 제공합니다.

## MoAI-ADK란?

### 해결하는 문제

현대 소프트웨어 개발에는 다음과 같은 문제들이 존재합니다:

1. **AI 페어 프로그래밍의 체계 부재**: Claude Code 같은 AI 도구를 사용하지만 일관된 방법론이 없음
2. **언어별 도구 파편화**: 각 언어마다 다른 개발 도구와 워크플로우
3. **추적성 관리의 복잡성**: 요구사항부터 코드까지 연결 고리 관리 어려움
4. **문서-코드 불일치**: 개발 진행에 따라 문서가 오래됨

### MoAI-ADK의 해결책

MoAI-ADK는 **SPEC-First TDD 자동화 프레임워크**로 다음을 제공합니다:

- **3단계 워크플로우**: SPEC 작성 → TDD 구현 → 문서 동기화
- **7개 전문 에이전트**: 각 단계를 자동화하는 AI 에이전트
- **@TAG 추적성**: 요구사항부터 구현까지 완전한 추적성
- **범용 언어 지원**: TypeScript, Python, Java, Go, Rust, C++, C#, PHP 등

## 핵심 개념 3가지

### 1. SPEC-First: 명세 없이는 코드 없음

**EARS 방법론**을 활용한 체계적인 요구사항 작성:

```markdown
### Ubiquitous Requirements
- 시스템은 사용자 인증 기능을 제공해야 한다

### Event-driven Requirements
- WHEN 사용자가 로그인하면, 시스템은 JWT 토큰을 발급해야 한다

### State-driven Requirements
- WHILE 사용자가 인증된 상태일 때, 시스템은 보호된 리소스 접근을 허용해야 한다

### Constraints
- 액세스 토큰 만료시간은 15분을 초과하지 않아야 한다
```

**왜 SPEC-First인가?**

- **명확한 계약**: 구현 전에 무엇을 만들지 정의
- **커뮤니케이션 향상**: 팀 간 공통 언어
- **변경 추적**: 요구사항 변경 이력 관리
- **AI 친화적**: Claude Code가 SPEC을 기반으로 정확히 구현

### 2. TDD-First: 테스트 없이는 구현 없음

**Red-Green-Refactor 사이클**:

```typescript
// @TEST:AUTH-001: 유효한 사용자 인증 테스트
describe('AuthService', () => {
  test('should authenticate valid user', async () => {
    // RED: 실패하는 테스트 작성
    const service = new AuthService();
    const result = await service.authenticate('user', 'pass');
    expect(result.token).toBeDefined();
  });
});

// GREEN: 최소한의 코드로 통과
class AuthService {
  async authenticate(username: string, password: string) {
    // 구현...
    return { token: 'jwt-token' };
  }
}

// REFACTOR: 품질 개선
class AuthService {
  constructor(private tokenService: TokenService) {}

  async authenticate(username: string, password: string) {
    // 리팩토링된 구현...
  }
}
```

**언어별 TDD 지원**:

- **TypeScript**: Vitest + strict typing (92.9% 성공률)
- **Python**: pytest + mypy
- **Java**: JUnit + Maven/Gradle
- **Go**: go test + table-driven tests
- **Rust**: cargo test + doc tests

### 3. TAG-First: 추적성 없이는 완성 없음

**@TAG 시스템**으로 요구사항부터 코드까지 완전한 추적성:

```typescript
// @FEATURE:AUTH-001 | Chain: @REQ:AUTH-001 → @DESIGN:AUTH-001 → @TASK:AUTH-001 → @TEST:AUTH-001
// Related: @SEC:AUTH-001, @DOCS:AUTH-001

/**
 * @API:AUTH-001: 사용자 인증 API
 */
class AuthService {
  /**
   * @SEC:AUTH-001: 입력값 보안 검증
   */
  async authenticate(username: string, password: string): Promise<AuthResult> {
    // 구현...
  }
}
```

**TAG 체계**:

- **Primary Chain**: @REQ → @DESIGN → @TASK → @TEST (필수)
- **Implementation**: @FEATURE, @API, @UI, @DATA
- **Quality**: @PERF, @SEC, @DOCS, @DEBT
- **Meta**: @OPS, @RELEASE, @DEPRECATED

## 아키텍처 다이어그램

```
MoAI-ADK Architecture
┌─────────────────────────────────────────────────┐
│         TypeScript CLI & Core Engine            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │   init   │ │  doctor  │ │  status  │  ...  │
│  └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│      Universal Language Support                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ TypeScript│ │  Python  │ │   Java   │  ...  │
│  └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│        Claude Code Integration                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │  Agents  │ │ Commands │ │   Hooks  │       │
│  └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────┘
```

## SPEC-013 전환: Python → TypeScript

### 전환 전후 비교

#### Before (Python 하이브리드)

```
복잡한 아키텍처:
MoAI-ADK (Python) ↔ TypeScript 브릿지 ↔ 사용자 프로젝트

- 15MB 패키지 크기
- 4.6초 빌드 시간
- Python + TypeScript 이중 의존성
- 하이브리드 복잡성 관리
```

#### After (TypeScript 단일 스택)

```
단순한 아키텍처:
MoAI-ADK (TypeScript) → 언어별 TDD 도구 → 사용자 프로젝트

- 195KB 패키지 크기 (99% 절감)
- 182ms 빌드 시간 (96% 개선)
- Node.js 단일 런타임
- 언어별 직접 도구 호출
```

### 주요 개선 지표

| 지표 | Before | After | 개선율 |
|------|--------|-------|--------|
| 패키지 크기 | 15MB | 195KB | 99% 절감 |
| 빌드 시간 | 4.6초 | 182ms | 96% 단축 |
| 테스트 성공률 | 80% | 92.9% | 16% 향상 |
| 메모리 사용량 | 150MB | 75MB | 50% 절감 |
| 언어 지원 | 제한적 | 8+ 언어 | 무제한 확장 |

## 핵심 통계

### 성능 지표

- ✅ **182ms** 빌드 시간 (Bun 98% 향상)
- ✅ **195KB** 패키지 크기
- ✅ **92.9%** 테스트 성공률 (Vitest)
- ✅ **94.8%** 린터 성능 향상 (Biome)

### TRUST 5원칙 준수율

- ✅ **92%** 전체 준수율 (목표 82% 대비 112% 초과 달성)
  - T (Test First): 80%
  - R (Readable): 100%
  - U (Unified): 90%
  - S (Secured): 100%
  - T (Trackable): 90%

### 언어 지원

- 🌍 **8개 주요 언어**: TypeScript, Python, Java, Go, Rust, C++, C#, PHP
- 🔧 자동 언어 감지 및 도구 매핑
- 📦 언어별 최적 테스트 프레임워크 선택

## 다음 단계

### 시작하기

1. **[설치](/getting-started/installation)**: 시스템 요구사항 확인 및 설치
2. **[빠른 시작](/getting-started/quick-start)**: 5분 안에 첫 기능 구현
3. **[프로젝트 초기화](/getting-started/project-setup)**: 프로젝트 구조 이해

### 핵심 개념 학습

1. **[SPEC-First TDD](/concepts/spec-first-tdd)**: 방법론 완전 가이드
2. **[TAG 시스템](/concepts/tag-system)**: 추적성 관리 방법
3. **[3단계 워크플로우](/concepts/workflow)**: 개발 사이클 이해
4. **[TRUST 원칙](/concepts/trust-principles)**: 품질 기준 학습

### Claude Code 통합

1. **[에이전트 가이드](/claude/agents)**: 7개 전문 에이전트 활용
2. **[워크플로우 명령어](/claude/commands)**: 5개 핵심 명령어 사용
3. **[이벤트 훅](/claude/hooks)**: 자동화 시스템 이해

## 참고 자료

- **GitHub**: [MoAI-ADK Repository](https://github.com/modu-ai/moai-adk)
- **NPM**: [@moai/adk](https://www.npmjs.com/package/@moai/adk)
- **커뮤니티**: [GitHub Discussions](https://github.com/modu-ai/moai-adk/discussions)