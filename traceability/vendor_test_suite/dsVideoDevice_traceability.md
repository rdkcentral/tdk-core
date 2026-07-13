# Device Settings Video Device (dsVideoDevice) — Traceability

> **Module:** Device Settings Video Device HAL (`dsVideoDevice`) | **Req ID Prefix:** `VTS-DSVIDEODEVICE` **Total requirements:** 12 | **Total test cases:** 34 (30 L1 + 4 L2) **Source:** [test_l1_dsVideoDevice.c](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c) · [test_l2_dsVideoDevice.c](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsVideoDevice.c)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/dsvideodevice/
├── dsVideoDevice_requirements.md
├── dsVideoDevice_traceability.md
└── testcases/
    ├── VTS-DSVIDEODEVICE-001/   (2 tests   — Init/term lifecycle)
    ├── VTS-DSVIDEODEVICE-002/   (1 test    — Get video device handle)
    ├── VTS-DSVIDEODEVICE-003/   (3 tests   — DFC set/get data integrity)
    ├── VTS-DSVIDEODEVICE-004/   (2 tests   — HDR capabilities profile compliance)
    ├── VTS-DSVIDEODEVICE-005/   (2 tests   — Supported coding formats profile compliance)
    ├── VTS-DSVIDEODEVICE-006/   (2 tests   — Video codec info profile compliance)
    ├── VTS-DSVIDEODEVICE-007/   (1 test    — Force-disable HDR)
    ├── VTS-DSVIDEODEVICE-008/   (2 tests   — FRF mode set/get)
    ├── VTS-DSVIDEODEVICE-009/   (1 test    — Get current display framerate)
    ├── VTS-DSVIDEODEVICE-010/   (1 test    — Set display framerate)
    ├── VTS-DSVIDEODEVICE-011/   (2 tests   — Framerate pre/post change callbacks)
    └── VTS-DSVIDEODEVICE-012/   (15 tests  — API error handling)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

> L2 counts reflect the **source** device suite; the sink-only `SetAndVerifyDisplayframerate` and `SetAndVerifyFRFMode` L2 scenarios are not registered on source targets.

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `VTS-DSVIDEODEVICE-001` | 2 | [dsVideoDeviceInit_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L116) [dsVideoDeviceTerm_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L197) |
| `VTS-DSVIDEODEVICE-002` | 1 | [dsGetVideoDevice_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L282) |
| `VTS-DSVIDEODEVICE-003` | 3 | [dsSetDFC_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L384) [dsGetDFC_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L539) [SetAndGetDFC_source](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsVideoDevice.c#L97) |
| `VTS-DSVIDEODEVICE-004` | 2 | [dsGetHDRCapabilities_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L698) [GetHDRCapabilities](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsVideoDevice.c#L171) |
| `VTS-DSVIDEODEVICE-005` | 2 | [dsGetSupportedVideoCodingFormats_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L820) [GetSupportedVideoCodingFormats](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsVideoDevice.c#L232) |
| `VTS-DSVIDEODEVICE-006` | 2 | [dsGetVideoCodecInfo_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L942) [GetVideoCodecInfo_source](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l2_dsVideoDevice.c#L289) |
| `VTS-DSVIDEODEVICE-007` | 1 | [dsForceDisableHDRSupport_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1120) |
| `VTS-DSVIDEODEVICE-008` | 2 | [dsSetFRFMode_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1238) [dsGetFRFMode_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1401) |
| `VTS-DSVIDEODEVICE-009` | 1 | [dsGetCurrentDisplayframerate_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1555) |
| `VTS-DSVIDEODEVICE-010` | 1 | [dsSetDisplayframerate_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1718) |
| `VTS-DSVIDEODEVICE-011` | 2 | [dsRegisterFrameratePreChangeCB_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1885) [dsRegisterFrameratePostChangeCB_pos](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L2007) |
| `VTS-DSVIDEODEVICE-012` | 15 | [dsVideoDeviceInit_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L159) [dsVideoDeviceTerm_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L241) [dsGetVideoDevice_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L327) [dsSetDFC_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L453) [dsGetDFC_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L614) [dsGetHDRCapabilities_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L757) [dsGetSupportedVideoCodingFormats_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L877) [dsGetVideoCodecInfo_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1026) [dsForceDisableHDRSupport_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1178) [dsSetFRFMode_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1316) [dsGetFRFMode_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1469) [dsGetCurrentDisplayframerate_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1633) [dsSetDisplayframerate_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1786) [dsRegisterFrameratePreChangeCB_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L1936) [dsRegisterFrameratePostChangeCB_neg](https://github.com/rdkcentral/rdk-halif-test-device_settings/blob/6.0.1/src/test_l1_dsVideoDevice.c#L2058) |
