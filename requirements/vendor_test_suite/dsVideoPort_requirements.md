# Device Settings Video Port — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DSVIDEOPORT‑001` | SHALL successfully initialize the Device Settings Video Port sub-system and successfully terminate it, supporting re-initialization after a prior termination without error. |
| `VTS‑DSVIDEOPORT‑002` | SHALL return a valid video port handle for each supported port type and index, with repeated requests for the same port type and index returning an equal handle. |
| `VTS‑DSVIDEOPORT‑003` | SHALL enable and disable each supported video port, with the reported enable state matching the state that was set. |
| `VTS‑DSVIDEOPORT‑004` | SHALL report the display connection status and the port active status of a video port, each with a valid status consistent across repeated reads. |
| `VTS‑DSVIDEOPORT‑005` | SHALL report whether the connected display supports audio surround and retrieve the surround mode, with the reported capability matching the value expected for the connected display. |
| `VTS‑DSVIDEOPORT‑006` | SHALL set the display resolution of a supported video port, with the reported resolution matching the value that was set. |
| `VTS‑DSVIDEOPORT‑007` | SHALL retrieve the resolutions supported by the connected TV, with the reported set matching the supported resolutions declared in the device profile. |
| `VTS‑DSVIDEOPORT‑008` | SHALL retrieve the connected TV's HDR capabilities, with the reported capabilities matching the value declared in the device profile. |
| `VTS‑DSVIDEOPORT‑009` | SHALL enable HDCP content protection on a supported video port, report the HDCP enabled state, and report the HDCP authentication status, each with a valid status. |
| `VTS‑DSVIDEOPORT‑010` | SHALL retrieve the current HDCP protocol version, the connected receiver's HDCP protocol version, and the negotiated HDCP protocol version, each with the version matching the value expected from the device profile and connected receiver. |
| `VTS‑DSVIDEOPORT‑011` | SHALL set the preferred HDMI/HDCP protocol preference of a supported video port, with the reported preference matching the value that was set. |
| `VTS‑DSVIDEOPORT‑012` | SHALL retrieve the color space of a supported video port, with the reported color space matching the value expected for the connected display. |
| `VTS‑DSVIDEOPORT‑013` | SHALL retrieve the color depth of a supported video port, with the reported color depth matching the value expected for the connected display. |
| `VTS‑DSVIDEOPORT‑014` | SHALL retrieve the color depth capabilities of a supported video port, with the reported capabilities matching the value declared in the device profile. |
| `VTS‑DSVIDEOPORT‑015` | SHALL set the preferred color depth of a supported video port, with the reported color depth matching the value that was set. |
| `VTS‑DSVIDEOPORT‑016` | SHALL retrieve the quantization range of a supported video port, with the reported range matching the value expected for the connected display. |
| `VTS‑DSVIDEOPORT‑017` | SHALL retrieve the matrix coefficients of a supported video port, with the reported coefficients matching the value expected for the connected display. |
| `VTS‑DSVIDEOPORT‑018` | SHALL retrieve the current video EOTF (Electro-Optical Transfer Function) of a supported video port, reporting a valid EOTF value. |
| `VTS‑DSVIDEOPORT‑019` | SHALL report the HDR output status of a supported video port, reset the video output to SDR, and force the HDR output mode, for valid parameters on supported device types; where the operation is not supported, it reports an operation-not-supported error. |
| `VTS‑DSVIDEOPORT‑020` | SHALL retrieve the combined current output settings of a supported video port, reporting valid output values. |
| `VTS‑DSVIDEOPORT‑021` | SHALL set the force-disable-4K state of a supported video port, with the reported state matching the value that was set. |
| `VTS‑DSVIDEOPORT‑022` | SHALL report the IgnoreEDID status of a supported video port with a valid status; where the operation is not supported, it reports an operation-not-supported error. |
| `VTS‑DSVIDEOPORT‑023` | SHALL set the video port background color for valid color values on supported device types; where the operation is not supported, it reports an operation-not-supported error. |
| `VTS‑DSVIDEOPORT‑024` | SHALL successfully register event callbacks for video format updates and for HDCP status changes. |
| `VTS‑DSVIDEOPORT‑025` | SHALL report an already-initialized error on repeated initialization, a not-initialized error for operations invoked before initialization or after termination, and an invalid-parameter error for invalid or null port handles, NULL output pointers, or out-of-range parameter values. |
