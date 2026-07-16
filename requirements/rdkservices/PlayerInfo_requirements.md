## PlayerInfo Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `PI‑REQ‑001` | SHALL return the list of supported audio codecs matching the device-specific expected values, and return the list of supported video codecs matching the expected values |
| `PI‑REQ‑002` | SHALL report the audio equivalence enabled state, Dolby Atmos metadata support, and current Dolby sound mode |
| `PI‑REQ‑003` | SHALL successfully enable and disable Dolby Atmos output mode and confirm the resulting state, and SHALL set and verify all supported display resolutions |
| `PI‑REQ‑004` | SHALL emit the dolby_audiomodechanged event when the Dolby audio mode changes |
| `PI‑REQ‑005` | SHALL emit the statechange event with the correct plugin state when the PlayerInfo plugin is activated and deactivated |
