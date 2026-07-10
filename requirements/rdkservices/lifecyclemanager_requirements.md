# RDK Services — LifecycleManager Plugin Requirements

> **Module:** LifecycleManager (`org.rdk.LifecycleManager.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_LifecycleManager.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_LifecycleManager.md)
> **Total requirements:** 9 | **Total test cases:** 40

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | API Category | Classification | # Tests | Test Cases |
|--------|-------------|----------------|---------|------------|
| RDKSVC-REQ-001 | appReady notification — valid and boundary appId inputs | Lifecycle API | 7 | Verify_AppReady_Valid_AppId, Verify_AppReady_Empty_AppId, Verify_AppReady_Numeric_AppId, Verify_AppReady_Special_Char_AppId, Verify_AppReady_Long_String_AppId, LifecycleManager_Verify_AppReady_Boolean_AppId, LifecycleManager_Verify_AppReady_Without_Parameters |
| RDKSVC-REQ-002 | closeApp — valid appId with valid and empty close reasons | Lifecycle API | 3 | CloseApp_Valid_AppId_USER_EXIT_CloseReason, CloseApp_Valid_AppId_ERROR_CloseReason, CloseApp_ValidAppId_EmptyCloseReason |
| RDKSVC-REQ-003 | closeApp — valid appId with invalid close reason types | Lifecycle API | 4 | CloseApp_Valid_AppId_Numeric_CloseReason, CloseApp_Valid_AppId_Special_Char_CloseReason, CloseApp_Valid_AppId_Boolean_CloseReason, CloseApp_Valid_AppId_Long_String_CloseReason |
| RDKSVC-REQ-004 | closeApp — empty appId and missing parameters | Lifecycle API | 6 | CloseApp_Empty_AppId_USER_EXIT_CloseReason, CloseApp_Empty_AppId_ERROR_CloseReason, CloseApp_Empty_AppId_KILL_AND_RUN_CloseReason, CloseApp_Empty_AppId_KILL_AND_ACTIVATE_CloseReason, LifecycleManager_CloseApp_Empty_Params, CloseApp_Without_Parameters |
| RDKSVC-REQ-005 | closeApp — invalid appId string across all close reasons | Lifecycle API | 4 | CloseApp_Invalid_AppId_USER_EXIT_CloseReason, CloseApp_Invalid_AppId_ERROR_CloseReason, CloseApp_Invalid_AppId_KILL_AND_RUN_CloseReason, CloseApp_Invalid_AppId_KILL_AND_ACTIVATE_CloseReason |
| RDKSVC-REQ-006 | closeApp — numeric appId across all close reasons | Lifecycle API | 4 | CloseApp_Numeric_AppId_USER_EXIT_CloseReason, CloseApp_Numeric_AppId_ERROR_CloseReason, CloseApp_Numeric_AppId_KILL_AND_RUN_CloseReason, CloseApp_Numeric_AppId_KILL_AND_ACTIVATE_CloseReason |
| RDKSVC-REQ-007 | closeApp — special character appId across all close reasons | Lifecycle API | 4 | CloseApp_Special_Char_AppId_USER_EXIT_CloseReason, CloseApp_Special_Char_AppId_ERROR_CloseReason, CloseApp_Special_Char_AppId_KILL_AND_RUN_CloseReason, CloseApp_Special_Char_AppId_KILL_AND_ACTIVATE_CloseReason |
| RDKSVC-REQ-008 | closeApp — boolean appId across all close reasons | Lifecycle API | 4 | CloseApp_Boolean_AppId_USER_EXIT_CloseReason, CloseApp_Boolean_AppId_ERROR_CloseReason, CloseApp_Boolean_AppId_KILL_AND_RUN_CloseReason, CloseApp_Boolean_AppId_KILL_AND_ACTIVATE_CloseReason |
| RDKSVC-REQ-009 | closeApp — long string appId across all close reasons | Lifecycle API | 4 | CloseApp_Long_String_AppId_USER_EXIT_CloseReason, CloseApp_Long_String_AppId_ERROR_CloseReason, CloseApp_Long_String_AppId_KILL_AND_RUN_CloseReason, CloseApp_Long_String_AppId_KILL_AND_ACTIVATE_CloseReason |
| | **Total** | | **40** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL implement the LifecycleManager `appReady` JSON-RPC method to accept a valid application identifier and return a successful response, and return correct error codes for empty, numeric, special-character, long-string, boolean, and missing application identifier inputs. |
| `RDKSVC-REQ-002` | SHALL implement the LifecycleManager `closeApp` JSON-RPC method to accept a valid application identifier with USER_EXIT and ERROR close reasons and initiate app closure, and return a correct error response when the close reason is empty. |
| `RDKSVC-REQ-003` | SHALL return correct error codes for `closeApp` requests with a valid application identifier and a numeric, special-character, boolean, or long-string close reason value. |
| `RDKSVC-REQ-004` | SHALL return correct error codes for `closeApp` requests submitted with an empty application identifier across all close reason values (USER_EXIT, ERROR, KILL_AND_RUN, KILL_AND_ACTIVATE), and for requests submitted with empty parameters or without any parameters. |
| `RDKSVC-REQ-005` | SHALL return correct error codes for `closeApp` requests with an invalid application identifier string across all close reason values (USER_EXIT, ERROR, KILL_AND_RUN, KILL_AND_ACTIVATE). |
| `RDKSVC-REQ-006` | SHALL return correct error codes for `closeApp` requests with a numeric application identifier across all close reason values (USER_EXIT, ERROR, KILL_AND_RUN, KILL_AND_ACTIVATE). |
| `RDKSVC-REQ-007` | SHALL return correct error codes for `closeApp` requests with a special-character application identifier across all close reason values (USER_EXIT, ERROR, KILL_AND_RUN, KILL_AND_ACTIVATE). |
| `RDKSVC-REQ-008` | SHALL return correct error codes for `closeApp` requests with a boolean application identifier value across all close reason values (USER_EXIT, ERROR, KILL_AND_RUN, KILL_AND_ACTIVATE). |
| `RDKSVC-REQ-009` | SHALL return correct error codes for `closeApp` requests with a long-string application identifier across all close reason values (USER_EXIT, ERROR, KILL_AND_RUN, KILL_AND_ACTIVATE). |
