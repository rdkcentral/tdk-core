# Power Manager — Specifications

| Req ID | Test Scope |
|:-------|:--------------------------------------|
| `VTS‑POWERMANAGER‑001` | SHALL initialize the Power Manager HAL via `PLAT_INIT()` returning `PWRMGR_SUCCESS`, and SHALL terminate the module via `PLAT_TERM()` returning `PWRMGR_SUCCESS`. The module SHALL support re-initialization after a prior termination. |
| `VTS‑POWERMANAGER‑002` | SHALL set the device power state via `PLAT_API_SetPowerState()` for each power state defined in the device profile, returning `PWRMGR_SUCCESS`. |
| `VTS‑POWERMANAGER‑003` | SHALL retrieve the current device power state via `PLAT_API_GetPowerState()` returning `PWRMGR_SUCCESS`. |
| `VTS‑POWERMANAGER‑004` | SHALL, when a power state is set via `PLAT_API_SetPowerState()` and subsequently retrieved via `PLAT_API_GetPowerState()`, return a retrieved power state that matches the value that was set. |
| `VTS‑POWERMANAGER‑005` | SHALL configure each supported wakeup source to both enabled and disabled states via `PLAT_API_SetWakeupSrc()` returning `PWRMGR_SUCCESS`. |
| `VTS‑POWERMANAGER‑006` | SHALL retrieve the current enable state of each supported wakeup source via `PLAT_API_GetWakeupSrc()` returning `PWRMGR_SUCCESS`. |
| `VTS‑POWERMANAGER‑007` | SHALL, when a wakeup source enable state is set via `PLAT_API_SetWakeupSrc()` and subsequently retrieved via `PLAT_API_GetWakeupSrc()`, return an enable state that matches the value that was set. |
| `VTS‑POWERMANAGER‑008` | SHALL enforce the following error code contracts across all `plat_power` APIs:<br>`PLAT_INIT()` SHALL return `PWRMGR_ALREADY_INITIALIZED` when it is called while the module is already initialized<br>every `plat_power` API SHALL return `PWRMGR_NOT_INITIALIZED` when it is invoked without prior initialization or after the module has already been terminated<br>`PLAT_API_SetPowerState()`, `PLAT_API_GetPowerState()`, `PLAT_API_SetWakeupSrc()`, and `PLAT_API_GetWakeupSrc()` SHALL each return `PWRMGR_INVALID_ARGUMENT` when called with an out-of-range parameter value or a NULL output pointer. |
