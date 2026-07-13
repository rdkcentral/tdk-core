# RMF Audio Capture — Requirements

> **Module:** RMF Audio Capture HAL (`rmfAudioCapture`) | **Req ID Prefix:** `VTS-RMFAUDIOCAPTURE`
> **Total requirements:** 8 | **Total test cases:** 17 (16 L1 + 1 L2)

---

## Requirements Document

| Req ID | Classification | Test Scope *(Verify that the DUT...)* |
|--------|----------------|---------------------------------------|
| `VTS-RMFAUDIOCAPTURE-001` | Lifecycle | SHALL open an audio capture session via `RMF_AudioCapture_Open()` and a typed primary capture session via `RMF_AudioCapture_Open_Type()` with `RMF_AC_TYPE_PRIMARY`, each returning `RMF_SUCCESS` with a valid non-null handle, and SHALL close an open session via `RMF_AudioCapture_Close()` returning `RMF_SUCCESS`. |
| `VTS-RMFAUDIOCAPTURE-002` | Functional | SHALL retrieve the default capture settings via `RMF_AudioCapture_GetDefaultSettings()`, returning `RMF_SUCCESS` with a populated settings structure. |
| `VTS-RMFAUDIOCAPTURE-003` | Functional | SHALL start a capture session via `RMF_AudioCapture_Start()` with a valid data-ready callback and stop it via `RMF_AudioCapture_Stop()`, each returning `RMF_SUCCESS`, and during an active capture session non-zero audio data SHALL be delivered to the registered data-ready callback within the expected timeframe. |
| `VTS-RMFAUDIOCAPTURE-004` | Functional | SHALL retrieve the capture status via `RMF_AudioCapture_GetStatus()`, returning `RMF_SUCCESS` with a populated status structure. |
| `VTS-RMFAUDIOCAPTURE-005` | Functional | SHALL retrieve the current active settings via `RMF_AudioCapture_GetCurrentSettings()`, returning `RMF_SUCCESS` with a populated settings structure. |
| `VTS-RMFAUDIOCAPTURE-006` | Error Handling | SHALL return `RMF_INVALID_STATE` from every `rmfAudioCapture` API when it is invoked in an invalid session state — opening while a session is already open, closing an already-closed handle, querying default settings while no session is open, starting capture while already started, or stopping or querying current settings while capture is not started. |
| `VTS-RMFAUDIOCAPTURE-007` | Error Handling | SHALL return `RMF_INVALID_HANDLE` from `RMF_AudioCapture_Close()`, `RMF_AudioCapture_Start()`, `RMF_AudioCapture_Stop()`, `RMF_AudioCapture_GetStatus()`, and `RMF_AudioCapture_GetCurrentSettings()` when they are called with a NULL or outdated handle. |
| `VTS-RMFAUDIOCAPTURE-008` | Error Handling | SHALL return `RMF_INVALID_PARM` from every `rmfAudioCapture` API when it is called with a NULL handle pointer, a NULL settings or status pointer, an invalid capture type, or an out-of-range format, sampling frequency, or data-ready callback. |
