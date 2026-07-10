# RDK Services — PackageManager Plugin Requirements

> **Module:** PackageManager (`org.rdk.PackageManager.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_PackageManager.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_PackageManager.md)
> **Total requirements:** 9 | **Total test cases:** 41

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | Functional Capability | Classification | # Tests | Test Cases |
|--------|----------------------|----------------|---------|------------|
| RDKSVC-REQ-001 | Installed package listing | Query API | 1 | PackageManager_ListPackages_Functionality |
| RDKSVC-REQ-002 | Package installation | Lifecycle API | 3 | PackageManager_Install_ValidParameters, PackageManager_Install_InvalidParameters, PackageManager_Install_EmptyParameters |
| RDKSVC-REQ-003 | Package uninstallation | Lifecycle API | 5 | PackageManager_Uninstall_ValidParameters, PackageManager_Uninstall_InvalidParameter, PackageManager_Uninstall_EmptyParameters, PackageManager_Uninstall_InvalidParameters, PackageManager_Uninstall_TwoTimes |
| RDKSVC-REQ-004 | Package state query | Query API | 7 | PackageManager_GetPackageState_EmptyParameters, PackageManager_GetPackageState_InvalidParameters, PackageManager_Check_Package_State_After_Install, PackageManager_Check_Package_State_After_Uninstall, PackageManager_GetPackageState_ValidPackageId_InvalidVersion, PackageManager_GetPackageState_InvalidPackageId_ValidVersion, PackageManager_GetPackageState_NoParameters |
| RDKSVC-REQ-005 | Package configuration retrieval | Configuration API | 5 | PackageManager_Config_ValidParameters, PackageManager_Config_EmptyParameters, PackageManager_Config_InvalidParameters, PackageManager_Config_EmptyPackageId_ValidVersion, PackageManager_Config_ValidPackageId_EmptyVersion |
| RDKSVC-REQ-006 | Package lock operations | Lock Management API | 9 | PackageManager_Lock_Package_ValidParameters, PackageManager_Lock_Package_EmptyParameters, PackageManager_Lock_Package_InvalidParameters, PackageManager_Lock_Package_EmptyPackageId, PackageManager_Lock_Package_EmptyVersion, PackageManager_Lock_Package_EmptyLockReason, PackageManager_Lock_Package_InvalidPackageId, PackageManager_Lock_Package_InvalidVersion, PackageManager_Lock_Package_NoParameters |
| RDKSVC-REQ-007 | Package unlock operations | Lock Management API | 5 | PackageManager_Unlock_Package_ValidParameters, PackageManager_Unlock_Package_EmptyParameters, PackageManager_Unlock_Package_InvalidPackageId_EmptyVersion, PackageManager_Unlock_Package_EmptyPackageId_InvalidVersion, PackageManager_Unlock_Package_NoParameters |
| RDKSVC-REQ-008 | Locked package information query | Lock Management API | 5 | PackageManager_GetLockedInfo_ValidParameters, PackageManager_GetLockedInfo_EmptyParameters, PackageManager_GetLockedInfo_InvalidPackageId_EmptyVersion, PackageManager_GetLockedInfo_EmptyPackageId_InvalidVersion, PackageManager_GetLockedInfo_NoParameters |
| RDKSVC-REQ-009 | Package installation status event notification | Event API | 1 | PackageManager_Check_On_AppInstallationStatus_Event |
| | **Total** | | **41** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL return a list of all currently installed packages with correct response schema. |
| `RDKSVC-REQ-002` | SHALL install a package with valid parameters and return correct error responses for installation requests with invalid and empty parameters. |
| `RDKSVC-REQ-003` | SHALL uninstall a package with valid parameters, correctly handle a second uninstall of an already-removed package, and return correct error responses for uninstall requests with invalid and empty parameters. |
| `RDKSVC-REQ-004` | SHALL return the current state of a package after installation and after uninstallation, and return correct error responses for state queries with empty parameters, invalid parameters, an invalid version with a valid package identifier, an invalid package identifier with a valid version, and no parameters. |
| `RDKSVC-REQ-005` | SHALL return the configuration for a package with valid identifier and version, and return correct error responses for configuration queries with empty parameters, invalid parameters, empty package identifier with valid version, and valid package identifier with empty version. |
| `RDKSVC-REQ-006` | SHALL lock a package with valid identifier, version, and lock reason, and return correct error responses for lock requests with empty parameters, invalid parameters, empty package identifier, empty version, empty lock reason, invalid package identifier, invalid version, and no parameters. |
| `RDKSVC-REQ-007` | SHALL unlock a package with valid parameters, and return correct error responses for unlock requests with empty parameters, invalid package identifier with empty version, empty package identifier with invalid version, and no parameters. |
| `RDKSVC-REQ-008` | SHALL return lock information for a package with valid parameters, and return correct error responses for locked-info queries with empty parameters, invalid package identifier with empty version, empty package identifier with invalid version, and no parameters. |
| `RDKSVC-REQ-009` | SHALL fire an installation status notification with correct package identifier and installation state payload when a package installation status changes. |
