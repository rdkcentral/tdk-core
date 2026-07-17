## HdmiCecSource Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `HDMICEC‑REQ‑001` | SHALL return a list of CEC-enabled devices when a CEC-capable device is connected, return an empty device list when no CEC-capable devices are connected, and return an error response for getDeviceList, getEnabled, getOSDName, getVendorId, and getOTPEnabled when the CEC driver is not enabled |
| `HDMICEC‑REQ‑002` | SHALL successfully enable and disable the HdmiCEC driver via setEnabled and reflect the updated state in subsequent getEnabled calls |
| `HDMICEC‑REQ‑003` | SHALL retrieve the current OSD name, successfully update it, confirm the updated name is returned by a subsequent call, and return an error response when setOSDName is invoked with an invalid name |
| `HDMICEC‑REQ‑004` | SHALL successfully enable and disable the OTP option, confirm the state is correctly reflected via getOTPEnabled, and return an error when an OTP action is performed while the OTP option is disabled |
| `HDMICEC‑REQ‑005` | SHALL retrieve the current vendor ID, successfully update it, confirm the updated value is returned by a subsequent call, and return an error response when setVendorId is invoked with an empty value |
| `HDMICEC‑REQ‑006` | SHALL successfully send a standby CEC message to a connected device, and return an error when a standby message is sent while the CEC driver is not enabled |
| `HDMICEC‑REQ‑007` | SHALL return the correct active source status as false when the DUT is not the active source, and return true when the DUT is the active source |
| `HDMICEC‑REQ‑008` | SHALL emit the onDeviceInfoUpdated event when device information genuinely changes (e.g., OSD name change), not emit the event when the same OSD name is set or when no device info changes, emit the standbyMessageReceived event when a standby CEC message is received, and emit the onActiveSourceStatusUpdated event when standby or performOTP is called |
| `HDMICEC‑REQ‑009` | SHALL emit the statechange event with the correct plugin state when the HdmiCecSource plugin is activated and deactivated, and emit the all event for the same lifecycle transitions |
| `HDMICEC‑REQ‑010` | SHALL return an error response when sendKeyPressEvent is invoked without parameters, with an invalid logical address, with an invalid key code, or with missing key code or logical address parameters, and return an error when setEnabled or setOTPEnabled are invoked without parameters |
