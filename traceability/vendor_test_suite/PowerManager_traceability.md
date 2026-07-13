# Power Manager — Traceability

> **Module:** Power Manager HAL (`plat_power`) | **Req ID Prefix:** `VTS-POWERMANAGER` **Total requirements:** 10 | **Total test cases:** 14 (12 L1 + 2 L2) **Source:** [test_l1_plat_power.c](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c) · [test_l2_plat_power.c](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l2_plat_power.c)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/powermanager/
├── PowerManager_requirements.md
├── PowerManager_traceability.md
└── testcases/
    ├── VTS-POWERMANAGER-001/   (2 tests — Module init/term lifecycle)
    ├── VTS-POWERMANAGER-002/   (1 test  — Set power state)
    ├── VTS-POWERMANAGER-003/   (1 test  — Get power state)
    ├── VTS-POWERMANAGER-004/   (1 test  — Power state set/get data integrity)
    ├── VTS-POWERMANAGER-005/   (1 test  — Set wakeup source)
    ├── VTS-POWERMANAGER-006/   (1 test  — Get wakeup source)
    ├── VTS-POWERMANAGER-007/   (1 test  — Wakeup source set/get data integrity)
    ├── VTS-POWERMANAGER-008/   (1 test  — Error handling: already-initialized)
    ├── VTS-POWERMANAGER-009/   (5 tests — Error handling: not-initialized)
    └── VTS-POWERMANAGER-010/   (4 tests — Error handling: invalid argument)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

> Each negative test verifies more than one error-handling requirement, so the same test case is listed under every requirement it covers (per-row counts therefore overlap).

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `VTS-POWERMANAGER-001` | 2 | [PLAT_INIT_pos](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L112) [PLAT_TERM_pos](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L190) |
| `VTS-POWERMANAGER-002` | 1 | [PLAT_SetPowerState_pos](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L274) |
| `VTS-POWERMANAGER-003` | 1 | [PLAT_GetPowerState_pos](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L379) |
| `VTS-POWERMANAGER-004` | 1 | [L2_SetAndGetPowerState](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l2_plat_power.c#L87) |
| `VTS-POWERMANAGER-005` | 1 | [PLAT_SetWakeupSrc_pos](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L480) |
| `VTS-POWERMANAGER-006` | 1 | [PLAT_GetWakeupSrc_pos](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L609) |
| `VTS-POWERMANAGER-007` | 1 | [L2_SetAndGetWakeupSrc](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l2_plat_power.c#L148) |
| `VTS-POWERMANAGER-008` | 1 | [PLAT_INIT_neg](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L150) |
| `VTS-POWERMANAGER-009` | 5 | [PLAT_TERM_neg](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L229) [PLAT_SetPowerState_neg](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L328) [PLAT_GetPowerState_neg](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L429) [PLAT_SetWakeupSrc_neg](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L557) [PLAT_GetWakeupSrc_neg](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L692) |
| `VTS-POWERMANAGER-010` | 4 | [PLAT_SetPowerState_neg](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L328) [PLAT_GetPowerState_neg](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L429) [PLAT_SetWakeupSrc_neg](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L557) [PLAT_GetWakeupSrc_neg](https://github.com/rdkcentral/rdk-halif-test-power_manager/blob/1.5.4/src/test_l1_plat_power.c#L692) |
