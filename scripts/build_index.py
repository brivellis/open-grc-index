#!/usr/bin/env python3
"""Build dist/index.json (and dist/llms.txt) from entries/*.yaml.

The site (brivellis.com) reads dist/index.json at build time. Entries are sorted
alphabetically by name; nothing is ranked. House entries keep house: true so the
site can label them.

Usage: python3 scripts/build_index.py [repo_root]
"""
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SITE = "https://brivellis.com/open-grc-index"

TYPE_LABELS = {
    "open-source-tool": "Open-source tool",
    "free-template": "Free template or kit",
    "free-course": "Free course",
    "mcp-server": "MCP server or AI connector",
    "open-dataset": "Open dataset or mapping",
    "official-guidance": "Official free guidance",
}


def main() -> int:
    entries = []
    for path in sorted((ROOT / "entries").glob("*.yaml")):
        with path.open(encoding="utf-8") as fh:
            entries.append(yaml.safe_load(fh))
    entries.sort(key=lambda e: e["name"].casefold())
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    payload = {
        "name": "Brivellis Open GRC Index",
        "description": "A free, open index of GRC resources: open-source tools, free templates and kits, free courses, MCP servers, open datasets and official guidance. Alphabetical; nothing is ranked; nothing is paid.",
        "homepage": SITE + "/",
        "source": "https://github.com/brivellis/open-grc-index",
        "data_licence": "CC-BY-4.0",
        # Deterministic, so CI can check that dist/ is current: the newest check date.
        "last_checked": max((e["last_checked"] for e in entries), default=None),
        "count": len(entries),
        "types": TYPE_LABELS,
        "entries": entries,
    }
    (out / "index.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Brivellis Open GRC Index",
        "",
        "> A free, open index of GRC resources (open-source tools, free kits, free courses, MCP servers, open datasets, official guidance) for ISO/IEC 27001, ISO/IEC 20000-1, ISO 22301, ISO/IEC 42001 and NIST CSF 2.0. Alphabetical, sourced, nothing paid or ranked. Entries marked House are Brivellis's own.",
        "",
        f"- Full data (JSON): {SITE}/index.json",
        "- Source and registration: https://github.com/brivellis/open-grc-index",
        "",
        "## Entries",
    ]
    for e in entries:
        house = " (House)" if e.get("house") else ""
        lines.append(f"- [{e['name']}]({SITE}/{e['id']}/){house}: {TYPE_LABELS[e['type']]}. {e['summary']}")
    (out / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote dist/index.json and dist/llms.txt ({len(entries)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
