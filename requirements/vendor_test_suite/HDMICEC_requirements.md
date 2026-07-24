# HDMI CEC — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑HDMICEC‑001` | SHALL open the CEC HAL obtaining a valid non-zero handle and close the handle, supporting a subsequent re-open after close. |
| `VTS‑HDMICEC‑002` | SHALL retrieve the device physical address as a valid value reflecting the HDMI topology. |
| `VTS‑HDMICEC‑003` | SHALL retrieve the HAL-allocated logical address as a valid value, and, when the source device is not connected to a sink, report logical-address unavailability at open time. |
| `VTS‑HDMICEC‑004` | SHALL register a receive callback, including acceptance of a null callback to deregister. |
| `VTS‑HDMICEC‑005` | SHALL transmit a CEC frame synchronously; for a frame addressed to a non-existent device the transmission is reported as sent but not acknowledged, and a broadcast frame is reported as successfully sent. |
| `VTS‑HDMICEC‑006` | SHALL, as a source device, report the sink-only logical-address add and remove operations as unsupported for all invocation scenarios. |
| `VTS‑HDMICEC‑007` | SHALL report an already-open error on repeated open, a not-opened error for operations invoked before open or after close, an invalid-handle error for invalid handles, and an invalid-argument error for null handle, data, or output pointers or an invalid data length. |
