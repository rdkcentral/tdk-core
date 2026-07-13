# HDMI CEC (HDMICEC) — Traceability

> **Module:** HDMI CEC HAL (`HDMICEC`) | **Req ID Prefix:** `VTS-HDMICEC` **Total requirements:** 9 | **Total test cases:** 17 (16 L1 + 1 L2) **Source:** [test_l1_hdmi_cec_driver.c](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c) · [test_l2_hdmi_cec_source_driver.c](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l2_hdmi_cec_source_driver.c)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/hdmicec/
├── HDMICEC_requirements.md
├── HDMICEC_traceability.md
└── testcases/
    ├── VTS-HDMICEC-001/   (2 tests   — Open/close lifecycle)
    ├── VTS-HDMICEC-002/   (1 test    — Get physical address)
    ├── VTS-HDMICEC-003/   (2 tests   — Get logical address / availability)
    ├── VTS-HDMICEC-004/   (1 test    — Register Rx callback)
    ├── VTS-HDMICEC-005/   (1 test    — Synchronous CEC transmit)
    ├── VTS-HDMICEC-006/   (4 tests   — Source rejects sink-only logical-address ops)
    ├── VTS-HDMICEC-007/   (1 test    — Error handling: already-open)
    ├── VTS-HDMICEC-008/   (5 tests   — Error handling: not-opened)
    └── VTS-HDMICEC-009/   (6 tests   — Error handling: invalid handle/argument)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

> Counts reflect the **source** device suite (`[L1 HDMI CEC Source TestCase]` / `[L2 HDMICEC Source Test Case]`). The deprecated `HdmiCecSetTxCallback` and `HdmiCecTxAsync` APIs and the sink-only L1/L2 scenarios are not registered on source targets. The source L2 suite registers a single scenario.
>
> Each negative test verifies more than one error-handling requirement, so the same test case is listed under every requirement it covers (per-row counts therefore overlap).

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `VTS-HDMICEC-001` | 2 | [open_Positive](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L248) [close_Positive](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L337) |
| `VTS-HDMICEC-002` | 1 | [getPhysicalAddress_Positive](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L442) |
| `VTS-HDMICEC-003` | 2 | [getLogicalAddress_Positive (source)](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L1016) [L2_LogicalAddressUnavailability](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l2_hdmi_cec_source_driver.c#L104) |
| `VTS-HDMICEC-004` | 1 | [setRxCallback_Positive](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L1137) |
| `VTS-HDMICEC-005` | 1 | [Tx_Positive (source)](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L1522) |
| `VTS-HDMICEC-006` | 4 | [addLogicalAddress_Positive](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L588) [addLogicalAddress_negative](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L501) [removeLogicalAddress_Positive](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L762) [removeLogicalAddress_negative](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L649) |
| `VTS-HDMICEC-007` | 1 | [open_negative](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L199) |
| `VTS-HDMICEC-008` | 5 | [close_negative](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L290) [getPhysicalAddress_negative](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L388) [getLogicalAddress_negative (source)](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L958) [setRxCallback_negative](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L1067) [Tx_negative (source)](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L1448) |
| `VTS-HDMICEC-009` | 6 | [open_negative](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L199) [close_negative](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L290) [getPhysicalAddress_negative](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L388) [getLogicalAddress_negative (source)](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L958) [setRxCallback_negative](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L1067) [Tx_negative (source)](https://github.com/rdkcentral/rdk-halif-test-hdmi_cec/blob/1.6.1/src/test_l1_hdmi_cec_driver.c#L1448) |
