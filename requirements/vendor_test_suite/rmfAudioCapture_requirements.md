# RMF Audio Capture — Requirements

> **Module:** RMF Audio Capture HAL (`rmfAudioCapture`) | **Req ID Prefix:** `VTS-RMFAUDIOCAPTURE`
> **Total requirements:** 3 | **Total test cases:** 17 (16 L1 + 1 L2)

---

## Step 1 — Requirement Categorisation Grouping

Requirements are grouped by **functional capability** of the `rmfAudioCapture` HAL interface.
The module provides open/close session lifecycle (including typed open), capture control
(default-settings retrieval, start, stop), and status/settings queries.

Positive L1 tests validate individual API correctness in isolation. The single L2 test drives an
end-to-end capture workflow — open, start with a data-ready callback, wait for audio buffers, and
stop — verifying non-zero audio data is delivered. As this validates behavioural data flow rather
than a write-then-read-back, it is grouped as **Functional**. All negative L1 tests exclusively
verify `RMF_INVALID_PARM` and `RMF_INVALID_STATE` contracts and are consolidated into a single
**Error Handling** requirement.

| Req ID | Functional Capability | Classification | # Tests |
|--------|-----------------------|----------------|---------|
| VTS-RMFAUDIOCAPTURE-001 | Audio capture session open and close lifecycle (default and typed) | Lifecycle | 3 |
| VTS-RMFAUDIOCAPTURE-002 | Capture control and settings/status retrieval — default settings, start, stop, status, current settings | Functional | 6 |
| VTS-RMFAUDIOCAPTURE-003 | API error handling — invalid-parameter and invalid-state conditions | Error Handling | 8 |
| | **Total** | | **17** |

---

### VTS-RMFAUDIOCAPTURE-001 — Audio capture session open and close lifecycle (default and typed) (3 tests)

L1 positive (3): RMF_Open_Type_primary_L1_pos, RMF_Open_L1_pos, RMF_Close_L1_pos

---

### VTS-RMFAUDIOCAPTURE-002 — Capture control and settings/status retrieval (6 tests)

L1 positive (5): RMF_GetDefaultSettings_L1_pos, RMF_Start_L1_pos, RMF_Stop_L1_pos, RMF_GetStatus_L1_pos, RMF_GetCurrentSettings_L1_pos

L2 (1): l2_rmf_primary_data_check

---

### VTS-RMFAUDIOCAPTURE-003 — API error handling (8 tests)

L1 negative (8): RMF_Open_Type_primary_L1_neg, RMF_Open_L1_neg, RMF_Close_L1_neg, RMF_GetDefaultSettings_L1_neg, RMF_Start_L1_neg, RMF_Stop_L1_neg, RMF_GetStatus_L1_neg, RMF_GetCurrentSettings_L1_neg

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `VTS-RMFAUDIOCAPTURE-001` | SHALL open an audio capture session via `RMF_AudioCapture_Open()` and open a typed primary capture session via `RMF_AudioCapture_Open_Type()` with `RMF_AC_TYPE_PRIMARY`, each returning `RMF_SUCCESS` with a valid non-null handle. SHALL close an open capture session via `RMF_AudioCapture_Close()` returning `RMF_SUCCESS`. |
| `VTS-RMFAUDIOCAPTURE-002` | SHALL retrieve the default capture settings via `RMF_AudioCapture_GetDefaultSettings()` returning `RMF_SUCCESS` with a populated settings structure. SHALL start a capture session via `RMF_AudioCapture_Start()` with a valid data-ready callback and stop it via `RMF_AudioCapture_Stop()`, each returning `RMF_SUCCESS`. SHALL retrieve the capture status via `RMF_AudioCapture_GetStatus()` and the current active settings via `RMF_AudioCapture_GetCurrentSettings()`, each returning `RMF_SUCCESS` with a populated structure. During an active capture session, non-zero audio data SHALL be delivered to the registered data-ready callback within the expected timeframe. |
| `VTS-RMFAUDIOCAPTURE-003` | SHALL enforce the following error code contracts across all `rmfAudioCapture` APIs: `RMF_AudioCapture_Open()`, `RMF_AudioCapture_Open_Type()`, `RMF_AudioCapture_Close()`, `RMF_AudioCapture_GetDefaultSettings()`, `RMF_AudioCapture_Start()`, `RMF_AudioCapture_GetStatus()`, and `RMF_AudioCapture_GetCurrentSettings()` SHALL each return `RMF_INVALID_PARM` when called with a NULL handle or NULL output/settings pointer; `RMF_AudioCapture_Stop()` SHALL return `RMF_INVALID_STATE` when called on a handle that has not been started. |
