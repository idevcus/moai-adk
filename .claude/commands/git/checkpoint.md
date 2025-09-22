---
name: git:checkpoint
description: 자동 체크포인트 생성 - 개인 모드에서 작업 진행 상황을 안전하게 백업
argument-hint: [message]
allowed-tools: Bash(git:*), Read, Write, Glob, Grep
---

# Git 자동 체크포인트

개인 모드에서 작업 진행 상황을 자동으로 백업하여 언제든 안전하게 복구할 수 있도록 합니다.

## 🎯 핵심 기능

### 자동 체크포인트 생성
- 현재 작업 상태를 WIP(Work In Progress) 커밋으로 저장
- 타임스탬프 기반 체크포인트 ID 생성
- 로컬 백업 브랜치 자동 생성

### 사용법

```bash
# 기본 체크포인트 생성
/git:checkpoint

# 메시지와 함께 체크포인트 생성
/git:checkpoint "JWT 인증 로직 작업 중"

# 명세 완료 시 자동 체크포인트
/git:checkpoint "SPEC-001 명세 작성 완료"
```

## 📋 실행 과정

### 1. 환경 확인
- `.moai/config.json`에서 모드 확인 (personal/team)
- 개인 모드가 아닌 경우 안내 메시지 표시

### 2. 체크포인트 생성
```bash
# 타임스탬프 생성
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
CHECKPOINT_ID="checkpoint_${TIMESTAMP}"

# 현재 변경사항 스테이징
git add -A

# WIP 커밋 생성
git commit -m "🔄 Checkpoint: ${TIMESTAMP} - ${MESSAGE}"

# 백업 브랜치 생성 (현재 브랜치에서)
git branch "${CHECKPOINT_ID}" HEAD
```

### 3. 메타데이터 저장
```json
// .moai/checkpoints/metadata.json에 추가
{
  "checkpoints": [
    {
      "id": "checkpoint_20250120_153000",
      "timestamp": "2025-01-20T15:30:00Z",
      "branch": "develop",
      "commit": "a1b2c3d",
      "message": "JWT 인증 로직 작업 중",
      "files_changed": 5,
      "mode": "personal"
    }
  ]
}
```

## 🔧 모드별 동작

### 개인 모드 (Personal Mode)
- **자동 체크포인트**: 5분마다 자동 실행
- **간소화된 메시지**: 타임스탬프 기반
- **로컬 중심**: 원격 푸시 없음
- **실험 보호**: 안전한 실험 환경 제공

### 팀 모드 (Team Mode)
- **수동 체크포인트**: 필요시에만 실행
- **구조화된 메시지**: 작업 내용 명시
- **원격 동기화**: 팀 공유 고려
- **리뷰 준비**: PR 전 정리용

## ⚙️ 설정 옵션

### .moai/config.json
```json
{
  "git_strategy": {
    "personal": {
      "auto_checkpoint": true,
      "checkpoint_interval": 300,  // 5분
      "max_checkpoints": 50,       // 최대 보관 개수
      "cleanup_days": 7            // 7일 후 자동 정리
    }
  }
}
```

## 📊 체크포인트 관리

### 자동 정리
- 7일 이상 된 체크포인트 자동 삭제
- 최대 50개 체크포인트 유지
- 중요한 체크포인트는 태그로 보호

### 충돌 방지
- 체크포인트 생성 전 Git 상태 확인
- 진행 중인 merge/rebase 감지
- 안전한 상태에서만 체크포인트 생성

## 🎯 Constitution 5원칙 준수

### 1. Simplicity (단순성)
- 단일 명령어로 모든 백업 처리
- 복잡한 Git 명령어 숨김
- 사용자는 `/git:checkpoint`만 실행

### 2. Architecture (아키텍처)
- git-manager 에이전트와 연동
- 모듈화된 체크포인트 시스템
- 명령어와 에이전트 책임 분리

### 3. Testing (테스트)
- 체크포인트로 안전한 실험 환경
- 롤백 기능으로 TDD 지원
- 실패해도 복구 가능한 구조

### 4. Observability (관찰가능성)
- 모든 체크포인트 로깅
- 메타데이터로 추적성 확보
- 체크포인트 히스토리 관리

### 5. Versioning (버전관리)
- 시맨틱 체크포인트 번호
- 브랜치 기반 백업 전략
- 하위 호환성 보장

## 🚨 에러 처리

### 일반적인 에러 상황
```bash
# Git 저장소가 아닌 경우
ERROR: "Git 저장소가 아닙니다. 'git init' 또는 MoAI 프로젝트를 초기화하세요."

# 변경사항이 없는 경우
INFO: "변경사항이 없어 체크포인트를 생성하지 않습니다."

# 팀 모드에서 자동 체크포인트 시도
WARNING: "팀 모드에서는 수동 체크포인트만 지원됩니다."
```

## 💡 사용 팁

### 개발 시나리오별 활용
```bash
# 실험적 코드 작성 전
/git:checkpoint "실험 시작: 새로운 알고리즘 적용"

# 리팩토링 전
/git:checkpoint "리팩토링 전 백업"

# 명세 작성 완료
/git:checkpoint "SPEC-001 명세 완성"

# 위험한 변경 전
/git:checkpoint "데이터베이스 스키마 변경 전"
```

모든 체크포인트는 git-manager 에이전트와 연동되어 자동으로 관리됩니다.