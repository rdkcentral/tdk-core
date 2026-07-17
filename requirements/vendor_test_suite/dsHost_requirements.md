# Device Settings Host (dsHost) — Specifications

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DSHOST‑001` | SHALL initialize the DS Host HAL module via `dsHostInit()` returning `dsERR_NONE` and terminate the module via `dsHostTerm()` returning `dsERR_NONE`, supporting re-initialization after a prior termination without error. |
| `VTS‑DSHOST‑002` | SHALL retrieve the current CPU temperature via `dsGetCPUTemperature()` returning a valid floating-point value, with consecutive calls returning consistent values within the platform-defined temperature range specified in the device profile. |
| `VTS‑DSHOST‑003` | SHALL retrieve the platform SoC identifier string via `dsGetSocIDFromSDK()` returning a non-empty string that is consistent across successive calls and matches the expected SoC ID value defined in the device profile. |
| `VTS‑DSHOST‑004` | SHALL retrieve the host EDID data via `dsGetHostEDID()` returning a non-null EDID byte buffer with a non-zero length, with consecutive calls returning identical EDID content. |
| `VTS‑DSHOST‑005` | SHALL enforce the following error code contracts across all `dsHost` APIs:<br>`dsHostInit()` returns `dsERR_ALREADY_INITIALIZED` when it is called while the module is already initialized<br>every `dsHost` API returns `dsERR_NOT_INITIALIZED` when it is invoked without prior initialization or after the module has already been terminated<br>every `dsHost` API returns `dsERR_INVALID_PARAM` when it is called with a NULL output pointer or buffer. |
