# Device Settings Host (dsHost) — Requirements

> **Module:** Device Settings Host HAL (`dsHost`) | **Req ID Prefix:** `VTS-DSHOST`
> **Total requirements:** 5 | **Total test cases:** 12 (10 L1 + 2 L2)

---

## Step 1 — Requirement Categorisation Grouping

Requirements are grouped by **functional capability** of the `dsHost` HAL interface.
Positive L1 and L2 test cases validate correct API behaviour and profile conformance.
Negative L1 test cases are grouped separately under Error Handling, as they exclusively
verify `dsERR_NOT_INITIALIZED`, `dsERR_ALREADY_INITIALIZED`, and `dsERR_INVALID_PARAM`
error code contracts.

| Req ID | Functional Capability | Classification | # Tests |
|--------|-----------------------|----------------|---------|
| VTS-DSHOST-001 | DS Host HAL module initialization and termination lifecycle | Lifecycle | 2 |
| VTS-DSHOST-002 | CPU temperature retrieval | Functional | 2 |
| VTS-DSHOST-003 | SoC ID retrieval and profile validation | Profile Compliance | 2 |
| VTS-DSHOST-004 | Host EDID retrieval | Functional | 1 |
| VTS-DSHOST-005 | API error handling — not-initialized, already-initialized, and invalid-parameter conditions | Error Handling | 5 |
| | **Total** | | **12** |

---

### VTS-DSHOST-001 — DS Host HAL module initialization and termination lifecycle (2 tests)

L1 positive (2): dsHostInit_L1_positive, dsHostTerm_L1_positive

---

### VTS-DSHOST-002 — CPU temperature retrieval (2 tests)

L1 positive (1): dsGetCPUTemperature_L1_positive

L2 (1): L2_GetCPUTemperature

---

### VTS-DSHOST-003 — SoC ID retrieval and profile validation (2 tests)

L1 positive (1): dsGetSocIDFromSDK_L1_positive

L2 (1): L2_GetAndVerifySocID

---

### VTS-DSHOST-004 — Host EDID retrieval (1 test)

L1 positive (1): dsGetHostEDID_L1_positive

---

### VTS-DSHOST-005 — API error handling (5 tests)

L1 negative (5): dsHostInit_L1_negative, dsHostTerm_L1_negative, dsGetCPUTemperature_L1_negative, dsGetSocIDFromSDK_L1_negative, dsGetHostEDID_L1_negative

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `VTS-DSHOST-001` | SHALL initialize the DS Host HAL module via `dsHostInit()` returning `dsERR_NONE` and SHALL terminate the module via `dsHostTerm()` returning `dsERR_NONE`. The module SHALL support re-initialization after a prior termination without error. |
| `VTS-DSHOST-002` | SHALL retrieve the current CPU temperature via `dsGetCPUTemperature()` returning a valid floating-point value, with consecutive calls returning consistent values within the platform-defined temperature range specified in the device profile. |
| `VTS-DSHOST-003` | SHALL retrieve the platform SoC identifier string via `dsGetSocIDFromSDK()` returning a non-empty string that is consistent across successive calls and matches the expected SoC ID value defined in the device profile. |
| `VTS-DSHOST-004` | SHALL retrieve the host EDID data via `dsGetHostEDID()` returning a non-null EDID byte buffer with a non-zero length, with consecutive calls returning identical EDID content. |
| `VTS-DSHOST-005` | SHALL enforce the following error code contracts across all `dsHost` APIs: `dsHostInit()` SHALL return `dsERR_ALREADY_INITIALIZED` when called while the module is already initialized; `dsHostTerm()` SHALL return `dsERR_NOT_INITIALIZED` when called without prior initialization or after the module has already been terminated; `dsGetCPUTemperature()`, `dsGetSocIDFromSDK()`, and `dsGetHostEDID()` SHALL each return `dsERR_NOT_INITIALIZED` when invoked before initialization or after termination, and SHALL return `dsERR_INVALID_PARAM` when called with a NULL output pointer or buffer. |
