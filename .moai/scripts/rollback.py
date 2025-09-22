#!/usr/bin/env python3
"""
MoAI-ADK Git Rollback Script
체크포인트 기반 안전한 롤백 시스템
"""

import json
import sys
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple, Any, cast


class MoAIRollback:
    def __init__(self) -> None:
        self.project_root = self._find_project_root()
        self.checkpoints_dir = self.project_root / ".moai" / "checkpoints"
        self.metadata_file = self.checkpoints_dir / "metadata.json"

    def _find_project_root(self) -> Path:
        """프로젝트 루트 디렉토리 찾기"""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".moai").exists():
                return current
            current = current.parent
        raise RuntimeError("MoAI 프로젝트 루트를 찾을 수 없습니다")

    def _load_metadata(self) -> Dict[str, Any]:
        """체크포인트 메타데이터 로드"""
        if not self.metadata_file.exists():
            return {"checkpoints": []}

        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            return cast(Dict[str, Any], json.load(f))

    def _save_metadata(self, metadata: Dict[str, Any]) -> None:
        """체크포인트 메타데이터 저장"""
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def _run_git_command(self, cmd: str) -> Tuple[bool, str, str]:
        """Git 명령어 실행"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return (
                result.returncode == 0,
                result.stdout.strip(),
                result.stderr.strip()
            )
        except Exception as e:
            return False, "", str(e)

    def _get_project_mode(self) -> str:
        """프로젝트 모드 확인"""
        config_file = self.project_root / ".moai" / "config.json"
        if not config_file.exists():
            return "unknown"

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = cast(Dict[str, Any], json.load(f))
                project = cast(Dict[str, Any], config.get('project', {}))
                mode = project.get('mode', 'unknown')
                return mode if isinstance(mode, str) else "unknown"
        except (
            FileNotFoundError,
            json.JSONDecodeError,
            KeyError
        ):
            return "unknown"

    def list_checkpoints(self) -> None:
        """체크포인트 목록 표시"""
        metadata = self._load_metadata()
        checkpoints = metadata.get("checkpoints", [])

        if not checkpoints:
            print("📋 사용 가능한 체크포인트가 없습니다.")
            return

        print("📋 사용 가능한 체크포인트:")
        print(
            "ID                           시간              "
            "메시지                   파일수"
        )
        print("-" * 80)

        for cp in reversed(checkpoints[-10:]):  # 최근 10개만 표시
            timestamp = datetime.fromisoformat(cp['timestamp'])
            time_str = timestamp.strftime("%H:%M")
            ago = datetime.now() - timestamp
            if ago.days > 0:
                time_display = f"{time_str} ({ago.days}일 전)"
            elif ago.seconds > 3600:
                hours = ago.seconds // 3600
                time_display = f"{time_str} ({hours}시간 전)"
            else:
                minutes = ago.seconds // 60
                time_display = f"{time_str} ({minutes}분 전)"

            print(
                f"{cp['id']:<28} {time_display:<16} "
                f"{cp['message'][:20]:<20} {cp.get('files_changed', 0)}"
            )

    def find_checkpoint_by_time(
        self, time_expr: str
    ) -> Optional[Dict[str, Any]]:
        """시간 표현으로 체크포인트 찾기"""
        metadata = self._load_metadata()
        checkpoints = metadata.get("checkpoints", [])

        if not checkpoints:
            return None

        # 시간 파싱
        target_time = self._parse_time_expression(time_expr)
        if not target_time:
            print(f"⚠️ 시간 표현을 이해할 수 없습니다: {time_expr}")
            return None

        # 대상 시점 이전(또는 같은 시점)의 가장 가까운 체크포인트 찾기
        closest_cp = None
        min_diff = float('inf')

        for cp in checkpoints:
            try:
                cp_time = datetime.fromisoformat(cp['timestamp'])
            except Exception:
                continue

            # 대상 시점 이후의 체크포인트는 제외 (롤백 의미에 맞게 과거만 허용)
            if cp_time > target_time:
                continue

            diff = (target_time - cp_time).total_seconds()

            if 0 <= diff < min_diff:
                min_diff = diff
                closest_cp = cp

        return closest_cp

    def _parse_time_expression(self, time_expr: str) -> Optional[datetime]:
        """시간 표현 파싱"""
        now = datetime.now()

        if "분 전" in time_expr or "분전" in time_expr:
            try:
                minutes = int(
                    ''.join(filter(str.isdigit, time_expr))
                )
                return now - timedelta(minutes=minutes)
            except ValueError:
                return None
        elif "시간 전" in time_expr or "시간전" in time_expr:
            try:
                hours = int(
                    ''.join(filter(str.isdigit, time_expr))
                )
                return now - timedelta(hours=hours)
            except ValueError:
                return None
        elif "오전" in time_expr:
            return now.replace(hour=9, minute=0, second=0, microsecond=0)

        return None

    def rollback_to_checkpoint(
        self, checkpoint_id: str, force: bool = False
    ) -> bool:
        """특정 체크포인트로 롤백"""
        # 개인 모드 확인
        if self._get_project_mode() != "personal":
            print("⚠️ 롤백은 개인 모드에서만 사용 가능합니다.")
            return False

        metadata = self._load_metadata()
        checkpoints = metadata.get("checkpoints", [])

        # 체크포인트 찾기
        target_cp = None
        for cp in checkpoints:
            if cp['id'] == checkpoint_id:
                target_cp = cp
                break

        if not target_cp:
            print(f"❌ 체크포인트를 찾을 수 없습니다: {checkpoint_id}")
            return False

        # 현재 상태 확인
        success, status_output, _ = self._run_git_command(
            "git status --porcelain"
        )
        if status_output and not force:
            print("⚠️ 커밋되지 않은 변경사항이 있습니다.")
            print("다음 중 선택하세요:")
            print("1. 현재 상태를 체크포인트로 저장 후 롤백")
            print("2. 변경사항을 버리고 롤백")
            print("3. 롤백 취소")

            choice = input("선택 (1-3): ").strip()
            if choice == "1":
                self._create_safety_checkpoint()
            elif choice == "2":
                pass  # 변경사항 버림
            else:
                print("롤백이 취소되었습니다.")
                return False

        # 롤백 실행
        print(f"🔄 체크포인트 {checkpoint_id}로 롤백 중...")

        commit_hash = target_cp.get('commit_hash')
        if not commit_hash:
            print("❌ 체크포인트에 커밋 해시가 없습니다.")
            return False

        # 롤백 전 현재 커밋 기록 (이력 정확성 보장)
        _, before_commit, _ = self._run_git_command("git rev-parse HEAD")

        success, _, error = self._run_git_command(
            f"git reset --hard {commit_hash}"
        )
        if not success:
            print(f"❌ 롤백 실패: {error}")
            return False

        # 작업 디렉토리 정리
        self._run_git_command("git clean -fd")

        # 롤백 기록
        self._log_rollback(checkpoint_id, target_cp, from_commit=before_commit)

        print(f"✅ 체크포인트 {checkpoint_id}로 롤백 완료")
        print(f"📅 복원된 시점: {target_cp['timestamp']}")
        print(f"💬 메시지: {target_cp['message']}")

        return True

    def _create_safety_checkpoint(self) -> None:
        """안전 체크포인트 생성"""
        from datetime import datetime

        timestamp = datetime.now().isoformat()
        # 긴 라인 분리: 타임스탬프에서 콜론/대시/닷 제거 후 앞 15자 사용
        ts_clean = (
            timestamp.replace(":", "").replace("-", "").replace(".", "")
        )
        checkpoint_id = f"safety_{ts_clean[:15]}"

        # 현재 커밋 해시 가져오기
        success, commit_hash, _ = self._run_git_command("git rev-parse HEAD")
        if not success:
            print("⚠️ 안전 체크포인트 생성 실패")
            return

        # 메타데이터 업데이트
        metadata = self._load_metadata()
        if "checkpoints" not in metadata:
            metadata["checkpoints"] = []

        metadata["checkpoints"].append({
            "id": checkpoint_id,
            "timestamp": timestamp,
            "commit_hash": commit_hash,
            "message": "롤백 전 안전 백업",
            "type": "safety",
            "files_changed": 0
        })

        self._save_metadata(metadata)
        print(f"💾 안전 체크포인트 생성: {checkpoint_id}")

    def _log_rollback(
        self,
        checkpoint_id: str,
        _checkpoint_data: Dict[str, Any],
        from_commit: Optional[str] = None,
    ) -> None:
        """롤백 기록"""
        metadata = self._load_metadata()
        if "rollback_history" not in metadata:
            metadata["rollback_history"] = []

        # from 커밋은 롤백 이전 커밋을 우선 사용하고,
        # 없으면 현재 HEAD(롤백 후)로 대체
        if from_commit:
            current_from = from_commit
            success = True
        else:
            success, current_from, _ = self._run_git_command(
                "git rev-parse HEAD"
            )

        metadata["rollback_history"].append({
            "timestamp": datetime.now().isoformat(),
            "from": current_from if success else "unknown",
            "to": checkpoint_id,
            "reason": "사용자 요청",
            "mode": self._get_project_mode()
        })

        self._save_metadata(metadata)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MoAI-ADK 체크포인트 롤백"
    )
    parser.add_argument(
        "action", nargs="?", help="롤백 대상 (체크포인트 ID)"
    )
    parser.add_argument(
        "--list", action="store_true", help="체크포인트 목록 표시"
    )
    parser.add_argument(
        "--last", action="store_true", help="마지막 체크포인트로 롤백"
    )
    parser.add_argument(
        "--time", help="시간 기반 롤백 (예: '30분 전')"
    )
    parser.add_argument("--force", action="store_true", help="강제 롤백")

    args = parser.parse_args()
    rollback = MoAIRollback()

    try:
        if args.list:
            rollback.list_checkpoints()
        elif args.last:
            metadata = rollback._load_metadata()
            checkpoints = metadata.get("checkpoints", [])
            if checkpoints:
                last_cp = checkpoints[-1]
                rollback.rollback_to_checkpoint(
                    last_cp['id'], args.force
                )
            else:
                print("❌ 사용 가능한 체크포인트가 없습니다.")
        elif args.time:
            cp = rollback.find_checkpoint_by_time(args.time)
            if cp:
                print(
                    f"🎯 찾은 체크포인트: {cp['id']} - {cp['message']}"
                )
                rollback.rollback_to_checkpoint(cp['id'], args.force)
            else:
                print(
                    "❌ 해당 시간에 맞는 체크포인트를 찾을 수 없습니다."
                )
        elif args.action:
            rollback.rollback_to_checkpoint(args.action, args.force)
        else:
            parser.print_help()

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
