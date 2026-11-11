"""Claude Code PreToolUse hook: keep file edits inside the active Implementation Plan.

The active plan is inferred from the repository: the one Implementation Plan
under docs/.ai/<work-item>/ whose Human Review status records approval and not
yet full execution. When exactly one such plan exists, an Edit, Write,
MultiEdit, or NotebookEdit of a repository file outside its Files in Scope is
blocked (exit code 2). Files under docs/.ai/ and files outside the repository
are always allowed. When no plan, several plans, or no file list is found, the
hook allows the edit: it never guesses.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PLAN_GLOB = "docs/.ai/*/*Implementation_Plan*.md"
BACKTICK_PATH = re.compile(r"`([^`\s]+)`")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}[ \t]*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def _strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def is_active(plan_text: str) -> bool:
    status = _strip_comments(_section(plan_text, "Human Review")).lower()
    if "not yet executed" in status:
        return "approved" in status
    return "approved by" in status and "executed" not in status


def files_in_scope(plan_text: str) -> set[str]:
    section = _strip_comments(_section(plan_text, "Files in Scope"))
    paths: set[str] = set()
    for line in section.splitlines():
        if not line.lstrip().startswith(("-", "*", "|")):
            continue
        for token in BACKTICK_PATH.findall(line):
            if "/" in token or "." in token:
                token = token.replace("\\", "/")
                paths.add(token[2:] if token.startswith("./") else token)
    return paths


def repository_root(start: Path) -> Path | None:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def decide(payload: dict) -> tuple[bool, str]:
    tool_input = payload.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not target:
        return True, ""
    cwd = Path(payload.get("cwd") or ".").resolve()
    root = repository_root(cwd)
    if root is None:
        return True, ""
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = cwd / target_path
    try:
        rel = target_path.resolve().relative_to(root).as_posix()
    except ValueError:
        return True, ""
    if rel.startswith("docs/.ai/"):
        return True, ""

    active = [p for p in sorted(root.glob(PLAN_GLOB)) if is_active(p.read_text(encoding="utf-8", errors="replace"))]
    if len(active) != 1:
        return True, ""
    plan = active[0]
    scope = files_in_scope(plan.read_text(encoding="utf-8", errors="replace"))
    if not scope:
        return True, ""
    if rel in scope or any(entry.endswith("/") and rel.startswith(entry) for entry in scope):
        return True, ""
    plan_rel = plan.relative_to(root).as_posix()
    return False, (
        f"Blocked by production-engineering-standards: {rel} is not in the Files in Scope of "
        f"{plan_rel}, the one approved Implementation Plan not yet executed. "
        "Do not edit it. Stop and tell the user; a change outside the plan needs an amended "
        "or new Implementation Plan approved by the user."
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    allowed, reason = decide(payload)
    if allowed:
        return 0
    print(reason, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
