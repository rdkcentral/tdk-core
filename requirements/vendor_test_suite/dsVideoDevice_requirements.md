# Device Settings Video Device — Requirements

> **Module:** Device Settings Video Device HAL (`dsVideoDevice`) | **Req ID Prefix:** `VTS-DSVIDEODEVICE`
> **Total requirements:** 12 | **Total test cases:** 34 (30 L1 + 4 L2)

---

## Requirements Document

| Req ID | Classification | Test Scope *(Verify that the DUT...)* |
|--------|----------------|---------------------------------------|
| `VTS-DSVIDEODEVICE-001` | Lifecycle | SHALL initialize the Video Device sub-system via `dsVideoDeviceInit()` returning `dsERR_NONE` and SHALL terminate it via `dsVideoDeviceTerm()` returning `dsERR_NONE`, supporting re-initialization after a prior termination without error. |
| `VTS-DSVIDEODEVICE-002` | Functional | SHALL retrieve a valid video-device handle for each supported device index via `dsGetVideoDevice()` returning `dsERR_NONE`. |
| `VTS-DSVIDEODEVICE-003` | Data Integrity | SHALL apply each supported Decoder Format Conversion (DFC) zoom mode via `dsSetDFC()` and, on reading it back via `dsGetDFC()`, return the same value that was set, each call returning `dsERR_NONE`. |
| `VTS-DSVIDEODEVICE-004` | Profile Compliance | SHALL retrieve the HDR capabilities via `dsGetHDRCapabilities()` returning `dsERR_NONE` with a value that matches the HDR capabilities declared in the device profile. |
| `VTS-DSVIDEODEVICE-005` | Profile Compliance | SHALL retrieve the supported video coding formats via `dsGetSupportedVideoCodingFormats()` returning `dsERR_NONE` with a value that matches the supported formats declared in the device profile. |
| `VTS-DSVIDEODEVICE-006` | Profile Compliance | SHALL retrieve the video codec information via `dsGetVideoCodecInfo()` returning `dsERR_NONE` with codec information that matches the values declared in the device profile. |
| `VTS-DSVIDEODEVICE-007` | Functional | SHALL force-disable HDR support via `dsForceDisableHDRSupport()` returning `dsERR_NONE`. |
| `VTS-DSVIDEODEVICE-008` | Data Integrity | SHALL set the Frame Rate Following (FRF) mode via `dsSetFRFMode()` and retrieve it via `dsGetFRFMode()`, each returning `dsERR_NONE` with the retrieved mode reflecting the value applied. |
| `VTS-DSVIDEODEVICE-009` | Functional | SHALL retrieve the current display framerate via `dsGetCurrentDisplayframerate()` returning `dsERR_NONE` with a valid framerate string. |
| `VTS-DSVIDEODEVICE-010` | Functional | SHALL set the display framerate via `dsSetDisplayframerate()` returning `dsERR_NONE`. |
| `VTS-DSVIDEODEVICE-011` | Functional | SHALL register the pre-framerate-change callback via `dsRegisterFrameratePreChangeCB()` and the post-framerate-change callback via `dsRegisterFrameratePostChangeCB()`, each returning `dsERR_NONE`. |
| `VTS-DSVIDEODEVICE-012` | Error Handling | SHALL enforce the following error code contracts across all `dsVideoDevice` APIs:<br>`dsVideoDeviceInit()` SHALL return `dsERR_ALREADY_INITIALIZED` when called while already initialized<br>`dsVideoDeviceTerm()`, `dsGetVideoDevice()`, `dsSetDFC()`, `dsGetDFC()`, `dsGetHDRCapabilities()`, `dsGetSupportedVideoCodingFormats()`, `dsGetVideoCodecInfo()`, `dsForceDisableHDRSupport()`, `dsSetFRFMode()`, `dsGetFRFMode()`, `dsGetCurrentDisplayframerate()`, `dsSetDisplayframerate()`, `dsRegisterFrameratePreChangeCB()`, and `dsRegisterFrameratePostChangeCB()` SHALL each return `dsERR_NOT_INITIALIZED` when invoked before initialization or after termination, and SHALL return `dsERR_INVALID_PARAM` when called with a NULL output pointer, an invalid handle, or an out-of-range value. |
