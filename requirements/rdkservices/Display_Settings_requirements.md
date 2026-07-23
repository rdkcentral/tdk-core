## Display_Settings Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `DS‑REQ‑001` | SHALL return the STB-supported resolutions, the TV-supported resolutions, the connected video displays, the default resolution, and the currently supported resolutions, and successfully set and verify all supported resolutions; also return the current and supported video formats |
| `DS‑REQ‑002` | SHALL return the STB HDR support capability, the TV HDR support capability, the TV HDR capabilities list, and the current and supported video formats |
| `DS‑REQ‑003` | SHALL return the host EDID data and the connected device EDID data |
| `DS‑REQ‑004` | SHALL return the supported audio ports, return the supported audio modes for HDMI0, return settop audio capabilities for HDMI0, return MS12 capabilities for HDMI0, enable and disable the HDMI0 audio port, and return the supported audio modes when no audio port parameter is provided |
| `DS‑REQ‑005` | SHALL return and update the zoom settings on the connected video display |
| `DS‑REQ‑006` | SHALL report the correct video port in-standby status for a valid display, confirm the active input value for a valid display, and return an error response for an invalid display when querying active input value or standby status |
| `DS‑REQ‑007` | SHALL support MS12 audio features including audio compression set/get, dialog enhancement set/get and error handling, DRC mode set/get, and volume leveller set/get for HDMI0 and for all supported mode variants |
| `DS‑REQ‑008` | SHALL correctly report the connected device as a repeater or non-repeater via isConnectedDeviceRepeater |
| `DS‑REQ‑009` | SHALL successfully set and get the audio volume level on HDMI0 including negative values, return the audio gain setting, mute and unmute audio on HDMI0 and emit the mute status changed event, set and get audio delay and audio delay offset, and set the audio mixing status on HDMI0 |
| `DS‑REQ‑010` | SHALL report the current output settings including video and audio format information, and return the supported and current audio formats |
| `DS‑REQ‑011` | SHALL enable and disable Dolby Volume Mode, report the sink Atmos capability, and enable and disable Dolby Atmos output mode |
| `DS‑REQ‑012` | SHALL emit the mute status changed event when audio mute state changes and not emit the event when mute state does not change; emit the volume level changed event when volume changes and not emit the event when volume does not change; correctly reflect mute status after volume increase, volume decrease, and direct mute via key-code operations |
| `DS‑REQ‑013` | SHALL correctly set and verify the color depth capability, and successfully set and verify a fader control value for HDMI0 within range; return an error response when fader control is set with empty or out-of-range values |
| `DS‑REQ‑014` | SHALL persist the selected resolution across a reboot when persistence is enabled, not persist the resolution when persistence is disabled, confirm resolution persists for at least 30 seconds after reboot, emit the resolution pre-change event before a resolution change, and report the correct display connected status after the device returns from light sleep |
