#!/usr/bin/env python3
"""Validate the marketplace manifest, every plugin manifest, and every skill.

Runs with the standard library only so CI needs no install step. Exits 1 and
prints one line per problem when something is wrong.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PLUGINS_DIR = ROOT / "plugins"

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)*$")
MAX_DESCRIPTION = 1024

errors: list[str] = []


def fail(where: Path | str, message: str) -> None:
    location = where.relative_to(ROOT) if isinstance(where, Path) else where
    errors.append(f"{location}: {message}")


def load_json(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(path, "file is missing")
        return None
    except json.JSONDecodeError as exc:
        fail(path, f"invalid JSON ({exc})")
        return None
    if not isinstance(data, dict):
        fail(path, "top level must be a JSON object")
        return None
    return data


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    """Read the leading --- block. Handles `key: value` and folded values."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(path, "missing YAML frontmatter (file must start with ---)")
        return None
    end = text.find("\n---", 3)
    if end == -1:
        fail(path, "frontmatter is never closed with ---")
        return None

    fields: dict[str, str] = {}
    key = None
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1] in (" ", "\t") and key:
            fields[key] += " " + line.strip()
            continue
        if ":" not in line:
            fail(path, f"frontmatter line is not `key: value`: {line!r}")
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        fields[key] = value.strip().strip("'\"")
    return fields


def check_skill(skill_dir: Path, seen: dict[str, Path]) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(skill_dir, "skill directory has no SKILL.md")
        return

    fields = parse_frontmatter(skill_md)
    if fields is None:
        return

    name = fields.get("name", "")
    if not name:
        fail(skill_md, "frontmatter is missing `name`")
    elif name != skill_dir.name:
        fail(skill_md, f"name `{name}` does not match directory `{skill_dir.name}`")
    elif not KEBAB.match(name):
        fail(skill_md, f"name `{name}` must be lowercase kebab-case")

    description = fields.get("description", "")
    if not description:
        fail(skill_md, "frontmatter is missing `description`")
    elif len(description) > MAX_DESCRIPTION:
        fail(skill_md, f"description is {len(description)} chars, limit is {MAX_DESCRIPTION}")

    if name:
        if name in seen:
            fail(skill_md, f"duplicate skill name `{name}`, already used by {seen[name].relative_to(ROOT)}")
        else:
            seen[name] = skill_md


def check_plugin(plugin_dir: Path, entry: dict, seen: dict[str, Path]) -> None:
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    manifest = load_json(manifest_path)
    if manifest is None:
        return

    for field in ("name", "description", "version"):
        if not manifest.get(field):
            fail(manifest_path, f"missing required field `{field}`")

    version = manifest.get("version", "")
    if version and not SEMVER.match(version):
        fail(manifest_path, f"version `{version}` is not semver (x.y.z)")

    if manifest.get("name") != plugin_dir.name:
        fail(manifest_path, f"name `{manifest.get('name')}` does not match directory `{plugin_dir.name}`")

    # The tag and release workflows read the version from both files, so drift
    # between them would ship a release under the wrong number.
    for field in ("name", "description", "version"):
        if entry.get(field) != manifest.get(field):
            fail(
                MARKETPLACE,
                f"plugin `{plugin_dir.name}` {field} is {entry.get(field)!r} here "
                f"but {manifest.get(field)!r} in plugin.json",
            )

    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        return
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        check_skill(skill_dir, seen)


def main() -> int:
    marketplace = load_json(MARKETPLACE)
    if marketplace is None:
        print("\n".join(errors), file=sys.stderr)
        return 1

    if not marketplace.get("name"):
        fail(MARKETPLACE, "missing required field `name`")
    if not isinstance(marketplace.get("owner"), dict):
        fail(MARKETPLACE, "missing required object `owner`")

    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or not entries:
        fail(MARKETPLACE, "`plugins` must be a non-empty array")
        print("\n".join(errors), file=sys.stderr)
        return 1

    seen_skills: dict[str, Path] = {}
    listed: set[str] = set()

    for entry in entries:
        name = entry.get("name")
        if not name:
            fail(MARKETPLACE, "a plugin entry has no `name`")
            continue
        if name in listed:
            fail(MARKETPLACE, f"plugin `{name}` is listed twice")
            continue
        listed.add(name)

        source = entry.get("source")
        if not isinstance(source, str):
            # Remote sources (git-subdir and friends) live outside this repo.
            continue
        plugin_dir = (ROOT / source).resolve()
        if not plugin_dir.is_dir():
            fail(MARKETPLACE, f"plugin `{name}` points at missing directory `{source}`")
            continue
        check_plugin(plugin_dir, entry, seen_skills)

    if PLUGINS_DIR.is_dir():
        for plugin_dir in sorted(p for p in PLUGINS_DIR.iterdir() if p.is_dir()):
            if plugin_dir.name not in listed:
                fail(plugin_dir, "plugin directory is not listed in marketplace.json")

    if errors:
        print(f"Validation failed with {len(errors)} problem(s):\n", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(listed)} plugin(s) and {len(seen_skills)} skill(s). All good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
