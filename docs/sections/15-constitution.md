# MoAI-ADK 개발 가이드 거버넌스

## 🚦 개발 가이드 5원칙

MoAI-ADK의 품질 거버넌스는 개발 가이드 5원칙을 기반으로 합니다.

### 1. Simplicity First
**원칙**: 프로젝트 복잡도를 최소화

**검증 항목**:
- 컴포넌트 개수 ≤ 10개
- 의존성 깊이 ≤ 3단계
- 설정 파일 개수 ≤ 5개

**위반 시 조치**:
```bash
❌ 복잡도 초과 감지
🔧 제안: 컴포넌트 병합 또는 분리
📋 ADR 작성 필요
```

### 2. Test-Driven Development
**원칙**: RED-GREEN-REFACTOR 사이클 강제

**검증 항목**:
- 테스트 커버리지 ≥ 80%
- 모든 기능은 테스트 우선 작성
- 실패하는 테스트부터 시작

**위반 시 조치**:
```bash
❌ 테스트 없는 코드 감지
🚫 구현 차단
📝 테스트 케이스 작성 요구
```

### 3. Living Documentation
**원칙**: 코드와 문서의 실시간 동기화

**검증 항목**:
- 모든 API는 문서화
- @TAG 추적성 100%
- 변경 시 자동 문서 업데이트

**위반 시 조치**:
```bash
❌ 문서 동기화 누락 감지
🔄 자동 동기화 실행
📋 누락 문서 생성
```

### 4. Observable by Default
**원칙**: 모든 시스템은 관찰 가능해야 함

**검증 항목**:
- 구조화된 로깅
- 메트릭 수집
- 에러 추적

**위반 시 조치**:
```bash
❌ 로깅 누락 감지
📊 로깅 코드 자동 추가
🔍 모니터링 설정 제안
```

### 5. Version Everything
**원칙**: 모든 변경사항은 버전 관리

**검증 항목**:
- Git 커밋 메시지 규칙 준수
- CHANGELOG 자동 업데이트
- 시맨틱 버저닝

**위반 시 조치**:
```bash
❌ 버전 관리 규칙 위반
📝 올바른 커밋 메시지 제안
🏷️ 태그 생성 안내
```

## 🎯 최신 개발 가이드 Check 사례 (2025년 1월)

### SPEC-001: 마법사 UX 개선 개발 가이드 승인
**Claude Code 명령어 개선 아키텍처가 개발 가이드 5원칙을 완벽히 통과**했습니다.

#### 검증 결과
1. **✅ Simplicity**: 3개 컴포넌트 설계 (≤10 제한 준수)
   - WizardController (마법사 제어)
   - OutputRenderer (마크다운 출력)
   - AgentOrchestrator (Task 도구 연동)

2. **✅ Architecture**: 기존 MoAI 에이전트 시스템 완벽 활용
   - steering-architect, spec-manager, tag-indexer 연동
   - 의존성 역전 원칙 준수

3. **✅ Testing**: TDD 강제 시스템 유지
   - Red-Green-Refactor 사이클 보장
   - 커버리지 목표 85% 설정

4. **✅ Observability**: 마법사 사용 로깅 및 상태 추적 강화
   - `.moai/indexes/state.json` 진행 상황 관리
   - 구조화된 로깅 추가

5. **✅ Versioning**: MoAI-ADK 표준 버전 체계 준수
   - 시맨틱 버저닝 적용
   - ADR-001 문서 생성

#### 승인 결과
- **상태**: ✅ **승인됨 - 즉시 적용**
- **승인일**: 2025-01-20
- **유효기간**: 1년 (2026-01-20까지)
- **다음 검토**: 2025-04-20

## 개발 가이드 Check 프로세스

### 자동 검증 플로우
```mermaid
flowchart TD
    A[/moai:3-plan 실행] --> B[5원칙 검증]
    B --> C{모든 원칙 통과?}
    C -->|예| D[품질 게이트 통과]
    C -->|아니오| E[수정 요구]
    E --> F[자동 수정 제안]
    F --> G[재검증]
    G --> C
```

### 검증 항목 체크리스트
```markdown
☐ 1. Simplicity: 복잡도 임계값 확인
☐ 2. Testing: 테스트 커버리지 80% 이상
☐ 3. Documentation: @TAG 추적성 완성
☐ 4. Observability: 로깅 시스템 구비
☐ 5. Versioning: Git 워크플로우 준수
```

## Amendment Process (수정 프로세스)

### 개발 가이드 변경 절차
1. **변경 제안**: ADR 문서 작성
2. **영향 분석**: 기존 코드에 미치는 영향 평가
3. **팀 승인**: 팀원 과반수 동의
4. **점진적 적용**: 단계별 변경 적용



## 거버넌스 메트릭

### 준수율 측정
```json
{
  "constitution_compliance": {
    "simplicity": 0.95,
    "testing": 0.88,
    "documentation": 0.92,
    "observability": 0.85,
    "versioning": 0.98,
    "overall": 0.916
  },
  "trend": "+0.05 (vs last month)",
  "violations": {
    "total": 12,
    "critical": 2,
    "resolved": 10
  }
}
```

### 품질 게이트 통과율
```markdown
📊 월별 품질 게이트 통과율
- 9월: 94% (94/100 SPEC)
- 8월: 91% (89/98 SPEC)
- 7월: 88% (85/97 SPEC)

📈 개선 추세: +3% 월 평균
```

## 팀별 거버넌스 정책

### 팀 규모별 조정
```json
{
  "small_team": {
    "constitution_check": "relaxed",
    "review_required": false,
    "automation_level": "high"
  },
  "large_team": {
    "constitution_check": "strict",
    "review_required": true,
    "automation_level": "maximum"
  }
}
```

### 프로젝트 유형별 조정
```json
{
  "prototype": {
    "testing_threshold": 0.6,
    "documentation_required": false
  },
  "production": {
    "testing_threshold": 0.9,
    "documentation_required": true,
    "security_scan": true
  }
}
```

개발 가이드 거버넌스는 **자동화된 품질 보장**과 **팀 협업 최적화**를 통해 지속 가능한 개발 문화를 구축합니다.
