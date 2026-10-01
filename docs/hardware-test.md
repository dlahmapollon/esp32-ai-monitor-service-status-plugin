# Hardware test guide

Record the companion OS and version, board variant, firmware version and
selected package. The firmware should report `"sceneProtocol":1` in
`get_info`.

1. In **Plugins**, inspect the local `.aimplugin` file. Confirm the service
   name, version, author, official HTTPS data origin and SHA-256, then install
   it. Assign the service view to a **Display** window and select that window.
2. Compare the displayed state with the service's official status page.
   Confirm that the service name, status text and indicator color are readable.
   The plugin shows the page's overall status, not individual components.
3. On a CYD, check portrait and both landscape orientations. On an S3, check
   the square layout. Also check light and dark display themes and the German
   and English display languages. Look for clipped or overlapping text.
4. Switch to and from another window using touch and automatic switching.
   Check that the clock and AI windows retain their content.
5. Disconnect the companion from the internet while this view is selected.
   After the next refresh, check that an error or stale-data screen is visible.
   Reconnect and verify that the current status returns. The device needs the
   companion connected over USB; this plugin does not fetch data over ESP32
   Wi-Fi.
6. Restart the companion and power cycle the display. Check that installed
   packages and window assignments persist. Remove a package and confirm its
   assigned window is handled correctly.

Live pages may remain operational throughout the test. Use the host render
command with the sample responses in `fixture.json` and `fixtures/` to check
every indicator color and label, including the `Unknown` fallback, without
waiting for a real incident.

## Text-box sizing

Firmware scales node coordinates and box dimensions from 0-1000 to panel
pixels, but Montserrat font sizes remain fixed pixel sizes. A title box must
fit the complete font line height on the smallest supported panel. On the
320x240 CYD in landscape, a height of 250 provides 60 pixels for the
48-pixel title font. Check the bottom of the service title, including
descenders, in both themes and orientations; successful host rendering alone
does not prove that firmware text is unclipped.

## Verified hardware result — 2026-10-01

Daniel confirmed complete service titles and readable status text for Claude,
OpenAI and GitHub v1.0.1 on a CYD ILI9341, firmware 2.23.0-beta.1, using
the Windows PR-7 test companion, German language, dark theme and landscape-left
orientation. The device acknowledged scenes for all three live sources.
Package consistency and 72 host-render combinations (three services, two
themes, two languages and six status fixtures, each with all layouts) passed.
Portrait, landscape-right, light-theme hardware and S3 hardware were not
visually verified in this test.
