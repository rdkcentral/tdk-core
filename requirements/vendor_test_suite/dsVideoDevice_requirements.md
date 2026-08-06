# Device Settings Video Device — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DSVIDEODEVICE‑001` | SHALL successfully initialize the Video Device sub-system, successfully terminate it, support re-initialization after a prior termination, and retrieve a valid video-device handle for each supported device index. |
| `VTS‑DSVIDEODEVICE‑002` | SHALL preserve data integrity across the video device configuration controls — Decoder Format Conversion (DFC) zoom mode, Frame Rate Following (FRF) mode, and display framerate — with each reported value matching the value that was set, and successfully force-disable HDR support. |
| `VTS‑DSVIDEODEVICE‑003` | SHALL retrieve the HDR capabilities, the supported video coding formats, and the video codec information, each matching the values declared in the device profile. |
| `VTS‑DSVIDEODEVICE‑004` | SHALL retrieve the current display framerate reporting a valid framerate value. |
| `VTS‑DSVIDEODEVICE‑005` | SHALL successfully register the pre-framerate-change callback and the post-framerate-change callback on supported device types, reporting an operation-not-supported error where the operation is not supported by the DUT. |
| `VTS‑DSVIDEODEVICE‑006` | SHALL report an already-initialized error on repeated initialization, a not-initialized error for operations invoked before initialization or after termination, and an invalid-parameter error for NULL output pointers, invalid handles, or out-of-range values. |
