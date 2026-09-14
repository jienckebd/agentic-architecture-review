#!/usr/bin/env python3
"""Validate this project skill and its Codex-Claude mirror without dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {"__pycache__"}
REQUIRED_CASE_FIELDS = {
    "id",
    "mode",
    "query",
    "setup",
    "expected_behaviors",
    "forbidden_behaviors",
}


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_evals(errors: list[str]) -> None:
    path = SKILL_DIR / "evals" / "cases.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        add_error(errors, f"{path.relative_to(SKILL_DIR)}: {exc}")
        return

    if payload.get("schema_version") != 1:
        add_error(errors, "evals/cases.json: schema_version must be 1")

    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) < 3:
        add_error(errors, "evals/cases.json: cases must contain at least three cases")
        return

    seen: set[str] = set()
    for index, case in enumerate(cases):
        label = f"evals/cases.json case {index + 1}"
        if not isinstance(case, dict):
            add_error(errors, f"{label}: must be an object")
            continue

        missing = REQUIRED_CASE_FIELDS - set(case)
        if missing:
            add_error(errors, f"{label}: missing {sorted(missing)}")

        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            add_error(errors, f"{label}: id must be a non-empty string")
        elif case_id in seen:
            add_error(errors, f"{label}: duplicate id {case_id!r}")
        else:
            seen.add(case_id)

        for field in ("expected_behaviors", "forbidden_behaviors"):
            values = case.get(field)
            if not isinstance(values, list) or not values:
                add_error(errors, f"{label}: {field} must be a non-empty list")
            elif any(not isinstance(value, str) or not value.strip() for value in values):
                add_error(errors, f"{label}: {field} must contain non-empty strings")


def validate_references(errors: list[str]) -> None:
    skill_path = SKILL_DIR / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    for target in re.findall(r"\]\(((?:references|evals)/[^)]+)\)", text):
        if not (SKILL_DIR / target).is_file():
            add_error(errors, f"SKILL.md: linked file does not exist: {target}")

    for path in sorted((SKILL_DIR / "references").glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) > 100 and "## Contents" not in lines[:20]:
            add_error(
                errors,
                f"{path.relative_to(SKILL_DIR)}: references over 100 lines need "
                "a Contents section in the first 20 lines",
            )


def skill_files(directory: Path) -> dict[Path, bytes]:
    result: dict[Path, bytes] = {}
    for path in directory.rglob("*"):
        if not path.is_file() or path.suffix == ".pyc":
            continue
        relative = path.relative_to(directory)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        result[relative] = path.read_bytes()
    return result


def find_mirror() -> Path | None:
    platform_root = next(
        (parent for parent in SKILL_DIR.parents if parent.name in {".codex", ".claude"}),
        None,
    )
    if platform_root is None:
        return None

    other = ".claude" if platform_root.name == ".codex" else ".codex"
    return platform_root.parent / other / "skills" / SKILL_DIR.name


def validate_mirror(errors: list[str], notes: list[str]) -> None:
    """Compare against a Codex-Claude mirror when one is installed.

    A standalone checkout has no .claude or .codex parent and no sibling copy,
    so there is nothing to compare. That is a valid single-copy install, not a
    failure; only a mirror that exists and has drifted is an error.
    """
    mirror = find_mirror()
    if mirror is None:
        notes.append("no .codex or .claude project root; skipped mirror parity check")
        return
    if not mirror.is_dir():
        notes.append(f"no mirror installed at {mirror}; skipped mirror parity check")
        return

    current_files = skill_files(SKILL_DIR)
    mirror_files = skill_files(mirror)
    if current_files.keys() != mirror_files.keys():
        only_current = sorted(str(path) for path in current_files.keys() - mirror_files.keys())
        only_mirror = sorted(str(path) for path in mirror_files.keys() - current_files.keys())
        add_error(
            errors,
            f"mirror file sets differ; only here={only_current}, only mirror={only_mirror}",
        )
        return

    different = [
        str(path)
        for path in sorted(current_files)
        if current_files[path] != mirror_files[path]
    ]
    if different:
        add_error(errors, f"mirror content differs: {different}")


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []
    validate_evals(errors)
    validate_references(errors)
    validate_mirror(errors, notes)

    for note in notes:
        print(f"NOTE: {note}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Skill evaluation fixtures, references, and mirror are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

