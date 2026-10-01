#!/usr/bin/env python3
"""Validate status packages and attention states with the real format-2 host."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "none": None, "minor": "degraded", "major": "major-outage",
    "critical": "critical-outage", "maintenance": None,
    "unexpected": None, None: None,
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", help="PR #11 aimonitor-plugin-host executable")
    host = str(Path(parser.parse_args().host).resolve())
    checks = 0
    with tempfile.TemporaryDirectory() as temp:
        fixture = Path(temp) / "source.json"
        for service in ("claude", "openai", "github"):
            package = ROOT / f"status-{service}.aimplugin"
            info = json.loads(subprocess.check_output([host, "inspect", str(package)], text=True))
            assert info["id"] == f"org.aimonitor.status.{service}"
            assert info["version"] == "1.1.0"
            for indicator, active in EXPECTED.items():
                fixture.write_text(json.dumps({"status": {"indicator": indicator}} if indicator is not None else {}))
                for theme in ("dark", "light"):
                    for locale in ("en", "de"):
                        result = json.loads(subprocess.check_output([
                            host, "render", str(package), "-", "all", str(fixture),
                            f"--theme={theme}", f"--locale={locale}",
                        ], text=True))
                        expected = {rule: rule == active for rule in ("degraded", "major-outage", "critical-outage")}
                        assert result["attention"] == expected, (service, indicator, result["attention"])
                        assert set(result["scenes"]) == {"portrait", "landscape", "square"}
                        checks += 1
    print(f"Passed {checks} host attention/render checks across all three services")

if __name__ == "__main__":
    main()
