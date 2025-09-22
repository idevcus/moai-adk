---
name: moai:git:sync
description: 🔄 원격 동기화
argument-hint: [ACTION] - push, pull, both, status, --auto, --safe 중 하나
allowed-tools: Bash(git:*), Bash(python3:*), Read, Write, Glob, Grep
model: haiku
---

# MoAI-ADK 동기화 시스템

Mode-optimized remote repository synchronization strategies.

## Current Environment Check

- Current branch: !`git branch --show-current`
- Remote status: !`git status -b --porcelain | head -1`
- Uncommitted changes: !`git status --porcelain | wc -l`
- Commits ahead: !`git rev-list --count @{u}..HEAD 2>/dev/null || echo "0"`
- Commits behind: !`git rev-list --count HEAD..@{u} 2>/dev/null || echo "0"`
- Project mode: !`python3 -c "import json; config=json.load(open('.moai/config.json')); print(config['project']['mode'])" 2>/dev/null || echo "unknown"`

## Task

Execute synchronization: "$ARGUMENTS"

### Sync Actions:

#### If "push" provided:
- Push current branch to remote
- Handle upstream branch setup if needed
- Show push results and any conflicts

#### If "pull" provided:
- Pull latest changes from remote
- Handle merge conflicts if they occur
- Update local branch with remote changes

#### If "both" provided:
- First pull latest changes
- Then push local commits
- Handle any merge conflicts in between

#### If "status" provided:
- Show detailed synchronization status
- Display commits ahead/behind
- Show any uncommitted changes

#### If "--auto" provided:
- Automatically determine sync strategy based on mode
- Personal mode: minimal syncing
- Team mode: full GitFlow sync

#### If "--safe" provided:
- Create checkpoint before syncing
- Allow rollback if sync fails
- Preserve local changes during conflicts

## Sync Process:

1. **Check remote connection**: !`git remote -v`
2. **Fetch latest refs**: !`git fetch origin`
3. **Analyze differences**: Compare local and remote
4. **Execute sync strategy**: Based on mode and arguments
5. **Handle conflicts**: Provide resolution guidance if needed
6. **Update tracking**: Log sync operation

## 🎯 핵심 기능

### 모드별 동기화 전략
- **개인 모드**: 선택적 동기화, 로컬 우선
- **팀 모드**: 자동 동기화, 원격 우선
- **충돌 방지**: 스마트 충돌 감지 및 해결
- **백업 보장**: 동기화 전 자동 백업

### 사용법

```bash
# 기본 동기화 (모드에 따라 자동 결정)
/git:sync

# 원격에서 가져오기만
/git:sync --pull

# 원격으로 푸시만
/git:sync --push

# 양방향 동기화
/git:sync --both

# 강제 동기화 (충돌 무시)
/git:sync --force
```

## 📋 모드별 동기화 전략

### 개인 모드 (Personal Mode)

#### 기본 동작
```bash
# 1. 현재 상태 백업
/git:checkpoint "동기화 전 백업"

# 2. 원격 상태 확인
git fetch origin

# 3. 로컬 우선 정책
if [[ $(git status --porcelain) ]]; then
    echo "✅ 로컬 변경사항 우선 - 푸시 스킵"
    SYNC_ACTION="pull_only"
else
    echo "🔄 양방향 동기화 수행"
    SYNC_ACTION="both"
fi
```

#### 특징
- **로컬 중심**: 작업 중인 내용 보호 우선
- **선택적 푸시**: 완성된 작업만 원격 전송
- **자동 백업**: 동기화 전 체크포인트 생성
- **충돌 회피**: 복잡한 merge 상황 피함

### 팀 모드 (Team Mode)

#### 기본 동작
```bash
# 1. 원격 최신 상태 가져오기
git fetch origin

# 2. 충돌 감지 및 해결
if [[ $(git status --porcelain) ]]; then
    echo "🔄 변경사항 있음 - 스마트 병합 수행"
    handle_team_merge
else
    echo "⚡ 깔끔한 상태 - 빠른 동기화"
    git pull --ff-only origin $(git branch --show-current)
fi

# 3. 자동 푸시 (팀 공유)
git push origin $(git branch --show-current)
```

#### 특징
- **원격 우선**: 팀 작업 최신 상태 유지
- **자동 병합**: 충돌 시 스마트 해결
- **즉시 공유**: 완료된 작업 자동 푸시
- **브랜치 관리**: feature 브랜치 자동 추적

## 🔧 스마트 동기화 로직

### 충돌 감지 및 해결
```bash
detect_conflicts() {
    local remote_branch="origin/$(git branch --show-current)"
    local local_ahead=$(git rev-list --count ${remote_branch}..HEAD)
    local local_behind=$(git rev-list --count HEAD..${remote_branch})

    if [[ $local_ahead -gt 0 && $local_behind -gt 0 ]]; then
        echo "diverged:$local_ahead:$local_behind"
    elif [[ $local_ahead -gt 0 ]]; then
        echo "ahead:$local_ahead"
    elif [[ $local_behind -gt 0 ]]; then
        echo "behind:$local_behind"
    else
        echo "up_to_date"
    fi
}
```

### 자동 병합 전략
```bash
handle_smart_merge() {
    local conflict_status="$1"

    case "$conflict_status" in
        "diverged:"*)
            echo "🔀 브랜치 분기 감지 - 자동 병합 시도"
            attempt_auto_merge
            ;;
        "ahead:"*)
            echo "⬆️ 로컬이 앞섬 - 푸시 수행"
            git push origin HEAD
            ;;
        "behind:"*)
            echo "⬇️ 원격이 앞섬 - 풀 수행"
            git pull --ff-only
            ;;
        "up_to_date")
            echo "✅ 이미 최신 상태"
            ;;
    esac
}
```

