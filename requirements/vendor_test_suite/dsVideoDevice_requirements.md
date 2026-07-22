# Device Settings Video Device — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DSVIDEODEVICE‑001` | SHALL successfully initialize the Video Device sub-system and successfully terminate it, supporting re-initialization after a prior termination without error. |
| `VTS‑DSVIDEODEVICE‑002` | SHALL retrieve a valid video-device handle for each supported device index. |
| `VTS‑DSVIDEODEVICE‑003` | SHALL apply each supported Decoder Format Conversion (DFC) zoom mode and, on reading it back, report the same value that was set. |
| `VTS‑DSVIDEODEVICE‑004` | SHALL retrieve the HDR capabilities and report a value that matches the HDR capabilities declared in the device profile. |
| `VTS‑DSVIDEODEVICE‑005` | SHALL retrieve the supported video coding formats and report a value that matches the supported formats declared in the device profile. |
| `VTS‑DSVIDEODEVICE‑006` | SHALL retrieve the video codec information and report values that match those declared in the device profile. |
| `VTS‑DSVIDEODEVICE‑007` | SHALL successfully force-disable HDR support. |
| `VTS‑DSVIDEODEVICE‑008` | SHALL set the Frame Rate Following (FRF) mode and retrieve it, with the reported mode reflecting the value that was applied. |
| `VTS‑DSVIDEODEVICE‑009` | SHALL retrieve the current display framerate and report a valid framerate value. |
| `VTS‑DSVIDEODEVICE‑010` | SHALL set the display framerate. |
| `VTS‑DSVIDEODEVICE‑011` | SHALL register the pre-framerate-change callback and the post-framerate-change callback. |
| `VTS‑DSVIDEODEVICE‑012` | SHALL enforce the following error handling contracts across all Device Settings Video Device operations:<br>report an already-initialized error when initialization is attempted while the module is already initialized<br>report a not-initialized error when any operation is attempted without prior initialization or after the module has already been terminated<br>report an invalid-parameter error when any operation is called with a NULL output pointer, an invalid handle, or an out-of-range value. |
