# Deep Sleep Manager — Traceability

> **Module:** Deep Sleep Manager HAL (`deepSleepMgr`) | **Req ID Prefix:** `VTS-DEEPSLEEP` **Total requirements:** 8 | **Total test cases:** 14 (12 L1 + 2 L2) **Source:** [test_l1_deepSleepMgr.c](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c) · [test_l2_deepSleepMgr.c](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l2_deepSleepMgr.c)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/deepsleep/
├── DeepSleep_requirements.md
├── DeepSleep_traceability.md
└── testcases/
    ├── VTS-DEEPSLEEP-001/   (2 tests — Init/term lifecycle)
    ├── VTS-DEEPSLEEP-002/   (3 tests — Deep sleep entry + timed wakeup verification)
    ├── VTS-DEEPSLEEP-003/   (1 test  — Post-wakeup processing)
    ├── VTS-DEEPSLEEP-004/   (1 test  — Last wakeup reason retrieval)
    ├── VTS-DEEPSLEEP-005/   (1 test  — Last wakeup key-code retrieval)
    ├── VTS-DEEPSLEEP-006/   (1 test  — Error handling: already-initialized)
    ├── VTS-DEEPSLEEP-007/   (5 tests — Error handling: not-initialized)
    └── VTS-DEEPSLEEP-008/   (3 tests — Error handling: invalid argument)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

> Each negative test verifies more than one error-handling requirement, so the same test case is listed under every requirement it covers (per-row counts therefore overlap).

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `VTS-DEEPSLEEP-001` | 2 | [PLAT_INIT_pos](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L115) [PLAT_TERM_pos](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L202) |
| `VTS-DEEPSLEEP-002` | 3 | [PLAT_SetDeepSleep_pos](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L379) [SetDsAndVerifyWakeup1sec](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l2_deepSleepMgr.c#L86) [SetDsAndVerifyWakeup10sec](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l2_deepSleepMgr.c#L143) |
| `VTS-DEEPSLEEP-003` | 1 | [PLAT_DeepSleepWakeup_pos](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L287) |
| `VTS-DEEPSLEEP-004` | 1 | [PLAT_GetLastWakeupReason_pos](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L508) |
| `VTS-DEEPSLEEP-005` | 1 | [PLAT_GetLastWakeupKeyCode_pos](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L608) |
| `VTS-DEEPSLEEP-006` | 1 | [PLAT_INIT_neg](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L162) |
| `VTS-DEEPSLEEP-007` | 5 | [PLAT_TERM_neg](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L242) [PLAT_DeepSleepWakeup_neg](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L331) [PLAT_SetDeepSleep_neg](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L445) [PLAT_GetLastWakeupReason_neg](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L558) [PLAT_GetLastWakeupKeyCode_neg](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L653) |
| `VTS-DEEPSLEEP-008` | 3 | [PLAT_SetDeepSleep_neg](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L445) [PLAT_GetLastWakeupReason_neg](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L558) [PLAT_GetLastWakeupKeyCode_neg](https://github.com/rdkcentral/rdk-halif-test-deepsleep_manager/blob/1.4.3/src/test_l1_deepSleepMgr.c#L653) |