## 📊 동기화 상태 표시

### 실시간 상태 대시보드
```bash
show_sync_status() {
    echo "📡 Git 동기화 상태"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🌿 현재 브랜치: $(git branch --show-current)"
    echo "📍 현재 커밋: $(git rev-parse --short HEAD)"
    echo "🔄 동기화 모드: $(get_sync_mode)"
    echo ""

    local status=$(detect_conflicts)
    case "$status" in
        "up_to_date")
            echo "✅ 원격과 동기화됨"
            ;;
        "ahead:"*)
            local count=$(echo "$status" | cut -d: -f2)
            echo "⬆️ 로컬이 ${count}개 커밋 앞섭니다"
            ;;
        "behind:"*)
            local count=$(echo "$status" | cut -d: -f2)
            echo "⬇️ 원격이 ${count}개 커밋 앞섭니다"
            ;;
        "diverged:"*)
            local ahead=$(echo "$status" | cut -d: -f2)
            local behind=$(echo "$status" | cut -d: -f3)
            echo "🔀 브랜치가 분기됨 (로컬 +${ahead}, 원격 +${behind})"
            ;;
    esac
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}
```

## 🚨 안전장치

### 동기화 전 검증
```bash
pre_sync_checks() {
    # 1. Git 저장소 확인
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        echo "❌ Git 저장소가 아닙니다"
        return 1
    fi

    # 2. 원격 저장소 연결 확인
    if ! git remote get-url origin >/dev/null 2>&1; then
        echo "⚠️ 원격 저장소가 설정되지 않았습니다"
        return 1
    fi

    # 3. 네트워크 연결 확인
    if ! git ls-remote origin >/dev/null 2>&1; then
        echo "🌐 원격 저장소에 연결할 수 없습니다"
        return 1
    fi

    return 0
}
```

### 동기화 후 검증
```bash
post_sync_verification() {
    # 1. 동기화 성공 확인
    local pre_sync_hash="$1"
    local post_sync_hash=$(git rev-parse HEAD)

    if [[ "$pre_sync_hash" != "$post_sync_hash" ]]; then
        echo "✅ 동기화 완료: $pre_sync_hash → $post_sync_hash"
    else
        echo "ℹ️ 변경사항 없음"
    fi

    # 2. 작업 디렉토리 상태 확인
    if git status --porcelain | grep -q .; then
        echo "⚠️ 커밋되지 않은 변경사항이 있습니다"
        git status --short
    fi

    # 3. 원격 동기화 상태 재확인
    git fetch origin >/dev/null 2>&1
    local final_status=$(detect_conflicts)
    if [[ "$final_status" == "up_to_date" ]]; then
        echo "🎯 원격 저장소와 완전히 동기화됨"
    else
        echo "⚠️ 추가 동기화가 필요할 수 있습니다: $final_status"
    fi
}
```

## 🔄 자동 동기화 옵션

### 개인 모드 자동화
```json
// .moai/config.json
{
  "git_strategy": {
    "personal": {
      "auto_sync": false,           // 수동 동기화 기본
      "sync_on_spec_complete": true, // 명세 완료 시 동기화
      "backup_before_sync": true,   // 동기화 전 백업
      "conflict_strategy": "local_priority" // 로컬 우선
    }
  }
}
```

### 팀 모드 자동화
```json
{
  "git_strategy": {
    "team": {
      "auto_sync": true,            // 자동 동기화 활성
      "sync_interval": 1800,        // 30분마다
      "auto_push": true,            // 커밋 후 자동 푸시
      "conflict_strategy": "remote_priority" // 원격 우선
    }
  }
}
```

## 📈 동기화 통계

### 동기화 이력 추적
```json
{
  "sync_history": [
    {
      "timestamp": "2025-01-20T16:30:00Z",
      "mode": "personal",
      "action": "pull_only",
      "files_changed": 3,
      "conflicts_resolved": 0,
      "duration_ms": 1250
    }
  ],
  "sync_stats": {
    "total_syncs": 45,
    "avg_duration": 1100,
    "conflict_rate": 0.02,
    "success_rate": 0.98
  }
}
```

## 💡 사용 시나리오

### 개인 개발 워크플로우
```bash
# 하루 시작 - 최신 상태 확인
/git:sync --pull

# 작업 중 - 로컬 작업 보호
/git:checkpoint "새 기능 작업 중"

# 완료 후 - 선택적 공유
/git:sync --push
```

### 팀 개발 워크플로우
```bash
# PR 전 - 최신 상태로 업데이트
/git:sync --both

# 충돌 해결 후 - 안전한 푸시
/git:sync --force

# 정기 동기화 - 자동 실행
# (팀 모드에서는 30분마다 자동)
```

## 🎯 Constitution 5원칙 준수

1. **Simplicity**: 단일 명령어로 모든 동기화 처리
2. **Architecture**: git-manager와 체계적 연동
3. **Testing**: 동기화 전 백업으로 안전성 보장
4. **Observability**: 모든 동기화 작업 추적
5. **Versioning**: 동기화 이력 체계적 관리

모든 동기화 작업은 git-manager 에이전트가 안전하고 효율적으로 처리합니다.