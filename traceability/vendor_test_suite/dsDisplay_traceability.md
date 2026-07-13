# Device Settings Display — Traceability

> **Module:** Device Settings Display HAL (`dsDisplay`) | **Req ID Prefix:** `VTS-DSDISPLAY` **Total requirements:** 10 | **Total test cases:** 28 (26 L1 + 2 L2) **Source:** [test_l1_dsDisplay.c](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c) · [test_l2_dsDisplay.c](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsDisplay.c)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/dsdisplay/
├── dsDisplay_requirements.md
├── dsDisplay_traceability.md
└── testcases/
    ├── VTS-DSDISPLAY-001/   (2 tests   — Init/term lifecycle)
    ├── VTS-DSDISPLAY-002/   (1 test    — Display device handle acquisition)
    ├── VTS-DSDISPLAY-003/   (1 test    — EDID information retrieval)
    ├── VTS-DSDISPLAY-004/   (1 test    — Raw EDID byte-buffer retrieval)
    ├── VTS-DSDISPLAY-005/   (2 tests   — Display aspect ratio / default profile compliance)
    ├── VTS-DSDISPLAY-006/   (1 test    — Display-event callback registration)
    ├── VTS-DSDISPLAY-007/   (3 tests   — AVI content type get/set data integrity)
    ├── VTS-DSDISPLAY-008/   (2 tests   — AVI scan information get/set)
    ├── VTS-DSDISPLAY-009/   (2 tests   — ALLM get/set)
    └── VTS-DSDISPLAY-010/   (13 tests  — API error handling)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

> L2 counts reflect the **source** device suite; the sink-only `RetrieveAndValidateEDID` L2 scenario is not registered on source targets.

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `VTS-DSDISPLAY-001` | 2 | [dsDisplayInit_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L117) [dsDisplayTerm_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L215) |
| `VTS-DSDISPLAY-002` | 1 | [dsGetDisplay_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L319) |
| `VTS-DSDISPLAY-003` | 1 | [dsGetEDID_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L468) |
| `VTS-DSDISPLAY-004` | 1 | [dsGetEDIDBytes_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L642) |
| `VTS-DSDISPLAY-005` | 2 | [dsGetDisplayAspectRatio_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L822) [TestDefaultAspectRatio_src](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsDisplay.c#L191) |
| `VTS-DSDISPLAY-006` | 1 | [dsRegisterDisplayEventCB_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L991) |
| `VTS-DSDISPLAY-007` | 3 | [dsGetAVIContentType_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1138) [dsSetAVIContentType_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1306) [SetAndGetAVIContentType_src](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsDisplay.c#L267) |
| `VTS-DSDISPLAY-008` | 2 | [dsGetAVIScanInfo_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1475) [dsSetAVIScanInfo_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1643) |
| `VTS-DSDISPLAY-009` | 2 | [dsGetAllmEnabled_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1813) [dsSetAllmEnabled_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1980) |
| `VTS-DSDISPLAY-010` | 13 | [dsDisplayInit_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L169) [dsDisplayTerm_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L268) [dsGetDisplay_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L397) [dsGetEDID_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L566) [dsGetEDIDBytes_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L734) [dsGetDisplayAspectRatio_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L905) [dsRegisterDisplayEventCB_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1064) [dsGetAVIContentType_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1218) [dsSetAVIContentType_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1386) [dsGetAVIScanInfo_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1555) [dsSetAVIScanInfo_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1724) [dsGetAllmEnabled_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L1893) [dsSetAllmEnabled_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsDisplay.c#L2065) |
