---
name: moai:git:checkpoint
description: 💾 개인 모드 체크포인트 시스템
argument-hint: [메시지] - 체크포인트 메시지 또는 --list, --status, --cleanup 옵션
allowed-tools: Bash(git:*), Bash(python3:*), Read, Write, Glob, Grep
model: sonnet
---

# MoAI 스마트 체크포인트 시스템

**요청사항**: $ARGUMENTS

개인 모드에서 안전한 실험을 위한 Constitution 5원칙 준수 Claude Code 기반 지능형 체크포인트 시스템입니다.

## 현재 상태 확인

!`echo "=== 체크포인트 상태 ==="`
!`echo "📍 현재 브랜치: $(git branch --show-current)"`
!`echo "📝 변경사항: $(git status --porcelain | wc -l)개"`
!`echo "🎯 모드: $(python3 -c "import json; config=json.load(open('.moai/config.json')); print(config['project']['mode'])" 2>/dev/null || echo "unknown")"`
!`echo "💾 체크포인트: $(git branch | grep -c checkpoint_)개"`

## 체크포인트 메시지 생성

사용자가 메시지를 제공했다면 그대로 사용하고, 그렇지 않다면 Claude가 변경사항을 분석해서 의미있는 체크포인트 메시지를 생성합니다.

### 1. 변경사항 분석 (메시지가 없는 경우)

!`git status --porcelain`
!`git diff --stat`

### 2. 체크포인트 메시지 결정

**요청된 메시지**: "$ARGUMENTS"

만약 사용자가 메시지를 제공하지 않았다면, 위의 변경사항을 분석해서 다음 가이드라인에 따라 의미있는 체크포인트 메시지를 생성해주세요:

- 🧪 실험 시작/진행: 새로운 접근법 시도, 개념 검증
- 🔄 리팩토링 중간점: 코드 구조 변경 과정
- 💡 아이디어 백업: 임시 구현, 프로토타입
- 🐛 디버깅 체크포인트: 문제 해결 과정 백업
- ✨ 기능 실험: 새로운 기능 시도
- 📝 문서 작업: 문서화 과정 백업

**실제 변경 내용을 보고 구체적이고 의미있는 체크포인트 메시지를 생성해주세요.**

### 3. 체크포인트 실행

위에서 결정된 메시지로 체크포인트를 생성합니다.

## 사용법

```bash
# 기본 체크포인트 생성
/moai:git:checkpoint "실험 시작"

# 자동 메시지 체크포인트
/moai:git:checkpoint

# 체크포인트 목록 확인
/moai:git:checkpoint --list

# 시스템 상태 확인
/moai:git:checkpoint --status

# 오래된 체크포인트 정리
/moai:git:checkpoint --cleanup
```

## 특징

- **개인 모드 전용**: 팀 모드에서는 사용 제한으로 충돌 방지
- **자동 타임스탬프**: checkpoint_YYYYMMDD_HHMMSS 형식으로 생성
- **안전한 실험**: 언제든 롤백 가능한 체크포인트 브랜치 생성
- **자동 정리**: 7일 이상 된 체크포인트 자동 삭제 기능
- **브랜치 기반**: Git 브랜치로 관리되어 완전한 상태 복원 가능

체크포인트는 실험적 코드 작성, 리팩토링, 위험한 변경 작업 전에 생성하여 안전한 개발 환경을 제공합니다.
