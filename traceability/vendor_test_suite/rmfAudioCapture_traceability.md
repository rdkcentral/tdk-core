# RMF Audio Capture — Traceability

> **Module:** RMF Audio Capture HAL (`rmfAudioCapture`) | **Req ID Prefix:** `VTS-RMFAUDIOCAPTURE` **Total requirements:** 6 | **Total test cases:** 17 (16 L1 + 1 L2) **Source:** [test_l1_rmfAudioCapture.c](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c) · [test_l2_rmfAudioCapture.c](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l2_rmfAudioCapture.c)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/rmfaudiocapture/
├── rmfAudioCapture_requirements.md
├── rmfAudioCapture_traceability.md
└── testcases/
    ├── VTS-RMFAUDIOCAPTURE-001/   (3 tests — Open/Open_Type/Close session lifecycle)
    ├── VTS-RMFAUDIOCAPTURE-002/   (1 test  — Default settings retrieval)
    ├── VTS-RMFAUDIOCAPTURE-003/   (3 tests — Start/Stop capture + data delivery)
    ├── VTS-RMFAUDIOCAPTURE-004/   (1 test  — Capture status retrieval)
    ├── VTS-RMFAUDIOCAPTURE-005/   (1 test  — Current settings retrieval)
    └── VTS-RMFAUDIOCAPTURE-006/   (8 tests — API error handling)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `VTS-RMFAUDIOCAPTURE-001` | 3 | [RMF_Open_L1_pos](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L291) [RMF_Open_Type_primary_L1_pos](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L185) [RMF_Close_L1_pos](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L420) |
| `VTS-RMFAUDIOCAPTURE-002` | 1 | [RMF_GetDefaultSettings_L1_pos](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L512) |
| `VTS-RMFAUDIOCAPTURE-003` | 3 | [RMF_Start_L1_pos](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L629) [RMF_Stop_L1_pos](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L856) [l2_rmf_primary_data_check](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l2_rmfAudioCapture.c#L195) |
| `VTS-RMFAUDIOCAPTURE-004` | 1 | [RMF_GetStatus_L1_pos](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L1013) |
| `VTS-RMFAUDIOCAPTURE-005` | 1 | [RMF_GetCurrentSettings_L1_pos](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L1177) |
| `VTS-RMFAUDIOCAPTURE-006` | 8 | [RMF_Open_Type_primary_L1_neg](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L235) [RMF_Open_L1_neg](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L359) [RMF_Close_L1_neg](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L461) [RMF_GetDefaultSettings_L1_neg](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L565) [RMF_Start_L1_neg](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L753) [RMF_Stop_L1_neg](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L938) [RMF_GetStatus_L1_neg](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L1088) [RMF_GetCurrentSettings_L1_neg](https://github.com/rdkcentral/rdk-halif-test-rmf_audio_capture/blob/1.5.4/src/test_l1_rmfAudioCapture.c#L1272) |
