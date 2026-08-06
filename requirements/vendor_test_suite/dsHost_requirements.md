# Device Settings Host — Specifications

## Requirements

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑DSHOST‑001` | SHALL successfully initialize the DS Host HAL module, successfully terminate it, and support re-initialization after a prior termination without error. |
| `VTS‑DSHOST‑002` | SHALL retrieve host information — the current CPU temperature within the platform-defined range, the platform SoC identifier, and the host EDID data — each as a valid, non-empty value that is consistent across successive reads and matches the values declared in the device profile. |
| `VTS‑DSHOST‑003` | SHALL report an already-initialized error on repeated initialization, a not-initialized error for operations invoked before initialization or after termination, and an invalid-parameter error for NULL output pointers or buffers. |
