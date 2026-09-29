# AI Monitor Service Status plugin

Public service health for the [AI Monitor](https://github.com/tobymarks/esp32-ai-monitor)
ESP32 display. The companion app fetches a Statuspage-compatible JSON endpoint
and sends a small scene over USB. The package contains only a declarative
manifest; it runs no third-party code on the computer or ESP32. This repository
contains the plugin packages and their source manifest, separate from the
companion application's plugin manager.

## Choose a service

Install the package for the status page you want to see:

| Package | Status page |
| --- | --- |
| `status-claude.aimplugin` | [Claude](https://status.claude.com/) |
| `status-openai.aimplugin` | [OpenAI](https://status.openai.com/) |
| `status-github.aimplugin` | [GitHub](https://www.githubstatus.com/) |

Each package is a separate view, so more than one can be installed and assigned
to different windows. The current display-plugin format accepts one fixed HTTPS
source per package. Service choice therefore happens by installing the matching
package, rather than through a setting in the companion app.

This repository is private, so the companion cannot install its packages from
an unauthenticated GitHub URL. Download the chosen `.aimplugin` file while
signed in to GitHub, or use a local clone of this repository. In **Plugins**,
choose the local file, inspect its author, HTTPS data origin, checksum and
unsigned state, then install it. In **Display**, assign the new view to a
window and select it. The companion and firmware must support display plugins
(`sceneProtocol: 1`). These packages also use the companion's localization and
light-theme extensions; older companion builds that lack them will reject the
package.

The view refreshes about every five minutes while assigned to a window. It
shows the page's overall indicator as Operational, Degraded, Major outage,
Critical outage, Maintenance or Unknown. The status color and text work in
portrait, landscape and square layouts, with dark and light themes and English
and ASCII-only German display text. Network failures and stale data use the
companion's built-in status screens. A healthy overall status does not guarantee
that every individual product or account is unaffected.

## Build another Statuspage service

`plugin.json` is the Claude source manifest. Python's standard library builds
the deterministic preset packages:

```sh
python3 scripts/package.py
python3 scripts/package.py --check
```

To build a package for another public page with the same `status.indicator`
schema, use its **direct** `/api/v2/status.json` endpoint:

```sh
python3 scripts/package.py --custom example "Example Service" \
  https://status.example.com/api/v2/status.json
```

This creates `status-example.aimplugin` with its own stable plugin ID. Use a
different lowercase ID for each service. Confirm that the endpoint returns
JSON with `status.indicator` and the standard Statuspage values before
installing. The plugin host does not follow HTTP redirects, so use the final
HTTPS address. No account or API key should appear in the URL.

## Validate

Run `python3 scripts/package.py --check` to verify that the committed packages
match the source manifest. With the AI Monitor checkout alongside this
repository, run the shared host validator and render the synthetic fixture:

```sh
cargo run --quiet --locked --manifest-path ../esp32-ai-monitor/companion-windows/Cargo.toml \
  -p aimonitor-plugin-host -- inspect status-claude.aimplugin
cargo run --quiet --locked --manifest-path ../esp32-ai-monitor/companion-windows/Cargo.toml \
  -p aimonitor-plugin-host -- render status-claude.aimplugin - all fixture.json
cargo run --quiet --locked --manifest-path ../esp32-ai-monitor/companion-windows/Cargo.toml \
  -p aimonitor-plugin-host -- render status-claude.aimplugin - all fixture.json --locale=de --theme=light
```

Repeat the `inspect` and `render` commands with `status-openai.aimplugin` and
`status-github.aimplugin`. To check the live source, omit `fixture.json` from
the render command. This calls the service over HTTPS. Then follow the
[hardware test guide](docs/hardware-test.md) to verify the actual display,
window switching, offline behavior and restart persistence.

All three built-in endpoints were checked directly on 2026-09-29. They are
public HTTPS JSON sources and need no API key. Packages are unsigned; the
companion displays and checks a SHA-256 checksum during installation.
