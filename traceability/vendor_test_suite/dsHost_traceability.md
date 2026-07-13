# Device Settings Host (dsHost) — Traceability

> **Module:** Device Settings Host HAL (`dsHost`) | **Req ID Prefix:** `VTS-DSHOST` **Total requirements:** 7 | **Total test cases:** 12 (10 L1 + 2 L2) **Source:** [test_l1_dsHost.c](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c) · [test_l2_dsHost.c](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsHost.c)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/dshost/
├── dsHost_requirements.md
├── dsHost_traceability.md
└── testcases/
    ├── VTS-DSHOST-001/   (2 tests   — Init/term lifecycle)
    ├── VTS-DSHOST-002/   (2 tests   — CPU temperature profile compliance)
    ├── VTS-DSHOST-003/   (2 tests   — SoC ID profile compliance)
    ├── VTS-DSHOST-004/   (1 test    — Host EDID retrieval)
    ├── VTS-DSHOST-005/   (1 test    — Error handling: already-initialized)
    ├── VTS-DSHOST-006/   (4 tests   — Error handling: not-initialized)
    └── VTS-DSHOST-007/   (3 tests   — Error handling: invalid-parameter)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

> L2 counts reflect the **source** device suite; the sink-only `ValidateHostEDID` L2 scenario is not registered on source targets.
> Each negative test verifies more than one error-handling requirement, so the same test case is listed under every requirement it covers (per-row counts therefore overlap).

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `VTS-DSHOST-001` | 2 | [dsHostInit_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L119) [dsHostTerm_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L208) |
| `VTS-DSHOST-002` | 2 | [dsGetCPUTemperature_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L304) [GetCPUTemperature](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsHost.c#L100) |
| `VTS-DSHOST-003` | 2 | [dsGetSocIDFromSDK_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L410) [GetAndVerifySocID](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsHost.c#L158) |
| `VTS-DSHOST-004` | 1 | [dsGetHostEDID_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L523) |
| `VTS-DSHOST-005` | 1 | [dsHostInit_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L166) |
| `VTS-DSHOST-006` | 4 | [dsHostTerm_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L256) [dsGetCPUTemperature_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L355) [dsGetSocIDFromSDK_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L467) [dsGetHostEDID_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L583) |
| `VTS-DSHOST-007` | 3 | [dsGetCPUTemperature_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L355) [dsGetSocIDFromSDK_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L467) [dsGetHostEDID_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsHost.c#L583) |
