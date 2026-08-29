#!/usr/bin/env python3
"""Print one `name<TAB>version<TAB>path` line per local plugin in the marketplace.

Shared by the auto-tag and release workflows so both derive tag names the same
way. Plugins with a remote source are skipped: this repo does not build them.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())

    for entry in marketplace.get("plugins", []):
        source = entry.get("source")
        if not isinstance(source, str):
            continue
        manifest = ROOT / source / ".claude-plugin" / "plugin.json"
        if not manifest.is_file():
            print(f"missing {manifest}", file=sys.stderr)
            return 1
        plugin = json.loads(manifest.read_text())
        rel = (ROOT / source).resolve().relative_to(ROOT)
        print(f"{plugin['name']}\t{plugin['version']}\t{rel}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
