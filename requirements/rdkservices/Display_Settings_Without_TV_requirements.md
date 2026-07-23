## Display_Settings_Without_TV Plugin — Specifications


| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `DSWTV‑REQ‑001` | SHALL return a failure response when readEDID is called and no TV is connected, confirming EDID data is unavailable without a display |
| `DSWTV‑REQ‑002` | SHALL return an empty connected video displays list when no TV is connected, and return false for the active input status when no TV is connected both with and without a video port parameter |
| `DSWTV‑REQ‑003` | SHALL return the expected HDCP status and audio ports connection status when no TV is connected, confirming graceful API behaviour in a no-display environment |
| `DSWTV‑REQ‑004` | SHALL return the expected error response for getCurrentResolution, getDefaultResolution, and getPortName when no TV is connected, and return the expected error response when setCurrentResolution is invoked without TV |
