# Device Settings Video Device — Requirements

> **Module:** Device Settings Video Device HAL (`dsVideoDevice`) | **Req ID Prefix:** `VTS-DSVIDEODEVICE`
> **Total requirements:** 6 | **Total test cases:** 34 (30 L1 + 4 L2)

---

## Step 1 — Requirement Categorisation Grouping

Requirements are grouped by **functional capability** of the `dsVideoDevice` HAL interface. The
module provides init/term lifecycle, video-device handle retrieval, DFC (zoom mode) and HDR control,
capability/codec queries, and display framerate control with change callbacks.

Positive L1 tests validate individual API correctness in isolation (return codes; getters verifying
values within the profile's supported set). The `dsGetDFC` positive test verifies the retrieved zoom
mode is one of the supported DFC values from the device profile, so it is classified as **Profile
Compliance**, grouped with the L2 tests that cross-check HDR capabilities, supported video coding
formats, and codec information against the profile. The L2 `SetAndGetDFC` test writes each DFC value
and reads it back verifying the same value — a genuine round-trip — so it is **Data Integrity**. All
negative L1 tests are consolidated into a single **Error Handling** requirement.

| Req ID | Functional Capability | Classification | # Tests |
|--------|-----------------------|----------------|---------|
| VTS-DSVIDEODEVICE-001 | Video device sub-system initialization and termination lifecycle | Lifecycle | 2 |
| VTS-DSVIDEODEVICE-002 | Video device handle, DFC/HDR control, and capability/codec queries | Functional | 6 |
| VTS-DSVIDEODEVICE-003 | Display framerate control and framerate-change callbacks | Functional | 6 |
| VTS-DSVIDEODEVICE-004 | Capability, codec, and DFC values compliant with the device profile | Profile Compliance | 4 |
| VTS-DSVIDEODEVICE-005 | DFC set-and-read-back integrity | Data Integrity | 1 |
| VTS-DSVIDEODEVICE-006 | API error handling — not-initialized and invalid-parameter conditions | Error Handling | 15 |
| | **Total** | | **34** |

---

### VTS-DSVIDEODEVICE-001 — Video device sub-system initialization and termination lifecycle (2 tests)

L1 positive (2): dsVideoDeviceInit_positive, dsVideoDeviceTerm_positive

---

### VTS-DSVIDEODEVICE-002 — Video device handle, DFC/HDR control, and capability/codec queries (6 tests)

L1 positive (6): dsGetVideoDevice_positive, dsSetDFC_positive, dsGetHDRCaps_positive, dsGetSupportVidFormats_positive, dsGetVideoCodecInfo_positive, dsForceDisableHDR_positive

---

### VTS-DSVIDEODEVICE-003 — Display framerate control and framerate-change callbacks (6 tests)

L1 positive (6): dsSetFRFMode_positive, dsGetFRFMode_positive, dsGetCurrDispFramerate_positive, dsSetDisplayframerate_positive, dsRegFrameratePreCB_positive, dsRegFrameratePostCB_positive

---

### VTS-DSVIDEODEVICE-004 — Capability, codec, and DFC values compliant with the device profile (4 tests)

L1 positive (1): dsGetDFC_positive

L2 (3): GetHDRCapabilities, GetSupportedVideoCodingFormats, GetVideoCodecInfo

---

### VTS-DSVIDEODEVICE-005 — DFC set-and-read-back integrity (1 test)

L2 (1): SetAndGetDFC

---

### VTS-DSVIDEODEVICE-006 — API error handling (15 tests)

L1 negative (15): dsVideoDeviceInit_negative, dsVideoDeviceTerm_negative, dsGetVideoDevice_negative, dsSetDFC_negative, dsGetHDRCaps_negative, dsGetSupportVidFormats_negative, dsGetVideoCodecInfo_negative, dsSetFRFMode_negative, dsGetFRFMode_negative, dsGetCurrDispFramerate_negative, dsSetDisplayframerate_negative, dsRegFrameratePreCB_negative, dsRegFrameratePostCB_negative, dsGetDFC_negative, dsForceDisableHDR_negative

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `VTS-DSVIDEODEVICE-001` | SHALL initialize the Video Device sub-system via `dsVideoDeviceInit()` returning `dsERR_NONE` and SHALL terminate it via `dsVideoDeviceTerm()` returning `dsERR_NONE`. |
| `VTS-DSVIDEODEVICE-002` | SHALL retrieve a valid video-device handle for each index via `dsGetVideoDevice()`, apply a Decoder Format Conversion (DFC) zoom mode via `dsSetDFC()`, query HDR capabilities via `dsGetHDRCapabilities()`, query supported video coding formats via `dsGetSupportedVideoCodingFormats()`, query video codec information via `dsGetVideoCodecInfo()`, and force-disable HDR via `dsForceDisableHDR()`, each returning `dsERR_NONE` with valid output. |
| `VTS-DSVIDEODEVICE-003` | SHALL get and set the Frame Rate Following mode via `dsGetFRFMode()` / `dsSetFRFMode()`, retrieve the current display framerate via `dsGetCurrentDisplayframerate()`, set the display framerate via `dsSetDisplayframerate()`, and register the pre- and post- framerate-change callbacks via `dsRegisterFrameratePreChangeCB()` / `dsRegisterFrameratePostChangeCB()`, each returning `dsERR_NONE`. |
| `VTS-DSVIDEODEVICE-004` | SHALL return values that comply with the device profile: the DFC zoom mode retrieved via `dsGetDFC()` SHALL be one of the supported DFC values declared in the profile; the HDR capabilities from `dsGetHDRCapabilities()`, the supported formats from `dsGetSupportedVideoCodingFormats()`, and the codec information from `dsGetVideoCodecInfo()` SHALL each match the corresponding values declared in the device profile. |
| `VTS-DSVIDEODEVICE-005` | SHALL, for each supported DFC value, apply the value via `dsSetDFC()` and, on reading it back via `dsGetDFC()`, return the same value that was set. |
| `VTS-DSVIDEODEVICE-006` | SHALL enforce the following error code contracts across all `dsVideoDevice` APIs: `dsVideoDeviceInit()` SHALL return an error when called while already initialized; `dsVideoDeviceTerm()`, `dsGetVideoDevice()`, `dsSetDFC()`, `dsGetDFC()`, `dsGetHDRCapabilities()`, `dsGetSupportedVideoCodingFormats()`, `dsGetVideoCodecInfo()`, `dsSetFRFMode()`, `dsGetFRFMode()`, `dsGetCurrentDisplayframerate()`, `dsSetDisplayframerate()`, `dsForceDisableHDR()`, `dsRegisterFrameratePreChangeCB()`, and `dsRegisterFrameratePostChangeCB()` SHALL return `dsERR_NOT_INITIALIZED` when invoked before initialization or after termination, and SHALL return `dsERR_INVALID_PARAM` when called with a NULL output pointer, an invalid handle, or an out-of-range value. |
