# Device Settings Display — Requirements

> **Module:** Device Settings Display HAL (`dsDisplay`) | **Req ID Prefix:** `VTS-DSDISPLAY`
> **Total requirements:** 10 | **Total test cases:** 28 (26 L1 + 2 L2)

---

## Requirements Document

| Req ID | Classification | Test Scope *(Verify that the DUT...)* |
|--------|----------------|---------------------------------------|
| `VTS-DSDISPLAY-001` | Lifecycle | SHALL initialize the Display sub-system via `dsDisplayInit()` returning `dsERR_NONE` and SHALL terminate it via `dsDisplayTerm()` returning `dsERR_NONE`. |
| `VTS-DSDISPLAY-002` | Functional | SHALL return a valid display device handle for each supported video port via `dsGetDisplay()` returning `dsERR_NONE`. |
| `VTS-DSDISPLAY-003` | Functional | SHALL retrieve the connected display's EDID information via `dsGetEDID()` returning `dsERR_NONE` with valid EDID data. |
| `VTS-DSDISPLAY-004` | Functional | SHALL retrieve the connected display's raw EDID byte buffer and its length via `dsGetEDIDBytes()` returning `dsERR_NONE`. |
| `VTS-DSDISPLAY-005` | Profile Compliance | SHALL retrieve the display aspect ratio of a valid display handle via `dsGetDisplayAspectRatio()` returning `dsERR_NONE`, and the default reported aspect ratio SHALL be `dsVIDEO_ASPECT_RATIO_16x9`. |
| `VTS-DSDISPLAY-006` | Functional | SHALL register a display-event callback for a valid display handle via `dsRegisterDisplayEventCallback()` returning `dsERR_NONE`. |
| `VTS-DSDISPLAY-007` | Data Integrity | SHALL, for each valid AVI content type, set the value via `dsSetAVIContentType()` returning `dsERR_NONE`, and the value retrieved via `dsGetAVIContentType()` SHALL match the value that was set. |
| `VTS-DSDISPLAY-008` | Functional | SHALL set the AVI scan information of a valid display handle via `dsSetAVIScanInformation()` returning `dsERR_NONE`, and retrieve it via `dsGetAVIScanInformation()` returning `dsERR_NONE` with a valid value. |
| `VTS-DSDISPLAY-009` | Functional | SHALL set the Auto Low Latency Mode (ALLM) enabled status of a valid display handle via `dsSetAllmEnabled()` returning `dsERR_NONE`, and retrieve it via `dsGetAllmEnabled()` returning `dsERR_NONE` with a valid value. |
| `VTS-DSDISPLAY-010` | Error Handling | SHALL enforce the following error code contracts across all `dsDisplay` APIs:<br>`dsDisplayInit()` SHALL return `dsERR_ALREADY_INITIALIZED` when called while already initialized<br>`dsDisplayTerm()` SHALL return `dsERR_NOT_INITIALIZED` when called without prior initialization or after the module has already been terminated<br>all remaining `dsDisplay` APIs SHALL return `dsERR_NOT_INITIALIZED` when invoked before initialization or after termination, and SHALL return `dsERR_INVALID_PARAM` when called with an invalid handle, a NULL output pointer, or an out-of-range parameter value. |
