# Device Settings Video Port — Requirements

> **Module:** Device Settings Video Port HAL (`dsVideoPort`) | **Req ID Prefix:** `VTS-DSVIDEOPORT`
> **Total requirements:** 27 | **Total test cases:** 93 (78 L1 + 15 L2)

---

## Requirements Document

| Req ID | Classification | Test Scope *(Verify that the DUT...)* |
|--------|----------------|---------------------------------------|
| `VTS-DSVIDEOPORT-001` | Lifecycle | SHALL initialize the Device Settings Video Port sub-system via `dsVideoPortInit()` returning `dsERR_NONE` and SHALL terminate it via `dsVideoPortTerm()` returning `dsERR_NONE`. The module SHALL support re-initialization after a prior termination without error. |
| `VTS-DSVIDEOPORT-002` | Functional | SHALL return a valid video port handle for each supported port type and index via `dsGetVideoPort()` returning `dsERR_NONE`, with repeated calls for the same port type and index returning an equal handle. |
| `VTS-DSVIDEOPORT-003` | Data Integrity | SHALL enable and disable each supported video port via `dsEnableVideoPort()` returning `dsERR_NONE`, and the enable state retrieved via `dsIsVideoPortEnabled()` SHALL match the state that was set. |
| `VTS-DSVIDEOPORT-004` | Functional | SHALL report the display connection status of a video port via `dsIsDisplayConnected()` and the port active status via `dsIsVideoPortActive()`, each returning `dsERR_NONE` with a valid status consistent across repeated calls. |
| `VTS-DSVIDEOPORT-005` | Profile Compliance | SHALL report whether the connected display supports audio surround via `dsIsDisplaySurround()` and retrieve the surround mode via `dsGetSurroundMode()`, each returning `dsERR_NONE` with the reported capability matching the value expected for the connected display. |
| `VTS-DSVIDEOPORT-006` | Data Integrity | SHALL set the display resolution of a supported video port via `dsSetResolution()` returning `dsERR_NONE`, and the resolution retrieved via `dsGetResolution()` SHALL match the value that was set. |
| `VTS-DSVIDEOPORT-007` | Profile Compliance | SHALL retrieve the resolutions supported by the connected TV via `dsSupportedTvResolutions()` returning `dsERR_NONE`, with the reported bitmask matching the supported resolutions declared in the device profile configuration. |
| `VTS-DSVIDEOPORT-008` | Profile Compliance | SHALL retrieve the connected TV's HDR capabilities via `dsGetTVHDRCapabilities()` returning `dsERR_NONE`, with the reported capabilities matching the value declared in the device profile configuration. |
| `VTS-DSVIDEOPORT-009` | Functional | SHALL enable HDCP content protection on a supported video port via `dsEnableHDCP()` returning `dsERR_NONE`, report the HDCP enabled state via `dsIsHDCPEnabled()`, and report the HDCP authentication status via `dsGetHDCPStatus()`, each returning `dsERR_NONE` with a valid status. |
| `VTS-DSVIDEOPORT-010` | Profile Compliance | SHALL retrieve the current HDCP protocol version via `dsGetHDCPProtocol()`, the connected receiver's HDCP protocol version via `dsGetHDCPReceiverProtocol()`, and the negotiated (current) HDCP protocol version via `dsGetHDCPCurrentProtocol()`, each returning `dsERR_NONE` with the version matching the value expected from the device profile and connected receiver. |
| `VTS-DSVIDEOPORT-011` | Data Integrity | SHALL set the preferred HDMI/HDCP protocol preference of a supported video port via `dsSetHdmiPreference()` returning `dsERR_NONE`, and the preference retrieved via `dsGetHdmiPreference()` SHALL match the value that was set. |
| `VTS-DSVIDEOPORT-012` | Profile Compliance | SHALL retrieve the color space of a supported video port via `dsGetColorSpace()` returning `dsERR_NONE`, with the reported color space matching the value expected for the connected display. |
| `VTS-DSVIDEOPORT-013` | Profile Compliance | SHALL retrieve the color depth of a supported video port via `dsGetColorDepth()` returning `dsERR_NONE`, with the reported color depth matching the value expected for the connected display. |
| `VTS-DSVIDEOPORT-014` | Profile Compliance | SHALL retrieve the color depth capabilities of a supported video port via `dsColorDepthCapabilities()` returning `dsERR_NONE`, with the reported capabilities matching the value declared in the device profile configuration. |
| `VTS-DSVIDEOPORT-015` | Data Integrity | SHALL set the preferred color depth of a supported video port via `dsSetPreferredColorDepth()` returning `dsERR_NONE`, and the color depth retrieved via `dsGetPreferredColorDepth()` SHALL match the value that was set. |
| `VTS-DSVIDEOPORT-016` | Profile Compliance | SHALL retrieve the quantization range of a supported video port via `dsGetQuantizationRange()` returning `dsERR_NONE`, with the reported range matching the value expected for the connected display. |
| `VTS-DSVIDEOPORT-017` | Profile Compliance | SHALL retrieve the matrix coefficients of a supported video port via `dsGetMatrixCoefficients()` returning `dsERR_NONE`, with the reported coefficients matching the value expected for the connected display. |
| `VTS-DSVIDEOPORT-018` | Functional | SHALL retrieve the current video EOTF (Electro-Optical Transfer Function) of a supported video port via `dsGetVideoEOTF()` returning `dsERR_NONE` with a valid `dsHDRStandard_t` value. |
| `VTS-DSVIDEOPORT-019` | Functional | SHALL report the HDR output status of a supported video port via `dsIsOutputHDR()`, reset the video output to SDR via `dsResetOutputToSDR()`, and force the HDR output mode via `dsSetForceHDRMode()`, each returning `dsERR_NONE` for valid parameters on supported device types, and returning `dsERR_OPERATION_NOT_SUPPORTED` where the operation is not supported. |
| `VTS-DSVIDEOPORT-020` | Functional | SHALL retrieve the combined current output settings of a supported video port via `dsGetCurrentOutputSettings()` returning `dsERR_NONE` with valid output values. |
| `VTS-DSVIDEOPORT-021` | Data Integrity | SHALL set the force-disable-4K state of a supported video port via `dsSetForceDisable4KSupport()` returning `dsERR_NONE`, and the state retrieved via `dsGetForceDisable4KSupport()` SHALL match the value that was set. |
| `VTS-DSVIDEOPORT-022` | Functional | SHALL report the IgnoreEDID status of a supported video port via `dsGetIgnoreEDIDStatus()` returning `dsERR_NONE` with a valid status, or `dsERR_OPERATION_NOT_SUPPORTED` where the operation is not supported. |
| `VTS-DSVIDEOPORT-023` | Functional | SHALL set the video port background color via `dsSetBackgroundColor()` returning `dsERR_NONE` for valid color values on supported device types, and returning `dsERR_OPERATION_NOT_SUPPORTED` where the operation is not supported. |
| `VTS-DSVIDEOPORT-024` | Functional | SHALL successfully register event callbacks for video format updates via `dsVideoFormatUpdateRegisterCB()` and for HDCP status changes via `dsRegisterHdcpStatusCallback()`, each returning `dsERR_NONE`. |
| `VTS-DSVIDEOPORT-025` | Error Handling | SHALL return `dsERR_ALREADY_INITIALIZED` from `dsVideoPortInit()` when it is called while the module is already initialized. |
| `VTS-DSVIDEOPORT-026` | Error Handling | SHALL return `dsERR_NOT_INITIALIZED` from every `dsVideoPort` API when it is invoked without prior initialization or after the module has already been terminated. |
| `VTS-DSVIDEOPORT-027` | Error Handling | SHALL return `dsERR_INVALID_PARAM` from every `dsVideoPort` API when it is called with an invalid or null port handle, a NULL output pointer, or an out-of-range parameter value. |
