# AI Monitor Service Status Plugins

Show the public service status of **Claude, OpenAI and GitHub** on your
[AI Monitor](https://github.com/tobymarks/esp32-ai-monitor) ESP32 desk display.

Each service has its own installable `.aimplugin` package. The AI Monitor
companion app fetches the official status feed and sends the display scene to
the ESP32 over USB. No service account or API key is required.

## Download

Current package version: **1.1.0** (manifest format **2**).

**Requires a companion app with manifest format 2 support.** Upstream
[PR #11](https://github.com/tobymarks/esp32-ai-monitor/pull/11) is merged.
As of 2026-10-05, use [macOS 1.32.0](https://github.com/tobymarks/esp32-ai-monitor/releases/tag/app-v1.32.0)
or [Windows beta 1.4.1](https://github.com/tobymarks/esp32-ai-monitor/releases/tag/win-beta-v1.4.1).
Windows stable 1.3.0 and older Mac apps cannot install these packages.

For older companions, download the fixed **format-1 v1.0.1** packages:
[Claude](https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/3d71e4d370095b7625a18eafad4d90389e5d9ae6/status-claude.aimplugin),
[OpenAI](https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/3d71e4d370095b7625a18eafad4d90389e5d9ae6/status-openai.aimplugin),
[GitHub](https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/3d71e4d370095b7625a18eafad4d90389e5d9ae6/status-github.aimplugin).
These links stay on v1.0.1 and do not provide intelligent switching.

| Service | Download package | Official status page |
| --- | --- | --- |
| Claude | [status-claude.aimplugin](https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/main/status-claude.aimplugin) | [status.claude.com](https://status.claude.com/) |
| OpenAI | [status-openai.aimplugin](https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/main/status-openai.aimplugin) | [status.openai.com](https://status.openai.com/) |
| GitHub | [status-github.aimplugin](https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/main/status-github.aimplugin) | [githubstatus.com](https://www.githubstatus.com/) |

Install one service or all three. Each installed package becomes a separate
view that you can assign to a display window.

## Requirements

- An AI Monitor ESP32 display, connected to your computer with a USB data cable.
- The Windows or macOS AI Monitor companion app with a **Plugins** tab,
  localization, light scenes and **manifest format 2 support** (see compatible releases above).
- Firmware that reports `sceneProtocol: 1` in its `get_info` response.
- Internet access on the computer for the official status feeds.

Get the companion app and firmware from the
[AI Monitor project](https://github.com/tobymarks/esp32-ai-monitor).
Plugin support depends on the companion and firmware build: if the Plugins tab
is missing or the package is rejected as unsupported, update to a build that
includes the required features. Once compatible firmware is installed,
adding these plugins does not require another firmware flash.

## Installation

### Install a downloaded file

1. Download a package from the table above. Keep its `.aimplugin` extension;
   do not unzip it. If your browser displays the file instead, open it in the
   [repository file list](https://github.com/dlahmapollon/esp32-ai-monitor-service-status-plugin)
   and choose **Download raw file**.
2. Open the AI Monitor companion app and select **Plugins**.
3. Choose the local `.aimplugin` file, then click **Inspect**.
4. Check the service name, version, author, official HTTPS data origin and
   SHA-256 checksum. These packages are unsigned; this is expected.
5. Click **Install**.
6. Open **Display**, add the service view to a window and select that window.
7. Keep the companion app running and the ESP32 connected over USB. The status
   appears after the companion fetches the service feed.

Repeat these steps for additional services. Use touch navigation or timed
window switching to move between your status views and existing AI dashboards.

### Install from a URL

The companion also accepts a direct HTTPS package URL in **Plugins**. Paste one
of the following URLs into the source field, click **Inspect**, review the
package, then click **Install**. Assign it to a window as described above.

**Claude**

```text
https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/main/status-claude.aimplugin
```

**OpenAI**

```text
https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/main/status-openai.aimplugin
```

**GitHub**

```text
https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/main/status-github.aimplugin
```

Use the raw package URL, rather than a GitHub `blob` page URL. The links above
track the packages on `main`; inspecting before installation shows the version
and checksum you are about to install. These URLs now deliver format 2;
use the fixed v1.0.1 links above if your companion is older.

## Automatic switching when a service is disrupted

1. Install the v1.1.0 package in a compatible companion app listed above.
2. Add its service view to a Display window.
3. Select **Intelligent switching** (German: **Intelligenter Wechsel**) as the
   window-switching mode.

When a later successful refresh first reports **Degraded**, **Major outage**
or **Critical outage**, the plugin requests a switch to its service status
window. A change to another disruption level can request another switch, so
an escalation from degraded to a major outage is noticed too. The status page
stays on the ESP32 display; no browser is opened.

The first successful fetch establishes a baseline, so an outage already
present at startup does not cause a switch. Repeated unchanged states,
recovery to Operational, Maintenance, Unknown and failed fetches do not
request switches. The rules read the official feed values directly and work
in either display language.

Detection happens on the approximately five-minute refresh cycle. The
companion then applies its switching policy: at least two minutes on the
current window, ten minutes of cooldown per window and ten minutes of pause
after touch navigation. Events expire after five minutes. These limits mean
a request may be delayed or expire; it is not an unconditional immediate jump.
Manual and timed switching remain available.

### Compatibility and versioning

`attentionRules` is a new manifest field, so v1.1.0 uses **formatVersion 2**,
following the [maintainer's versioning guidance](https://github.com/tobymarks/esp32-ai-monitor/pull/11#issuecomment-5912894571).
Package version (`1.1.0`), manifest format (`2`) and firmware scene protocol
(`1`) are separate version numbers. This feature requires the newer companion,
with no change to the firmware scene protocol.

Older companions cannot install these packages. In particular, Mac
1.32.0-beta.1 and Windows 1.3.0 may report a technical error such as
`unknown field attentionRules`. Companions with PR #11 check the format
version before strict manifest parsing and report when a newer app is needed.
Existing format-1 packages remain valid on compatible companions; they do not
request automatic switches. Future new manifest fields require a new format
version too.

## What the display shows

The view shows the service name, a colored indicator and the official status
page's overall state:

| Status | Indicator |
| --- | --- |
| Operational | Green |
| Degraded | Amber |
| Major outage / Critical outage | Red |
| Maintenance | Slate blue |
| Unknown | Gray |

Data refreshes approximately every five minutes while the view is assigned to
a window. The layouts support portrait, landscape and square displays, dark
and light themes, and English and ASCII-only German text.

The overall status is an aggregate: an operational page does not guarantee
that every component, product or account is unaffected. For incident details,
open the service's official status page.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| No Plugins tab | Use a companion build with display-plugin support. |
| Package rejected / unknown field attentionRules | Update to a format-2 companion listed above, or use the fixed v1.0.1 downloads. Download the actual `.aimplugin` file. |
| Installed, but nothing appears | Add the service view to a Display window and select it. Check the USB connection. |
| Error or stale-data screen | Check the computer's internet access and the official status feed. The companion provides the error screens. |
| No updates after closing the app | Keep the companion running. These plugins fetch data on the computer, not over ESP32 Wi-Fi. |
| Want to update a plugin | Inspect and install the newer package with the same plugin ID. |

## Validation and development

The display layouts in version 1.0.1 were visually checked on a CYD ILI9341 in landscape-left,
with German text and the dark theme, for all three services. Package checks
and host rendering passed for all layouts, both themes, both languages and
six status fixtures. The v1.1.0 attention rules are checked against the PR #11 plugin host;
a service-status hardware switching test has not been completed.
Other hardware and orientations have not all been
visually verified; see the [hardware test guide](docs/hardware-test.md).

To rebuild the three deterministic packages using Python's standard library:

```sh
python3 scripts/package.py
python3 scripts/package.py --check
```

See [Build and validate](docs/authoring.md) for custom Statuspage services,
the shared host validator and fixture-based checks. `plugin.json` is the
Claude source manifest; the build script derives the OpenAI and GitHub packages.

The packages contain declarative JSON manifests, with no executable plugin
code. They use one fixed public HTTPS source per service and are independent
community plugins, not official products of Anthropic, OpenAI or GitHub.

## License

Licensed under the [MIT License](LICENSE).
