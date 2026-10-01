# Build and validate service status plugins

## Build another Statuspage service

`plugin.json` is the Claude source manifest (package v1.1.0, format 2).
The generated packages inherit its attention rules. Use a plugin host built
from AI Monitor PR #11 or a later release containing it; older hosts reject
these format-2 packages. Python's standard library builds
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
[hardware test guide](hardware-test.md) to verify the actual display,
window switching, offline behavior and restart persistence.


## Validate disruption rules

The rules compare raw `status.indicator` values: `minor`, `major` and
`critical`. Each level has a distinct stable rule ID, allowing severity
changes to request attention. Do not match translated display strings.
`none`, `maintenance`, unknown or missing indicators remain inactive.

Run the integration checks against the actual PR #11 plugin host:

```sh
python3 scripts/test_attention.py /path/to/aimonitor-plugin-host
```

These checks validate all packages and render every layout, both themes and
both languages for each supported indicator and missing data. The host emits
rule states; baseline tracking and false-to-true switching are owned by the
companion. See the README for its timing limits. A new manifest field requires
a higher format version; package version bumps do not replace that requirement.
