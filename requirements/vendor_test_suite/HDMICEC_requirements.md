# HDMI CEC — Requirements

> **Module:** HDMI CEC HAL (`HDMICEC`) | **Req ID Prefix:** `VTS-HDMICEC`
> **Total requirements:** 7 | **Total test cases:** 17 (16 L1 + 1 L2)

---

## Requirements Document

| Req ID | Classification | Test Scope *(Verify that the DUT...)* |
|--------|----------------|---------------------------------------|
| `VTS-HDMICEC-001` | Lifecycle | SHALL open the CEC HAL and obtain a valid non-zero handle via `HdmiCecOpen()` returning `HDMI_CEC_IO_SUCCESS`, and SHALL close the handle via `HdmiCecClose()` returning `HDMI_CEC_IO_SUCCESS`, supporting a subsequent re-open after close. |
| `VTS-HDMICEC-002` | Functional | SHALL retrieve the device physical address via `HdmiCecGetPhysicalAddress()` returning `HDMI_CEC_IO_SUCCESS` with a valid physical address value reflecting the HDMI topology. |
| `VTS-HDMICEC-003` | Functional | SHALL retrieve the HAL-allocated logical address via `HdmiCecGetLogicalAddress()` returning `HDMI_CEC_IO_SUCCESS` with a valid logical address value, and SHALL, when the source device is not connected to a sink, report logical-address unavailability by returning `HDMI_CEC_IO_LOGICALADDRESS_UNAVAILABLE` from `HdmiCecOpen()`. |
| `VTS-HDMICEC-004` | Functional | SHALL register a receive callback via `HdmiCecSetRxCallback()` returning `HDMI_CEC_IO_SUCCESS`, including acceptance of a NULL callback to deregister. |
| `VTS-HDMICEC-005` | Functional | SHALL transmit a CEC frame synchronously via `HdmiCecTx()` returning `HDMI_CEC_IO_SUCCESS`; for a frame addressed to a non-existent device the transmission SHALL be reported as sent but not acknowledged (`HDMI_CEC_IO_SENT_BUT_NOT_ACKD`), and a broadcast frame SHALL return `HDMI_CEC_IO_SUCCESS`. |
| `VTS-HDMICEC-006` | Functional | SHALL, as a source device, report the sink-only logical-address management operations `HdmiCecAddLogicalAddress()` and `HdmiCecRemoveLogicalAddress()` as unsupported by returning `HDMI_CEC_IO_OPERATION_NOT_SUPPORTED` for all invocation scenarios. |
| `VTS-HDMICEC-007` | Error Handling | SHALL enforce the following error code contracts across the source `HDMICEC` APIs:<br>`HdmiCecOpen()` SHALL return `HDMI_CEC_IO_INVALID_ARGUMENT` for a NULL handle pointer and `HDMI_CEC_IO_ALREADY_OPEN` when called while already open<br>`HdmiCecClose()` SHALL return `HDMI_CEC_IO_NOT_OPENED` when called without a prior open or after close, and `HDMI_CEC_IO_INVALID_HANDLE` for an invalid handle<br>`HdmiCecGetPhysicalAddress()`, `HdmiCecGetLogicalAddress()`, `HdmiCecSetRxCallback()`, and `HdmiCecTx()` SHALL each return `HDMI_CEC_IO_NOT_OPENED` when invoked before open or after close, `HDMI_CEC_IO_INVALID_HANDLE` for an invalid handle, and `HDMI_CEC_IO_INVALID_ARGUMENT` for a NULL data/output pointer or an invalid data length. |
