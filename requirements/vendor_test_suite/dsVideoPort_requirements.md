# Device Settings Video Port — Requirements

> **Module:** Device Settings Video Port HAL (`dsVideoPort`) | **Req ID Prefix:** `VTS-DSVIDEOPORT`
> **Total requirements:** 6 | **Total test cases:** 93 (78 L1 + 15 L2)

---

## Step 1 — Requirement Categorisation Grouping

Requirements are grouped by **functional capability** of the `dsVideoPort` HAL interface.
The module provides initialization/termination lifecycle, read-only port/display/output status
queries, event-callback registration, video-output control operations, paired Set/Get workflows,
and a large set of capability queries whose returned values are cross-checked against the device
profile configuration.

Positive L1 tests validate individual API correctness in isolation — either by checking the return
code, by reading a value twice and confirming consistency, or by comparing the returned value
against the device profile. L2 tests validate end-to-end workflows. Where an L2 test performs a
Set→Get→verify round-trip, the classification is **Data Integrity**. Where an L1 or L2 test compares
the retrieved value against the device profile configuration, the classification is
**Profile Compliance**. Read-consistency queries, callback registrations, and write/enable-only
operations are **Functional**. All negative L1 tests are consolidated into a single **Error Handling**
requirement.

| Req ID | Functional Capability | Classification | # Tests |
|--------|-----------------------|----------------|---------|
| VTS-DSVIDEOPORT-001 | dsVideoPort sub-system initialization and termination lifecycle | Lifecycle | 2 |
| VTS-DSVIDEOPORT-002 | Video port handle retrieval, port/display/output status queries, and event callback registration | Functional | 14 |
| VTS-DSVIDEOPORT-003 | Video output control — HDCP enable, SDR reset, background color, force HDR mode, and force-disable-4K | Functional | 5 |
| VTS-DSVIDEOPORT-004 | Port enable, display resolution, HDMI preference, and preferred color depth — Set/Get round-trip | Data Integrity | 8 |
| VTS-DSVIDEOPORT-005 | Display, HDCP, resolution, and color capability values verified against the device profile | Profile Compliance | 25 |
| VTS-DSVIDEOPORT-006 | API error handling — not-initialized, already-initialized, and invalid-argument conditions | Error Handling | 39 |
| | **Total** | | **93** |

---

### VTS-DSVIDEOPORT-001 — dsVideoPort sub-system initialization and termination lifecycle (2 tests)

L1 positive (2): dsVideoPortInit_pos, dsVideoPortTerm_pos

---

### VTS-DSVIDEOPORT-002 — Video port handle retrieval, port/display/output status queries, and event callback registration (14 tests)

L1 positive (12): dsGetVideoPort_pos, dsIsVideoPortEnabled_pos, dsIsDisplayConnected_pos, dsIsVideoPortActive_pos, dsIsOutputHDR_pos, dsGetVideoEOTF_pos, dsGetCurrentOutputSettings_pos, dsGetIgnoreEDIDStatus_pos, GetForceDisable4KSupport_pos, dsGetHDCPStatus_pos, VideoFormatUpdateRegCB_pos, dsRegisterHdcpStatusCB_pos

L2 (2): VerifyDisplayAndPortStatus, GetHDCPStatus

---

### VTS-DSVIDEOPORT-003 — Video output control: HDCP enable, SDR reset, background color, force HDR mode, and force-disable-4K (5 tests)

L1 positive (5): dsEnableHDCP_pos, dsResetOutputToSDR_pos, dsSetBackgroundColor_pos, dsSetForceHDRMode_pos, SetForceDisable4KSupport_pos

---

### VTS-DSVIDEOPORT-004 — Port enable, display resolution, HDMI preference, and preferred color depth (Set/Get round-trip) (8 tests)

L1 positive (4): dsEnableVideoPort_pos, dsSetResolution_pos, dsSetHdmiPreference_pos, dsSetPreferredColorDepth_pos

L2 (4): EnableDisabledVideoPorts, SetAndGetResolution_src, SetAndGetHdmiPreference, SetAndGetPreferredColorDepth_src

---

### VTS-DSVIDEOPORT-005 — Display, HDCP, resolution, and color capability values verified against the device profile (25 tests)

L1 positive (16): dsIsDisplaySurround_pos, dsGetSurroundMode_pos, dsIsHDCPEnabled_pos, dsGetResolution_pos, dsGetHDCPProtocol_pos, GetHDCPReceiverProtocol_pos, GetHDCPCurrentProtocol_pos, dsGetTVHDRCapabilities_pos, dsSupportedTvResolutions_pos, dsGetMatrixCoefficients_pos, dsGetColorDepth_pos, dsGetColorSpace_pos, dsGetQuantizationRange_pos, dsGetHdmiPreference_pos, dsColorDepthCapb_pos, dsGetPreferredColorDepth_pos

L2 (9): RetrieveVerifySurroundModeCapb, VerifySupportedTvRes, GetHDRCapabilities, VerifyHDCPProtocolStatus, GetColorSpace, GetColorDepth, GetQuantizationRange, GetMatrixCoefficients, CheckColorDepthCapb_src

---

### VTS-DSVIDEOPORT-006 — API error handling (39 tests)

