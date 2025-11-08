#!/usr/bin/env python3
"""Increment the Clickomania build version and propagate it to dependent files."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "version.json"
MANIFEST_FILE = ROOT / "manifest.json"
SERVICE_WORKER_FILE = ROOT / "service-worker.js"
INDEX_FILE = ROOT / "index.html"
BASE_VERSION = "1.0"


def load_build_number() -> int:
    if VERSION_FILE.exists():
        with VERSION_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            return int(data.get("build", 0))
    return 0


def store_build_number(build: int) -> None:
    with VERSION_FILE.open("w", encoding="utf-8") as fh:
        json.dump({"build": build}, fh, indent=2)
        fh.write("\n")


def format_version(build: int) -> str:
    return f"{BASE_VERSION}.{build}"


def update_manifest(version: str) -> None:
    if not MANIFEST_FILE.exists():
        raise SystemExit("manifest.json is required for version bumping")
    with MANIFEST_FILE.open("r", encoding="utf-8") as fh:
        manifest = json.load(fh)
    manifest["version"] = version
    with MANIFEST_FILE.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")


def update_service_worker(version: str) -> None:
    if not SERVICE_WORKER_FILE.exists():
        raise SystemExit("service-worker.js is required for version bumping")
    contents = SERVICE_WORKER_FILE.read_text(encoding="utf-8")
    new_contents, replacements = re.subn(
        r"const APP_VERSION = '[^']+';",
        f"const APP_VERSION = '{version}';",
        contents,
    )
    if replacements != 1:
        raise SystemExit("Failed to update APP_VERSION in service-worker.js")
    SERVICE_WORKER_FILE.write_text(new_contents, encoding="utf-8")


def update_index_meta(version: str) -> None:
    if not INDEX_FILE.exists():
        raise SystemExit("index.html is required for version bumping")
    contents = INDEX_FILE.read_text(encoding="utf-8")
    if 'name="app-version"' not in contents:
        raise SystemExit(
            "index.html must contain a meta tag named 'app-version' for version bumping"
        )
    new_contents, replacements = re.subn(
        r'(<meta name="app-version" content=")[^"]+(" />)',
        rf"\g<1>{version}\g<2>",
        contents,
    )
    if replacements != 1:
        raise SystemExit("Failed to update app-version meta tag in index.html")
    INDEX_FILE.write_text(new_contents, encoding="utf-8")


def main() -> None:
    current_build = load_build_number()
    next_build = current_build + 1
    store_build_number(next_build)
    version = format_version(next_build)
    update_manifest(version)
    update_service_worker(version)
    update_index_meta(version)


if __name__ == "__main__":
    main()
