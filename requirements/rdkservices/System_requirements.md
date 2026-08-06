## System Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `SYS‑REQ‑001` | SHALL return the ESTB MAC address, serial number, all MAC addresses (WiFi, Bluetooth, ETH, RF4CE), model number, device type, box IP address, build type, image version, and manufacturing serial number via the respective API methods, and validate the device MAC address against the expected value |
| `SYS‑REQ‑002` | SHALL return the firmware version string, report the firmware upgrade progress/status via getFirmwareUpdateInfo, and validate a firmware upgrade completion via the corresponding API |
| `SYS‑REQ‑003` | SHALL return the current device uptime, and confirm that the system uptime reflects a reset after a reboot operation |
| `SYS‑REQ‑004` | SHALL return the requested RFC configuration values, return the RFC enabled status, and return an empty result when queried with an empty RFC parameter list |
| `SYS‑REQ‑005` | SHALL successfully set and get the power state, confirm the power state before a reboot from both the running and standby states, and return an error response when setPowerState is invoked with an invalid state value |
| `SYS‑REQ‑006` | SHALL successfully set and get the time zone DST, set and get all supported time zones individually, confirm the time zone persists after a reboot, emit the onTimeZoneDSTChanged event when the time zone is changed, and return an error response when an invalid time zone is set |
| `SYS‑REQ‑007` | SHALL successfully set the device to NORMAL mode, emit the onSystemModeChanged event when the system mode changes, and return an error response when an invalid mode value is set |
| `SYS‑REQ‑008` | SHALL emit the onRebootRequest event when a reboot is initiated |
| `SYS‑REQ‑009` | SHALL successfully enable and disable telemetry opt-out, return the device public IP address, and return the HDR capabilities supported by the device |
| `SYS‑REQ‑010` | SHALL successfully toggle the network standby mode and confirm the updated state via the onNetworkStandbyModeChanged event, and confirm the SSH service state after a reboot from standby |
| `SYS‑REQ‑011` | SHALL successfully set and retrieve a friendly name, confirm the friendly name persists after a reboot, and return the expected response when an empty string is set as the friendly name |
| `SYS‑REQ‑012` | SHALL successfully set and get a valid territory and region, and return an error response when setTerritory is invoked with invalid, empty, missing combinations of territory and region parameters |
| `SYS‑REQ‑013` | SHALL emit the statechange event with the correct plugin state when the System plugin is activated and deactivated, and return an error response when an API is called with an invalid or unsupported parameter key |
