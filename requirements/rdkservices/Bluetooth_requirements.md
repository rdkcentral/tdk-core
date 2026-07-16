## Bluetooth Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `BT‑REQ‑001` | SHALL retrieve the current Bluetooth device name via getName and successfully update it via setName, confirming the updated name is returned by a subsequent getName call |
| `BT‑REQ‑002` | SHALL retrieve the current Bluetooth discoverable status, toggle it via setDiscoverable, and confirm the updated value is returned by a subsequent isDiscoverable call |
| `BT‑REQ‑003` | SHALL successfully scan for LOUDSPEAKER and LE profile Bluetooth devices, and SHALL emit the onRequestFailed event with PAIRING_FAILED status when a pair request is sent to an invalid device |
| `BT‑REQ‑004` | SHALL return a valid API version number |
| `BT‑REQ‑005` | SHALL emit the statechange event with the correct plugin state when the Bluetooth plugin is activated and deactivated, and SHALL emit the all event for the same lifecycle transitions |
| `BT‑REQ‑006` | SHALL successfully pair and unpair a LOUDSPEAKER device, and SHALL successfully connect to and disconnect from a LOUDSPEAKER device |
| `BT‑REQ‑007` | SHALL return an appropriate error response when a WiFi connect attempt fails with an invalid or unreachable device |
