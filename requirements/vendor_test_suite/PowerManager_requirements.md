# Power Manager — Requirements

> **Module:** Power Manager HAL (`plat_power`) | **Req ID Prefix:** `VTS-POWERMANAGER`
> **Total requirements:** 8 | **Total test cases:** 14 (12 L1 + 2 L2)

---

## Requirements Document

| Req ID | Classification | Test Scope *(Verify that the DUT...)* |
|--------|----------------|---------------------------------------|
| `VTS-POWERMANAGER-001` | Lifecycle | SHALL initialize the Power Manager HAL via `PLAT_INIT()` returning `PWRMGR_SUCCESS`, and SHALL terminate the module via `PLAT_TERM()` returning `PWRMGR_SUCCESS`. The module SHALL support re-initialization after a prior termination. |
| `VTS-POWERMANAGER-002` | Functional | SHALL set the device power state via `PLAT_API_SetPowerState()` for each power state defined in the device profile, returning `PWRMGR_SUCCESS`. |
| `VTS-POWERMANAGER-003` | Functional | SHALL retrieve the current device power state via `PLAT_API_GetPowerState()` returning `PWRMGR_SUCCESS`. |
| `VTS-POWERMANAGER-004` | Data Integrity | SHALL, when a power state is set via `PLAT_API_SetPowerState()` and subsequently retrieved via `PLAT_API_GetPowerState()`, return a retrieved power state that matches the value that was set. |
| `VTS-POWERMANAGER-005` | Functional | SHALL configure each supported wakeup source to both enabled and disabled states via `PLAT_API_SetWakeupSrc()` returning `PWRMGR_SUCCESS`. |
| `VTS-POWERMANAGER-006` | Functional | SHALL retrieve the current enable state of each supported wakeup source via `PLAT_API_GetWakeupSrc()` returning `PWRMGR_SUCCESS`. |
| `VTS-POWERMANAGER-007` | Data Integrity | SHALL, when a wakeup source enable state is set via `PLAT_API_SetWakeupSrc()` and subsequently retrieved via `PLAT_API_GetWakeupSrc()`, return an enable state that matches the value that was set. |
| `VTS-POWERMANAGER-008` | Error Handling | SHALL enforce the following error code contracts across all `plat_power` APIs:<br>`PLAT_INIT()` SHALL return `PWRMGR_ALREADY_INITIALIZED` when called while the module is already initialized<br>`PLAT_TERM()` SHALL return `PWRMGR_NOT_INITIALIZED` when called without prior initialization or after the module has already been terminated<br>`PLAT_API_SetPowerState()` SHALL return `PWRMGR_NOT_INITIALIZED` when invoked before initialization or after termination, and `PWRMGR_INVALID_ARGUMENT` when called with an out-of-range power state<br>`PLAT_API_GetPowerState()` SHALL return `PWRMGR_NOT_INITIALIZED` when invoked before initialization or after termination, and `PWRMGR_INVALID_ARGUMENT` when called with a NULL output pointer<br>`PLAT_API_SetWakeupSrc()` SHALL return `PWRMGR_NOT_INITIALIZED` when invoked before initialization or after termination, and `PWRMGR_INVALID_ARGUMENT` when called with an out-of-range wakeup source<br>`PLAT_API_GetWakeupSrc()` SHALL return `PWRMGR_NOT_INITIALIZED` when invoked before initialization or after termination, and `PWRMGR_INVALID_ARGUMENT` when called with a NULL output pointer |
