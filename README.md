# AI Monitor Service Status Plugins

Show the public service status of **Claude, OpenAI and GitHub** on your
[AI Monitor](https://github.com/tobymarks/esp32-ai-monitor) ESP32 desk display.

Each service has its own installable `.aimplugin` package. The AI Monitor
companion app fetches the official status feed and sends the display scene to
the ESP32 over USB. No service account or API key is required.

## Download

Current package version: **1.0.1**.

| Service | Download package | Official status page |
| --- | --- | --- |
| Claude | [status-claude.aimplugin](https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/main/status-claude.aimplugin) | [status.claude.com](https://status.claude.com/) |
| OpenAI | [status-openai.aimplugin](https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/main/status-openai.aimplugin) | [status.openai.com](https://status.openai.com/) |
| GitHub | [status-github.aimplugin](https://raw.githubusercontent.com/dlahmapollon/esp32-ai-monitor-service-status-plugin/main/status-github.aimplugin) | [githubstatus.com](https://www.githubstatus.com/) |

Install one service or all three. Each installed package becomes a separate
view that you can assign to a display window.

## Requirements

- An AI Monitor ESP32 display, connected to your computer with a USB data cable.
- The Windows or macOS AI Monitor companion app with a **Plugins** tab and
  support for localized plugins and light scenes.
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
and checksum you are about to install.

## What the display shows

The view shows the service name, a colored indicator and the official status
page's overall state:

| Status | Indicator |
| --- | --- |
| Operational | Green |
| Degraded | Amber |
| Major outage / Critical outage | Red |
| Maintenance | Purple |
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
| Package rejected | Check support for localization and light scenes; download the actual `.aimplugin` file. |
| Installed, but nothing appears | Add the service view to a Display window and select it. Check the USB connection. |
| Error or stale-data screen | Check the computer's internet access and the official status feed. The companion provides the error screens. |
| No updates after closing the app | Keep the companion running. These plugins fetch data on the computer, not over ESP32 Wi-Fi. |
| Want to update a plugin | Inspect and install the newer package with the same plugin ID. |

## Validation and development

Version 1.0.1 was visually checked on a CYD ILI9341 in landscape-left,
with German text and the dark theme, for all three services. Package checks
and host rendering passed for all layouts, both themes, both languages and
six status fixtures. Other hardware and orientations have not all been
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
