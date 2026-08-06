# RMF Audio Capture — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑RMFAUDIOCAPTURE‑001` | SHALL open an audio capture session and a primary audio capture session, each with a valid non-null handle, and close an open session. |
| `VTS‑RMFAUDIOCAPTURE‑002` | SHALL retrieve the default capture settings as a populated settings structure. |
| `VTS‑RMFAUDIOCAPTURE‑003` | SHALL start a capture session with a valid data-ready callback and stop it, with non-zero audio data delivered to the registered data-ready callback within the expected timeframe during an active capture session. |
| `VTS‑RMFAUDIOCAPTURE‑004` | SHALL retrieve the capture status as a populated status structure. |
| `VTS‑RMFAUDIOCAPTURE‑005` | SHALL retrieve the current active settings as a populated settings structure. |
| `VTS‑RMFAUDIOCAPTURE‑006` | SHALL report an invalid-state error for operations invoked in an invalid session state (e.g., opening while already open, closing when closed, or starting/stopping capture out of order), an invalid-handle error for null or outdated handles, and an invalid-parameter error for null handle, settings, or status pointers, an invalid capture type, or out-of-range format, sampling frequency, or callback values. |
