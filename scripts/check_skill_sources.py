#!/usr/bin/env python3
"""Compare imported skills with every configured upstream source tree.

The registry stores the upstream commit and the SHA-256 of each imported skill
tree at import time. This command does not overwrite local skills or metadata;
it reports upstream updates, local customizations, missing skills, and upstream
skills that have not been imported.

By default each unique repository is fetched once into a temporary directory.
Use --checkout REPOSITORY=PATH for existing clones when checking offline.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "skill-sources.json"


def tree_sha256(directory: Path) -> str:
    """Hash sorted relative paths and bytes, including all regular files."""
    digest = hashlib.sha256()
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        digest.update(path.relative_to(directory).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def git_output(*args: str) -> str:
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def get_repo(
    repository: str,
    ref: str,
    temp_root: Path,
    checkouts: dict[str, Path],
) -> Path:
    checkout_key = repository.removesuffix(".git")
    if checkout_key in checkouts:
        return checkouts[checkout_key].resolve()

    clone_path = temp_root / f"repo-{hashlib.sha256(repository.encode()).hexdigest()[:12]}"
    subprocess.run(
        ["git", "clone", "--quiet", "--depth", "1", "--branch", ref, repository, str(clone_path)],
        check=True,
    )
    return clone_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkout",
        action="append",
        metavar="REPOSITORY=PATH",
        default=[],
        help="use an existing clone for this repository instead of fetching (repeatable)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 when any drift or unimported upstream skills are found",
    )
    args = parser.parse_args()

    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read {REGISTRY.relative_to(ROOT)}: {exc}", file=sys.stderr)
        return 2

    sources = registry.get("sources")
    if not isinstance(sources, list) or not sources:
        print("skill-sources.json must contain a non-empty sources array", file=sys.stderr)
        return 2

    repositories = {(source["repository"], source["ref"]) for source in sources}
    checkouts: dict[str, Path] = {}
    for value in args.checkout:
        repository, separator, path = value.partition("=")
        if not separator or not repository or not path:
            print("--checkout must be REPOSITORY=PATH", file=sys.stderr)
            return 2
        checkouts[repository.removesuffix(".git")] = Path(path)

    findings: list[tuple[str, str]] = []
    try:
        with tempfile.TemporaryDirectory(prefix="skill-source-check-") as tmp:
            temp_root = Path(tmp)
            repo_checkouts: dict[tuple[str, str], Path] = {}
            for repository, ref in sorted(repositories):
                repo_checkouts[(repository, ref)] = get_repo(
                    repository, ref, temp_root, checkouts
                )

            tracked_local_paths: set[str] = set()
            for source in sources:
                repo = repo_checkouts[(source["repository"], source["ref"])]
                source_root = repo / source["path"]
                if not source_root.is_dir():
                    raise FileNotFoundError(
                        f"upstream source directory does not exist: {source['repository']}:{source['path']}"
                    )

                if source.get("single_skill"):
                    upstream_skills = {source_root.name: source_root}
                else:
                    upstream_skills = {
                        item.name: item
                        for item in source_root.iterdir()
                        if item.is_dir() and (item / "SKILL.md").is_file()
                    }
                tracked = {item["name"]: item for item in source.get("skills", [])}
                current_commit = git_output("-C", str(repo), "rev-parse", "HEAD")
                print(f"Source {source['repository']}:{source['path']} @ {current_commit[:12]}")
                observed_commits = {
                    item.get("observed_upstream_commit") or item.get("imported_commit")
                    for item in tracked.values()
                } - {None}
                if observed_commits and current_commit not in observed_commits:
                    baseline = ", ".join(sorted(commit[:12] for commit in observed_commits))
                    print(f"  source-advanced   last observed at {baseline}")
                    findings.append(("source-advanced", source["path"]))

                for name, item in sorted(tracked.items()):
                    tracked_local_paths.add(item["local_path"])
                    upstream_dir = upstream_skills.get(name)
                    local_dir = ROOT / item["local_path"]
                    if upstream_dir is None:
                        findings.append(("upstream-missing", name))
                        print(f"  upstream-missing  {name}")
                        continue
                    if not local_dir.is_dir():
                        findings.append(("local-missing", name))
                        print(f"  local-missing     {name} -> {item['local_path']}")
                        continue

                    upstream_hash = tree_sha256(upstream_dir)
                    local_hash = tree_sha256(local_dir)
                    upstream_baseline = item.get("observed_upstream_sha256") or item.get("imported_sha256")
                    local_baseline = item.get("local_baseline_sha256") or item.get("imported_sha256")
                    statuses = []
                    if upstream_baseline and upstream_hash != upstream_baseline:
                        statuses.append("upstream-changed")
                    if local_baseline and local_hash != local_baseline:
                        statuses.append("local-customized")
                    if upstream_hash != local_hash:
                        statuses.append("local-differs-from-upstream")
                    if not item.get("imported_commit"):
                        statuses.append("import-history-unknown")
                    if statuses:
                        for status in statuses:
                            findings.append((status, name))
                        print(f"  {' + '.join(statuses):<34} {name}")
                    else:
                        print(f"  current           {name}")

                for name in sorted(set(upstream_skills) - set(tracked)):
                    findings.append(("not-imported", name))
                    print(f"  not-imported      {name} (available upstream in {source['path']})")

            local_skills_root = ROOT / "plugins"
            for skill_md in sorted(local_skills_root.glob("*/skills/*/SKILL.md")):
                relative = skill_md.parent.relative_to(ROOT).as_posix()
                if relative not in tracked_local_paths:
                    findings.append(("provenance-missing", skill_md.parent.name))
                    print(f"  provenance-missing {relative}")


    except (OSError, subprocess.CalledProcessError, KeyError, TypeError) as exc:
        print(f"Source crawl failed: {exc}", file=sys.stderr)
        return 2

    if findings:
        counts: dict[str, int] = {}
        for status, _ in findings:
            counts[status] = counts.get(status, 0) + 1
        summary = ", ".join(f"{status}={count}" for status, count in sorted(counts.items()))
        print(f"Findings: {summary}")
        return 1 if args.strict else 0

    print("All tracked skills match their imported upstream versions; no unimported skills found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
