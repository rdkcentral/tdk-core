# Power Manager — Requirements

> **Module:** Power Manager HAL (`plat_power`) | **Req ID Prefix:** `VTS-POWERMANAGER`
> **Total requirements:** 4 | **Total test cases:** 14 (12 L1 + 2 L2)

---

## Step 1 — Requirement Categorisation Grouping

Requirements are grouped by **functional capability** of the `plat_power` HAL interface.
Positive L1 tests validate individual API correctness. L2 tests validate end-to-end
set/get workflows verifying that written values are read back correctly (Data Integrity).
All negative L1 tests exclusively check `PWRMGR_NOT_INITIALIZED`, `PWRMGR_ALREADY_INITIALIZED`,
and `PWRMGR_INVALID_ARGUMENT` error contracts and are consolidated into a single
Error Handling requirement.

| Req ID | Functional Capability | Classification | # Tests |
|--------|-----------------------|----------------|---------|
| VTS-POWERMANAGER-001 | Power Manager HAL module initialization and termination lifecycle | Lifecycle | 2 |
| VTS-POWERMANAGER-002 | Power state configuration and retrieval | Functional | 3 |
| VTS-POWERMANAGER-003 | Wakeup source enable/disable configuration and retrieval | Data Integrity | 3 |
| VTS-POWERMANAGER-004 | API error handling — not-initialized, already-initialized, and invalid-argument conditions | Error Handling | 6 |
| | **Total** | | **14** |

---

### VTS-POWERMANAGER-001 — Power Manager HAL module initialization and termination lifecycle (2 tests)

L1 positive (2): PLAT_INIT_pos, PLAT_TERM_pos

---

### VTS-POWERMANAGER-002 — Power state configuration and retrieval (3 tests) <!-- Functional -->

L1 positive (2): PLAT_SetPowerState_pos, PLAT_GetPowerState_pos

L2 (1): L2_SetAndGetPowerState

---

### VTS-POWERMANAGER-003 — Wakeup source enable/disable configuration and retrieval (3 tests)

L1 positive (2): PLAT_SetWakeupSrc_pos, PLAT_GetWakeupSrc_pos

L2 (1): L2_SetAndGetWakeupSrc

---

### VTS-POWERMANAGER-004 — API error handling (6 tests)

L1 negative (6): PLAT_INIT_neg, PLAT_TERM_neg, PLAT_SetPowerState_neg, PLAT_GetPowerState_neg, PLAT_SetWakeupSrc_neg, PLAT_GetWakeupSrc_neg

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `VTS-POWERMANAGER-001` | SHALL initialize the Power Manager HAL via `PLAT_INIT()` returning `PWRMGR_SUCCESS` and SHALL terminate the module via `PLAT_TERM()` returning `PWRMGR_SUCCESS`. The module SHALL support re-initialization after a prior termination without error. |
| `VTS-POWERMANAGER-002` | SHALL set the device power state via `PLAT_API_SetPowerState()` for each power state defined in the device profile, returning `PWRMGR_SUCCESS`. SHALL retrieve the current power state via `PLAT_API_GetPowerState()` returning `PWRMGR_SUCCESS` with consistent values across successive calls. When a power state is set and then retrieved, the retrieved value SHALL match the value that was set. |
| `VTS-POWERMANAGER-003` | SHALL configure each supported wakeup source to enabled and disabled states via `PLAT_API_SetWakeupSrc()` returning `PWRMGR_SUCCESS`. SHALL retrieve the current enable state of each wakeup source via `PLAT_API_GetWakeupSrc()` returning `PWRMGR_SUCCESS`. The retrieved enable state SHALL match the value that was last set for that wakeup source. |
| `VTS-POWERMANAGER-004` | SHALL enforce the following error code contracts across all `plat_power` APIs: `PLAT_INIT()` SHALL return `PWRMGR_ALREADY_INITIALIZED` when called while the module is already initialized; `PLAT_TERM()` SHALL return `PWRMGR_NOT_INITIALIZED` when called without prior initialization or after the module has already been terminated; `PLAT_API_SetPowerState()`, `PLAT_API_GetPowerState()`, `PLAT_API_SetWakeupSrc()`, and `PLAT_API_GetWakeupSrc()` SHALL each return `PWRMGR_NOT_INITIALIZED` when invoked before initialization or after termination, and SHALL return `PWRMGR_INVALID_ARGUMENT` when called with an invalid or out-of-range argument or a NULL output pointer. |
