# Device Settings Video Port — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DSVIDEOPORT‑001` | SHALL successfully initialize the Device Settings Video Port sub-system, successfully terminate it, support re-initialization after a prior termination, and return a valid video port handle for each supported port type and index with repeated requests returning an equal handle. |
| `VTS‑DSVIDEOPORT‑002` | SHALL preserve data integrity across the video port configuration controls — port enable/disable, display resolution, preferred HDMI/HDCP protocol preference, preferred color depth, force-disable-4K state, and video port background color — with each reported value matching the value that was set, and reporting an operation-not-supported error where the operation is not supported by the DUT. |
| `VTS‑DSVIDEOPORT‑003` | SHALL retrieve the supported TV resolutions, the connected TV's HDR capabilities, the color depth capabilities, and the current, receiver, and negotiated HDCP protocol versions, each matching the values declared in the device profile and connected receiver. |
| `VTS‑DSVIDEOPORT‑004` | SHALL report the display connection and port active status, audio surround capability and mode, color space, color depth, quantization range, matrix coefficients, current video EOTF, combined current output settings, and IgnoreEDID status, each with a valid value consistent with the connected display; where an operation is not supported, it reports an operation-not-supported error. |
| `VTS‑DSVIDEOPORT‑005` | SHALL enable HDCP content protection on a supported video port, report the HDCP enabled state, and report the HDCP authentication status, each with a valid status. |
| `VTS‑DSVIDEOPORT‑006` | SHALL report the HDR output status of a supported video port, reset the video output to SDR, and force the HDR output mode, for valid parameters on supported device types, reporting an operation-not-supported error where the operation is not supported. |
| `VTS‑DSVIDEOPORT‑007` | SHALL successfully register event callbacks for video format updates and for HDCP status changes. |
| `VTS‑DSVIDEOPORT‑008` | SHALL report an already-initialized error on repeated initialization, a not-initialized error for operations invoked before initialization or after termination, and an invalid-parameter error for invalid or null port handles, NULL output pointers, or out-of-range parameter values. |
