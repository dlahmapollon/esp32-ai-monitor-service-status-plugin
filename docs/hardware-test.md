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
