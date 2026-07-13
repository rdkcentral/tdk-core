# Device Settings Host (dsHost) — Requirements

> **Module:** Device Settings Host HAL (`dsHost`) | **Req ID Prefix:** `VTS-DSHOST`
> **Total requirements:** 7 | **Total test cases:** 12 (10 L1 + 2 L2)

---

## Requirements Document

| Req ID | Classification | Test Scope *(Verify that the DUT...)* |
|--------|----------------|---------------------------------------|
| `VTS-DSHOST-001` | Lifecycle | SHALL initialize the DS Host HAL module via `dsHostInit()` returning `dsERR_NONE` and SHALL terminate the module via `dsHostTerm()` returning `dsERR_NONE`. The module SHALL support re-initialization after a prior termination without error. |
| `VTS-DSHOST-002` | Profile Compliance | SHALL retrieve the current CPU temperature via `dsGetCPUTemperature()` returning a valid floating-point value, with consecutive calls returning consistent values within the platform-defined temperature range specified in the device profile. |
| `VTS-DSHOST-003` | Profile Compliance | SHALL retrieve the platform SoC identifier string via `dsGetSocIDFromSDK()` returning a non-empty string that is consistent across successive calls and matches the expected SoC ID value defined in the device profile. |
| `VTS-DSHOST-004` | Functional | SHALL retrieve the host EDID data via `dsGetHostEDID()` returning a non-null EDID byte buffer with a non-zero length, with consecutive calls returning identical EDID content. |
| `VTS-DSHOST-005` | Error Handling | SHALL return `dsERR_ALREADY_INITIALIZED` from `dsHostInit()` when it is called while the module is already initialized. |
| `VTS-DSHOST-006` | Error Handling | SHALL return `dsERR_NOT_INITIALIZED` from every `dsHost` API when it is invoked without prior initialization or after the module has already been terminated. |
| `VTS-DSHOST-007` | Error Handling | SHALL return `dsERR_INVALID_PARAM` from every `dsHost` API when it is called with a NULL output pointer or buffer. |
