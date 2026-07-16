## Device_Info Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `DI‑REQ‑001` | SHALL return comprehensive system information including CPU load, uptime, and memory stats via systeminfo, and SHALL return a system date that matches the actual DUT date |
| `DI‑REQ‑002` | SHALL return a non-empty list of network interface addresses including MAC and IP fields via the addresses method |
| `DI‑REQ‑003` | SHALL return the expected error message when the socketinfo method is invoked, confirming the API is unsupported |
| `DI‑REQ‑004` | SHALL return correct and validated device identity data including serial number, model name, model ID, firmware version, device type, SoC name, and manufacturer, with firmware version and serial number individually validated against device-specific expected values |
| `DI‑REQ‑005` | SHALL return the list of supported audio ports matching the device-specific expected values, and SHALL return the list of supported video displays matching the expected values |
| `DI‑REQ‑006` | SHALL return a valid host EDID data string matching the device-specific expected length and content, the supported HDCP version matching the configured expected value, and the default resolution matching the expected value |
| `DI‑REQ‑007` | SHALL remain functional after repeated activate/deactivate stress cycles, and SHALL emit the statechange event with the correct plugin state when activated and deactivated |
| `DI‑REQ‑008` | SHALL return valid SoC name and manufacturer information via the respective API properties |
