# RMF Audio Capture — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑RMFAUDIOCAPTURE‑001` | SHALL open an audio capture session and a primary audio capture session, each with a valid non-null handle, and close an open session. |
| `VTS‑RMFAUDIOCAPTURE‑002` | SHALL retrieve the default capture settings as a populated settings structure. |
| `VTS‑RMFAUDIOCAPTURE‑003` | SHALL start a capture session with a valid data-ready callback and stop it, with non-zero audio data delivered to the registered data-ready callback within the expected timeframe during an active capture session. |
| `VTS‑RMFAUDIOCAPTURE‑004` | SHALL retrieve the capture status as a populated status structure. |
| `VTS‑RMFAUDIOCAPTURE‑005` | SHALL retrieve the current active settings as a populated settings structure. |
| `VTS‑RMFAUDIOCAPTURE‑006` | SHALL enforce the following error handling contracts across all RMF Audio Capture operations:<br>report an invalid-state error when any operation is invoked in an invalid session state — opening while a session is already open, closing an already-closed session, querying default settings while no session is open, starting capture while already started, or stopping or querying current settings while capture is not started<br>report an invalid-handle error when a close, start, stop, status, or current-settings operation is called with a null or outdated handle<br>report an invalid-parameter error when any operation is called with a null handle pointer, a null settings or status pointer, an invalid capture type, or an out-of-range format, sampling frequency, or data-ready callback. |
