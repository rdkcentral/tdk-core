# HDMI CEC — Requirements

> **Module:** HDMI CEC HAL (`HDMICEC`) | **Req ID Prefix:** `VTS-HDMICEC`
> **Total requirements:** 3 | **Total test cases:** 20 (16 L1 + 4 L2)

---

## Step 1 — Requirement Categorisation Grouping

Requirements are grouped by **functional capability** of the HDMI CEC HAL interface in source-device
mode. The module provides open/close handle lifecycle, physical and logical address retrieval,
Rx/Tx callback registration, and synchronous/asynchronous CEC frame transmission.

Positive L1 tests validate individual API correctness in isolation. The L2 tests drive end-to-end
workflows — reading the HAL-allocated addresses and transmitting broadcast/unicast CEC frames while
verifying the transmission outcome. As these validate behavioural correctness (valid address ranges,
send/ACK results) rather than a write-then-read-back of the same value, they are grouped as
**Functional**. All negative L1 tests exclusively verify invalid-argument and invalid-state error
contracts and are consolidated into a single **Error Handling** requirement.

> **Note:** `HdmiCecAddLogicalAddress` and `HdmiCecRemoveLogicalAddress` are sink-device-only APIs and are not exercised by this source-mode suite.

| Req ID | Functional Capability | Classification | # Tests |
|--------|-----------------------|----------------|---------|
| VTS-HDMICEC-001 | CEC HAL handle open and close lifecycle | Lifecycle | 2 |
| VTS-HDMICEC-002 | Physical/logical address retrieval, Rx/Tx callback registration, and CEC frame transmission | Functional | 10 |
| VTS-HDMICEC-003 | API error handling — invalid-argument and wrong-state conditions | Error Handling | 8 |
| | **Total** | | **20** |

---

### VTS-HDMICEC-001 — CEC HAL handle open and close lifecycle (2 tests)

L1 positive (2): HdmiCecOpen_positive, HdmiCecClose_positive

---

### VTS-HDMICEC-002 — Physical/logical address retrieval, Rx/Tx callback registration, and CEC frame transmission (10 tests)

L1 positive (6): HdmiCecGetPhysicalAddress_positive, HdmiCecGetLogicalAddress_positive, HdmiCecSetRxCallback_positive, HdmiCecSetTxCallback_positive, HdmiCecTx_positive, HdmiCecTxAsync_positive

L2 (4): GetPhysicalAddress, GetLogicalAddress, VerifyCECBroadcast, VerifyCECTxNoAck

---

### VTS-HDMICEC-003 — API error handling (8 tests)

L1 negative (8): HdmiCecOpen_negative, HdmiCecClose_negative, HdmiCecGetPhysicalAddress_negative, HdmiCecGetLogicalAddress_negative, HdmiCecSetRxCallback_negative, HdmiCecSetTxCallback_negative, HdmiCecTx_negative, HdmiCecTxAsync_negative

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `VTS-HDMICEC-001` | SHALL open the CEC HAL and obtain a valid handle via `HdmiCecOpen()` returning `HDMI_CEC_IO_SUCCESS`, and SHALL close the handle via `HdmiCecClose()` returning `HDMI_CEC_IO_SUCCESS`. |
| `VTS-HDMICEC-002` | SHALL retrieve the device physical address via `HdmiCecGetPhysicalAddress()` returning `HDMI_CEC_IO_SUCCESS` with a valid non-zero address reflecting the HDMI topology. SHALL retrieve the HAL-allocated logical address via `HdmiCecGetLogicalAddress()` returning `HDMI_CEC_IO_SUCCESS` with a valid address value. SHALL register a receive callback via `HdmiCecSetRxCallback()` and a transmit-completion callback via `HdmiCecSetTxCallback()`, each returning `HDMI_CEC_IO_SUCCESS`. SHALL transmit a CEC frame synchronously via `HdmiCecTx()` and asynchronously via `HdmiCecTxAsync()`, returning `HDMI_CEC_IO_SUCCESS` on successful send; for a frame addressed to a non-existent device, the synchronous transmission SHALL indicate the frame was sent but not acknowledged (`HDMI_CEC_IO_SENT_BUT_NOT_ACKD`). |
| `VTS-HDMICEC-003` | SHALL enforce the following error code contracts across all `HDMICEC` APIs: `HdmiCecOpen()` SHALL return an error when called while already open; `HdmiCecClose()` SHALL return an error when called without a prior open; `HdmiCecGetPhysicalAddress()`, `HdmiCecGetLogicalAddress()`, `HdmiCecSetRxCallback()`, `HdmiCecSetTxCallback()`, `HdmiCecTx()`, and `HdmiCecTxAsync()` SHALL return `HDMI_CEC_IO_INVALID_ARGUMENT` (or the appropriate error) when called with an invalid handle, a NULL data/output pointer, a NULL callback, or a zero data length. |
