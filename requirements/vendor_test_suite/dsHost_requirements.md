# Device Settings Host (dsHost) — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DSHOST‑001` | SHALL successfully initialize the DS Host HAL module and successfully terminate it, supporting re-initialization after a prior termination without error. |
| `VTS‑DSHOST‑002` | SHALL retrieve the current CPU temperature as a valid value, with consecutive reads returning consistent values within the platform-defined temperature range declared in the device profile. |
| `VTS‑DSHOST‑003` | SHALL retrieve the platform SoC identifier as a non-empty value that is consistent across successive reads and matches the expected SoC identifier declared in the device profile. |
| `VTS‑DSHOST‑004` | SHALL retrieve the host EDID data as a non-null buffer with a non-zero length, with consecutive reads returning identical EDID content. |
| `VTS‑DSHOST‑005` | SHALL report an already-initialized error on repeated initialization, a not-initialized error for operations invoked before initialization or after termination, and an invalid-parameter error for NULL output pointers or buffers. |
