#!/usr/bin/env python3
"""Validate every entry in entries/ against schema/entry.schema.json and the index rules.

Usage: python3 scripts/validate.py [repo_root]
Exit code 0 = all entries valid; 1 = at least one error. Warnings never fail the run.
"""
import datetime as dt
import json
import pathlib
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SCHEMA = json.loads((ROOT / "schema" / "entry.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)
STALE_DAYS = 365

# Words that read as ranking or sales copy; the index describes, it does not sell.
BANNED = ["best", "leading", "#1", "world-class", "cheapest", "guaranteed", "certified by brivellis"]


def load(path: pathlib.Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main() -> int:
    errors, warnings, ids, urls = [], [], set(), {}
    files = sorted((ROOT / "entries").glob("*.y*ml"))
    if not files:
        print("No entries found in entries/.")
        return 1
    today = dt.date.today()
    for path in files:
        name = path.name
        if path.suffix != ".yaml":
            errors.append(f"{name}: use the .yaml extension")
        try:
            data = load(path)
        except yaml.YAMLError as exc:
            errors.append(f"{name}: YAML error: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{name}: top level must be a mapping")
            continue
        for err in sorted(VALIDATOR.iter_errors(data), key=lambda e: [str(x) for x in e.path]):
            where = "/".join(str(p) for p in err.path) or "(entry)"
            hint = ""
            if isinstance(err.instance, bool):
                hint = ' (put yes/no in quotes: "yes")'
            elif not isinstance(err.instance, (str, list, dict, int, float)) and err.instance is not None:
                hint = ' (put dates in quotes: "2026-11-14")'
            errors.append(f"{name}: {where}: {err.message}{hint}")
        eid = data.get("id")
        if eid and eid != path.stem:
            errors.append(f"{name}: id '{eid}' must equal the file name '{path.stem}'")
        if eid in ids:
            errors.append(f"{name}: duplicate id '{eid}'")
        ids.add(eid)
        url = (data.get("url") or "").rstrip("/").lower()
        if url and url in urls:
            errors.append(f"{name}: same url as {urls[url]}")
        urls[url] = name
        ai = data.get("ai_ready") or {}
        for flag in ("mcp", "api", "llms_txt"):
            if ai.get(flag) == "yes" and not ai.get(f"{flag}_source"):
                errors.append(f"{name}: ai_ready.{flag} is 'yes' but {flag}_source is missing")
        summary = (data.get("summary") or "").lower()
        for word in BANNED:
            if word in summary.split() or (len(word) > 4 and word in summary):
                errors.append(f"{name}: summary uses ranking/sales wording '{word}'")
        checked = data.get("last_checked")
        try:
            age = (today - dt.date.fromisoformat(checked)).days if checked else None
        except ValueError:
            age = None
            errors.append(f"{name}: last_checked is not a real date")
        if age is not None and age < -1:  # one day of slack for time zones
            errors.append(f"{name}: last_checked is in the future")
        if age is not None and age > STALE_DAYS:
            warnings.append(f"{name}: last checked {age} days ago (re-check due)")
    for w in warnings:
        print(f"WARNING {w}")
    for e in errors:
        print(f"ERROR   {e}")
    print(f"{len(files)} entries, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