L1 negative (39): dsVideoPortInit_neg, dsVideoPortTerm_neg, dsGetVideoPort_neg, dsIsVideoPortEnabled_neg, dsIsDisplayConnected_neg, dsIsDisplaySurround_neg, dsGetSurroundMode_neg, VideoFormatUpdateRegCB_neg, dsIsVideoPortActive_neg, dsEnableHDCP_neg, dsIsHDCPEnabled_neg, dsEnableVideoPort_neg, dsSetResolution_neg, dsGetResolution_neg, dsRegisterHdcpStatusCB_neg, dsGetHDCPStatus_neg, dsGetHDCPProtocol_neg, GetHDCPReceiverProtocol_neg, GetHDCPCurrentProtocol_neg, dsGetTVHDRCapabilities_neg, dsSupportedTvResolutions_neg, SetForceDisable4KSupport_neg, GetForceDisable4KSupport_neg, dsGetVideoEOTF_neg, dsGetMatrixCoefficients_neg, dsGetColorDepth_neg, dsGetColorSpace_neg, dsGetQuantizationRange_neg, dsGetCurrentOutputSettings_neg, dsIsOutputHDR_neg, dsResetOutputToSDR_neg, dsSetHdmiPreference_neg, dsGetHdmiPreference_neg, dsGetIgnoreEDIDStatus_neg, dsSetBackgroundColor_neg, dsSetForceHDRMode_neg, dsColorDepthCapb_neg, dsGetPreferredColorDepth_neg, dsSetPreferredColorDepth_neg

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `VTS-DSVIDEOPORT-001` | SHALL initialize the Device Settings Video Port sub-system via `dsVideoPortInit()` returning `dsERR_NONE` and SHALL terminate it via `dsVideoPortTerm()` returning `dsERR_NONE`. The module SHALL support re-initialization after a prior termination without error. |
| `VTS-DSVIDEOPORT-002` | SHALL return a valid video port handle for each supported port type and index via `dsGetVideoPort()` returning `dsERR_NONE`, with repeated calls for the same port returning an equal handle. SHALL report the port enabled status via `dsIsVideoPortEnabled()`, the display connection status via `dsIsDisplayConnected()`, the port active status via `dsIsVideoPortActive()`, the HDR output status via `dsIsOutputHDR()`, the current video EOTF via `dsGetVideoEOTF()`, the combined current output settings via `dsGetCurrentOutputSettings()`, the IgnoreEDID status via `dsGetIgnoreEDIDStatus()`, the force-disable-4K state via `dsGetForceDisable4KSupport()`, and the HDCP authentication status via `dsGetHDCPStatus()`, each returning `dsERR_NONE` (or `dsERR_OPERATION_NOT_SUPPORTED` where the operation is unsupported for the port or device type) with consistent results across repeated calls. SHALL successfully register event callbacks for video format updates via `dsVideoFormatUpdateRegisterCB()` and for HDCP status changes via `dsRegisterHdcpStatusCallback()`, each returning `dsERR_NONE`. |
| `VTS-DSVIDEOPORT-003` | SHALL enable HDCP content protection on the video port via `dsEnableHDCP()`, reset the video output to SDR via `dsResetOutputToSDR()`, set the video port background color via `dsSetBackgroundColor()`, force the HDR output mode via `dsSetForceHDRMode()`, and set the force-disable-4K state via `dsSetForceDisable4KSupport()`, each returning `dsERR_NONE` for valid parameters on supported source devices, and returning `dsERR_OPERATION_NOT_SUPPORTED` on device types where the operation is not supported. |
| `VTS-DSVIDEOPORT-004` | SHALL enable and disable the video port via `dsEnableVideoPort()` and confirm the enable state via `dsIsVideoPortEnabled()`; set the display resolution via `dsSetResolution()` and confirm it via `dsGetResolution()`; set the preferred HDMI/HDCP protocol preference via `dsSetHdmiPreference()` and confirm it via `dsGetHdmiPreference()`; and set the preferred color depth via `dsSetPreferredColorDepth()` and confirm it via `dsGetPreferredColorDepth()`, each returning `dsERR_NONE` for valid values on supported ports. The port enable state, resolution, HDMI preference, and preferred color depth retrieved after a Set operation SHALL match the value that was configured. |
| `VTS-DSVIDEOPORT-005` | SHALL retrieve the display audio-surround support via `dsIsDisplaySurround()` and the surround mode via `dsGetSurroundMode()`; the HDCP enabled state via `dsIsHDCPEnabled()`; the current, receiver, and negotiated HDCP protocol versions via `dsGetHDCPProtocol()`, `dsGetHDCPReceiverProtocol()`, and `dsGetHDCPCurrentProtocol()`; the current resolution via `dsGetResolution()`; the TV HDR capabilities via `dsGetTVHDRCapabilities()`; the supported TV resolutions via `dsSupportedTvResolutions()`; the matrix coefficients via `dsGetMatrixCoefficients()`; the color depth via `dsGetColorDepth()`; the color space via `dsGetColorSpace()`; the quantization range via `dsGetQuantizationRange()`; the HDMI preference via `dsGetHdmiPreference()`; the color depth capabilities via `dsColorDepthCapabilities()`; and the preferred color depth via `dsGetPreferredColorDepth()`, each returning `dsERR_NONE` (or `dsERR_OPERATION_NOT_SUPPORTED` where unsupported for the device type), with each returned value matching the corresponding value declared in the device profile configuration, or the profile-defined default value expected for the current display-connection state. |
| `VTS-DSVIDEOPORT-006` | SHALL enforce the following error code contracts across all `dsVideoPort` APIs: `dsVideoPortInit()` SHALL return `dsERR_ALREADY_INITIALIZED` when called while already initialized; `dsVideoPortTerm()` SHALL return `dsERR_NOT_INITIALIZED` when called without prior initialization or after the module has already been terminated; all remaining `dsVideoPort` APIs SHALL return `dsERR_NOT_INITIALIZED` when invoked before initialization or after termination, and SHALL return `dsERR_INVALID_PARAM` when called with an invalid or null port handle, a NULL output pointer, or an out-of-range parameter value. |
