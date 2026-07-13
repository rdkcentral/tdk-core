# Deep Sleep Manager — Requirements

> **Module:** Deep Sleep Manager HAL (`deepSleepMgr`) | **Req ID Prefix:** `VTS-DEEPSLEEP`
> **Total requirements:** 8 | **Total test cases:** 14 (12 L1 + 2 L2)

---

## Requirements Document

| Req ID | Classification | Test Scope *(Verify that the DUT...)* |
|--------|----------------|---------------------------------------|
| `VTS-DEEPSLEEP-001` | Lifecycle | SHALL initialize the Deep Sleep Management module via `PLAT_DS_INIT()` returning `DEEPSLEEPMGR_SUCCESS` and terminate it via `PLAT_DS_TERM()` returning `DEEPSLEEPMGR_SUCCESS`, and SHALL support re-initialization after a prior termination without error. |
| `VTS-DEEPSLEEP-002` | Functional | SHALL place the CPE into deep sleep via `PLAT_DS_SetDeepSleep()` for a valid timeout with network standby both disabled and enabled, returning `DEEPSLEEPMGR_SUCCESS`. Following a timed deep sleep cycle, the wakeup reason retrieved via `PLAT_DS_GetLastWakeupReason()` SHALL be the timer wakeup reason (`DEEPSLEEP_WAKEUPREASON_TIMER`). |
| `VTS-DEEPSLEEP-003` | Functional | SHALL complete post-wakeup platform processing via `PLAT_DS_DeepSleepWakeup()` returning `DEEPSLEEPMGR_SUCCESS`. |
| `VTS-DEEPSLEEP-004` | Functional | SHALL retrieve the last wakeup reason via `PLAT_DS_GetLastWakeupReason()`, returning a valid `DeepSleep_WakeupReason_t` value with `DEEPSLEEPMGR_SUCCESS`. |
| `VTS-DEEPSLEEP-005` | Functional | SHALL retrieve the last wakeup key code via `PLAT_DS_GetLastWakeupKeyCode()`, returning a valid `DeepSleepMgr_WakeupKeyCode_Param_t` value with `DEEPSLEEPMGR_SUCCESS`. |
| `VTS-DEEPSLEEP-006` | Error Handling | SHALL return `DEEPSLEEPMGR_ALREADY_INITIALIZED` from `PLAT_DS_INIT()` when it is called while the module is already initialized. |
| `VTS-DEEPSLEEP-007` | Error Handling | SHALL return `DEEPSLEEPMGR_NOT_INITIALIZED` from every `deepSleepMgr` API when it is invoked without prior initialization or after the module has already been terminated. |
| `VTS-DEEPSLEEP-008` | Error Handling | SHALL return `DEEPSLEEPMGR_INVALID_ARGUMENT` from `PLAT_DS_SetDeepSleep()`, `PLAT_DS_GetLastWakeupReason()`, and `PLAT_DS_GetLastWakeupKeyCode()` when they are called with a NULL output pointer or an out-of-range parameter value. |
