# Deep Sleep Manager — Requirements

> **Module:** Deep Sleep Manager HAL (`deepSleepMgr`) | **Req ID Prefix:** `VTS-DEEPSLEEP`
> **Total requirements:** 3 | **Total test cases:** 14 (12 L1 + 2 L2)

---

## Step 1 — Requirement Categorisation Grouping

Requirements are grouped by **functional capability** of the `deepSleepMgr` HAL interface.
The module provides initialization/termination lifecycle, deep sleep entry and post-wakeup
processing, and retrieval of the last wakeup reason and key code.

Positive L1 tests validate individual API correctness in isolation. The two L2 tests drive the
device into an actual timed deep sleep and verify the reported wakeup reason on return — an
end-to-end behavioural workflow rather than a write-then-read-back of the same value, so they are
grouped as **Functional**. All negative L1 tests exclusively verify `DEEPSLEEPMGR_NOT_INITIALIZED`,
`DEEPSLEEPMGR_ALREADY_INITIALIZED`, and `DEEPSLEEPMGR_INVALID_ARGUMENT` contracts and are
consolidated into a single **Error Handling** requirement.

| Req ID | Functional Capability | Classification | # Tests |
|--------|-----------------------|----------------|---------|
| VTS-DEEPSLEEP-001 | Deep Sleep Manager initialization and termination lifecycle | Lifecycle | 2 |
| VTS-DEEPSLEEP-002 | Deep sleep entry, post-wakeup processing, and wakeup reason/key-code retrieval | Functional | 6 |
| VTS-DEEPSLEEP-003 | API error handling — not-initialized, already-initialized, and invalid-argument conditions | Error Handling | 6 |
| | **Total** | | **14** |

---

### VTS-DEEPSLEEP-001 — Deep Sleep Manager initialization and termination lifecycle (2 tests)

L1 positive (2): PLAT_INIT_pos, PLAT_TERM_pos

---

### VTS-DEEPSLEEP-002 — Deep sleep entry, post-wakeup processing, and wakeup reason/key-code retrieval (6 tests)

L1 positive (4): PLAT_SetDeepSleep_pos, PLAT_DeepSleepWakeup_pos, PLAT_GetLastWakeupReason_pos, PLAT_GetLastWakeupKeyCode_pos

L2 (2): SetDsAndVerifyWakeup1sec, SetDsAndVerifyWakeup10sec

---

### VTS-DEEPSLEEP-003 — API error handling (6 tests)

L1 negative (6): PLAT_INIT_neg, PLAT_TERM_neg, PLAT_DeepSleepWakeup_neg, PLAT_SetDeepSleep_neg, PLAT_GetLastWakeupReason_neg, PLAT_GetLastWakeupKeyCode_neg

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `VTS-DEEPSLEEP-001` | SHALL initialize the Deep Sleep Management module via `PLAT_DS_INIT()` returning `DEEPSLEEPMGR_SUCCESS` and SHALL terminate it via `PLAT_DS_TERM()` returning `DEEPSLEEPMGR_SUCCESS`. The module SHALL support re-initialization after a prior termination without error. |
| `VTS-DEEPSLEEP-002` | SHALL place the CPE into deep sleep via `PLAT_DS_SetDeepSleep()` for a valid timeout with network standby both disabled and enabled, returning `DEEPSLEEPMGR_SUCCESS`. SHALL complete post-wakeup platform processing via `PLAT_DS_DeepSleepWakeup()` returning `DEEPSLEEPMGR_SUCCESS`. SHALL retrieve the last wakeup reason via `PLAT_DS_GetLastWakeupReason()` returning a valid `DeepSleep_WakeupReason_t` value and the last wakeup key code via `PLAT_DS_GetLastWakeupKeyCode()` returning a valid key code, each returning `DEEPSLEEPMGR_SUCCESS`. Following a timed deep sleep cycle, the reported wakeup reason SHALL be the timer wakeup reason. |
| `VTS-DEEPSLEEP-003` | SHALL enforce the following error code contracts across all `deepSleepMgr` APIs: `PLAT_DS_INIT()` SHALL return `DEEPSLEEPMGR_ALREADY_INITIALIZED` when called while the module is already initialized; `PLAT_DS_TERM()` SHALL return `DEEPSLEEPMGR_NOT_INITIALIZED` when called without prior initialization or after the module has already been terminated; `PLAT_DS_DeepSleepWakeup()`, `PLAT_DS_SetDeepSleep()`, `PLAT_DS_GetLastWakeupReason()`, and `PLAT_DS_GetLastWakeupKeyCode()` SHALL each return `DEEPSLEEPMGR_NOT_INITIALIZED` when invoked before initialization or after termination, and SHALL return `DEEPSLEEPMGR_INVALID_ARGUMENT` when called with a NULL output pointer or an out-of-range deep sleep timeout value. |
