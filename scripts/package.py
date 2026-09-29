#!/usr/bin/env python3
"""Build deterministic service-status plugin packages."""

import argparse
import copy
import hashlib
import io
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZIP_STORED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "plugin.json"
PRESETS = {
    "claude": ("Claude", "https://status.claude.com/api/v2/status.json"),
    "openai": ("OpenAI", "https://status.openai.com/api/v2/status.json"),
    "github": ("GitHub", "https://www.githubstatus.com/api/v2/status.json"),
}


def source_url(value: str) -> str:
    if not value.isascii() or any(not 0x21 <= ord(char) <= 0x7E for char in value):
        raise ValueError("URL must contain only printable ASCII without whitespace")
    url = urlsplit(value)
    if (
        url.scheme != "https"
        or not url.hostname
        or url.username is not None
        or url.password is not None
        or url.fragment
        or url.query
        or url.path != "/api/v2/status.json"
    ):
        raise ValueError("URL must be a credential-free HTTPS Statuspage /api/v2/status.json endpoint")
    return value


def make_manifest(slug: str, name: str, url: str) -> bytes:
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,15}", slug):
        raise ValueError("service ID must be 1-16 lowercase letters, digits or hyphens")
    if (not name or len(name) > 16 or not name.isascii() or not name.isprintable()
            or "{" in name or "}" in name):
        raise ValueError("service name must be 1-16 printable ASCII characters without braces")
    manifest = copy.deepcopy(json.loads(MANIFEST.read_text(encoding="utf-8")))
    manifest["id"] = f"org.aimonitor.status.{slug}"
    validated_url = source_url(url)

    def rename(value):
        if isinstance(value, str):
            return value.replace("Claude", name)
        if isinstance(value, list):
            return [rename(item) for item in value]
        if isinstance(value, dict):
            return {rename(key): rename(item) for key, item in value.items()}
        return value

    manifest = rename(manifest)
    manifest["source"]["url"] = validated_url
    if len(name) > 10:
        # Keep longer custom names within the title boxes on smaller panels.
        for variant in ("scenes", "lightScenes"):
            for layout, font in (("portrait", 20), ("landscape", 24), ("square", 36)):
                for node in manifest[variant][layout]["nodes"]:
                    if node["type"] == "text" and node["text"] == name:
                        node["font"] = font
    return (json.dumps(manifest, ensure_ascii=True, indent=2) + "\n").encode("utf-8")


def make_package(manifest: bytes) -> bytes:
    if len(manifest) > 64 * 1024:
        raise ValueError("manifest exceeds the plugin format limit")
    stream = io.BytesIO()
    info = ZipInfo("plugin.json", (1980, 1, 1, 0, 0, 0))
    info.create_system = 3
    # Stored bytes avoid zlib-version differences between Windows and Linux.
    info.compress_type = ZIP_STORED
    info.external_attr = 0o100644 << 16
    with ZipFile(stream, "w") as archive:
        archive.writestr(info, manifest)
    package = stream.getvalue()
    if len(package) > 256 * 1024:
        raise ValueError("package exceeds the plugin format limit")
    return package


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the three committed preset packages")
    parser.add_argument("--custom", nargs=3, metavar=("ID", "NAME", "URL"),
                        help="build a package for another public Statuspage endpoint")
    args = parser.parse_args()
    if args.check and args.custom:
        parser.error("--check and --custom cannot be combined")
    if args.custom and args.custom[0] in PRESETS:
        parser.error("custom service ID must not replace a preset package")
    services = {args.custom[0]: (args.custom[1], args.custom[2])} if args.custom else PRESETS
    for slug, (name, url) in services.items():
        try:
            package = make_package(make_manifest(slug, name, url))
        except ValueError as error:
            parser.error(str(error))
        path = ROOT / f"status-{slug}.aimplugin"
        if args.check:
            if not path.is_file():
                parser.error(f"{path.name} is missing; run python3 scripts/package.py")
            if path.read_bytes() != package:
                parser.error(f"{path.name} differs from plugin.json; rebuild it")
            with ZipFile(path) as archive:
                if archive.namelist() != ["plugin.json"]:
                    parser.error(f"{path.name} must contain only plugin.json")
        else:
            path.write_bytes(package)
        print(f"{path.name}: {hashlib.sha256(package).hexdigest()}")


if __name__ == "__main__":
    main()
