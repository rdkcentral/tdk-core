## Display_Info Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `DINFO‑REQ‑001` | SHALL return a boolean audio passthrough status (isaudiopassthrough) indicating whether HDMI audio is passed through to the TV |
| `DINFO‑REQ‑002` | SHALL return a boolean HDMI connection status (connected), and SHALL return the correct disconnected status when queried without a TV connected |
| `DINFO‑REQ‑003` | SHALL return the current display width in pixels, the display height in pixels, and the vertical frequency, each consistent with the active resolution reported by DisplaySettings; SHALL emit the updated resolution via the pre-change and post-change display update events when the resolution is changed |
| `DINFO‑REQ‑004` | SHALL return the HDCP protocol version in use on the active HDMI output |
| `DINFO‑REQ‑005` | SHALL return the display port name string for the active HDMI output |
| `DINFO‑REQ‑006` | SHALL return EDID data of the expected length for the connected TV |
| `DINFO‑REQ‑007` | SHALL return the HDR formats supported by the connected TV, the HDR formats supported by the STB, and the HDR format currently in use |
| `DINFO‑REQ‑008` | SHALL return the total GPU RAM available and the amount of free GPU RAM |
| `DINFO‑REQ‑009` | SHALL return the physical display width and height in centimetres, the colour space, colour depth, quantization range, colorimetry list, and EOTF for the connected display |
| `DINFO‑REQ‑010` | SHALL remain functional after repeated activate/deactivate stress cycles, and SHALL emit the statechange event with the correct plugin state when activated and deactivated |
