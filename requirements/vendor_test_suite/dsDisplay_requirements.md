# Device Settings Display — Requirements

> **Module:** Device Settings Display HAL (`dsDisplay`) | **Req ID Prefix:** `VTS-DSDISPLAY`
> **Total requirements:** 5 | **Total test cases:** 28 (26 L1 + 2 L2)

---

## Step 1 — Requirement Categorisation Grouping

Requirements are grouped by **functional capability** of the `dsDisplay` HAL interface. The module
provides init/term lifecycle, display handle and EDID retrieval, aspect-ratio and display-event
reporting, and AVI signaling and ALLM control.

Positive L1 tests validate individual API correctness in isolation — checking return codes and, for
getters, expected default values. The L2 `TestDefaultAspectRatio_src` test verifies the reported
default aspect ratio and is grouped with the display-information queries as **Functional**. The L2
`SetAndGetAVIContentType_src` test writes each valid content type and reads it back verifying the
same value — a genuine round-trip — so it is classified as **Data Integrity**. All negative L1 tests
exclusively verify `dsERR_NOT_INITIALIZED`, `dsERR_INVALID_PARAM`, and related error contracts and
are consolidated into a single **Error Handling** requirement.

| Req ID | Functional Capability | Classification | # Tests |
|--------|-----------------------|----------------|---------|
| VTS-DSDISPLAY-001 | DS Display sub-system initialization and termination lifecycle | Lifecycle | 2 |
| VTS-DSDISPLAY-002 | Display handle, EDID, aspect-ratio retrieval and display-event registration | Functional | 6 |
| VTS-DSDISPLAY-003 | AVI signaling and ALLM get/set control | Functional | 6 |
| VTS-DSDISPLAY-004 | AVI content type set-and-read-back integrity | Data Integrity | 1 |
| VTS-DSDISPLAY-005 | API error handling — not-initialized and invalid-parameter conditions | Error Handling | 13 |
| | **Total** | | **28** |

---

### VTS-DSDISPLAY-001 — DS Display sub-system initialization and termination lifecycle (2 tests)

L1 positive (2): dsDisplayInit_pos, dsDisplayTerm_pos

---

### VTS-DSDISPLAY-002 — Display handle, EDID, aspect-ratio retrieval and display-event registration (6 tests)

L1 positive (5): dsGetDisplay_pos, dsGetEDID_pos, dsGetEDIDBytes_pos, dsGetDisplayAspectRatio_pos, dsRegisterDisplayEventCB_pos

L2 (1): TestDefaultAspectRatio_src

---

### VTS-DSDISPLAY-003 — AVI signaling and ALLM get/set control (6 tests)

L1 positive (6): dsGetAVIContentType_pos, dsSetAVIContentType_pos, dsGetAVIScanInfo_pos, dsSetAVIScanInfo_pos, dsGetAllmEnabled_pos, dsSetAllmEnabled_pos

---

### VTS-DSDISPLAY-004 — AVI content type set-and-read-back integrity (1 test)

L2 (1): SetAndGetAVIContentType_src

---

### VTS-DSDISPLAY-005 — API error handling (13 tests)

L1 negative (13): dsDisplayInit_neg, dsDisplayTerm_neg, dsGetDisplay_neg, dsGetEDID_neg, dsGetEDIDBytes_neg, dsGetDisplayAspectRatio_neg, dsRegisterDisplayEventCB_neg, dsGetAVIContentType_neg, dsSetAVIContentType_neg, dsGetAVIScanInfo_neg, dsSetAVIScanInfo_neg, dsGetAllmEnabled_neg, dsSetAllmEnabled_neg

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `VTS-DSDISPLAY-001` | SHALL initialize the Display sub-system via `dsDisplayInit()` returning `dsERR_NONE` and SHALL terminate it via `dsDisplayTerm()` returning `dsERR_NONE`. |
| `VTS-DSDISPLAY-002` | SHALL retrieve a valid display handle for each supported port via `dsGetDisplay()`, retrieve the connected display's EDID information via `dsGetEDID()` and its raw EDID bytes via `dsGetEDIDBytes()`, retrieve the display aspect ratio via `dsGetDisplayAspectRatio()`, and register a display-event callback via `dsRegisterDisplayEventCallback()`, each returning `dsERR_NONE` with valid output. The default reported aspect ratio SHALL be `dsVIDEO_ASPECT_RATIO_16x9`. |
| `VTS-DSDISPLAY-003` | SHALL get and set the AVI content type via `dsGetAVIContentType()` / `dsSetAVIContentType()`, get and set the AVI scan information via `dsGetAVIScanInformation()` / `dsSetAVIScanInformation()`, and get and set the ALLM enabled status via `dsGetAllmEnabled()` / `dsSetAllmEnabled()`, each returning `dsERR_NONE`. |
| `VTS-DSDISPLAY-004` | SHALL, for each valid AVI content type, apply the value via `dsSetAVIContentType()` and, on reading it back via `dsGetAVIContentType()`, return the same value that was set. |
| `VTS-DSDISPLAY-005` | SHALL enforce the following error code contracts across all `dsDisplay` APIs: `dsDisplayInit()` SHALL return an error when called while already initialized; `dsDisplayTerm()`, `dsGetDisplay()`, `dsGetEDID()`, `dsGetEDIDBytes()`, `dsGetDisplayAspectRatio()`, `dsRegisterDisplayEventCallback()`, `dsGetAVIContentType()`, `dsSetAVIContentType()`, `dsGetAVIScanInformation()`, `dsSetAVIScanInformation()`, `dsGetAllmEnabled()`, and `dsSetAllmEnabled()` SHALL return `dsERR_NOT_INITIALIZED` when invoked before initialization or after termination, and SHALL return `dsERR_INVALID_PARAM` when called with a NULL output pointer, an invalid handle, or an out-of-range value. |
