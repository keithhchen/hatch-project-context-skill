#!/usr/bin/env python3
"""Validate the OpenAI/Codex and pure Anthropic skill entry points."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def read_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path}: missing YAML frontmatter")

    end = text.find("\n---\n", 4)
    if end == -1:
        fail(f"{path}: unterminated YAML frontmatter")

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip().strip('"\'')

    return fields, text[end + len("\n---\n") :]


def validate_metadata(path: Path, expected_name: str) -> tuple[dict[str, str], str]:
    fields, body = read_frontmatter(path)
    for required in ("name", "description"):
        if not fields.get(required):
            fail(f"{path}: missing required field {required!r}")

    name = fields["name"]
    if name != expected_name:
        fail(f"{path}: name {name!r} does not match {expected_name!r}")
    if not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        fail(f"{path}: invalid skill name {name!r}")
    if len(fields["description"]) > 1024:
        fail(f"{path}: description exceeds 1024 characters")

    return fields, body


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    openai_skill = root / "SKILL.md"
    anthropic_skill = root / "skills" / "hatch-project-context" / "SKILL.md"

    if not openai_skill.is_file():
        fail(f"missing {openai_skill}")
    if not anthropic_skill.is_file():
        fail(f"missing {anthropic_skill}")

    openai_fields, openai_body = validate_metadata(openai_skill, "hatch-project-context")
    anthropic_fields, anthropic_body = validate_metadata(
        anthropic_skill, "hatch-project-context"
    )

    if openai_fields["description"] != anthropic_fields["description"]:
        fail("OpenAI and Anthropic descriptions have diverged")

    for path in (openai_skill, anthropic_skill):
        raw = path.read_text(encoding="utf-8")
        if "dependency: feishu-cli" not in raw or "executable: lark-cli" not in raw:
            fail(f"{path}: Feishu CLI dependency metadata is missing")

    if openai_body != anthropic_body:
        fail("OpenAI and Anthropic instruction bodies have diverged")

    required_dependency_instructions = (
        "command -v lark-cli",
        "帮我安装飞书 CLI：https://open.feishu.cn/document/no_class/mcp-archive/feishu-cli-installation-guide.md",
        "https://www.feishu.cn/feishu-cli",
    )
    for instruction in required_dependency_instructions:
        if instruction not in openai_body:
            fail(f"skill is missing Feishu CLI instruction: {instruction}")

    openai_references = root / "references"
    anthropic_references = root / "skills" / "hatch-project-context" / "references"
    if not (openai_references / "sources.md").is_file():
        fail("missing OpenAI references/sources.md")
    if not (anthropic_references / "sources.md").is_file():
        fail("missing Anthropic references/sources.md")
    if "references/sources.md" not in openai_body:
        fail("OpenAI skill does not link references/sources.md")
    if "references/sources.md" not in anthropic_body:
        fail("Anthropic skill does not link references/sources.md")

    openai_reference_files = {
        path.relative_to(openai_references)
        for path in openai_references.rglob("*")
        if path.is_file()
    }
    anthropic_reference_files = {
        path.relative_to(anthropic_references)
        for path in anthropic_references.rglob("*")
        if path.is_file()
    }
    if openai_reference_files != anthropic_reference_files:
        fail("OpenAI and Anthropic reference file lists have diverged")
    for relative_path in openai_reference_files:
        if (openai_references / relative_path).read_bytes() != (
            anthropic_references / relative_path
        ).read_bytes():
            fail(f"reference file has diverged: {relative_path}")

    if not (root / "agents" / "openai.yaml").is_file():
        fail("missing agents/openai.yaml")

    print("Skill layout is valid for OpenAI/Codex and pure Anthropic Agent Skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
