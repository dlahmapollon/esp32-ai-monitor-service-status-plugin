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

## Install

1. Use a Mac or Windows AI Monitor companion with the **Plugins** tab. Connect
   firmware that reports `"sceneProtocol":1` in `get_info`. The companion must
   also support plugin localization and light scenes; older builds reject these
   packages.
2. While signed in to GitHub, open the desired `.aimplugin` file in this
   repository and click **Download raw file**. Alternatively, use the file from
   a local clone of this repository.
3. In the companion's **Plugins** tab, choose the downloaded local file and
   click **Inspect**. Confirm the service name, author, official HTTPS data
   origin, checksum and unsigned state, then click **Install**.
4. In **Display**, add the service view to a window and select that window.
   Leave the companion connected to the ESP32 over USB. The first status should
   appear after the companion fetches the service's public JSON endpoint.
5. To monitor another service, repeat steps 2–4 with its package and assign it
   to another window. You can use manual or timed window switching.

This repository is private. Do not paste a GitHub file or raw URL into the
companion's URL installer: it cannot authenticate to private GitHub downloads.
Use the local file import described above.

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
different lowercase ID for each service; the preset IDs `claude`, `openai`,
and `github` are reserved. The display name may contain up to 16 printable
ASCII characters, excluding braces. Confirm that the endpoint returns JSON
with `status.indicator` and the standard Statuspage values. Then run the
`inspect` and `render` commands below with your new package name before
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
`status-github.aimplugin`. Test the remaining status labels and colors by
substituting `fixtures/operational.json`, `fixtures/major.json`,
`fixtures/critical.json`, `fixtures/maintenance.json`, and
`fixtures/unknown.json` for `fixture.json` in the render command. The last
fixture checks the fallback for an unrecognized indicator. To check the live
source, omit the fixture path from the render command. This calls the service
over HTTPS. Then follow the
[hardware test guide](docs/hardware-test.md) to verify the actual display,
window switching, offline behavior and restart persistence.

All three built-in endpoints were checked directly on 2026-09-29. They are
public HTTPS JSON sources and need no API key. Packages are unsigned; the
companion displays and checks a SHA-256 checksum during installation.
